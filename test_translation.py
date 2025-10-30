# test_translation.py
# GPT-5 번역 품질 테스트 스크립트

import os
from translation_engine import gpt_translate_tagged, create_openai_client, build_prompt

def test_gpt5_translation():
    """GPT-5 번역 품질 테스트"""
    
    # API 키 확인
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ OPENAI_API_KEY 환경변수를 설정해주세요.")
        return False
    
    print("GPT-5 번역 품질 테스트 시작\n")
    
    # 테스트 케이스들
    test_cases = [
        {
            "text": "[[R1]]피더린은 혁신적인 뷰티 기술로 피부를 더욱 건강하고 아름답게 만들어줍니다.[[/R1]]",
            "target_lang": "English",
            "tone": "기본값",
            "description": "한국어 → 영어 (뷰티 제품 설명)"
        },
        {
            "text": "[[R1]]고객 만족도가 95%를 넘어서는 성과를 거두었습니다.[[/R1]]",
            "target_lang": "Chinese (Simplified)",
            "tone": "기본값",
            "description": "한국어 → 중국어 간체 (비즈니스 성과)"
        },
        {
            "text": "[[R1]]이 제품은 FDA 승인을 받은 안전한 성분으로만 제조되었습니다.[[/R1]]",
            "target_lang": "German",
            "tone": "Med/Pharma Pro (20y)",
            "description": "한국어 → 독일어 (의료기기 전문 톤)"
        },
        {
            "text": "[[R1]]20대 여성들을 위한 트렌디한 뷰티 제품을 소개합니다.[[/R1]]",
            "target_lang": "Japanese",
            "tone": "GenZ Female (20s)",
            "description": "한국어 → 일본어 (젊은 여성 타깃)"
        }
    ]
    
    client = create_openai_client(openai_api_key)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"테스트 {i}: {test_case['description']}")
        print(f"원문: {test_case['text']}")
        
        try:
            # 번역 실행
            translated = gpt_translate_tagged(
                test_case['text'],
                client,
                test_case['target_lang'],
                test_case['tone'],
                use_deepseek=False
            )
            
            print(f"번역: {translated}")
            
            # 품질 평가
            if translated and translated != test_case['text']:
                print("OK - 번역 성공")
            else:
                print("ERROR - 번역 실패 또는 원문과 동일")
            
        except Exception as e:
            print(f"ERROR - 오류 발생: {e}")
        
        print("-" * 60)
    
    print("GPT-5 번역 테스트 완료!")
    return True

def test_prompt_quality():
    """프롬프트 품질 테스트"""
    print("\n프롬프트 품질 테스트")
    
    test_text = "[[R1]]피더린은 혁신적인 뷰티 기술로 피부를 더욱 건강하고 아름답게 만들어줍니다.[[/R1]]"
    
    # 영어 프롬프트
    english_prompt = build_prompt(test_text, "English", "기본값")
    print("영어 프롬프트:")
    print(english_prompt[:200] + "...")
    print()
    
    # 중국어 프롬프트
    chinese_prompt = build_prompt(test_text, "Chinese (Simplified)", "기본값")
    print("중국어 프롬프트:")
    print(chinese_prompt[:200] + "...")
    print()

if __name__ == "__main__":
    print("GPT-5 번역 시스템 테스트\n")
    
    # 프롬프트 품질 테스트
    test_prompt_quality()
    
    # 실제 번역 테스트 (API 키가 있는 경우)
    if os.getenv("OPENAI_API_KEY"):
        test_gpt5_translation()
    else:
        print("API 키가 없어서 실제 번역 테스트를 건너뜁니다.")
        print("환경변수 OPENAI_API_KEY를 설정하고 다시 실행하세요.")
