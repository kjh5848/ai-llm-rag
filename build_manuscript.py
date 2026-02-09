import os
import re

def build_final_manuscript():
    # 1. 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(base_dir, "00_manuscript")
    output_file = os.path.join(source_dir, "전체_최종본.md")
    
    # 2. 01장 ~ 10장 디렉토리 목록 가져오기 (숫자 순서로 정렬)
    chapters = sorted([d for d in os.listdir(source_dir) 
                      if os.path.isdir(os.path.join(source_dir, d)) and re.match(r'^\d+장', d)])
    
    final_content = []
    
    print(f"🚀 빌드 시작: {output_file}")
    
    for chapter in chapters:
        chapter_path = os.path.join(source_dir, chapter)
        # 각 장 폴더 내부에서 '02.본문.md' 또는 '본문.md' 파일을 찾습니다.
        # 08장처럼 '집필.md' 등이 섞여 있을 수 있으니 우선순위를 둡니다.
        priority_files = ["02.본문.md", "본문.md", "집필.md"]
        target_file = None
        
        for pf in priority_files:
            if os.path.exists(os.path.join(chapter_path, pf)):
                target_file = pf
                break
        
        if target_file:
            print(f"  - {chapter} 합치는 중... ({target_file})")
            with open(os.path.join(chapter_path, target_file), "r", encoding="utf-8") as f:
                content = f.read().strip()
                # '#'으로 시작하는 제목이 없는 경우 장 제목 추가 (옵션)
                # content = f"# {chapter}\n\n" + content
                final_content.append(content)
                final_content.append("\n\n---\n\n") # 장 사이 구분선
        else:
            print(f"  ⚠️ {chapter}에서 본문 파일을 찾을 수 없습니다. 건너뜁니다.")

    # 3. 최종본 저장
    if final_content:
        # 마지막 구분선 제거
        final_content.pop()
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(final_content))
        print(f"✅ 빌드 완료! 총 {len(chapters)}개의 장이 통합되었습니다.")
    else:
        print("❌ 통합할 내용을 찾지 못했습니다.")

if __name__ == "__main__":
    build_final_manuscript()
