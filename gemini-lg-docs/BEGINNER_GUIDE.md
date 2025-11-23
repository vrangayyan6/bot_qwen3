# 초보자를 위한 완벽 가이드

## 📚 목차

1. [시작하기 전에](#시작하기-전에)
2. [기본 개념 이해하기](#기본-개념-이해하기)
3. [단계별 실행 가이드](#단계별-실행-가이드)
4. [첫 질문 해보기](#첫-질문-해보기)
5. [자주 묻는 질문](#자주-묻는-질문)
6. [문제 해결](#문제-해결)
7. [다음 단계](#다음-단계)

---

## 시작하기 전에

### 이 프로젝트는 무엇인가요?

이 프로젝트는 **AI 리서치 어시스턴트**입니다. 사용자가 질문을 하면:

1. AI가 검색어를 자동으로 생성합니다
2. 웹에서 관련 정보를 찾아옵니다
3. 정보가 부족하면 추가로 검색합니다
4. 모든 정보를 종합하여 출처와 함께 답변합니다

### 무엇을 배울 수 있나요?

- 최신 AI 기술 (LangGraph, Gemini) 사용법
- 풀스택 웹 애플리케이션 구조
- React 프론트엔드와 Python 백엔드 연동
- AI 에이전트 개발 기초

### 필요한 사전 지식

#### 필수
- 터미널(명령 프롬프트) 기본 사용법
- 텍스트 에디터 사용법

#### 권장 (없어도 괜찮아요!)
- Python 기초 지식
- JavaScript/React 기초 지식
- API 개념

---

## 기본 개념 이해하기

### 주요 용어 설명

#### 1. 프론트엔드 (Frontend)
- **설명**: 사용자가 직접 보고 상호작용하는 웹 페이지
- **이 프로젝트에서**: React로 만든 채팅 인터페이스
- **비유**: 식당의 홀 (손님이 있는 공간)

#### 2. 백엔드 (Backend)
- **설명**: 서버에서 실행되는 프로그램, 실제 작업 처리
- **이 프로젝트에서**: Python으로 만든 AI 리서치 에이전트
- **비유**: 식당의 주방 (요리가 만들어지는 곳)

#### 3. LangGraph
- **설명**: AI 에이전트를 만들기 위한 프레임워크
- **이 프로젝트에서**: 리서치 과정을 단계별로 관리
- **비유**: 요리 레시피 (단계별 작업 흐름)

#### 4. Gemini
- **설명**: Google이 만든 AI 언어 모델
- **이 프로젝트에서**: 검색어 생성, 정보 분석, 답변 작성
- **비유**: 똑똑한 요리사

#### 5. API 키 (API Key)
- **설명**: 서비스를 사용하기 위한 비밀번호 같은 것
- **이 프로젝트에서**: Gemini AI를 사용하기 위한 인증 키
- **비유**: 회원 카드 번호

### 프로젝트 구조 간단 설명

```
프로젝트 폴더/
│
├── frontend/           ← 웹 페이지 (React)
│   ├── src/           ← 소스 코드
│   └── package.json   ← 필요한 라이브러리 목록
│
├── backend/           ← 서버 프로그램 (Python)
│   ├── src/agent/    ← AI 에이전트 코드
│   └── pyproject.toml ← 필요한 라이브러리 목록
│
└── gemini-lg-docs/    ← 이 문서들!
```

---

## 단계별 실행 가이드

### 1단계: 필수 프로그램 설치

#### Windows 사용자

**1. Node.js 설치**
1. https://nodejs.org 방문
2. "LTS" 버전 다운로드 (추천)
3. 다운로드한 파일 실행하여 설치
4. 설치 확인:
   ```cmd
   node --version
   npm --version
   ```
   버전 번호가 나오면 성공!

**2. Python 설치**
1. https://www.python.org/downloads/ 방문
2. Python 3.11 이상 다운로드
3. 설치 시 **"Add Python to PATH" 체크** (중요!)
4. 설치 확인:
   ```cmd
   python --version
   ```

**3. Git 설치** (선택사항)
1. https://git-scm.com/download/win 방문
2. 다운로드 및 설치
3. 설치 확인:
   ```cmd
   git --version
   ```

#### macOS 사용자

**1. Homebrew 설치** (패키지 관리자)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Node.js 설치**
```bash
brew install node
node --version
npm --version
```

**3. Python 설치**
```bash
brew install python@3.11
python3 --version
```

#### Linux (Ubuntu/Debian) 사용자

```bash
# Node.js 설치
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python 설치
sudo apt-get update
sudo apt-get install python3.11 python3-pip

# 설치 확인
node --version
npm --version
python3 --version
```

### 2단계: Gemini API 키 발급

**왜 필요한가요?**
- AI 기능을 사용하려면 Google Gemini API에 접근해야 합니다
- API 키는 무료로 발급받을 수 있습니다

**발급 방법:**

1. **Google AI Studio 접속**
   - https://aistudio.google.com/apikey 방문

2. **Google 계정으로 로그인**

3. **"Create API Key" 버튼 클릭**

4. **API 키 복사**
   - 생성된 키를 안전한 곳에 복사해두세요
   - 예시: `AIzaSyABC123...` (이런 형태)

5. **주의사항**
   - API 키는 절대 공개하지 마세요
   - GitHub에 올리지 마세요
   - 다른 사람과 공유하지 마세요

### 3단계: 프로젝트 다운로드

**방법 1: Git 사용 (권장)**
```bash
git clone https://github.com/your-username/gemini-fullstack-langgraph-quickstart.git
cd gemini-fullstack-langgraph-quickstart
```

**방법 2: ZIP 파일 다운로드**
1. GitHub 페이지에서 "Code" > "Download ZIP" 클릭
2. 압축 해제
3. 터미널에서 해당 폴더로 이동:
   ```bash
   cd 다운로드받은폴더경로
   ```

### 4단계: API 키 설정

**1. 백엔드 폴더로 이동**
```bash
cd backend
```

**2. 환경 변수 파일 생성**

Windows (명령 프롬프트):
```cmd
copy .env.example .env
```

macOS/Linux:
```bash
cp .env.example .env
```

**3. .env 파일 편집**

텍스트 에디터로 `.env` 파일을 열고:
```
GEMINI_API_KEY="여기에_발급받은_API_키_붙여넣기"
```

예시:
```
GEMINI_API_KEY="AIzaSyABC123def456GHI789jkl012MNO345pqr"
```

**4. 저장 후 폴더 이동**
```bash
cd ..  # 프로젝트 루트로 돌아가기
```

### 5단계: 의존성 설치

**백엔드 의존성 설치**
```bash
cd backend
pip install .
cd ..
```

시간이 좀 걸릴 수 있습니다 (1-3분). 에러가 나지 않으면 성공입니다!

**프론트엔드 의존성 설치**
```bash
cd frontend
npm install
cd ..
```

역시 시간이 좀 걸립니다 (2-5분).

### 6단계: 프로젝트 실행

**방법 1: 한 번에 실행 (권장)**

프로젝트 루트 폴더에서:
```bash
make dev
```

**방법 2: 개별 실행**

터미널 2개를 열어서:

터미널 1 (백엔드):
```bash
cd backend
langgraph dev
```

터미널 2 (프론트엔드):
```bash
cd frontend
npm run dev
```

**실행 확인**
- 백엔드: http://localhost:2024
- 프론트엔드: http://localhost:5173/app
- 브라우저가 자동으로 열립니다

---

## 첫 질문 해보기

### 기본 사용법

1. **브라우저에서 http://localhost:5173/app 열기**

2. **화면 설명**
   - 상단: 제목과 설명
   - 중앙: 질문 입력창
   - 하단: Effort Level 선택 (Low/Medium/High)

3. **Effort Level이란?**
   - **Low**: 빠른 검색 (1회 검색, 1개 쿼리)
   - **Medium**: 균형잡힌 검색 (3회 반복, 3개 쿼리) - 권장
   - **High**: 깊이 있는 검색 (10회 반복, 5개 쿼리)

4. **질문 입력 예시**
   ```
   2024년 한국에서 가장 인기있는 K-POP 그룹은?
   ```
   또는
   ```
   최신 AI 기술 트렌드를 알려주세요
   ```

5. **진행 상황 관찰**
   - "Generating Search Queries": 검색어 생성 중
   - "Web Research": 웹에서 정보 수집 중
   - "Reflection": 정보 분석 중
   - "Finalizing Answer": 최종 답변 작성 중

6. **답변 확인**
   - 출처가 링크로 표시됩니다
   - 클릭하면 원본 페이지로 이동

### 추천 질문 예시

**쉬운 질문 (Low Effort)**
```
오늘 날씨는?
ChatGPT는 언제 출시되었나요?
```

**중간 난이도 (Medium Effort)**
```
2024년 AI 기술의 주요 발전은 무엇인가요?
최근 전기차 시장 동향을 알려주세요
```

**복잡한 질문 (High Effort)**
```
양자 컴퓨팅과 기존 컴퓨팅의 차이점을 상세히 설명해주세요
2024년 글로벌 경제 전망과 주요 변수를 분석해주세요
```

---

## 자주 묻는 질문

### Q1: API 키 에러가 나요
**A:**
1. `.env` 파일이 `backend/` 폴더에 있는지 확인
2. API 키가 따옴표 안에 정확히 들어갔는지 확인
3. API 키가 유효한지 Google AI Studio에서 확인

### Q2: 포트가 이미 사용 중이라고 나와요
**A:**
```bash
# 다른 프로그램이 포트를 사용 중입니다
# Windows: 작업 관리자에서 해당 프로세스 종료
# Mac/Linux:
lsof -ti:2024 | xargs kill  # 백엔드 포트
lsof -ti:5173 | xargs kill  # 프론트엔드 포트
```

### Q3: 느려요 / 답변이 안 나와요
**A:**
1. 인터넷 연결 확인
2. Effort Level을 Low로 낮춰보기
3. 질문을 더 구체적으로 바꿔보기
4. 터미널에서 에러 메시지 확인

### Q4: 한국어 답변이 이상해요
**A:**
- Gemini는 영어가 더 자연스럽습니다
- 질문을 영어로 해보세요
- 또는 "한국어로 답변해주세요"를 질문에 추가

### Q5: 비용이 드나요?
**A:**
- Gemini API 무료 할당량 내에서는 무료
- 월 사용량 제한 확인: https://ai.google.dev/pricing
- 일반적인 개인 사용은 무료 범위 내

---

## 문제 해결

### Python 관련 에러

**"python not found"**
```bash
# Python 설치 확인
python --version
python3 --version

# PATH 설정 확인 (설치 재시도)
```

**"pip not found"**
```bash
# pip 설치
python -m ensurepip --upgrade
```

**모듈을 찾을 수 없다는 에러**
```bash
cd backend
pip install . --force-reinstall
```

### Node.js 관련 에러

**"npm not found"**
```bash
# Node.js 재설치 필요
# https://nodejs.org 에서 다운로드
```

**의존성 설치 에러**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 백엔드 실행 에러

**"langgraph: command not found"**
```bash
pip install langgraph-cli
```

**"GEMINI_API_KEY is not set"**
```bash
# backend/.env 파일 확인
# API 키가 올바르게 설정되었는지 확인
```

### 프론트엔드 에러

**"Failed to fetch"**
- 백엔드가 실행 중인지 확인
- http://localhost:2024 접속 시도
- 방화벽 설정 확인

**빈 화면**
- 브라우저 콘솔 확인 (F12)
- 캐시 삭제 후 새로고침 (Ctrl+Shift+R)

---

## 다음 단계

### 기본 사용을 마스터했다면

1. **코드 커스터마이징**
   - [예제 및 튜토리얼](./EXAMPLES.md) 문서 참조
   - 프롬프트 수정해보기
   - UI 색상 변경해보기

2. **깊이 있게 이해하기**
   - [아키텍처](./ARCHITECTURE.md) 문서 읽기
   - [API 참조](./API_REFERENCE.md) 살펴보기

3. **배포하기**
   - Docker로 배포
   - 클라우드 서비스에 올리기
   - 친구들과 공유하기

### 학습 리소스

**LangGraph 배우기**
- 공식 문서: https://langchain-ai.github.io/langgraph/
- 튜토리얼: https://langchain-ai.github.io/langgraph/tutorials/

**React 배우기**
- 공식 문서: https://react.dev/
- 무료 강의: https://react.dev/learn

**Python 배우기**
- 점프 투 파이썬: https://wikidocs.net/book/1
- 공식 튜토리얼: https://docs.python.org/ko/3/tutorial/

### 커뮤니티

- GitHub Issues: 버그 리포트 및 질문
- GitHub Discussions: 아이디어 공유
- Discord: 실시간 채팅 (링크 확인 필요)

---

## 도움이 더 필요하세요?

**문서 순서대로 읽기:**
1. ✅ 초보자 가이드 (지금 읽는 문서)
2. 📖 [설치 가이드](./INSTALLATION.md) - 더 상세한 설치 방법
3. 🏗️ [아키텍처](./ARCHITECTURE.md) - 시스템 구조 이해
4. 💻 [API 참조](./API_REFERENCE.md) - 코드 레퍼런스
5. 🎯 [예제 및 튜토리얼](./EXAMPLES.md) - 실습 예제

**문제가 계속되나요?**
- GitHub Issues에 질문 남기기
- 에러 메시지 전체를 복사해서 공유
- 운영 체제, Python/Node 버전 명시

---

**축하합니다! 🎉**

여러분은 이제 최신 AI 기술을 활용한 풀스택 애플리케이션을 실행할 수 있게 되었습니다.
계속해서 탐구하고 실험해보세요!

**다음**: [예제 및 튜토리얼](./EXAMPLES.md)에서 더 많은 활용법을 배워보세요!
