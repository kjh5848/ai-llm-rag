import os
import glob
import argparse
from scripts.converter.pdf_strategy import convert_pdf_to_md
from scripts.converter.docx_strategy import convert_docx_to_md
from scripts.converter.xlsx_strategy import convert_xlsx_to_md
from scripts.embedding.embed_strategy import embed_md_file

# 설정
RAW_DATA_DIRS = ["data/docs"]  # 기존 raw 폴더와 docs 폴더 모두 감지
PROCESSED_DIR = "data/processed"
VECTOR_DB_DIR = "data/embedding_db"

def run_ingestion(target_file=None):
    """
    데이터 감지 -> 변환 -> 임베딩 통합 파이프라인
    :param target_file: 특정 파일만 처리하고 싶을 때 파일명 또는 패턴
    """
    print("=== Metacoding AI Assistant Ingestion Started ===")
    
    # 1. 지원하는 파일 패턴 정의
    patterns = {
        "**/*.pdf": convert_pdf_to_md,
        "**/*.docx": convert_docx_to_md,
        "**/*.xlsx": convert_xlsx_to_md
    }
    
    for raw_dir in RAW_DATA_DIRS:
        if not os.path.exists(raw_dir):
            continue
            
        print(f"-> Scanning directory: {raw_dir}")
        for pattern, strategy_func in patterns.items():
            # recursive=True를 통해 하위 폴더까지 탐색
            files = glob.glob(os.path.join(raw_dir, pattern), recursive=True)
            for file_path in files:
                file_name = os.path.basename(file_path)
                
                # 특정 파일 인자가 있는 경우 필터링
                if target_file and target_file not in file_name:
                    continue

                output_name = f"{os.path.splitext(file_name)[0]}.md"
                output_path = os.path.join(PROCESSED_DIR, output_name)
                
                print(f"   [Process] {file_name} ...")
                # Step 1: File to MD
                strategy_func(file_path, output_path)
                
                # Step 2: MD to Embedding
                embed_md_file(output_path, VECTOR_DB_DIR)
            
    print("=== Ingestion Completed ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Metacoding AI Assistant Data Ingestion")
    parser.add_argument("--file", "-f", help="특정 파일명 또는 패턴만 처리하고 싶을 때 사용")
    args = parser.parse_args()

    # 필요한 디렉토리 생성
    for directory in RAW_DATA_DIRS:
        os.makedirs(directory, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    
    run_ingestion(target_file=args.file)
