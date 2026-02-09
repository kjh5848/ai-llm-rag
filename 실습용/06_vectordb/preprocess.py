import os
import glob
from ai_pdf_to_md import refine_pdf_to_md_with_ai
from image_to_md import generate_image_markdown
from office_to_md import parse_docx_to_markdown, parse_excel_to_markdown

def preprocess_documents():
    """
    data/docs 하위의 모든 문서를 마크다운으로 변환합니다.
    폴더 구조(hr, ops 등)를 메타데이터로 활용합니다.
    """
    base_dir = "data/docs"
    output_base_dir = "parsed_data"

    if not os.path.exists(base_dir):
        print(f"❌ '{base_dir}' 폴더가 없습니다. 경로를 확인해주세요.")
        return

    print("🚀 사내 문서 전처리(Preprocessing) 시작...")
    
    # Walk through all directories and files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Determine category from folder name (e.g., data/docs/hr -> hr)
            relative_path = os.path.relpath(root, base_dir)
            category = relative_path if relative_path != "." else "general"
            
            output_dir = os.path.join(output_base_dir, category)
            os.makedirs(output_dir, exist_ok=True)
            
            file_name_no_ext = os.path.splitext(file)[0]
            
            if file.lower().endswith('.pdf'):
                output_md = os.path.join(output_dir, f"{file_name_no_ext}.md")
                print(f"📄 PDF 변환 중 (AI): {file} (Category: {category})")
                refine_pdf_to_md_with_ai(file_path, output_md)
                
            elif file.lower().endswith(('.png', '.jpg', '.jpeg')):
                output_md = os.path.join(output_dir, f"{file_name_no_ext}.md")
                print(f"🖼️ 이미지 분석 중: {file} (Category: {category})")
                generate_image_markdown(file_path, output_md)
                
            elif file.lower().endswith('.docx'):
                output_md = os.path.join(output_dir, f"{file_name_no_ext}.md")
                print(f"📄 Word 변환 중: {file} (Category: {category})")
                parse_docx_to_markdown(file_path, output_md)

            elif file.lower().endswith('.xlsx'):
                output_md = os.path.join(output_dir, f"{file_name_no_ext}.md")
                print(f"📊 Excel 변환 중: {file} (Category: {category})")
                parse_excel_to_markdown(file_path, output_md)

    print("\n✅ 모든 문서 처리가 완료되었습니다.")

if __name__ == "__main__":
    preprocess_documents()
