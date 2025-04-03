# Secure Article Management & Review System

Bu proje, akademik makale süreçlerini güvenli ve anonim bir şekilde yönetmek için geliştirilmiş bir Django tabanlı sistemdir. Yazarlar, editörler ve hakemler arasında şifreli, anonimleştirilmiş ve izlenebilir bir makale değerlendirme süreci sağlar.

---

## Uygulama Kurulumu ve Çalıştırılması

### Gereksinimler

- Python 3.10+
- pip (Python Paket Yöneticisi)
- Git (opsiyonel)
- `en_core_web_trf` spaCy modeli
- (Opsiyonel) PostgreSQL

### Kurulum

1. Python yüklü değilse [python.org](https://www.python.org/downloads/) üzerinden indirin.

2. Gereken paketleri kurun:

3. Veritabanı kurulumunu yapın:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Çalıştırma

```bash
python manage.py runserver
```

---

## Kullanıcı Rolleri

Bu sistemde 3 temel kullanıcı tipi bulunmaktadır:

### Yazar (Author)
- Giriş yapmadan makale yükleyebilir.
- Takip numarası ile makale durumu sorgular.
- Editörle mesajlaşabilir.
- Revize PDF yükleyebilir (eski dosya otomatik silinir).

### Editör (Editor)
- Tüm makaleleri görüntüler.
- Hakem atar, anonimleştirme başlatır.
- Şifrelenmiş bilgileri görüntüler.
- Yazar ve hakemle mesajlaşabilir.
- Revize makaleyi yeniden hakeme iletebilir.

### Hakem (Referee)
- Sisteme sadece dropdown ile girer.
- Atandığı makaleyi ve anonim PDF'ini görüntüler.
- Değerlendirme formu doldurur.
- Editörle mesajlaşabilir.

---

##  Anonimleştirme ve Şifreleme

- Abstract öncesindeki kişisel bilgiler (ad, kurum, e-posta) spaCy ve regex ile tespit edilir.
- Redakte edilen bilgiler `anonym_list`'e eklenir.
- Abstract sonrasında yalnızca bu bilgiler şifrelenir.
- AES ile şifrelenip `Article.encrypted_info` alanında saklanır.

---


##  Loglama Sistemi

- Sistem aksiyonları `ArticleLog` modeli ile kaydedilir.
- Loglar admin panelde ve ayrıca "See Logs" ekranında görüntülenebilir.

---
# Secure Article Management & Review System

This project is a Django-based system developed to manage academic article workflows securely and anonymously. It enables encrypted, anonymized, and trackable article review processes between authors, editors, and referees.

---

##  Installation and Running the Application

### Requirements

- Python 3.10+
- pip (Python Package Manager)
- Git (optional)
- `en_core_web_sm` spaCy model
- (Optional) PostgreSQL

### Setup

1. If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

2. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_trf
```
3. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```


### Running the App

```bash
python manage.py runserver
```

Then open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

##  User Roles

There are 3 main user types in this system:

###  Author
- Can upload articles without logging in.
- Tracks the article status via a unique **Tracking ID**.
- Can message the editor.
- Can upload a revised PDF (the old file is automatically removed).

###  Editor
- Views all uploaded articles.
- Assigns referees and initiates anonymization.
- Can view encrypted anonymized data.
- Can communicate with both authors and referees.
- Can reassign revised articles to referees.

###  Referee
- Logs in by simply selecting their name from a dropdown (no password required).
- Views assigned articles and their anonymized PDFs.
- Submits evaluations through a form.
- Can message the editor.

---

##  Anonymization & Encryption

- Personal information (name, institution, email) before the abstract is detected using spaCy and regex.
- These are stored in `anonym_list`.
- Only those items are redacted after the abstract.
- Redacted content is encrypted with AES and stored in the `Article.encrypted_info` field.

---



##  Logging System

- All key system actions are logged using the `ArticleLog` model.
- Logs can be viewed via the admin panel and the "See Logs" page.

---






### Makale Yükleme ve Takip Arayüzü(Article Upload and Tracking Interface)

![Makale Takip](https://github.com/iclalmillik/YazlabII-1/blob/main/images/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-04-01%20164620.png)

---

###  Editör Paneli – Makale Detayı(Editor Panel – Article Detail)

![Editör Paneli](https://github.com/iclalmillik/YazlabII-1/blob/main/images/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-04-01%20164641.png)

---

###  Makale Anahtar Kelimeleri ve Alan Ataması(Article Keywords and Area Assignment)

![Makale Detay](https://github.com/iclalmillik/YazlabII-1/blob/main/images/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-04-01%20164702.png)

---

###  Makale Takibi ve Editörle Mesajlaşma (Article Tracking and Messaging with the Editor)

![Anonimleştirme Ayarları](https://github.com/iclalmillik/YazlabII-1/blob/main/images/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-04-01%20164726.png)

---

### Makale Yükleme Sayfası(Upload Article Page)

![Keyword Analizi](https://github.com/iclalmillik/YazlabII-1/blob/main/images/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-04-01%20164733.png)

---

###  Anonimleştirme Ayarları Sayfası(Anonymization Settings Page)

![Mesajlaşma](https://github.com/iclalmillik/YazlabII-1/blob/main/images/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-04-01%20164755.png)








