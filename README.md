# 🌐 PPT AI Translation & Comparison

PowerPoint 프레젠테이션을 AI를 사용하여 번역하고, 번역 품질을 평가하며, 원본과 번역본을 비교할 수 있는 Streamlit 웹 애플리케이션입니다.

## ✨ 주요 기능

### 📤 번역
- **다국어 지원**: 12개 언어로 번역 가능
- **톤 선택**: 다양한 비즈니스 톤으로 번역
- **서식 보존**: 원본 PPT의 서식과 레이아웃 유지
- **API 선택**: OpenAI GPT-4 또는 DeepSeek 사용 가능

### 📊 비교
- **슬라이드별 비교**: 원본과 번역본을 슬라이드별로 비교
- **텍스트 비교**: 상세한 텍스트 내용 비교
- **시각적 비교**: 슬라이드 이미지 비교 (기본 구현)

### 🚩 검토
- **자동 품질 평가**: AI가 번역 품질을 자동으로 평가
- **신뢰도 점수**: 0-100% 신뢰도 점수 제공
- **문제점 감지**: 번역의 문제점을 자동으로 감지
- **재번역**: 문제가 있는 번역을 쉽게 재번역

## 🚀 배포 방법

### Streamlit Cloud 배포

1. **GitHub 저장소 준비**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/Teletobimy/ppt_ai_translation.git
   git push -u origin main
   ```

2. **Streamlit Cloud에서 배포**
   - [Streamlit Cloud](https://share.streamlit.io/)에 접속
   - "New app" 클릭
   - GitHub 저장소 연결: `Teletobimy/ppt_ai_translation`
   - Main file path: `streamlit_app.py`
   - "Deploy" 클릭

3. **API 키 설정**
   - Streamlit Cloud 대시보드에서 "Settings" → "Secrets" 이동
   - 다음 내용 추가:
   ```toml
   [api_keys]
   OPENAI_API_KEY = "your_openai_api_key_here"
   DEEPSEEK_API_KEY = "your_deepseek_api_key_here"
   ```

### 로컬 실행

1. **저장소 클론**
   ```bash
   git clone https://github.com/Teletobimy/ppt_ai_translation.git
   cd ppt_ai_translation
   ```

2. **가상환경 생성 및 활성화**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **환경 변수 설정**
   ```bash
   # Windows
   set OPENAI_API_KEY=your_openai_api_key_here
   set DEEPSEEK_API_KEY=your_deepseek_api_key_here
   
   # macOS/Linux
   export OPENAI_API_KEY=your_openai_api_key_here
   export DEEPSEEK_API_KEY=your_deepseek_api_key_here
   ```

5. **애플리케이션 실행**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📁 프로젝트 구조

```
PPT_translation_v1/
├── streamlit_app.py          # 메인 Streamlit 애플리케이션
├── translation_engine.py     # 핵심 번역 로직
├── accuracy_checker.py       # AI 정확도 평가 모듈
├── comparison_ui.py          # 비교 UI 컴포넌트
├── PPT_Language_Change.py    # 기존 데스크톱 앱 (참고용)
├── requirements.txt          # Python 의존성
├── .streamlit/
│   ├── config.toml          # Streamlit 설정
│   └── secrets.toml.template # API 키 템플릿
├── .gitignore               # Git 무시 파일
└── README.md                # 이 파일
```

## 🔧 설정

### API 키 설정

#### Streamlit Cloud
Streamlit Cloud 대시보드의 Secrets 섹션에서 설정:
```toml
[api_keys]
OPENAI_API_KEY = "sk-..."
DEEPSEEK_API_KEY = "sk-..."
```

#### 로컬 개발
환경 변수로 설정하거나 `.streamlit/secrets.toml` 파일 생성:
```toml
[api_keys]
OPENAI_API_KEY = "sk-..."
DEEPSEEK_API_KEY = "sk-..."
```

### 번역 설정

- **대상 언어**: 12개 언어 지원
- **톤 선택**: 4가지 비즈니스 톤
- **API 선택**: OpenAI 또는 DeepSeek (중국어 번역용)

## 🌍 지원 언어

- English
- Indonesian
- Italian
- French
- Spanish
- Korean
- Japanese
- Russian
- German
- Portuguese
- Chinese (Simplified)
- Chinese (Traditional)

## 🎨 톤 옵션

- **기본값**: 일반적인 뷰티 업계 톤
- **Med/Pharma Pro (20y)**: 의료기기/전문약사 20년 전문가 톤
- **Beauty Pro (20y, chic)**: 세련된 뷰티 20년 전문가 톤
- **GenZ Female (20s)**: 20대 여성 타깃의 친근한 톤

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI Models**: OpenAI GPT-4, DeepSeek
- **PPT Processing**: python-pptx
- **Image Processing**: Pillow
- **Deployment**: Streamlit Cloud

## 📝 사용 방법

1. **API 키 설정**: 사이드바에서 OpenAI API 키를 입력하세요
2. **번역 설정**: 대상 언어와 톤을 선택하세요
3. **파일 업로드**: 번역할 PPTX 파일을 업로드하세요
4. **번역 실행**: "번역 시작" 버튼을 클릭하세요
5. **결과 확인**: 비교 탭에서 원본과 번역본을 비교하세요
6. **품질 검토**: 검토 탭에서 플래그된 번역을 확인하세요

## 🔍 문제 해결

### 일반적인 문제

**Q: 번역이 제대로 되지 않아요**
A: API 키가 올바른지 확인하고, 네트워크 연결을 확인해주세요.

**Q: 서식이 깨져요**
A: 복잡한 서식이 있는 경우 일부 서식이 변경될 수 있습니다. 텍스트 내용은 정확히 번역됩니다.

**Q: 신뢰도 점수가 낮아요**
A: 낮은 신뢰도는 번역 품질이 개선될 수 있음을 의미합니다. 재번역 기능을 사용해보세요.

**Q: 시각적 비교가 작동하지 않아요**
A: 시각적 비교는 기본적인 텍스트 렌더링을 사용합니다. 정확한 슬라이드 이미지가 필요한 경우 텍스트 비교를 사용하세요.

### 로그 확인

오류가 발생한 경우 `error.log` 파일을 확인하세요.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

문제가 있거나 개선 사항이 있으시면 GitHub 저장소에 이슈를 등록해주세요.

## 🔗 링크

- [GitHub 저장소](https://github.com/Teletobimy/ppt_ai_translation)
- [Streamlit Cloud 배포](https://share.streamlit.io/)

## 📈 향후 계획

- [ ] 더 정확한 슬라이드 이미지 변환
- [ ] 배치 번역 기능
- [ ] 번역 히스토리 관리
- [ ] 사용자 정의 프롬프트
- [ ] 다국어 UI 지원
