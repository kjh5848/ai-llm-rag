import os
import glob
import subprocess
from typing import List, Dict

class IngestService:
    def __init__(self):
        self.docs_dir = "docs"
        self.md_dir = "data/markdown_docs"
        print(f"[IngestService] Initialized with docs_dir: {self.docs_dir}")

    def get_file_status(self) -> List[Dict]:
        """문서 폴더 내 파일들의 변환 및 임베딩 상태 확인"""
        files = []
        # 원본 파일 목록
        doc_files = glob.glob(os.path.join(self.docs_dir, "*.*"))
        
        for f in doc_files:
            if f.endswith('.md'): continue
            
            base_name = os.path.basename(f)
            md_path = os.path.join(self.md_dir, base_name + ".md")
            
            # 상태 체크
            is_converted = os.path.exists(md_path)
            # 임베딩 여부는 간단히 vector db 존재 여부로 판단 (실제로는 파일별 관리가 필요하지만 현재는 전체 단위)
            is_embedded = os.path.exists("data/embedding_db") if is_converted else False
            
            files.append({
                "name": base_name,
                "type": base_name.split('.')[-1].upper(),
                "converted": is_converted,
                "embedded": is_embedded
            })
        return files

    def run_convert(self, filename: str = None):
        """파일 변환 수행 (ingest.py 호출)"""
        cmd = ["./venv/bin/python", "ingest.py", "--mode", "convert"]
        if filename:
            cmd.extend(["--file", filename])
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            print(f"[IngestService] Conversion error: {e}")
            return False

    def run_embed(self):
        """임베딩 수행 (ingest.py 호출)"""
        try:
            subprocess.run(["./venv/bin/python", "ingest.py", "--mode", "embed"], check=True)
            return True
        except Exception as e:
            print(f"[IngestService] Embedding error: {e}")
            return False

# 싱글톤 인스턴스
ingest_service = IngestService()
