import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def embed_md_file(md_path, db_dir):
    """
    MD 파일을 읽어 텍스트 분할 후 임베딩 및 벡터 DB 저장
    """
    print(f"[Embed Strategy] Processing {md_path}...")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. 텍스트 분할 (Semantic Chunking을 위한 기본 단계)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(content)
    
    # 2. 임베딩 모델 설정
    embed_model = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask",
        model_kwargs={'device': 'cpu'}
    )
    
    # 3. 벡터 DB 저장 (Chroma)
    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embed_model,
        persist_directory=db_dir,
        metadatas=[{"source": os.path.basename(md_path)} for _ in chunks]
    )
    
    print(f"  -> Embedded {len(chunks)} chunks to {db_dir}")

if __name__ == "__main__":
    # Test code
    pass
