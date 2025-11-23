# 예제 및 튜토리얼

## 📚 목차

1. [기본 사용 예제](#기본-사용-예제)
2. [CLI로 질문하기](#cli로-질문하기)
3. [설정 커스터마이징](#설정-커스터마이징)
4. [프롬프트 수정하기](#프롬프트-수정하기)
5. [UI 커스터마이징](#ui-커스터마이징)
6. [새로운 노드 추가하기](#새로운-노드-추가하기)
7. [고급 활용법](#고급-활용법)

---

## 기본 사용 예제

### 웹 인터페이스로 질문하기

#### 1. 서버 실행
```bash
# 프로젝트 루트에서
make dev
```

#### 2. 브라우저 접속
http://localhost:5173/app

#### 3. 질문 예시

**간단한 정보 검색 (Low Effort)**
```
ChatGPT는 언제 출시되었나요?
```

**중간 복잡도 질문 (Medium Effort)**
```
2024년 한국의 AI 스타트업 트렌드를 알려주세요
```

**복잡한 분석 질문 (High Effort)**
```
양자 컴퓨팅과 기존 컴퓨팅의 차이점을 기술적으로 상세히 비교해주세요
```

#### 4. 결과 확인

답변에 포함되는 정보:
- 📝 **답변 내용**: AI가 생성한 종합 답변
- 🔗 **출처**: 마크다운 링크 형식 `[제목](URL)`
- 📊 **활동 타임라인**: 검색 과정 시각화

---

## CLI로 질문하기

### 기본 사용법

```bash
cd backend
python examples/cli_research.py "질문 내용"
```

### 예제 1: 간단한 질문

```bash
python examples/cli_research.py "2024년 올림픽은 어디서 개최되나요?"
```

**출력 예시:**
```
2024년 올림픽은 프랑스 파리에서 개최됩니다. 개최 기간은 7월 26일부터 8월 11일까지입니다.

출처:
- [Paris 2024 Official](https://olympics.com/en/paris-2024)
- [Wikipedia](https://en.wikipedia.org/wiki/2024_Summer_Olympics)
```

### 예제 2: 커스텀 설정

```bash
python examples/cli_research.py \
  "인공지능의 미래 전망은?" \
  --initial-queries 5 \
  --max-loops 3 \
  --reasoning-model gemini-2.5-pro
```

**옵션 설명:**
- `--initial-queries 5`: 초기에 5개의 다양한 검색 쿼리 생성
- `--max-loops 3`: 최대 3번까지 추가 검색 수행
- `--reasoning-model gemini-2.5-pro`: 최고 성능 모델 사용

### 예제 3: 스크립트에서 사용

**파일: `my_research.py`**
```python
#!/usr/bin/env python3
from langchain_core.messages import HumanMessage
from agent.graph import graph

questions = [
    "2024년 AI 트렌드는?",
    "양자 컴퓨팅의 실제 활용 사례는?",
    "블록체인의 미래는?"
]

for question in questions:
    print(f"\n{'='*60}")
    print(f"질문: {question}")
    print('='*60)

    state = {
        "messages": [HumanMessage(content=question)],
        "initial_search_query_count": 3,
        "max_research_loops": 2,
    }

    result = graph.invoke(state)
    answer = result["messages"][-1].content

    print(answer)
```

**실행:**
```bash
python my_research.py
```

---

## 설정 커스터마이징

### 환경 변수로 설정하기

**파일: `backend/.env`**
```env
# === 모델 설정 ===
QUERY_GENERATOR_MODEL="gemini-2.0-flash"
REFLECTION_MODEL="gemini-2.5-flash"
ANSWER_MODEL="gemini-2.5-pro"

# === 검색 설정 ===
NUMBER_OF_INITIAL_QUERIES=3
MAX_RESEARCH_LOOPS=2

# === LangSmith 추적 (디버깅) ===
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY="your-langsmith-api-key"
LANGCHAIN_PROJECT="my-research-agent"
```

### 프로그램에서 설정하기

```python
from agent.graph import graph
from langchain_core.messages import HumanMessage

config = {
    "configurable": {
        "query_generator_model": "gemini-2.0-flash",
        "reflection_model": "gemini-2.5-flash",
        "answer_model": "gemini-2.5-pro",
        "number_of_initial_queries": 5,
        "max_research_loops": 3,
    }
}

state = {
    "messages": [HumanMessage(content="AI 윤리란?")],
}

result = graph.invoke(state, config=config)
```

### 성능 vs 비용 최적화

#### 빠르고 저렴하게 (Low Cost)
```env
QUERY_GENERATOR_MODEL="gemini-2.0-flash"
REFLECTION_MODEL="gemini-2.0-flash"
ANSWER_MODEL="gemini-2.0-flash"
NUMBER_OF_INITIAL_QUERIES=1
MAX_RESEARCH_LOOPS=1
```

**특징:**
- ⚡ 빠른 응답 (10-30초)
- 💰 저렴한 비용
- 📊 간단한 질문에 적합

#### 균형잡힌 설정 (Balanced)
```env
QUERY_GENERATOR_MODEL="gemini-2.0-flash"
REFLECTION_MODEL="gemini-2.5-flash"
ANSWER_MODEL="gemini-2.5-flash"
NUMBER_OF_INITIAL_QUERIES=3
MAX_RESEARCH_LOOPS=2
```

**특징:**
- ⏱️ 적당한 속도 (30-60초)
- 💵 합리적인 비용
- 🎯 대부분의 질문에 적합

#### 고품질 (High Quality)
```env
QUERY_GENERATOR_MODEL="gemini-2.0-flash"
REFLECTION_MODEL="gemini-2.5-pro"
ANSWER_MODEL="gemini-2.5-pro"
NUMBER_OF_INITIAL_QUERIES=5
MAX_RESEARCH_LOOPS=5
```

**특징:**
- 🐌 느린 응답 (1-3분)
- 💎 높은 비용
- 🔬 복잡한 연구에 적합

---

## 프롬프트 수정하기

### 검색 쿼리 생성 프롬프트 수정

**파일: `backend/src/agent/prompts.py`**

**원본:**
```python
query_writer_instructions = """Your goal is to generate sophisticated and diverse web search queries...

Instructions:
- Always prefer a single search query, only add another query if...
- Each query should focus on one specific aspect...
"""
```

**커스텀 예시 1: 한국어 중심 검색**
```python
query_writer_instructions = """한국어 웹 검색을 위한 최적의 검색어를 생성하세요.

지침:
- 검색어는 한국어로 작성하되, 필요시 영어도 혼용 가능
- 한국 관련 정보를 우선적으로 찾을 수 있도록 구성
- ".kr" 도메인이나 한국 사이트를 우선 검색하도록 유도
- 최대 {number_queries}개의 쿼리 생성
- 현재 날짜: {current_date}

주제: {research_topic}
"""
```

**커스텀 예시 2: 학술 논문 검색**
```python
query_writer_instructions = """Generate academic-focused search queries.

Instructions:
- Prefer academic and scholarly sources
- Include terms like "research", "study", "paper", "journal"
- Target recent publications (within last 2 years)
- Maximum {number_queries} queries
- Current date: {current_date}

Topic: {research_topic}
"""
```

### 답변 생성 프롬프트 수정

**원본:**
```python
answer_instructions = """Generate a high-quality answer to the user's question...

Instructions:
- The current date is {current_date}.
- Generate a high-quality answer...
- Include the sources you used...
"""
```

**커스텀 예시: 한국어 답변 강제**
```python
answer_instructions = """사용자의 질문에 대해 한국어로 고품질 답변을 생성하세요.

지침:
- 현재 날짜: {current_date}
- 반드시 한국어로 답변을 작성하세요
- 출처는 마크다운 링크 형식으로 포함하세요 (예: [제목](URL))
- 전문적이면서도 이해하기 쉽게 작성하세요
- 불확실한 정보는 명시하세요

사용자 질문:
{research_topic}

수집된 정보:
{summaries}
"""
```

---

## UI 커스터마이징

### 색상 테마 변경

**파일: `frontend/src/global.css`**

**다크 모드 색상 변경:**
```css
@layer base {
  :root {
    /* 기본 배경색 변경 */
    --background: 222.2 84% 4.9%;  /* 더 어두운 배경 */

    /* 강조 색상 변경 */
    --primary: 210 100% 50%;  /* 파란색 계열 */

    /* 텍스트 색상 변경 */
    --foreground: 210 40% 98%;
  }
}
```

**라이트 모드 추가:**
```css
@layer base {
  :root.light {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
  }
}
```

### 로고 및 제목 변경

**파일: `frontend/src/components/WelcomeScreen.tsx`**

```typescript
// 제목 변경
<h1 className="...">
  나만의 AI 리서치 어시스턴트  {/* 변경됨 */}
</h1>

// 설명 변경
<p className="...">
  궁금한 것을 물어보세요. AI가 웹에서 정보를 찾아 정확한 답변을 드립니다.
</p>
```

### Effort Level 레이블 변경

**파일: `frontend/src/components/WelcomeScreen.tsx`**

```typescript
const effortLevels = [
  { value: "low", label: "빠른 검색", description: "1개 쿼리, 1회 반복" },
  { value: "medium", label: "표준 검색", description: "3개 쿼리, 3회 반복" },
  { value: "high", label: "깊이 있는 검색", description: "5개 쿼리, 10회 반복" },
]
```

### 입력창 placeholder 변경

**파일: `frontend/src/components/WelcomeScreen.tsx`**

```typescript
<Textarea
  placeholder="예: 2024년 AI 기술 트렌드를 알려주세요"  {/* 변경됨 */}
  className="..."
/>
```

---

## 새로운 노드 추가하기

### 예제: 요약 노드 추가

#### 1. 상태에 필드 추가

**파일: `backend/src/agent/state.py`**

```python
class OverallState(TypedDict):
    messages: Annotated[list, add_messages]
    search_query: Annotated[list, operator.add]
    web_research_result: Annotated[list, operator.add]
    sources_gathered: Annotated[list, operator.add]
    # 새로 추가
    summary: str  # 중간 요약 저장
    initial_search_query_count: int
    max_research_loops: int
    research_loop_count: int
    reasoning_model: str
```

#### 2. 노드 함수 정의

**파일: `backend/src/agent/graph.py`**

```python
def summarize_results(state: OverallState, config: RunnableConfig):
    """중간 결과를 요약합니다."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    configurable = Configuration.from_runnable_config(config)
    llm = ChatGoogleGenerativeAI(
        model=configurable.reflection_model,
        temperature=0,
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    prompt = f"""다음 검색 결과들을 간단히 요약해주세요:

{chr(10).join(state['web_research_result'])}
"""

    summary = llm.invoke(prompt).content

    return {"summary": summary}
```

#### 3. 그래프에 노드 추가

```python
# 노드 추가
builder.add_node("summarize_results", summarize_results)

# 엣지 수정
builder.add_edge("web_research", "summarize_results")  # 웹 리서치 후 요약
builder.add_edge("summarize_results", "reflection")   # 요약 후 반성
```

#### 4. 프롬프트에서 요약 사용

```python
def reflection(state: OverallState, config: RunnableConfig):
    # ...
    formatted_prompt = reflection_instructions.format(
        current_date=get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        summaries=state["summary"],  # 중간 요약 사용
    )
    # ...
```

---

## 고급 활용법

### 1. 스트리밍 출력 처리

```python
from agent.graph import graph
from langchain_core.messages import HumanMessage

state = {
    "messages": [HumanMessage(content="AI란 무엇인가요?")],
    "initial_search_query_count": 3,
}

# 스트리밍으로 실행
for chunk in graph.stream(state, stream_mode="updates"):
    print(chunk)
```

**출력 예시:**
```python
{'generate_query': {'search_query': ['AI 정의', '인공지능 개념', ...]}}
{'web_research': {'web_research_result': ['AI는...'], ...}}
{'reflection': {'is_sufficient': False, ...}}
...
```

### 2. 중간 상태 저장 및 재개

```python
from langgraph.checkpoint.memory import MemorySaver

# 체크포인터 생성
checkpointer = MemorySaver()

# 그래프 컴파일 시 체크포인터 추가
graph_with_checkpoints = builder.compile(checkpointer=checkpointer)

# 스레드 ID로 실행
config = {"configurable": {"thread_id": "my-session-1"}}

# 첫 번째 실행
result1 = graph_with_checkpoints.invoke(
    {"messages": [HumanMessage(content="AI란?")]},
    config=config
)

# 같은 스레드에서 후속 질문
result2 = graph_with_checkpoints.invoke(
    {"messages": [HumanMessage(content="더 자세히 설명해주세요")]},
    config=config
)
```

### 3. 병렬 처리 최적화

```python
import asyncio
from agent.graph import graph

async def process_multiple_questions(questions):
    """여러 질문을 병렬로 처리"""
    tasks = []

    for question in questions:
        state = {
            "messages": [HumanMessage(content=question)],
            "initial_search_query_count": 3,
        }
        task = graph.ainvoke(state)  # 비동기 실행
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results

# 실행
questions = [
    "2024년 AI 트렌드는?",
    "양자 컴퓨팅이란?",
    "블록체인의 미래는?"
]

results = asyncio.run(process_multiple_questions(questions))

for i, result in enumerate(results):
    print(f"\n질문 {i+1}: {questions[i]}")
    print(f"답변: {result['messages'][-1].content}")
```

### 4. 커스텀 도구 추가

```python
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """수학 계산을 수행합니다."""
    try:
        result = eval(expression)
        return f"계산 결과: {result}"
    except Exception as e:
        return f"계산 오류: {str(e)}"

# 그래프에 도구 추가
from agent.graph import builder

def tool_executor(state, config):
    """도구를 실행하는 노드"""
    # 도구 실행 로직
    pass

builder.add_node("tool_executor", tool_executor)
```

### 5. 데이터베이스에 결과 저장

```python
import sqlite3
from datetime import datetime

def save_to_db(question, answer, sources):
    """검색 결과를 데이터베이스에 저장"""
    conn = sqlite3.connect('research_history.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            sources TEXT,
            timestamp DATETIME
        )
    ''')

    cursor.execute('''
        INSERT INTO research_history (question, answer, sources, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (question, answer, str(sources), datetime.now()))

    conn.commit()
    conn.close()

# 사용 예시
result = graph.invoke(state)
answer = result["messages"][-1].content
sources = result.get("sources_gathered", [])

save_to_db(
    question="AI란 무엇인가요?",
    answer=answer,
    sources=sources
)
```

### 6. 웹훅으로 결과 전송

```python
import requests

def send_to_webhook(result):
    """결과를 웹훅으로 전송"""
    webhook_url = "https://your-webhook-url.com/callback"

    payload = {
        "question": result["messages"][0].content,
        "answer": result["messages"][-1].content,
        "sources": result.get("sources_gathered", []),
        "timestamp": datetime.now().isoformat()
    }

    response = requests.post(webhook_url, json=payload)
    return response.status_code

# 사용 예시
result = graph.invoke(state)
status = send_to_webhook(result)
print(f"웹훅 전송 상태: {status}")
```

---

## 실전 프로젝트 아이디어

### 1. 뉴스 요약 봇

```python
# 특정 주제의 최신 뉴스를 검색하고 요약
def news_summarizer(topic, date_range="last 7 days"):
    state = {
        "messages": [HumanMessage(
            content=f"{topic}에 대한 {date_range} 동안의 주요 뉴스를 요약해주세요"
        )],
        "initial_search_query_count": 5,
        "max_research_loops": 2,
    }

    result = graph.invoke(state)
    return result["messages"][-1].content
```

### 2. 연구 논문 파인더

```python
# 학술 논문 검색 및 요약
def research_paper_finder(research_topic, year=2024):
    custom_prompt = f"""
    Find recent academic papers about {research_topic} from {year}.
    Focus on:
    - Peer-reviewed journals
    - Conference proceedings
    - arXiv preprints

    Summarize key findings and methodologies.
    """

    state = {
        "messages": [HumanMessage(content=custom_prompt)],
        "initial_search_query_count": 5,
        "max_research_loops": 3,
    }

    return graph.invoke(state)
```

### 3. 경쟁사 분석 도구

```python
def competitor_analysis(company_name):
    state = {
        "messages": [HumanMessage(
            content=f"""
            {company_name}의 다음 정보를 조사해주세요:
            1. 최근 제품 출시 및 업데이트
            2. 시장 점유율 변화
            3. 주요 경쟁사와의 비교
            4. 최근 뉴스 및 이벤트
            """
        )],
        "initial_search_query_count": 5,
        "max_research_loops": 3,
    }

    return graph.invoke(state)
```

---

## 다음 단계

더 깊이 이해하고 싶다면:

1. **[아키텍처 문서](./ARCHITECTURE.md)** - 시스템 내부 동작 원리
2. **[API 참조](./API_REFERENCE.md)** - 모든 함수 및 클래스 상세 설명
3. **[초보자 가이드](./BEGINNER_GUIDE.md)** - 기본 개념 복습

---

## 커뮤니티 예제

더 많은 예제는 다음에서 확인하세요:

- GitHub Discussions
- 커뮤니티 위키
- 샘플 프로젝트 저장소

**여러분의 예제도 공유해주세요!** Pull Request를 통해 이 문서에 기여할 수 있습니다.
