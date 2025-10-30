# simple_test.py
# 간단한 GPT-5 테스트

import os
from translation_engine import gpt_translate_tagged, create_openai_client

def simple_test():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API 키가 없습니다.")
        return
    
    print("API 키 확인됨:", api_key[:10] + "...")
    
    try:
        client = create_openai_client(api_key)
        print("클라이언트 생성 성공")
        
        # 간단한 번역 테스트
        test_text = "[[R1]]안녕하세요[[/R1]]"
        print("원문:", test_text)
        
        result = gpt_translate_tagged(test_text, client, "English", "기본값", False)
        print("번역 결과:", result)
        
    except Exception as e:
        print("오류:", str(e))

if __name__ == "__main__":
    simple_test()
