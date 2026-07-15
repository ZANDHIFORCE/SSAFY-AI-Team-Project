import os
import sys
import unittest
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# backend 폴더를 sys.path에 동적으로 추가
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_path)

# .env 파일 로드
load_dotenv(dotenv_path=os.path.join(backend_path, ".env"))


class TestOpenAIConnection(unittest.TestCase):
    def test_openai_api_key_exists(self):
        """OPENAI_API_KEY 환경 변수가 로드되었는지 확인"""
        api_key = os.getenv("OPENAI_API_KEY")
        self.assertIsNotNone(api_key, "OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        self.assertTrue(api_key.startswith("sk-"), "OPENAI_API_KEY 형식이 올바르지 않습니다 ('sk-'로 시작해야 함).")

    def test_openai_api_connection(self):
        """실제 OpenAI API 호출을 통한 연결 상태 및 응답 테스트"""
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL", "gpt-5-mini")

        if not api_key:
            self.skipTest("OPENAI_API_KEY가 존재하지 않아 API 연결 테스트를 건너뜁니다.")

        # API 키 마스킹 출력
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "Too short"
        print(f"\n[Info] OpenAI API 연결 테스트 중...")
        print(f"[Info] API Key: {masked_key}")
        print(f"[Info] Model: {model_name}")

        try:
            client = OpenAI(api_key=api_key)
            
            # gpt-5-mini가 존재하지 않는 모델일 경우를 대비해, 
            # API 호출이 실패하면 gpt-4o-mini 등으로 자동 폴백해서 테스트할 수 있게 설계
            models_to_try = [model_name, "gpt-4o-mini", "gpt-3.5-turbo"]
            
            last_err = None
            for model in models_to_try:
                try:
                    print(f"[Info] '{model}' 모델로 API 호출 시도 중...")
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "user", "content": "Hello, this is a connection test. Please reply with 'OK'."}
                        ],
                        max_tokens=10
                    )
                    content = response.choices[0].message.content.strip()
                    print(f"[Success] API 호출 성공! 응답 내용: {content}")
                    
                    self.assertIsNotNone(content)
                    self.assertGreater(len(content), 0)
                    return  # 성공 시 테스트 종료
                except OpenAIError as err:
                    last_err = err
                    print(f"[Warning] '{model}' 모델 호출 실패: {err}")
            
            if last_err:
                raise last_err

        except OpenAIError as e:
            self.fail(f"OpenAI API 연결 실패 (OpenAIError): {e}")
        except Exception as e:
            self.fail(f"OpenAI API 연결 실패 (UnexpectedError): {e}")


if __name__ == "__main__":
    unittest.main()
