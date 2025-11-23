# API 참조 문서

## 📚 목차

1. [백엔드 API](#백엔드-api)
2. [LangGraph 노드](#langgraph-노드)
3. [상태 정의](#상태-정의)
4. [스키마 및 모델](#스키마-및-모델)
5. [유틸리티 함수](#유틸리티-함수)
6. [설정](#설정)
7. [프롬프트](#프롬프트)

---

## 백엔드 API

### FastAPI 애플리케이션

**위치:** `backend/src/agent/app.py`

#### 주요 엔드포인트

##### 프론트엔드 서빙

```python
app.mount("/app", create_frontend_router(), name="frontend")
```

**설명:**
- 프로덕션 환경에서 React 빌드 파일을 서빙합니다
- `/app` 경로에서 프론트엔드에 접근할 수 있습니다

**URL:** `http://localhost:8123/app` (프로덕션)

#### `create_frontend_router(build_dir="../frontend/dist")`

**매개변수:**
- `build_dir` (str): React 빌드 디렉토리 경로

**반환값:**
- `StaticFiles`: 정적 파일 서빙 라우터
- `Route`: 빌드가 준비되지 않은 경우 더미 라우터

**사용 예시:**
```python
from agent.app import create_frontend_router

router = create_frontend_router("./custom/build/path")
```

---

## LangGraph 노드

### 그래프 구조

**위치:** `backend/src/agent/graph.py`

```
START
  ↓
generate_query (검색 쿼리 생성)
  ↓
[병렬] web_research (웹 리서치 × N개)
  ↓
reflection (반성 및 분석)
  ↓
[조건부] web_research (추가 리서치) 또는 finalize_answer (최종 답변)
  ↓
END
```

### 노드 함수

#### `generate_query(state, config)`

**파일:** `backend/src/agent/graph.py:44`

**설명:**
사용자의 질문을 분석하여 최적의 검색 쿼리를 생성합니다.

**매개변수:**
- `state` (OverallState): 현재 그래프 상태
  - `messages`: 사용자 메시지
  - `initial_search_query_count`: 생성할 쿼리 개수
- `config` (RunnableConfig): 실행 설정

**반환값:**
```python
{
    "search_query": ["쿼리1", "쿼리2", "쿼리3"]
}
```

**사용 모델:**
- `gemini-2.0-flash` (기본값)
- Temperature: 1.0

**예시:**
```python
# 입력 상태
state = {
    "messages": [HumanMessage(content="2024년 AI 트렌드는?")],
    "initial_search_query_count": 3
}

# 출력
{
    "search_query": [
        "AI 기술 트렌드 2024",
        "인공지능 최신 동향",
        "머신러닝 발전 2024년"
    ]
}
```

---

#### `web_research(state, config)`

**파일:** `backend/src/agent/graph.py:95`

**설명:**
Google Search API를 사용하여 웹에서 정보를 검색합니다.

**매개변수:**
- `state` (WebSearchState): 검색 상태
  - `search_query` (str): 검색 쿼리
  - `id` (int): 쿼리 고유 ID
- `config` (RunnableConfig): 실행 설정

**반환값:**
```python
{
    "sources_gathered": [
        {
            "label": "출처 제목",
            "short_url": "https://vertexaisearch.cloud.google.com/id/1-0",
            "value": "https://원본-url.com"
        }
    ],
    "search_query": ["실행된 쿼리"],
    "web_research_result": ["검색 결과 요약 [출처](URL)"]
}
```

**사용 API:**
- Google Search API (Gemini Native Tool)

**처리 과정:**
1. 검색 쿼리 실행
2. URL 단축 (토큰 절약)
3. 인용 추출
4. 결과에 인용 마커 삽입

---

#### `reflection(state, config)`

**파일:** `backend/src/agent/graph.py:139`

**설명:**
수집된 정보를 분석하고 지식 격차를 파악합니다.

**매개변수:**
- `state` (OverallState): 전체 상태
  - `messages`: 원본 질문
  - `web_research_result`: 웹 검색 결과
  - `research_loop_count`: 현재 루프 횟수
- `config` (RunnableConfig): 실행 설정

**반환값:**
```python
{
    "is_sufficient": False,  # 정보 충분성
    "knowledge_gap": "부족한 정보에 대한 설명",
    "follow_up_queries": ["추가 검색 쿼리1", "추가 검색 쿼리2"],
    "research_loop_count": 1,
    "number_of_ran_queries": 3
}
```

**사용 모델:**
- `gemini-2.5-flash` (기본값)
- Temperature: 1.0

**동작:**
1. 현재까지의 결과 분석
2. 지식 격차 파악
3. 정보 충분성 평가
4. 필요시 추가 쿼리 생성

---

#### `evaluate_research(state, config)`

**파일:** `backend/src/agent/graph.py:183`

**설명:**
다음 단계를 결정하는 라우팅 함수입니다.

**매개변수:**
- `state` (ReflectionState): 반성 결과 상태
- `config` (RunnableConfig): 실행 설정

**반환값:**
- `"finalize_answer"`: 최종 답변 생성으로 이동
- `[Send(...)]`: 추가 웹 리서치 노드 생성

**조건:**
```python
if state["is_sufficient"] or state["research_loop_count"] >= max_research_loops:
    return "finalize_answer"
else:
    # 추가 리서치 수행
    return [Send("web_research", {...}), ...]
```

---

#### `finalize_answer(state, config)`

**파일:** `backend/src/agent/graph.py:220`

**설명:**
모든 정보를 종합하여 최종 답변을 생성합니다.

**매개변수:**
- `state` (OverallState): 전체 상태
  - `messages`: 원본 질문
  - `web_research_result`: 모든 검색 결과
  - `sources_gathered`: 수집된 출처
- `config` (RunnableConfig): 실행 설정

**반환값:**
```python
{
    "messages": [AIMessage(content="최종 답변 [출처](URL)")],
    "sources_gathered": [
        {
            "label": "실제 사용된 출처",
            "short_url": "단축 URL",
            "value": "원본 URL"
        }
    ]
}
```

**사용 모델:**
- `gemini-2.5-pro` (기본값)
- Temperature: 0 (일관성을 위해)

**처리:**
1. 모든 리서치 결과 종합
2. 고품질 답변 생성
3. 인용 URL 변환 (단축 → 원본)
4. 실제 사용된 출처만 필터링

---

## 상태 정의

**위치:** `backend/src/agent/state.py`

### `OverallState`

전체 그래프의 상태를 나타냅니다.

```python
class OverallState(TypedDict):
    messages: Annotated[list, add_messages]
    search_query: Annotated[list, operator.add]
    web_research_result: Annotated[list, operator.add]
    sources_gathered: Annotated[list, operator.add]
    initial_search_query_count: int
    max_research_loops: int
    research_loop_count: int
    reasoning_model: str
```

**필드:**

| 필드 | 타입 | 설명 |
|------|------|------|
| `messages` | `list` | 대화 메시지 (자동 병합) |
| `search_query` | `list` | 생성된 모든 검색 쿼리 (누적) |
| `web_research_result` | `list` | 웹 검색 결과 (누적) |
| `sources_gathered` | `list` | 수집된 출처 (누적) |
| `initial_search_query_count` | `int` | 초기 쿼리 개수 |
| `max_research_loops` | `int` | 최대 리서치 루프 |
| `research_loop_count` | `int` | 현재 루프 횟수 |
| `reasoning_model` | `str` | 사용할 모델 이름 |

**예시:**
```python
state = {
    "messages": [
        HumanMessage(content="양자 컴퓨팅이란?"),
        AIMessage(content="양자 컴퓨팅은...")
    ],
    "search_query": ["양자 컴퓨팅 기초", "큐비트 설명"],
    "web_research_result": ["검색 결과1", "검색 결과2"],
    "sources_gathered": [{"label": "...", ...}],
    "initial_search_query_count": 3,
    "max_research_loops": 2,
    "research_loop_count": 1,
    "reasoning_model": "gemini-2.5-pro"
}
```

---

### `ReflectionState`

반성 단계의 상태입니다.

```python
class ReflectionState(TypedDict):
    is_sufficient: bool
    knowledge_gap: str
    follow_up_queries: Annotated[list, operator.add]
    research_loop_count: int
    number_of_ran_queries: int
```

**필드:**

| 필드 | 타입 | 설명 |
|------|------|------|
| `is_sufficient` | `bool` | 정보가 충분한지 여부 |
| `knowledge_gap` | `str` | 부족한 정보 설명 |
| `follow_up_queries` | `list` | 추가 검색 쿼리 |
| `research_loop_count` | `int` | 현재 루프 횟수 |
| `number_of_ran_queries` | `int` | 실행된 쿼리 개수 |

---

### `WebSearchState`

개별 웹 검색의 상태입니다.

```python
class WebSearchState(TypedDict):
    search_query: str
    id: str
```

**필드:**

| 필드 | 타입 | 설명 |
|------|------|------|
| `search_query` | `str` | 검색 쿼리 텍스트 |
| `id` | `str` | 쿼리 고유 ID |

---

### `QueryGenerationState`

쿼리 생성 단계의 상태입니다.

```python
class QueryGenerationState(TypedDict):
    search_query: list[Query]
```

---

## 스키마 및 모델

**위치:** `backend/src/agent/tools_and_schemas.py`

### `SearchQueryList`

검색 쿼리 목록을 나타내는 Pydantic 모델입니다.

```python
class SearchQueryList(BaseModel):
    query: List[str]  # 검색 쿼리 목록
    rationale: str    # 쿼리 선택 근거
```

**사용:**
```python
from agent.tools_and_schemas import SearchQueryList

result = SearchQueryList(
    query=["AI 트렌드 2024", "머신러닝 발전"],
    rationale="최신 AI 기술 동향을 파악하기 위한 쿼리입니다."
)
```

---

### `Reflection`

반성 결과를 나타내는 Pydantic 모델입니다.

```python
class Reflection(BaseModel):
    is_sufficient: bool        # 정보 충분성
    knowledge_gap: str         # 지식 격차 설명
    follow_up_queries: List[str]  # 추가 쿼리
```

**사용:**
```python
from agent.tools_and_schemas import Reflection

reflection = Reflection(
    is_sufficient=False,
    knowledge_gap="양자 컴퓨팅의 실제 응용 사례가 부족합니다.",
    follow_up_queries=["양자 컴퓨팅 실제 활용 사례 2024"]
)
```

---

## 유틸리티 함수

**위치:** `backend/src/agent/utils.py`

### `get_research_topic(messages)`

**파일:** `backend/src/agent/utils.py:5`

**설명:**
메시지 리스트에서 리서치 주제를 추출합니다.

**매개변수:**
- `messages` (List[AnyMessage]): 대화 메시지 목록

**반환값:**
- `str`: 리서치 주제 문자열

**동작:**
- 단일 메시지: 해당 메시지 내용 반환
- 다중 메시지: 대화 히스토리 형식으로 결합

**예시:**
```python
from langchain_core.messages import HumanMessage, AIMessage
from agent.utils import get_research_topic

# 단일 메시지
messages = [HumanMessage(content="AI란 무엇인가요?")]
topic = get_research_topic(messages)
# 결과: "AI란 무엇인가요?"

# 다중 메시지
messages = [
    HumanMessage(content="AI란?"),
    AIMessage(content="인공지능입니다."),
    HumanMessage(content="더 자세히 설명해주세요")
]
topic = get_research_topic(messages)
# 결과:
# "User: AI란?
# Assistant: 인공지능입니다.
# User: 더 자세히 설명해주세요"
```

---

### `resolve_urls(urls_to_resolve, id)`

**파일:** `backend/src/agent/utils.py:22`

**설명:**
긴 Vertex AI Search URL을 짧은 형식으로 변환합니다.

**매개변수:**
- `urls_to_resolve` (List[Any]): 변환할 URL 객체 리스트
- `id` (int): 고유 식별자

**반환값:**
- `Dict[str, str]`: 원본 URL → 단축 URL 매핑

**목적:**
- 토큰 사용량 절약
- 처리 시간 단축

**예시:**
```python
from agent.utils import resolve_urls

# 입력: Google Search API 결과
urls = [
    {"web": {"uri": "https://example.com/very/long/url/path"}},
    {"web": {"uri": "https://another.com/another/long/path"}}
]

resolved = resolve_urls(urls, id=1)
# 결과:
# {
#     "https://example.com/very/long/url/path":
#         "https://vertexaisearch.cloud.google.com/id/1-0",
#     "https://another.com/another/long/path":
#         "https://vertexaisearch.cloud.google.com/id/1-1"
# }
```

---

### `insert_citation_markers(text, citations_list)`

**파일:** `backend/src/agent/utils.py:39`

**설명:**
텍스트에 인용 마커를 삽입합니다.

**매개변수:**
- `text` (str): 원본 텍스트
- `citations_list` (list): 인용 정보 목록

**반환값:**
- `str`: 인용 마커가 삽입된 텍스트

**인용 정보 구조:**
```python
{
    "start_index": 0,
    "end_index": 50,
    "segments": [
        {
            "label": "출처 제목",
            "short_url": "https://..."
        }
    ]
}
```

**예시:**
```python
from agent.utils import insert_citation_markers

text = "양자 컴퓨팅은 큐비트를 사용합니다."
citations = [
    {
        "start_index": 0,
        "end_index": 19,
        "segments": [
            {
                "label": "Wikipedia",
                "short_url": "https://vertexaisearch.cloud.google.com/id/1-0"
            }
        ]
    }
]

result = insert_citation_markers(text, citations)
# 결과: "양자 컴퓨팅은 큐비트를 사용합니다 [Wikipedia](https://vertexaisearch.cloud.google.com/id/1-0)."
```

---

### `get_citations(response, resolved_urls_map)`

**파일:** `backend/src/agent/utils.py:78`

**설명:**
Gemini 응답에서 인용 정보를 추출합니다.

**매개변수:**
- `response`: Gemini API 응답 객체
- `resolved_urls_map` (Dict): URL 매핑

**반환값:**
- `list`: 인용 정보 목록

**추출 정보:**
- 인용 위치 (start_index, end_index)
- 인용 출처 정보
- 단축 URL

---

## 설정

**위치:** `backend/src/agent/configuration.py`

### `Configuration`

에이전트 설정을 관리하는 Pydantic 모델입니다.

```python
class Configuration(BaseModel):
    query_generator_model: str = "gemini-2.0-flash"
    reflection_model: str = "gemini-2.5-flash"
    answer_model: str = "gemini-2.5-pro"
    number_of_initial_queries: int = 3
    max_research_loops: int = 2
```

**필드:**

| 필드 | 기본값 | 설명 |
|------|--------|------|
| `query_generator_model` | `gemini-2.0-flash` | 쿼리 생성 모델 |
| `reflection_model` | `gemini-2.5-flash` | 반성 모델 |
| `answer_model` | `gemini-2.5-pro` | 답변 생성 모델 |
| `number_of_initial_queries` | `3` | 초기 쿼리 개수 |
| `max_research_loops` | `2` | 최대 리서치 루프 |

**사용:**
```python
from agent.configuration import Configuration

# 기본 설정
config = Configuration()

# 커스텀 설정
config = Configuration(
    number_of_initial_queries=5,
    max_research_loops=3,
    answer_model="gemini-2.5-flash"
)
```

**환경 변수로 오버라이드:**
```bash
export QUERY_GENERATOR_MODEL="gemini-2.0-flash"
export NUMBER_OF_INITIAL_QUERIES=5
```

---

## 프롬프트

**위치:** `backend/src/agent/prompts.py`

### 프롬프트 템플릿

#### `query_writer_instructions`

**용도:** 검색 쿼리 생성

**주요 지침:**
- 단일 쿼리 선호
- 다양성 확보
- 최신 정보 중시

**변수:**
- `{number_queries}`: 생성할 쿼리 개수
- `{current_date}`: 현재 날짜
- `{research_topic}`: 리서치 주제

---

#### `web_searcher_instructions`

**용도:** 웹 검색 수행

**주요 지침:**
- 다양한 검색 수행
- 출처 추적
- 검색 결과만 사용 (창작 금지)

**변수:**
- `{current_date}`: 현재 날짜
- `{research_topic}`: 검색 주제

---

#### `reflection_instructions`

**용도:** 정보 분석 및 격차 파악

**주요 지침:**
- 지식 격차 식별
- 충분성 평가
- 자체 포함적 쿼리 생성

**변수:**
- `{current_date}`: 현재 날짜
- `{research_topic}`: 리서치 주제
- `{summaries}`: 현재까지의 요약

**출력 형식:**
```json
{
    "is_sufficient": true/false,
    "knowledge_gap": "설명",
    "follow_up_queries": ["쿼리"]
}
```

---

#### `answer_instructions`

**용도:** 최종 답변 생성

**주요 지침:**
- 고품질 답변 작성
- 출처 포함 필수 (마크다운 링크)
- 최신 정보 반영

**변수:**
- `{current_date}`: 현재 날짜
- `{research_topic}`: 사용자 질문
- `{summaries}`: 모든 리서치 요약

---

## CLI 사용법

**위치:** `backend/examples/cli_research.py`

### 명령줄에서 에이전트 실행

```bash
cd backend
python examples/cli_research.py "질문 내용"
```

**옵션:**

| 옵션 | 짧은 형식 | 기본값 | 설명 |
|------|-----------|--------|------|
| `--initial-queries` | - | 3 | 초기 쿼리 개수 |
| `--max-loops` | - | 2 | 최대 루프 횟수 |
| `--reasoning-model` | - | `gemini-2.5-pro-preview-05-06` | 추론 모델 |

**예시:**
```bash
# 기본 사용
python examples/cli_research.py "2024년 AI 트렌드는?"

# 커스텀 설정
python examples/cli_research.py \
  "양자 컴퓨팅이란?" \
  --initial-queries 5 \
  --max-loops 3 \
  --reasoning-model gemini-2.5-pro
```

**코드 구조:**
```python
def main():
    # 인자 파싱
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args()

    # 상태 구성
    state = {
        "messages": [HumanMessage(content=args.question)],
        "initial_search_query_count": args.initial_queries,
        "max_research_loops": args.max_loops,
        "reasoning_model": args.reasoning_model,
    }

    # 그래프 실행
    result = graph.invoke(state)
    print(result["messages"][-1].content)
```

---

## 프론트엔드 API

### useStream 훅

**위치:** `frontend/src/App.tsx`

```typescript
const thread = useStream<{
  messages: Message[];
  initial_search_query_count: number;
  max_research_loops: number;
  reasoning_model: string;
}>({
  apiUrl: "http://localhost:2024",  // 백엔드 URL
  assistantId: "agent",              // 에이전트 ID
  messagesKey: "messages",           // 메시지 키
  onUpdateEvent: (event) => {...},   // 이벤트 핸들러
  onError: (error) => {...}          // 에러 핸들러
})
```

**메서드:**
- `thread.submit(state)`: 메시지 전송
- `thread.stop()`: 실행 중지
- `thread.messages`: 메시지 목록
- `thread.isLoading`: 로딩 상태

---

## 다음 단계

- **[아키텍처](./ARCHITECTURE.md)**: 시스템 구조 깊이 이해
- **[예제 및 튜토리얼](./EXAMPLES.md)**: 실제 코드 커스터마이징
- **[초보자 가이드](./BEGINNER_GUIDE.md)**: 기본 사용법 복습

---

## 참고 자료

### 외부 문서
- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [Google Gemini API](https://ai.google.dev/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [React 공식 문서](https://react.dev/)

### 코드 위치 빠른 참조

| 기능 | 파일 |
|------|------|
| 에이전트 그래프 | `backend/src/agent/graph.py` |
| 상태 정의 | `backend/src/agent/state.py` |
| 설정 | `backend/src/agent/configuration.py` |
| 프롬프트 | `backend/src/agent/prompts.py` |
| 유틸리티 | `backend/src/agent/utils.py` |
| FastAPI 앱 | `backend/src/agent/app.py` |
| 프론트엔드 | `frontend/src/App.tsx` |
