# 설치 가이드

## 📚 목차

1. [시스템 요구사항](#시스템-요구사항)
2. [사전 준비](#사전-준비)
3. [개발 환경 설치](#개발-환경-설치)
4. [프로덕션 배포](#프로덕션-배포)
5. [환경 변수 설정](#환경-변수-설정)
6. [문제 해결](#문제-해결)

---

## 시스템 요구사항

### 최소 요구사항

| 항목 | 요구사항 |
|------|----------|
| **운영 체제** | Windows 10+, macOS 10.15+, Ubuntu 20.04+ |
| **메모리** | 4GB RAM |
| **디스크 공간** | 2GB 여유 공간 |
| **인터넷** | 안정적인 인터넷 연결 |

### 권장 사양

| 항목 | 권장사항 |
|------|----------|
| **메모리** | 8GB RAM 이상 |
| **디스크 공간** | 5GB 여유 공간 |
| **프로세서** | 멀티코어 프로세서 |

### 필수 소프트웨어

| 소프트웨어 | 버전 | 용도 |
|-----------|------|------|
| **Node.js** | 18.0.0+ | 프론트엔드 실행 |
| **npm** | 9.0.0+ | JavaScript 패키지 관리 |
| **Python** | 3.11+ | 백엔드 실행 |
| **pip** | 최신 버전 | Python 패키지 관리 |

### 선택 사항

| 소프트웨어 | 용도 |
|-----------|------|
| **Git** | 소스 코드 관리 |
| **Docker** | 컨테이너 기반 배포 |
| **Docker Compose** | 다중 컨테이너 관리 |

---

## 사전 준비

### 1. Google Gemini API 키 발급

#### 1.1 Google AI Studio 접속
1. 브라우저에서 https://aistudio.google.com/apikey 접속
2. Google 계정으로 로그인

#### 1.2 API 키 생성
1. "Create API Key" 버튼 클릭
2. 프로젝트 선택 또는 새 프로젝트 생성
3. 생성된 API 키 복사

#### 1.3 API 키 안전하게 보관
```
예시: AIzaSyABC123def456GHI789jkl012MNO345pqr
```

**⚠️ 주의사항:**
- API 키를 절대 공개 저장소에 올리지 마세요
- `.env` 파일은 `.gitignore`에 포함되어 있습니다
- API 키는 개인 메모장에 안전하게 보관하세요

#### 1.4 사용량 및 요금 확인
- 무료 할당량: https://ai.google.dev/pricing
- 월별 사용량 모니터링: https://console.cloud.google.com/

### 2. LangSmith API 키 발급 (선택사항)

LangSmith는 LangGraph 애플리케이션을 모니터링하고 디버깅하는 도구입니다.

#### 2.1 LangSmith 가입
1. https://smith.langchain.com/ 접속
2. 계정 생성 또는 로그인

#### 2.2 API 키 발급
1. Settings > API Keys 메뉴 이동
2. "Create API Key" 클릭
3. API 키 복사 및 저장

**언제 필요한가요?**
- 프로덕션 배포 시 필수
- 개발 중 에이전트 동작 추적 시 유용
- Docker Compose 사용 시 필요

---

## 개발 환경 설치

### 방법 1: 자동 설치 (권장)

#### 전체 과정 한 번에
```bash
# 1. 저장소 클론
git clone https://github.com/your-username/gemini-fullstack-langgraph-quickstart.git
cd gemini-fullstack-langgraph-quickstart

# 2. API 키 설정
cd backend
cp .env.example .env
# .env 파일을 편집하여 GEMINI_API_KEY 설정
cd ..

# 3. 의존성 설치 (백엔드)
cd backend
pip install .
cd ..

# 4. 의존성 설치 (프론트엔드)
cd frontend
npm install
cd ..

# 5. 개발 서버 실행
make dev
```

### 방법 2: 단계별 수동 설치

#### 2.1 저장소 다운로드

**Git 사용:**
```bash
git clone https://github.com/your-username/gemini-fullstack-langgraph-quickstart.git
cd gemini-fullstack-langgraph-quickstart
```

**ZIP 다운로드:**
1. GitHub 페이지에서 "Code" > "Download ZIP"
2. 압축 해제 후 터미널에서 해당 폴더로 이동

#### 2.2 환경 변수 설정

```bash
cd backend
```

**Windows:**
```cmd
copy .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env
# 또는
code .env  # VS Code 사용 시
```

**`.env` 파일 내용:**
```env
# Google Gemini API 키 (필수)
GEMINI_API_KEY="여기에_발급받은_API_키_입력"

# LangSmith 설정 (선택사항)
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY="여기에_LangSmith_API_키_입력"
# LANGCHAIN_PROJECT="gemini-research-agent"
```

저장 후 프로젝트 루트로 돌아가기:
```bash
cd ..
```

#### 2.3 백엔드 설치

```bash
cd backend
```

**의존성 설치:**
```bash
pip install .
```

**설치 확인:**
```bash
python -c "import langchain, langgraph; print('설치 성공!')"
```

**LangGraph CLI 설치:**
```bash
pip install langgraph-cli
langgraph --version
```

프로젝트 루트로 돌아가기:
```bash
cd ..
```

#### 2.4 프론트엔드 설치

```bash
cd frontend
```

**의존성 설치:**
```bash
npm install
```

**설치 확인:**
```bash
npm list react react-dom
```

프로젝트 루트로 돌아가기:
```bash
cd ..
```

#### 2.5 개발 서버 실행

**방법 A: Makefile 사용 (권장)**
```bash
make dev
```

**방법 B: 개별 실행**

터미널 1 (백엔드):
```bash
cd backend
langgraph dev
```

출력 예시:
```
- API: http://127.0.0.1:2024
- LangGraph Studio: http://127.0.0.1:2024/studio
Ready!
```

터미널 2 (프론트엔드):
```bash
cd frontend
npm run dev
```

출력 예시:
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

#### 2.6 접속 확인

브라우저에서 다음 URL 접속:

| 서비스 | URL | 설명 |
|--------|-----|------|
| **프론트엔드** | http://localhost:5173/app | 메인 애플리케이션 |
| **백엔드 API** | http://localhost:2024 | API 서버 |
| **LangGraph Studio** | http://localhost:2024/studio | 에이전트 시각화 도구 |

---

## 프로덕션 배포

### Docker를 사용한 배포

#### 사전 요구사항
- Docker 설치: https://docs.docker.com/get-docker/
- Docker Compose 설치: https://docs.docker.com/compose/install/

#### 1. 환경 변수 준비

프로젝트 루트에 `.env` 파일 생성:
```bash
touch .env
```

`.env` 파일 내용:
```env
# 필수
GEMINI_API_KEY=여기에_Gemini_API_키_입력

# 프로덕션에서 필수
LANGSMITH_API_KEY=여기에_LangSmith_API_키_입력
```

#### 2. Docker 이미지 빌드

```bash
docker build -t gemini-fullstack-langgraph -f Dockerfile .
```

빌드 시간: 약 5-10분

#### 3. Docker Compose로 실행

```bash
docker-compose up -d
```

서비스 시작 확인:
```bash
docker-compose ps
```

출력 예시:
```
NAME                COMMAND             STATUS
postgres            "docker-entrypoint…"   Up
redis               "docker-entrypoint…"   Up
gemini-backend      "langgraph serve"      Up
```

#### 4. 접속

브라우저에서 http://localhost:8123/app 접속

#### 5. 로그 확인

```bash
# 전체 로그
docker-compose logs -f

# 특정 서비스 로그
docker-compose logs -f gemini-backend
```

#### 6. 서비스 중지

```bash
# 중지
docker-compose stop

# 중지 및 컨테이너 삭제
docker-compose down

# 중지 및 볼륨도 삭제 (데이터베이스 초기화)
docker-compose down -v
```

### docker-compose.yml 구조

```yaml
services:
  postgres:     # 데이터베이스 (상태 저장)
  redis:        # 메시지 브로커 (스트리밍)
  backend:      # LangGraph 서버 + React 앱
```

### 포트 매핑

| 서비스 | 내부 포트 | 외부 포트 | 용도 |
|--------|----------|----------|------|
| Backend | 8000 | 8123 | API + Frontend |
| PostgreSQL | 5432 | 5433 | 데이터베이스 |
| Redis | 6379 | 6380 | 캐시/브로커 |

---

## 환경 변수 설정

### 백엔드 환경 변수

`backend/.env` 파일:

```env
# === 필수 설정 ===

# Google Gemini API 키
GEMINI_API_KEY="your-api-key-here"

# === 선택 설정 ===

# LangSmith 추적 (개발/디버깅용)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY="your-langsmith-api-key"
LANGCHAIN_PROJECT="my-research-agent"

# === 고급 설정 ===

# 모델 설정 (기본값 오버라이드)
QUERY_GENERATOR_MODEL="gemini-2.0-flash"
REFLECTION_MODEL="gemini-2.5-flash"
ANSWER_MODEL="gemini-2.5-pro"

# 검색 설정
NUMBER_OF_INITIAL_QUERIES=3
MAX_RESEARCH_LOOPS=2
```

### 프론트엔드 환경 변수

`frontend/.env.local` (필요시 생성):

```env
# 개발 환경 API URL (기본값: http://localhost:2024)
VITE_API_URL=http://localhost:2024

# 프로덕션 환경 API URL
# VITE_API_URL=http://localhost:8123
```

**참고:** 프론트엔드는 `App.tsx`에서 자동으로 환경 감지:
```typescript
apiUrl: import.meta.env.DEV
  ? "http://localhost:2024"      // 개발
  : "http://localhost:8123"       // 프로덕션
```

---

## 문제 해결

### 일반적인 문제

#### 1. "GEMINI_API_KEY is not set" 에러

**원인:** API 키가 설정되지 않음

**해결:**
```bash
cd backend
ls -la .env  # .env 파일 존재 확인

# 파일이 없으면
cp .env.example .env

# 파일 편집
nano .env
# 또는
code .env
```

`.env` 파일에 API 키 추가:
```env
GEMINI_API_KEY="실제_API_키_입력"
```

#### 2. 포트가 이미 사용 중

**에러 메시지:**
```
Error: listen EADDRINUSE: address already in use :::2024
```

**해결:**

**Windows:**
```cmd
# 포트 사용 프로세스 확인
netstat -ano | findstr :2024

# 프로세스 종료 (PID는 위 명령어 결과에서 확인)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# 포트 사용 프로세스 확인 및 종료
lsof -ti:2024 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

**또는 다른 포트 사용:**
```bash
# 백엔드
langgraph dev --port 3000

# 프론트엔드
npm run dev -- --port 3001
```

#### 3. Python 모듈을 찾을 수 없음

**에러 메시지:**
```
ModuleNotFoundError: No module named 'langchain'
```

**해결:**
```bash
cd backend

# 가상 환경 생성 (권장)
python -m venv venv

# 가상 환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 의존성 재설치
pip install --upgrade pip
pip install .
```

#### 4. npm 의존성 설치 실패

**에러 메시지:**
```
npm ERR! code ERESOLVE
```

**해결:**
```bash
cd frontend

# node_modules 삭제
rm -rf node_modules package-lock.json

# 캐시 정리
npm cache clean --force

# 재설치
npm install
```

#### 5. Docker 빌드 실패

**에러 메시지:**
```
ERROR [stage-x] failed to compute cache key
```

**해결:**
```bash
# Docker 캐시 삭제
docker system prune -a

# 빌드 재시도
docker build --no-cache -t gemini-fullstack-langgraph -f Dockerfile .
```

#### 6. "Failed to fetch" 프론트엔드 에러

**원인:** 백엔드가 실행되지 않음

**해결:**
1. 백엔드 실행 확인:
   ```bash
   curl http://localhost:2024
   ```

2. 백엔드가 응답하지 않으면 재시작:
   ```bash
   cd backend
   langgraph dev
   ```

3. 방화벽 설정 확인

### 성능 문제

#### 느린 응답 속도

**원인 및 해결:**

1. **인터넷 연결 확인**
   ```bash
   ping google.com
   ```

2. **Effort Level 조정**
   - High → Medium 또는 Low로 변경

3. **모델 변경**
   - `backend/.env`:
   ```env
   ANSWER_MODEL="gemini-2.0-flash"  # 더 빠른 모델
   ```

4. **검색 횟수 제한**
   - `backend/.env`:
   ```env
   NUMBER_OF_INITIAL_QUERIES=1
   MAX_RESEARCH_LOOPS=1
   ```

#### 메모리 부족

**증상:** 애플리케이션이 느려지거나 멈춤

**해결:**
```bash
# Node.js 메모리 제한 증가
NODE_OPTIONS="--max-old-space-size=4096" npm run dev
```

### 플랫폼별 문제

#### Windows 특정 문제

**PowerShell 실행 정책 에러:**
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**경로에 공백이 있을 때:**
```cmd
cd "C:\Users\My Name\Documents\project"
```

#### macOS 특정 문제

**Command Line Tools 설치:**
```bash
xcode-select --install
```

**Python 경로 문제:**
```bash
# python3 사용
python3 -m pip install .
```

#### Linux 특정 문제

**권한 에러:**
```bash
# npm 전역 패키지 권한 문제
sudo chown -R $USER:$USER ~/.npm
sudo chown -R $USER:$USER ~/.config
```

**Python 개발 패키지 설치:**
```bash
sudo apt-get install python3-dev python3-pip
```

---

## 설치 확인 체크리스트

설치가 완료되었는지 확인하세요:

- [ ] Node.js 설치 완료 (`node --version`)
- [ ] Python 설치 완료 (`python --version` 또는 `python3 --version`)
- [ ] Gemini API 키 발급 완료
- [ ] 저장소 클론 또는 다운로드 완료
- [ ] 백엔드 `.env` 파일 설정 완료
- [ ] 백엔드 의존성 설치 완료 (`pip install .`)
- [ ] 프론트엔드 의존성 설치 완료 (`npm install`)
- [ ] 백엔드 서버 실행 확인 (http://localhost:2024)
- [ ] 프론트엔드 실행 확인 (http://localhost:5173/app)
- [ ] 질문 입력 후 답변 수신 확인

---

## 다음 단계

설치가 완료되었다면:

1. **[초보자 가이드](./BEGINNER_GUIDE.md)** - 첫 질문 시도해보기
2. **[예제 및 튜토리얼](./EXAMPLES.md)** - 다양한 활용법 배우기
3. **[아키텍처](./ARCHITECTURE.md)** - 시스템 구조 이해하기

---

## 추가 리소스

### 공식 문서
- LangGraph: https://langchain-ai.github.io/langgraph/
- Google Gemini: https://ai.google.dev/
- React: https://react.dev/
- Vite: https://vitejs.dev/

### 도움말
- GitHub Issues: 버그 리포트 및 기능 요청
- GitHub Discussions: 커뮤니티 질문 및 답변
- Discord: 실시간 채팅 및 지원

---

**설치 완료!** 🎉

문제가 있으시면 [문제 해결](#문제-해결) 섹션을 참조하거나 GitHub Issues에 질문을 남겨주세요.
