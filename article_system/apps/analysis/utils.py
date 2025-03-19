import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import os

# Gerekli veri setlerini indir (eğer daha önce indirilmemişse)
nltk.download("stopwords")

def extract_text_from_pdf(pdf_path):
    """PDF dosyasından metin çıkarır."""
    text = ""
    with fitz.open(pdf_path) as doc:  # Dosya kapanma sorunlarını önler
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()

def extract_keywords(text, num_keywords=10):
    """Metinden en önemli anahtar kelimeleri çıkarır."""
    
    if not text.strip():  # Boş metin hatasını önlemek için kontrol
        return []

    # Küçük harfe çevir ve noktalama işaretlerini temizle
    text = text.lower().translate(str.maketrans("", "", string.punctuation))

    # TF-IDF ile kelime önem skorlarını hesapla
    vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)  # NLTK yerine sklearn stopwords
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_array = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]  # TF-IDF skorlarını al

    # En yüksek skorlu kelimeleri sırala ve en iyi N tanesini döndür
    keyword_scores = sorted(zip(feature_array, scores), key=lambda x: x[1], reverse=True)[:num_keywords]
    return [keyword[0] for keyword in keyword_scores]  # Sadece anahtar kelimeleri döndür

# Örnek Kullanım
if __name__ == "__main__":
    pdf_path = "example.pdf"  # PDF dosya yolunu buraya ekleyin
    if os.path.exists(pdf_path):
        text = extract_text_from_pdf(pdf_path)
        keywords = extract_keywords(text)
        print("Extracted Keywords:", keywords)
    else:
        print("Error: PDF file not found!")



