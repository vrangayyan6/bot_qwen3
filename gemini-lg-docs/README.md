# Gemini Fullstack LangGraph Quickstart - 한국어 문서

## 📚 목차

1. [프로젝트 소개](#프로젝트-소개)
2. [주요 기능](#주요-기능)
3. [프로젝트 구조](#프로젝트-구조)
4. [시작하기](#시작하기)
5. [문서 목록](#문서-목록)

## 프로젝트 소개

Gemini Fullstack LangGraph Quickstart는 React 프론트엔드와 LangGraph 기반 백엔드 에이전트를 사용한 풀스택 애플리케이션입니다.

이 프로젝트는 Google의 Gemini 모델과 LangGraph를 활용하여 다음과 같은 작업을 수행하는 **지능형 리서치 에이전트**를 구현합니다:

- 🔍 **자동 검색 쿼리 생성**: 사용자의 질문을 분석하여 최적의 검색어를 자동으로 생성합니다
- 🌐 **웹 리서치**: Google Search API를 활용하여 실시간으로 웹에서 정보를 수집합니다
- 🤔 **반성적 사고**: 수집된 정보를 분석하고 부족한 부분을 파악하여 추가 검색을 수행합니다
- 📄 **인용 포함 답변**: 수집한 정보를 바탕으로 출처가 명시된 고품질 답변을 생성합니다

<img src="../app.png" title="Gemini Fullstack LangGraph" alt="Gemini Fullstack LangGraph" width="90%">

## 주요 기능

### 💬 풀스택 아키텍처
- **프론트엔드**: React + Vite + TypeScript + Tailwind CSS
- **백엔드**: LangGraph + FastAPI + Google Gemini

### 🧠 지능형 리서치 에이전트
- Google Gemini 2.0 Flash를 사용한 동적 검색 쿼리 생성
- Google Search API를 통한 실시간 웹 검색
- 반복적인 리서치 루프로 정보 품질 향상
- 출처가 명확한 최종 답변 제공

### 🔄 개발 환경
- 프론트엔드 및 백엔드 핫 리로딩 지원
- Docker를 활용한 간편한 배포
- LangGraph Studio를 통한 에이전트 시각화

## 프로젝트 구조

```
gemini-fullstack-langgraph-quickstart/
├── frontend/               # React 프론트엔드 애플리케이션
│   ├── src/
│   │   ├── App.tsx        # 메인 애플리케이션 컴포넌트
│   │   ├── components/    # React 컴포넌트들
│   │   └── lib/           # 유틸리티 함수들
│   ├── package.json
│   └── vite.config.ts
│
├── backend/               # LangGraph 백엔드 애플리케이션
│   ├── src/
│   │   └── agent/
│   │       ├── graph.py           # LangGraph 에이전트 정의
│   │       ├── app.py             # FastAPI 애플리케이션
│   │       ├── configuration.py   # 설정 관리
│   │       ├── prompts.py         # AI 프롬프트 템플릿
│   │       ├── state.py           # 상태 정의
│   │       └── tools_and_schemas.py  # 도구 및 스키마
│   ├── examples/
│   │   └── cli_research.py        # CLI 예제
│   ├── pyproject.toml
│   └── langgraph.json
│
├── gemini-lg-docs/        # 한국어 문서 (이 디렉토리)
│   ├── README.md          # 메인 문서 (현재 파일)
│   ├── INSTALLATION.md    # 설치 가이드
│   ├── BEGINNER_GUIDE.md  # 초보자 가이드
│   ├── API_REFERENCE.md   # API 참조
│   ├── EXAMPLES.md        # 예제 및 튜토리얼
│   └── ARCHITECTURE.md    # 아키텍처 설명
│
├── Dockerfile             # Docker 이미지 빌드 설정
├── docker-compose.yml     # Docker Compose 설정
└── Makefile              # 개발 편의 스크립트
```

## 시작하기

### 빠른 시작

1. **필수 요구사항 확인**
   - Node.js 18 이상
   - Python 3.11 이상
   - Google Gemini API 키

2. **저장소 클론**
   ```bash
   git clone https://github.com/your-repo/gemini-fullstack-langgraph-quickstart.git
   cd gemini-fullstack-langgraph-quickstart
   ```

3. **API 키 설정**
   ```bash
   cd backend
   cp .env.example .env
   # .env 파일을 열고 GEMINI_API_KEY를 설정하세요
   ```

4. **의존성 설치 및 실행**
   ```bash
   # 프로젝트 루트에서
   make dev
   ```

5. **브라우저에서 확인**
   - 프론트엔드: http://localhost:5173/app
   - 백엔드 API: http://localhost:2024
   - LangGraph Studio: 자동으로 열립니다

더 자세한 내용은 [설치 가이드](./INSTALLATION.md)를 참조하세요.

## 문서 목록

### 📖 기본 문서
- **[설치 가이드](./INSTALLATION.md)**: 상세한 설치 및 설정 방법
- **[초보자 가이드](./BEGINNER_GUIDE.md)**: 프로젝트를 처음 접하는 분들을 위한 단계별 가이드
- **[아키텍처](./ARCHITECTURE.md)**: 시스템 구조와 동작 원리 상세 설명

### 🔧 기술 문서
- **[API 참조](./API_REFERENCE.md)**: 백엔드 API 및 함수 레퍼런스
- **[예제 및 튜토리얼](./EXAMPLES.md)**: 실용적인 예제 코드와 사용법

### 🎯 각 문서별 용도

| 문서 | 대상 | 내용 |
|------|------|------|
| 설치 가이드 | 모든 사용자 | 환경 설정, 의존성 설치, 실행 방법 |
| 초보자 가이드 | 초보자 | 개념 설명, 첫 프로젝트 실행, 기본 커스터마이징 |
| 아키텍처 | 개발자 | 시스템 구조, 컴포넌트 설명, 데이터 흐름 |
| API 참조 | 개발자 | 함수, 클래스, 엔드포인트 상세 설명 |
| 예제 및 튜토리얼 | 모든 사용자 | 실습 예제, 커스터마이징 방법, 고급 활용법 |

## 기술 스택

### 프론트엔드
- [React](https://reactjs.org/) - UI 프레임워크
- [Vite](https://vitejs.dev/) - 빌드 도구
- [TypeScript](https://www.typescriptlang.org/) - 타입 안전성
- [Tailwind CSS](https://tailwindcss.com/) - 스타일링
- [Shadcn UI](https://ui.shadcn.com/) - UI 컴포넌트
- [LangGraph SDK](https://github.com/langchain-ai/langgraph) - 백엔드 연동

### 백엔드
- [LangGraph](https://github.com/langchain-ai/langgraph) - AI 에이전트 프레임워크
- [FastAPI](https://fastapi.tiangolo.com/) - 웹 프레임워크
- [Google Gemini](https://ai.google.dev/models/gemini) - LLM 모델
- [Python 3.11+](https://www.python.org/) - 프로그래밍 언어

### 인프라
- [Docker](https://www.docker.com/) - 컨테이너화
- [Redis](https://redis.io/) - 스트리밍 및 캐싱
- [PostgreSQL](https://www.postgresql.org/) - 데이터베이스

## 에이전트 작동 방식

<img src="../agent.png" title="Agent Flow" alt="Agent Flow" width="60%">

1. **초기 쿼리 생성**: 사용자 질문을 분석하여 최적의 검색 쿼리 생성
2. **웹 리서치**: Google Search API로 각 쿼리에 대한 정보 수집
3. **반성 및 분석**: 수집된 정보의 충분성 평가 및 지식 격차 파악
4. **반복 개선**: 필요시 추가 쿼리 생성 및 재검색 (최대 루프 횟수까지)
5. **최종 답변**: 모든 정보를 종합하여 출처가 포함된 답변 생성

## 라이선스

이 프로젝트는 Apache License 2.0 라이선스를 따릅니다. 자세한 내용은 [LICENSE](../LICENSE) 파일을 참조하세요.

## 도움이 필요하신가요?

- 🐛 버그 리포트: [GitHub Issues](https://github.com/your-repo/gemini-fullstack-langgraph-quickstart/issues)
- 💬 질문 및 토론: [GitHub Discussions](https://github.com/your-repo/gemini-fullstack-langgraph-quickstart/discussions)
- 📧 이메일: your-email@example.com

## 기여하기

프로젝트에 기여하고 싶으시다면 다음 단계를 따라주세요:

1. 이 저장소를 포크합니다
2. 새로운 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

---

**다음 단계**: [초보자 가이드](./BEGINNER_GUIDE.md)를 읽고 프로젝트를 실행해보세요!
