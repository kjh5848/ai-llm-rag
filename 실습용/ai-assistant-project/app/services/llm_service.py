import os
import json
from langchain_community.llms import Ollama
from jinja2 import Environment, FileSystemLoader

class LLMService:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("LLM_MODEL_NAME", "deepseek-r1:8b")
        
        # Jinja2 템플릿 환경 설정
        template_dir = os.path.join(os.path.dirname(__file__), "prompts")
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        
        print(f"[LLMService] Initializing with {self.ollama_url}, model: {self.model_name}")
        self.llm = Ollama(base_url=self.ollama_url, model=self.model_name)

    def render_prompt(self, template_name: str, **kwargs) -> str:
        """템플릿을 렌더링합니다."""
        template = self.jinja_env.get_template(template_name)
        return template.render(**kwargs)

    def invoke(self, prompt: str) -> str:
        """LLM을 직접 호출합니다."""
        try:
            response = self.llm.invoke(prompt)
            # 사고 과정(CoT) 제거
            if "<think>" in response and "</think>" in response:
                response = response.split("</think>")[-1].strip()
            return response
        except Exception as e:
            print(f"[LLMService] Invoke error: {e}")
            return f"오류 발생: {str(e)}"

    def generate_answer(self, query: str, context: str) -> str:
        """템플릿을 사용하여 답변을 생성합니다."""
        rendered_prompt = self.render_prompt("answer_prompt.j2", query=query, context=context)
        return self.invoke(rendered_prompt)

    def classify_intent(self, query: str) -> dict:
        """라우터 템플릿을 사용하여 질문의 의도를 분석합니다."""
        rendered_prompt = self.render_prompt("router_prompt.j2", query=query)
        response = self.invoke(rendered_prompt)
        
        try:
            # JSON만 추출 (모델이 추가 설명을 붙일 경우 대비)
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            return {"route": "hybrid", "reason": "JSON 파싱 실패"}
        except:
            return {"route": "hybrid", "reason": "분석 오류 발생"}

# 싱글톤 인스턴스
llm_service = LLMService()
