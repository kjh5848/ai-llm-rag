from pypdf import PdfReader

reader = PdfReader("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/ai-llm-rag/ai-list.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

print(text)
