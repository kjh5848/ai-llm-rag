import os
import pandas as pd
from docx import Document
from datetime import datetime

def parse_docx_to_markdown(docx_path, output_path):
    """
    Word(.docx) 문서를 마크다운으로 변환합니다.
    """
    print(f"📄 Word 변환 중: {docx_path}")
    
    if not os.path.exists(docx_path):
        print(f"❌ 에러: 파일을 찾을 수 없습니다.")
        return

    try:
        doc = Document(docx_path)
        file_name = os.path.basename(docx_path)
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        md_content = f"""---
title: {file_name}
type: document
source: {docx_path}
date: {current_date}
---

"""
        for para in doc.paragraphs:
            if para.style.name.startswith('Heading'):
                level = int(para.style.name.split(' ')[-1])
                md_content += f"{'#' * level} {para.text}\n\n"
            else:
                md_content += f"{para.text}\n\n"
                
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        print(f"✅ Word 변환 완료: {output_path}")

    except Exception as e:
        print(f"❌ Word 변환 실패: {str(e)}")

def parse_excel_to_markdown(excel_path, output_path):
    """
    Excel(.xlsx) 문서를 마크다운 표로 변환합니다.
    """
    print(f"📊 Excel 변환 중: {excel_path}")
    
    if not os.path.exists(excel_path):
        print(f"❌ 에러: 파일을 찾을 수 없습니다.")
        return

    try:
        # Read all sheets
        xls = pd.ExcelFile(excel_path)
        file_name = os.path.basename(excel_path)
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        md_content = f"""---
title: {file_name}
type: spreadsheet
source: {excel_path}
date: {current_date}
---

"""
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            md_content += f"## Sheet: {sheet_name}\n\n"
            md_content += df.to_markdown(index=False)
            md_content += "\n\n"
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        print(f"✅ Excel 변환 완료: {output_path}")

    except Exception as e:
        print(f"❌ Excel 변환 실패: {str(e)}")

if __name__ == "__main__":
    # Test execution for Word
    docx_sample = "data/docs/general/Guide_v1.docx"
    docx_output = "parsed_data/general/Guide_v1.md"
    parse_docx_to_markdown(docx_sample, docx_output)

    # Test execution for Excel
    xlsx_sample = "data/docs/finance/Stats_2025.xlsx" 
    xlsx_output = "parsed_data/finance/Stats_2025.md"
    parse_excel_to_markdown(xlsx_sample, xlsx_output)
