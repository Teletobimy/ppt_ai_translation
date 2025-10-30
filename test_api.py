# test_api.py
# API 키 테스트

import os

def test_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"API Key found: {api_key[:10]}...{api_key[-4:]}")
        return True
    else:
        print("API Key not found")
        return False

if __name__ == "__main__":
    test_api_key()
