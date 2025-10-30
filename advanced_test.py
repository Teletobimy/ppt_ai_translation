# advanced_test.py
# 고급 GPT-5 번역 테스트

import os
from translation_engine import gpt_translate_tagged, create_openai_client

def advanced_test():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API 키가 없습니다.")
        return
    
    print("GPT-5 고급 번역 테스트 시작\n")
    
    try:
        client = create_openai_client(api_key)
        print("클라이언트 생성 성공")
        
        # 복잡한 뷰티 제품 설명 테스트
        test_cases = [
            {
                "text": "[[R1]]피더린은 혁신적인 뷰티 기술로 피부를 더욱 건강하고 아름답게 만들어줍니다.[[/R1]]",
                "lang": "English",
                "tone": "기본값"
            },
            {
                "text": "[[R1]]이 제품은 FDA 승인을 받은 안전한 성분으로만 제조되었습니다.[[/R1]]",
                "lang": "English", 
                "tone": "Med/Pharma Pro (20y)"
            },
            {
                "text": "[[R1]]20대 여성들을 위한 트렌디한 뷰티 제품을 소개합니다.[[/R1]]",
                "lang": "English",
                "tone": "GenZ Female (20s)"
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"=== 테스트 {i}: {case['tone']} 톤 ===")
            print(f"원문: {case['text']}")
            
            result = gpt_translate_tagged(
                case['text'], 
                client, 
                case['lang'], 
                case['tone'], 
                False
            )
            print(f"번역: {result}")
            print()
        
        print("GPT-5 고급 번역 테스트 완료!")
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    advanced_test()
