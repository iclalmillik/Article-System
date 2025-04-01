import os
from django.contrib import messages
from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from apps.articles.models import Article
from .utils import extract_keywords, extract_text_from_pdf
from .anoniymization import anonymize_pdf_auto
from .aes import decrypt_data_aes, encrypt_data_aes, generate_aes_key
from apps.articles.models import Article
from .models import SubjectArea
from .utils import extract_text_from_pdf, extract_keywords  
def analyze_keywords(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if not article.pdf_file or not os.path.exists(article.pdf_file.path):
        messages.error(request, "❌ PDF file not found. Please upload the article again.")
        return redirect('review:article_detail', article_id=article.id)  # veya uygun başka bir sayfa

    # PDF'ten metni çıkar
    pdf_text = extract_text_from_pdf(article.pdf_file.path)

    # Anahtar kelimeleri analiz et
    keywords = extract_keywords(pdf_text)

    # Tüm alanları çek (dropdown için)
    subject_areas = SubjectArea.objects.all()

    if request.method == 'POST':
        selected_area_id = request.POST.get('subject_area')
        new_area_name = request.POST.get('new_area', '').strip()

        if new_area_name:
            new_area, created = SubjectArea.objects.get_or_create(name=new_area_name)
            article.subject_area = new_area
        elif selected_area_id:
            article.subject_area_id = selected_area_id

        article.save()
        messages.success(request, "✅ Area assigned successfully.")
        return redirect('analysis:analyze_keywords', article_id=article.id)

    return render(request, 'analysis/analyze_keywords.html', {
        'keywords': keywords,
        'article': article,
        'subject_areas': subject_areas,
    })



from django.core.files.base import ContentFile
def anonymization_pdf(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    output_path = article.pdf_file.path.replace('.pdf', '_anonymized.pdf')

    if request.method == 'POST':
        hide_name  = request.POST.get('hide_name') == 'on'
        hide_org   = request.POST.get('hide_org') == 'on'
        hide_email = request.POST.get('hide_email') == 'on'
        org_whitelist = ["Some Trusted Organization", "Another Org"]

        try:
            # Anonimleştirme  + bilgi toplama
            redacted_text_info = anonymize_pdf_auto(
                input_pdf  = article.pdf_file.path,
                output_pdf = output_path,
                hide_name  = hide_name,
                hide_org   = hide_org,
                hide_email = hide_email,
                org_whitelist = org_whitelist
            )
        except Exception as e:
            print("Anonimleştirme sırasında hata oluştu:", e)
            redacted_text_info = ""

        # AES ile şifreleme
        aes_key = generate_aes_key()
        encrypted_info = encrypt_data_aes(redacted_text_info, aes_key)
        print("🔐 Encrypted Redacted Information:\n", encrypted_info)

        # AES ile çözüm 
        try:
            decrypted_info = decrypt_data_aes(encrypted_info, aes_key)
            print("🔓 Decrypted Redacted Information:\n", decrypted_info)
        except Exception as e:
            print("Şifre çözme sırasında hata:", e)
            decrypted_info = ""

     
        article.encrypted_info = encrypted_info
        article.save()

     
        if os.path.exists(output_path):
            with open(output_path, 'rb') as f:
                file_data = f.read()
            file_name = f"{article.id}_anonymized.pdf"
            article.anonymized_file.save(file_name, ContentFile(file_data))
            article.save()

        anonymized_file_url = article.anonymized_file.url if article.anonymized_file else None
        return render(request, 'anonymization_setting.html', {
            'article': article,
            'anonymized_file_url': anonymized_file_url,
            'hide_name': hide_name,
            'hide_org': hide_org,
            'hide_email': hide_email,
            'encrypted_info': encrypted_info,
            'decrypted_info': decrypted_info,
        })

    anonymized_file_url = article.anonymized_file.url if article.anonymized_file else None
    return render(request, 'anonymization_setting.html', {
        'article': article,
        'anonymized_file_url': anonymized_file_url,
    })
