from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from backend import models
from backend import schemas
from backend.database import engine, get_db

# Veritabanı tablolarını oluştur (Yoksa oluşturur, varsa dokunmaz)
try:
    models.Base.metadata.create_all(bind=engine)
    print("Veritabanı tabloları hazır.")
except Exception as e:
    print("Veritabanı bağlantı hatası! Lütfen MSSQL sunucusunun çalıştığından ve database.py ayarlarının doğru olduğundan emin olun.")
    print(f"Hata detayı: {e}")

app = FastAPI(title="Stok & Envanter API")

# CORS ayarları (Frontend'in API'ye istek atabilmesi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik dosyaları servis etme
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")

from fastapi.responses import RedirectResponse
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/app/index.html")

@app.post("/api/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/api/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(models.Product).order_by(models.Product.id).offset(skip).limit(limit).all()
    return products

@app.get("/api/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return product

@app.put("/api/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Ürün başarıyla silindi"}
