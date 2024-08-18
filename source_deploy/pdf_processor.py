import os
import pdfplumber
import spacy
import re
from unidecode import unidecode

class PDFProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.family_names = [
            'nguyen', 'tran', 'le', 'pham', 'vu', 'hoang', 'ngo', 'dang', 'bui', 'duong',
            'do', 'ha', 'dao', 'ly', 'ho', 'cao', 'van', 'to',
            'bach', 'chau', 'chung', 'luong', 'lam', 'loc', 'nghiem',
            'quang', 'phan', 'vo', 'son', 'hong', 'khanh', 'mac', 'hoai',
            'tang', 'ta', 'nghiem', 'phu', 'luc', 'quyen', 'tong', 'mau', 'hanh',
            'giang', 'tu', 'ba', 'phuong', 'khưu', 'diep', 'ham', 'dinh', 'phuc',
            'hanh', 'mai', 'lien', 'nho', 'ton', 'ngoc',
            'a', 'au', 'bao', 'bang', 'bac', 'ban', 'cat', 'can', 'cang',
            'cuong', 'co', 'cu', 'dao', 'doan', 'dinh', 'dau', 'duy', 'dien',
            'gia', 'hoai', 'hoa', 'hung', 'huynh', 'hue', 'khu', 'kim', 'kien',
            'kinh', 'la', 'lan', 'lien', 'mon', 'man', 'minh', 'nghia', 'nhan',
            'ninh', 'nham', 'nhat', 'pho', 'quach', 'quan', 'quang', 'quyen',
            'ton', 'tu', 'tong', 'van', 'vo', 'vu'
        ]

    def remove_accents(self, text):
        return unidecode(text)

    def is_vietnamese_name(self, name):
        name_no_accents = self.remove_accents(name.lower())
        parts = name_no_accents.split()
        surname = parts[0]
        return surname in self.family_names

    def extract_text_from_pdf(self, pdf_path, lines_to_read=20):
        text = ""
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"{pdf_path} không tồn tại hoặc không phải là tệp.")
        with pdfplumber.open(pdf_path) as pdf:
            for i in range(min(len(pdf.pages), 10)):
                page = pdf.pages[i]
                lines = page.extract_text().splitlines()
                for line in lines[:lines_to_read]:
                    text += line + "\n"
        return text

    def extract_names_and_emails(self, text):
        text_no_accents = self.remove_accents(text)
        doc = self.nlp(text_no_accents)
        
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        filtered_names = []
        for name in names:
            if len(name.split()) >= 2 and self.is_vietnamese_name(name):
                filtered_names.append(name)
                break 
        
        emails = list(set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_no_accents)))
        
        return filtered_names, emails

