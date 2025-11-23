# 아키텍처 문서

## 📚 목차

1. [시스템 개요](#시스템-개요)
2. [전체 아키텍처](#전체-아키텍처)
3. [백엔드 아키텍처](#백엔드-아키텍처)
4. [프론트엔드 아키텍처](#프론트엔드-아키텍처)
5. [데이터 흐름](#데이터-흐름)
6. [주요 컴포넌트](#주요-컴포넌트)
7. [배포 아키텍처](#배포-아키텍처)
8. [확장성 고려사항](#확장성-고려사항)

---

## 시스템 개요

### 목적

Gemini Fullstack LangGraph Quickstart는 **자율적인 AI 리서치 에이전트**를 구현한 풀스택 애플리케이션입니다.

### 핵심 기능

1. **자동 검색 쿼리 생성**: 사용자 질문 분석 → 최적 검색어 생성
2. **반복적 웹 리서치**: 정보 수집 → 분석 → 부족한 부분 재검색
3. **인용 포함 답변**: 모든 정보에 출처 명시
4. **실시간 스트리밍**: 검색 과정 실시간 시각화

### 기술 스택 요약

| 레이어 | 기술 | 역할 |
|--------|------|------|
| **프론트엔드** | React + Vite + TypeScript | UI/UX |
| **백엔드** | LangGraph + FastAPI + Python | AI 에이전트 |
| **AI 모델** | Google Gemini | LLM |
| **검색 API** | Google Search (Grounding) | 웹 검색 |
| **배포** | Docker + Redis + PostgreSQL | 프로덕션 |

---

## 전체 아키텍처

### 고수준 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│                         사용자                              │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/WebSocket
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   프론트엔드 (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ WelcomeScreen│  │ChatMessages  │  │ActivityTimeline│     │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│         useStream Hook (LangGraph SDK)                      │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/SSE
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  백엔드 (FastAPI + LangGraph)               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              LangGraph 에이전트                      │    │
│  │  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐│    │
│  │  │generate│──▶│  web   │──▶│reflect-│──▶│finalize││    │
│  │  │ query  │   │research│   │  ion   │   │ answer ││    │
│  │  └────────┘   └────────┘   └────────┘   └────────┘│    │
│  └─────────────────────────────────────────────────────┘    │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│Google Gemini │ │Google Search │ │  PostgreSQL  │
│     API      │ │     API      │ │   (상태저장)  │
└──────────────┘ └──────────────┘ └──────────────┘
```

### 통신 프로토콜

#### 개발 환경
```
프론트엔드 (5173) ←→ 백엔드 (2024)
        HTTP/Server-Sent Events (SSE)
```

#### 프로덕션 환경
```
클라이언트 ←→ Nginx (8123) ←→ 백엔드 (8000)
                               ↓
                        PostgreSQL (5432)
                        Redis (6379)
```

---

## 백엔드 아키텍처

### LangGraph 에이전트 구조

```
START
  │
  ▼
┌─────────────────────┐
│  generate_query     │  ← Gemini 2.0 Flash
│  (검색어 생성)       │     사용자 질문 분석
└──────────┬──────────┘     3~5개 쿼리 생성
           │
           ▼
    ┌─────────────┐
    │ Send (병렬) │
    └──┬──┬──┬───┘
       │  │  │
       ▼  ▼  ▼
┌─────────────────────┐ ×N
│   web_research      │  ← Google Search API
│   (웹 검색)         │     각 쿼리별 검색
└──────────┬──────────┘     인용 추출
           │
           ▼
┌─────────────────────┐
│    reflection       │  ← Gemini 2.5 Flash
│    (반성/분석)      │     정보 충분성 평가
└──────────┬──────────┘     지식 격차 파악
           │
           ▼
    ┌──────────────┐
    │  조건 분기    │
    └──┬────────┬──┘
       │        │
  부족  │        │ 충분
       │        │
       ▼        ▼
   (재검색)  ┌─────────────────────┐
             │  finalize_answer    │  ← Gemini 2.5 Pro
             │  (최종 답변)        │     종합 답변 생성
             └──────────┬──────────┘     인용 변환
                        │
                        ▼
                       END
```

### 상태 관리

#### OverallState (전체 상태)
```python
{
    "messages": [HumanMessage(...), AIMessage(...)],  # 대화 히스토리
    "search_query": ["쿼리1", "쿼리2", ...],          # 생성된 쿼리들
    "web_research_result": ["결과1", "결과2", ...],   # 검색 결과들
    "sources_gathered": [{...}, {...}, ...],          # 수집된 출처들
    "initial_search_query_count": 3,                  # 초기 쿼리 개수
    "max_research_loops": 2,                          # 최대 반복 횟수
    "research_loop_count": 1,                         # 현재 반복 횟수
    "reasoning_model": "gemini-2.5-pro"               # 사용 모델
}
```

**상태 업데이트 규칙:**
- `messages`: 자동 병합 (`add_messages` 리듀서)
- `search_query`, `web_research_result`, `sources_gathered`: 누적 (`operator.add`)
- 나머지: 덮어쓰기

### 노드 상세

#### 1. generate_query

**입력:**
```python
{
    "messages": [HumanMessage(content="AI란 무엇인가요?")],
    "initial_search_query_count": 3
}
```

**처리:**
1. 사용자 메시지에서 리서치 주제 추출
2. 프롬프트 템플릿에 주제 삽입
3. Gemini 2.0 Flash에 요청 (structured output)
4. 검색 쿼리 목록 생성

**출력:**
```python
{
    "search_query": [
        "인공지능 정의",
        "AI 역사와 발전",
        "AI 활용 분야"
    ]
}
```

**사용 모델:**
- `gemini-2.0-flash`: 빠른 쿼리 생성
- Temperature: 1.0 (다양성 확보)

---

#### 2. web_research (병렬 실행)

**병렬 처리 방식:**
```python
# Send를 통해 각 쿼리마다 별도 인스턴스 생성
[
    Send("web_research", {"search_query": "쿼리1", "id": 0}),
    Send("web_research", {"search_query": "쿼리2", "id": 1}),
    Send("web_research", {"search_query": "쿼리3", "id": 2})
]
```

**각 인스턴스 처리:**
1. Google Search API 호출 (Gemini Grounding)
2. 검색 결과 수신 (웹 페이지 내용 + 메타데이터)
3. URL 단축 (토큰 절약)
4. 인용 정보 추출
5. 텍스트에 인용 마커 삽입

**URL 단축 예시:**
```python
# 원본 (147자)
"https://www.example.com/articles/2024/artificial-intelligence-comprehensive-guide?utm_source=google&utm_medium=organic&page=1"

# 단축 (49자)
"https://vertexaisearch.cloud.google.com/id/0-1"
```

**출력 (각 인스턴스):**
```python
{
    "sources_gathered": [
        {
            "label": "Wikipedia",
            "short_url": "https://vertexaisearch.cloud.google.com/id/0-1",
            "value": "https://en.wikipedia.org/wiki/Artificial_intelligence"
        }
    ],
    "search_query": ["인공지능 정의"],
    "web_research_result": [
        "인공지능(AI)은 기계가 인간의 지능을 모방하는 기술입니다 [Wikipedia](https://vertexaisearch.cloud.google.com/id/0-1)."
    ]
}
```

---

#### 3. reflection

**입력:**
```python
{
    "messages": [HumanMessage(...)],
    "web_research_result": ["결과1", "결과2", "결과3"],
    "research_loop_count": 0
}
```

**처리:**
1. 모든 웹 검색 결과 취합
2. 프롬프트 구성 (주제 + 현재까지의 요약)
3. Gemini 2.5 Flash로 분석
4. 구조화된 출력 파싱 (JSON)

**출력:**
```python
{
    "is_sufficient": False,
    "knowledge_gap": "AI의 실제 응용 사례와 한계점이 부족합니다.",
    "follow_up_queries": [
        "인공지능 실제 활용 사례 2024",
        "AI 기술의 한계와 과제"
    ],
    "research_loop_count": 1
}
```

**판단 기준:**
- 정보 완성도
- 질문과의 관련성
- 세부 사항 충족도

---

#### 4. evaluate_research (라우팅)

**조건 평가:**
```python
if is_sufficient or research_loop_count >= max_research_loops:
    return "finalize_answer"
else:
    # 추가 검색 수행
    return [
        Send("web_research", {"search_query": query, "id": ...})
        for query in follow_up_queries
    ]
```

**루프 제한:**
- 무한 루프 방지
- 비용 관리
- 시간 제한

---

#### 5. finalize_answer

**입력:**
```python
{
    "messages": [HumanMessage(...)],
    "web_research_result": ["결과1", "결과2", ..., "결과N"],
    "sources_gathered": [{...}, {...}, ...]
}
```

**처리:**
1. 모든 검색 결과 종합
2. 답변 생성 프롬프트 구성
3. Gemini 2.5 Pro로 고품질 답변 생성
4. 단축 URL → 원본 URL 변환
5. 실제 사용된 출처만 필터링

**출력:**
```python
{
    "messages": [
        HumanMessage(...),
        AIMessage(content="AI는... [Wikipedia](https://en.wikipedia.org/...)")
    ],
    "sources_gathered": [
        {
            "label": "Wikipedia",
            "short_url": "...",
            "value": "https://en.wikipedia.org/wiki/..."
        }
    ]
}
```

---

### 에러 처리

```python
# graph.py에서의 에러 처리
try:
    result = llm.invoke(prompt)
except Exception as e:
    # LangGraph는 자동으로 재시도
    # max_retries=2 설정됨
    logger.error(f"Error: {e}")
    raise
```

**재시도 전략:**
- Gemini API: 최대 2회 재시도
- 지수 백오프 사용

---

## 프론트엔드 아키텍처

### 컴포넌트 구조

```
App.tsx (루트)
  │
  ├─ useStream Hook
  │   └─ LangGraph SDK
  │
  ├─ WelcomeScreen (초기 화면)
  │   ├─ Textarea (질문 입력)
  │   ├─ RadioGroup (Effort Level)
  │   └─ Select (Model 선택)
  │
  └─ ChatMessagesView (대화 화면)
      ├─ ScrollArea (메시지 목록)
      │   ├─ HumanMessage (사용자)
      │   └─ AIMessage (AI, 마크다운)
      │
      ├─ ActivityTimeline (실시간 진행상황)
      │   ├─ Generating Queries
      │   ├─ Web Research
      │   ├─ Reflection
      │   └─ Finalizing Answer
      │
      └─ InputSection (추가 질문)
```

### 상태 관리

#### useStream 훅

```typescript
const thread = useStream({
  apiUrl: "http://localhost:2024",
  assistantId: "agent",
  messagesKey: "messages",
  onUpdateEvent: (event) => {
    // 실시간 이벤트 처리
    if (event.generate_query) {
      // 쿼리 생성 이벤트
    } else if (event.web_research) {
      // 웹 검색 이벤트
    }
  }
})
```

**관리하는 상태:**
- `messages`: 대화 메시지 목록
- `isLoading`: 로딩 상태
- `error`: 에러 상태

#### 로컬 상태

```typescript
// 활동 타임라인 (실시간)
const [processedEventsTimeline, setProcessedEventsTimeline] =
  useState<ProcessedEvent[]>([]);

// 활동 히스토리 (메시지별)
const [historicalActivities, setHistoricalActivities] =
  useState<Record<string, ProcessedEvent[]>>({});
```

### 데이터 흐름 (프론트엔드)

```
사용자 입력
  │
  ▼
handleSubmit()
  │
  ├─ Effort 변환 (low/medium/high → 숫자)
  ├─ Model 선택
  └─ 메시지 구성
  │
  ▼
thread.submit({
  messages: [...],
  initial_search_query_count: N,
  max_research_loops: M,
  reasoning_model: "..."
})
  │
  ▼
백엔드로 HTTP 요청
  │
  ▼
Server-Sent Events (SSE) 수신
  │
  ├─ onUpdateEvent 트리거
  │   └─ Timeline 업데이트
  │
  └─ 메시지 업데이트
      └─ UI 리렌더링
```

### UI/UX 특징

#### 1. 반응형 디자인
```css
/* Tailwind CSS 활용 */
<div className="max-w-4xl mx-auto">  /* 최대 너비 제한 */
<div className="h-screen">           /* 전체 높이 */
```

#### 2. 자동 스크롤
```typescript
useEffect(() => {
  if (scrollAreaRef.current) {
    const viewport = scrollAreaRef.current.querySelector(
      "[data-radix-scroll-area-viewport]"
    );
    if (viewport) {
      viewport.scrollTop = viewport.scrollHeight;  // 맨 아래로
    }
  }
}, [thread.messages]);
```

#### 3. 마크다운 렌더링
```typescript
import ReactMarkdown from 'react-markdown'

<ReactMarkdown>
  {message.content}  // AI 답변을 마크다운으로 렌더링
</ReactMarkdown>
```

---

## 데이터 흐름

### 전체 데이터 흐름

#### 1. 질문 제출

```
브라우저
  │ POST /threads/{thread_id}/runs
  │ Body: {
  │   input: {
  │     messages: [...],
  │     initial_search_query_count: 3,
  │     max_research_loops: 2
  │   }
  │ }
  ▼
LangGraph Server
  │ 스레드 생성/조회
  │ 그래프 실행 시작
  ▼
```

#### 2. 실시간 업데이트

```
LangGraph Server
  │ SSE Stream 생성
  │
  ├─ event: generate_query
  │   data: {"generate_query": {"search_query": [...]}}
  │
  ├─ event: web_research (병렬)
  │   data: {"web_research": {"sources_gathered": [...]}}
  │
  ├─ event: reflection
  │   data: {"reflection": {"is_sufficient": false, ...}}
  │
  └─ event: finalize_answer
      data: {"finalize_answer": {"messages": [...]}}
  ▼
브라우저
  │ onUpdateEvent() 호출
  │ UI 업데이트
  ▼
```

#### 3. 최종 결과

```
LangGraph Server
  │ 그래프 실행 완료
  │ 상태 저장 (PostgreSQL)
  │
  │ event: messages/complete
  │ data: {
  │   messages: [Human, AI],
  │   sources_gathered: [...],
  │   ...
  │ }
  ▼
브라우저
  │ 최종 메시지 표시
  │ 로딩 상태 해제
  ▼
```

### 데이터 변환

#### 1. Effort Level 변환

```typescript
// 프론트엔드
const effortMapping = {
  "low": { queries: 1, loops: 1 },
  "medium": { queries: 3, loops: 3 },
  "high": { queries: 5, loops: 10 }
}
```

#### 2. URL 변환

```python
# 백엔드: 웹 검색 시
원본: "https://example.com/very/long/url/..."
  ↓ resolve_urls()
단축: "https://vertexaisearch.cloud.google.com/id/0-1"
  ↓ insert_citation_markers()
텍스트: "내용 [출처](https://vertexaisearch.cloud.google.com/id/0-1)"
  ↓ finalize_answer()
최종: "내용 [출처](https://example.com/very/long/url/...)"
```

---

## 주요 컴포넌트

### 백엔드 컴포넌트

#### 1. FastAPI 애플리케이션
**파일:** `backend/src/agent/app.py`

**역할:**
- 정적 파일 서빙 (프로덕션)
- LangGraph와의 통합

**라우트:**
- `/app/*`: 프론트엔드 (프로덕션)
- `/threads/*`: LangGraph API (자동 생성)

#### 2. LangGraph 그래프
**파일:** `backend/src/agent/graph.py`

**역할:**
- 에이전트 플로우 정의
- 노드 간 연결 관리
- 상태 전파

#### 3. Configuration
**파일:** `backend/src/agent/configuration.py`

**역할:**
- 설정 중앙 관리
- 환경 변수 통합
- 기본값 제공

### 프론트엔드 컴포넌트

#### 1. App.tsx
**역할:**
- 루트 컴포넌트
- 전역 상태 관리
- 라우팅 (Welcome ↔ Chat)

#### 2. WelcomeScreen
**역할:**
- 첫 질문 입력
- Effort Level 선택
- Model 선택

#### 3. ChatMessagesView
**역할:**
- 대화 표시
- 타임라인 표시
- 추가 질문 입력

---

## 배포 아키텍처

### 개발 환경

```
localhost:5173 (Vite Dev Server)
  │ HTTP
  ▼
localhost:2024 (LangGraph Dev Server)
  │
  ├─ Gemini API
  ├─ Google Search API
  └─ 메모리 내 상태 저장
```

### 프로덕션 환경 (Docker Compose)

```
┌─────────────────────────────────────────┐
│          Docker Network                 │
│                                         │
│  ┌────────────────┐                    │
│  │    Nginx       │ :8123              │
│  │  (리버스 프록시)│                    │
│  └────────┬───────┘                    │
│           │                             │
│           ▼                             │
│  ┌────────────────┐                    │
│  │  LangGraph     │ :8000              │
│  │   Backend      │                    │
│  │ (FastAPI +     │                    │
│  │  React Build)  │                    │
│  └────┬──┬────────┘                    │
│       │  │                             │
│       │  └──────┐                      │
│       │         │                      │
│       ▼         ▼                      │
│  ┌──────┐  ┌──────────┐               │
│  │Redis │  │PostgreSQL│               │
│  │:6379 │  │  :5432   │               │
│  └──────┘  └──────────┘               │
└─────────────────────────────────────────┘
         │         │
         ▼         ▼
    Gemini API  Google Search
```

#### 컨테이너 역할

| 컨테이너 | 이미지 | 역할 |
|----------|--------|------|
| **backend** | Custom | FastAPI + LangGraph + React 빌드 |
| **postgres** | postgres:16 | 상태 및 히스토리 저장 |
| **redis** | redis:7 | 스트리밍 브로커 |

#### 볼륨

```yaml
volumes:
  postgres-data:  # 데이터베이스 영구 저장
    driver: local
```

#### 네트워크

```yaml
networks:
  default:
    driver: bridge  # 컨테이너 간 통신
```

### Dockerfile 구조

```dockerfile
# 1단계: 프론트엔드 빌드
FROM node:20 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# 2단계: 백엔드 준비
FROM python:3.11-slim
WORKDIR /app/backend
COPY backend/ ./
RUN pip install .

# 3단계: 프론트엔드 빌드 복사
COPY --from=frontend-builder /app/frontend/dist ../frontend/dist

# 실행
CMD ["langgraph", "serve", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 확장성 고려사항

### 수평 확장 (Horizontal Scaling)

#### 백엔드 스케일 아웃
```yaml
# docker-compose.yml
services:
  backend:
    image: gemini-fullstack-langgraph
    deploy:
      replicas: 3  # 3개 인스턴스
```

**요구사항:**
- PostgreSQL: 공유 상태 저장소
- Redis: 스트리밍 브로커
- Load Balancer: 요청 분산

### 수직 확장 (Vertical Scaling)

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

### 캐싱 전략

#### 1. 검색 결과 캐싱
```python
import redis

cache = redis.Redis(host='localhost', port=6379)

def web_research_cached(query):
    # 캐시 확인
    cached = cache.get(f"search:{query}")
    if cached:
        return json.loads(cached)

    # 검색 수행
    result = web_research(query)

    # 캐시 저장 (1시간)
    cache.setex(f"search:{query}", 3600, json.dumps(result))
    return result
```

#### 2. LLM 응답 캐싱
```python
from langchain.cache import RedisCache
import langchain

langchain.llm_cache = RedisCache(
    redis_url="redis://localhost:6379"
)
```

### 비동기 처리

```python
# 비동기 그래프 실행
async def process_question(question):
    state = {
        "messages": [HumanMessage(content=question)],
        "initial_search_query_count": 3,
    }

    result = await graph.ainvoke(state)
    return result
```

### 모니터링

#### LangSmith 통합
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-key
LANGCHAIN_PROJECT=production
```

**모니터링 항목:**
- 요청 수
- 응답 시간
- 토큰 사용량
- 에러율

#### 커스텀 메트릭
```python
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests')
response_time = Histogram('response_time_seconds', 'Response time')

@response_time.time()
def process_request():
    request_count.inc()
    # 처리 로직
```

---

## 보안 고려사항

### API 키 관리

**절대 금지:**
```python
# ❌ 하드코딩
api_key = "AIzaSyABC123..."

# ❌ Git에 커밋
# .env 파일을 .gitignore에 추가하지 않음
```

**권장 방법:**
```python
# ✅ 환경 변수 사용
api_key = os.getenv("GEMINI_API_KEY")

# ✅ 시크릿 관리 시스템 (프로덕션)
from google.cloud import secretmanager
api_key = get_secret("gemini-api-key")
```

### CORS 설정

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 프로덕션
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 입력 검증

```python
from pydantic import BaseModel, Field

class QuestionInput(BaseModel):
    question: str = Field(..., max_length=1000)
    initial_search_query_count: int = Field(default=3, ge=1, le=10)
```

---

## 성능 최적화

### 1. 병렬 처리
- 웹 검색: 모든 쿼리 동시 실행
- Send 활용: LangGraph 네이티브 병렬 처리

### 2. 토큰 절약
- URL 단축: 긴 URL을 짧은 형식으로
- 프롬프트 최적화: 불필요한 정보 제거

### 3. 스트리밍
- SSE로 실시간 업데이트
- 사용자 경험 향상

---

## 다음 단계

아키텍처를 이해했다면:

1. **[API 참조](./API_REFERENCE.md)** - 구체적인 함수 및 클래스 학습
2. **[예제 및 튜토리얼](./EXAMPLES.md)** - 실제 커스터마이징 시도
3. **[초보자 가이드](./BEGINNER_GUIDE.md)** - 기본 사용법 복습

---

## 참고 자료

- [LangGraph 개념](https://langchain-ai.github.io/langgraph/concepts/)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [React 아키텍처](https://react.dev/learn/thinking-in-react)
- [Gemini API 가이드](https://ai.google.dev/docs)

---

**이제 시스템의 내부 동작을 완전히 이해하셨습니다!**

질문이나 개선 제안이 있다면 GitHub Issues에 남겨주세요.
