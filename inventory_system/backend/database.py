import os
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib

# Ekran görüntüsündeki ayarlarınız:
SERVER = os.getenv("DB_SERVER", r"(localdb)\MSSQLLocalDB")
DATABASE = os.getenv("DB_NAME", "InventoryDB")

# Veritabanı yoksa otomatik olarak oluştur (master veritabanına bağlanarak)
try:
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE=master;"
        f"Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()
    cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'{DATABASE}') CREATE DATABASE [{DATABASE}]")
    cursor.close()
    conn.close()
    print(f"Veritabanı kontrolü tamamlandı. '{DATABASE}' hazır.")
except Exception as e:
    print(f"Veritabanı oluşturulurken bir uyarı alındı: {e}")

# Gerçek bağlantı parametreleri
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)

SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
except Exception as e:
    print(f"Veritabanı motoru oluşturulurken hata: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
