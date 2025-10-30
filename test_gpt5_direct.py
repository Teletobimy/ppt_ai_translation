# test_gpt5_direct.py
# GPT-5 직접 테스트 스크립트

import os
import sys
from translation_engine import gpt_translate_tagged, create_openai_client

def test_gpt5_direct():
    """GPT-5 직접 테스트"""
    
    print("GPT-5 직접 번역 테스트 시작\n")
    
    # API 키를 직접 입력받거나 환경변수에서 가져오기
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API 키를 입력해주세요:")
        api_key = input().strip()
        if not api_key:
            print("API 키가 없어서 테스트를 종료합니다.")
            return False
    
    print(f"사용할 모델: GPT-5")
    print(f"API 키: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '***'}")
    print()
    
    # 테스트 케이스
    test_text = "[[R1]]피더린은 혁신적인 뷰티 기술로 피부를 더욱 건강하고 아름답게 만들어줍니다.[[/R1]]"
    
    print(f"원문: {test_text}")
    print()
    
    try:
        # 클라이언트 생성
        client = create_openai_client(api_key)
        print("OpenAI 클라이언트 생성 완료")
        
        # 영어 번역 테스트
        print("\n=== 영어 번역 테스트 ===")
        english_result = gpt_translate_tagged(
            test_text, 
            client, 
            "English", 
            "기본값", 
            use_deepseek=False
        )
        print(f"영어 번역: {english_result}")
        
        # 중국어 번역 테스트
        print("\n=== 중국어 번역 테스트 ===")
        chinese_result = gpt_translate_tagged(
            test_text, 
            client, 
            "Chinese (Simplified)", 
            "기본값", 
            use_deepseek=False
        )
        print(f"중국어 번역: {chinese_result}")
        
        # 일본어 번역 테스트
        print("\n=== 일본어 번역 테스트 ===")
        japanese_result = gpt_translate_tagged(
            test_text, 
            client, 
            "Japanese", 
            "기본값", 
            use_deepseek=False
        )
        print(f"일본어 번역: {japanese_result}")
        
        print("\nGPT-5 번역 테스트 완료!")
        return True
        
    except Exception as e:
        print(f"오류 발생: {e}")
        print(f"오류 타입: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_gpt5_direct()
