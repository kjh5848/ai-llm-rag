import sys
import os
import time

try:
    from playwright.sync_api import sync_playwright
    
    def html_to_pdf(html_path, pdf_path):
        print(f"Browser Launching...")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # 절대 경로 변환
            abs_html_path = os.path.abspath(html_path)
            if not os.path.exists(abs_html_path):
                print(f"❌ HTML 파일을 찾을 수 없음: {abs_html_path}")
                return

            url = f"file://{abs_html_path}"
            print(f"Loading: {url}")
            page.goto(url)
            
            # 렌더링 대기
            time.sleep(1)
            
            # PDF 저장
            page.pdf(path=pdf_path, format="A4", print_background=True, margin={"top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm"})
            browser.close()
            
            if os.path.exists(pdf_path):
                print(f"✅ PDF 생성 성공: {pdf_path}")
                print(f"   Size: {os.path.getsize(pdf_path)} bytes")
            else:
                print(f"❌ PDF 파일이 생성되지 않음.")

except ImportError:
    print("❌ Playwright 모듈이 설치되지 않았습니다.")
    sys.exit(1)
except Exception as e:
    print(f"❌ 에러 발생: {e}")
    sys.exit(1)

if __name__ == "__main__":
    html_file = "실습용/ex01/data/13_layout_test/13_다단편집_사내규정.html"
    pdf_file = "실습용/ex01/data/13_layout_test/13_다단편집_사내규정.pdf"
    
    # HTML 파일 존재 확인
    if not os.path.exists(html_file):
        print(f"ERROR: HTML file not found at {html_file}")
    else:
        html_to_pdf(html_file, pdf_file)
