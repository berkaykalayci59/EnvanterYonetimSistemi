# MSSQL & Python (FastAPI) Envanter Yönetim Sistemi

Bu proje, Python (FastAPI) ve MSSQL Server (LocalDB) kullanılarak geliştirilmiş modern ve hızlı bir Stok/Envanter Yönetim Sistemidir. Ön yüz (Frontend) kısmında HTML, Vanilla CSS (Glassmorphism tasarımı) ve JavaScript kullanılmıştır.

## Özellikler

*   **Modern Web Arayüzü**: Cam efekti (glassmorphism), pürüzsüz animasyonlar ve şık kullanıcı deneyimi.
*   **CRUD İşlemleri**: Ürün Ekleme, Silme, Güncelleme ve Listeleme işlemleri.
*   **Otomatik Veritabanı Kurulumu**: Sistem çalıştırıldığında gerekli MSSQL veritabanını (`InventoryDB`) ve tablolarını otomatik oluşturur.
*   **Hızlı ve Asenkron API**: FastAPI altyapısı sayesinde son derece performanslı backend mimarisi.

## Kullanılan Teknolojiler

*   **Backend**: Python, FastAPI, Uvicorn, SQLAlchemy, Pydantic
*   **Veritabanı**: MSSQL Server (pyodbc)
*   **Frontend**: HTML5, Vanilla CSS3, JavaScript (Fetch API)

## Kurulum ve Çalıştırma

1. Projeyi bilgisayarınıza klonlayın (veya indirin):
```bash
git clone https://github.com/KULLANICI_ADINIZ/inventory_system.git
cd inventory_system
```

2. Gerekli Python kütüphanelerini yükleyin:
```bash
pip install -r requirements.txt
```

3. *(Opsiyonel)* Eğer varsayılan `(localdb)\MSSQLLocalDB` haricinde farklı bir SQL Server kurulumunuz varsa, `backend/database.py` dosyasındaki sunucu ayarlarını güncelleyin.

4. Sunucuyu başlatın:
```bash
uvicorn backend.main:app --reload
```

5. Tarayıcınızı açın ve uygulamayı kullanmaya başlayın:
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

## Katkıda Bulunma ve Lisans
Bu proje açık kaynaklıdır ve eğitim/portföy amaçlı geliştirilmiştir. Dilediğiniz gibi çatallayabilir (fork), geliştirebilir ve kullanabilirsiniz.
