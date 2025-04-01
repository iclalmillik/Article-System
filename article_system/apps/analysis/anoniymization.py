import fitz  
import spacy
import re
from rapidfuzz import fuzz  
import cv2
import numpy as np



# NLP modeli 
nlp = spacy.load("en_core_web_trf")

def normalize_text(text):
   
    return " ".join(text.split()).lower()

def find_instances(page, target, threshold=85):
  
    instances = page.search_for(target)
    if instances:
        return instances

    norm_target = normalize_text(target)
    found_instances = []
    blocks = page.get_text("blocks")
    for b in blocks:
        block_rect = fitz.Rect(b[0], b[1], b[2], b[3])
        norm_block = normalize_text(b[4])
        score = fuzz.partial_ratio(norm_target, norm_block)
        if score >= threshold:
            found_instances.append(block_rect)
    return found_instances

def is_similar(candidate, pre_names, threshold=85):
   
    candidate_norm = normalize_text(candidate)
    for pre_name in pre_names:
        if fuzz.partial_ratio(candidate_norm, normalize_text(pre_name)) >= threshold:
            return True
    return False

def blur_images_on_page(doc, page, page_number, blur_kernel=(81, 81)):
   
 
    try:
        page_dict = page.get_text("dict")
        for block in page_dict["blocks"]:
            if block.get("type") == 1 and "image" in block:
                image_data = block["image"]
                if isinstance(image_data, int):
                    try:
                        img_dict = doc.extract_image(image_data)
                        img_bytes = img_dict["image"]
                    except Exception as e:
                        print(f"Page {page_number}: Error extracting image by xref: {e}")
                        continue
                elif isinstance(image_data, bytes):
                    img_bytes = image_data
                else:
                    print(f"Page {page_number}: Unsupported image data type: {type(image_data)}. Skipping block.")
                    continue

                bbox = block["bbox"]
                try:
                    np_arr = np.frombuffer(img_bytes, np.uint8)
                    img_cv = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    if img_cv is None:
                        print(f"Page {page_number}: OpenCV failed to decode image.")
                        continue
                  
                    blurred_cv = cv2.GaussianBlur(img_cv, blur_kernel, 0)
                    success, encoded_image = cv2.imencode(".png", blurred_cv)
                    if not success:
                        print(f"Page {page_number}: OpenCV failed to encode image.")
                        continue
                    new_img_bytes = encoded_image.tobytes()
                    page.insert_image(fitz.Rect(bbox), stream=new_img_bytes, overlay=True)
                    print(f"Page {page_number}: Blurred image inserted at {bbox}.")
                except Exception as inner_e:
                    print(f"Page {page_number}: Error processing image block: {inner_e}")
    except Exception as e:
        print(f"Page {page_number}: Error in blur_images_on_page function: {e}")

def anonymize_pdf_auto(input_pdf, output_pdf, hide_name=True, hide_org=True, hide_email=True, org_whitelist=None):
    
   
    if org_whitelist is None:
        org_whitelist = []
    
    doc = fitz.open(input_pdf)
    abstract_encountered = False
    references_encountered = False
    pre_abstract_names = set()
    redacted_info_list = []
    
    for page_number, page in enumerate(doc):
        text = page.get_text("text")
        lower_text = text.lower()
        abstract_index = lower_text.find("abstract")
        references_index = lower_text.find("references")
        
        # absratct öncesi
        if not abstract_encountered:
            if abstract_index != -1:
                text_to_process = text[:abstract_index]
                abstract_encountered = True
                print(f"Page {page_number}: Processing pre-abstract section.")
            else:
                text_to_process = text
                print(f"Page {page_number}: No 'abstract' found; processing entire page as pre-abstract.")
            
            targets = set()
            doc_spacy = nlp(text_to_process)
            if hide_name:
                names_found = {ent.text for ent in doc_spacy.ents if ent.label_ == "PERSON"}
                pre_abstract_names.update(names_found)
                targets |= names_found
            if hide_org:
                org_found = {ent.text for ent in doc_spacy.ents
                             if ent.label_ == "ORG" and ent.text.lower() not in [o.lower() for o in org_whitelist]}
                targets |= org_found
            if hide_email:
                email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
                emails_found = set(re.findall(email_pattern, text_to_process))
                targets |= emails_found
            
           
            for target in targets:
                redacted_info_list.append(target)
                instances = find_instances(page, target)
                if not instances:
                    print(f"Page {page_number}: Pre-abstract target not found: {target}")
                    continue
                for inst in instances:
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                try:
                    page.apply_redactions()
                    for inst in instances:
                        x, y = inst[0], inst[1]
                        page.insert_text((x, y + 9), "***", fontsize=10, color=(1, 1, 1))
                except Exception as e:
                    print(f"Page {page_number}: Error redacting pre-abstract target '{target}': {e}")
        
        # references bölümü
        elif not references_encountered and references_index != -1:
            references_encountered = True
            text_to_process = text[references_index:]
            print(f"Page {page_number}: Processing references section.")
            targets = set()
            if hide_name:
                names_found = {ent.text for ent in nlp(text_to_process).ents if ent.label_ == "PERSON"}
                names_to_redact = {candidate for candidate in names_found if is_similar(candidate, pre_abstract_names)}
                targets |= names_to_redact
            for target in targets:
                redacted_info_list.append(target)
                instances = find_instances(page, target)
                if not instances:
                    print(f"Page {page_number}: References target not found: {target}")
                    continue
                for inst in instances:
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                try:
                    page.apply_redactions()
                    for inst in instances:
                        x, y = inst[0], inst[1]
                        page.insert_text((x, y + 9), "***", fontsize=10, color=(1, 1, 1))
                except Exception as e:
                    print(f"Page {page_number}: Error redacting references target '{target}': {e}")
            
           
            blur_images_on_page(doc, page, page_number)
        
        # references sonrası 
        elif references_encountered:
            text_to_process = text
            print(f"Page {page_number}: Continuing processing in references section.")
            targets = set()
            if hide_name:
                names_found = {ent.text for ent in nlp(text_to_process).ents if ent.label_ == "PERSON"}
                names_to_redact = {candidate for candidate in names_found if is_similar(candidate, pre_abstract_names)}
                targets |= names_to_redact
            for target in targets:
                redacted_info_list.append(target)
                instances = find_instances(page, target)
                if not instances:
                    print(f"Page {page_number}: Continued references target not found: {target}")
                    continue
                for inst in instances:
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                try:
                    page.apply_redactions()
                    for inst in instances:
                        x, y = inst[0], inst[1]
                        page.insert_text((x, y + 9), "***", fontsize=10, color=(1, 1, 1))
                except Exception as e:
                    print(f"Page {page_number}: Error redacting continued references target '{target}': {e}")
            
            blur_images_on_page(doc, page, page_number)
        else:
            print(f"Page {page_number}: Skipping section between abstract and references.")
            continue
    
    doc.save(output_pdf)
    
  #toplanan bilgileri birleştirme
    redacted_info = ", ".join(redacted_info_list)
    return redacted_info
