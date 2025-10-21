# Gemini Fullstack LangGraph Quickstart プロジェクト解説ドキュメント

## 目次
1. [プロジェクト概要](#プロジェクト概要)
2. [ディレクトリ構成](#ディレクトリ構成)
3. [LangGraphの条件分岐メカニズム](#langgraphの条件分岐メカニズム)
4. [データベース実装](#データベース実装)
5. [設定管理システム](#設定管理システム)
6. [UI部分のワークフロー可視化](#ui部分のワークフロー可視化)

---

## プロジェクト概要

このプロジェクトは、**Gemini Fullstack LangGraph Quickstart**という名前のフルスタックAIエージェントアプリケーションです。LangGraphを使用したバックエンド（Python）とReact/TypeScriptを使用したフロントエンドで構成されています。

### 主要技術スタック
- **バックエンド**: Python + LangGraph + FastAPI
- **フロントエンド**: React + TypeScript + Vite
- **データベース**: PostgreSQL + Redis
- **AI**: Google Gemini API
- **デプロイ**: Docker + Docker Compose

---

## ディレクトリ構成

```
gemini-fullstack-langgraph-quickstart/
├── agent.png                    # エージェント関連の画像
├── app.png                      # アプリケーション関連の画像
├── docker-compose.yml           # Docker Compose設定
├── Dockerfile                   # Docker設定
├── LICENSE                      # ライセンスファイル
├── Makefile                     # ビルド・実行用Makefile
├── README.md                    # プロジェクト説明書
├── backend/                     # バックエンド（Python）
│   ├── build/                   # ビルド成果物
│   ├── examples/                # サンプルコード
│   ├── langgraph.json          # LangGraph設定
│   ├── LICENSE                  # ライセンス
│   ├── Makefile                # バックエンド用Makefile
│   ├── pyproject.toml          # Python依存関係管理
│   ├── src/agent/              # エージェント実装
│   │   ├── __init__.py
│   │   ├── app.py              # メインアプリケーション
│   │   ├── configuration.py    # 設定管理
│   │   ├── graph.py            # LangGraph定義
│   │   ├── prompts.py          # プロンプト定義
│   │   ├── state.py            # 状態管理
│   │   ├── tools_and_schemas.py # ツールとスキーマ定義
│   │   └── utils.py            # ユーティリティ関数
│   └── test-agent.ipynb        # エージェントテスト用Jupyter Notebook
└── frontend/                    # フロントエンド（React/TypeScript）
    ├── components.json          # UIコンポーネント設定
    ├── eslint.config.js         # ESLint設定
    ├── index.html              # HTMLエントリーポイント
    ├── node_modules/           # Node.js依存関係
    ├── package-lock.json       # 依存関係ロックファイル
    ├── package.json            # 依存関係管理
    ├── public/                 # 静的ファイル
    ├── src/                    # ソースコード
    │   ├── App.tsx             # メインアプリケーション
    │   ├── components/         # Reactコンポーネント
    │   │   ├── ActivityTimeline.tsx    # アクティビティタイムライン
    │   │   ├── ChatMessagesView.tsx    # チャットメッセージ表示
    │   │   ├── InputForm.tsx           # 入力フォーム
    │   │   ├── ui/                     # UIコンポーネント
    │   │   └── WelcomeScreen.tsx       # ウェルカム画面
    │   ├── global.css          # グローバルスタイル
    │   ├── lib/                # ライブラリ・ユーティリティ
    │   ├── main.tsx            # エントリーポイント
    │   └── vite-env.d.ts       # Vite型定義
    ├── tsconfig.json           # TypeScript設定
    ├── tsconfig.node.json      # Node.js用TypeScript設定
    └── vite.config.ts         # Vite設定
```

---

## LangGraphの条件分岐メカニズム

### `add_conditional_edges`の引数について

```python
builder.add_conditional_edges(
    "generate_query", continue_to_web_research, ["web_research"]
)
```

このメソッドの引数は以下の通りです：

1. **`"generate_query"`** - 遷移元のノード名
2. **`continue_to_web_research`** - ルーティング関数（条件判定関数）
3. **`["web_research"]`** - 可能な遷移先ノードのリスト

### `continue_to_web_research`関数の動作

```python
def continue_to_web_research(state: QueryGenerationState):
    """LangGraph node that sends the search queries to the web research node.

    This is used to spawn n number of web research nodes, one for each search query.
    """
    return [
        Send("web_research", {"search_query": search_query, "id": int(idx)})
        for idx, search_query in enumerate(state["search_query"])
    ]
```

### 重要なポイント

1. **`Send`オブジェクトのリストを返す**: これは**並列実行**を意味します
2. **複数の`web_research`ノードを並列実行**: 各検索クエリに対して独立した`web_research`ノードが作成されます
3. **`["web_research"]`の意味**: 可能な遷移先として`web_research`ノードが指定されている

### 実際の動作フロー

1. `generate_query`ノードが実行される
2. 複数の検索クエリが生成される（例：`["AIの最新動向", "機械学習の応用", "深層学習の課題"]`）
3. `continue_to_web_research`関数が呼ばれる
4. 各クエリに対して`Send("web_research", {...})`オブジェクトが作成される
5. **3つの`web_research`ノードが並列実行される**
6. 各ノードが独立してWeb検索を実行する

### 第三引数の役割

第三引数`["web_research"]`は：
- **型チェック用のアノテーション**
- **可能な遷移先の宣言**
- **LangGraphがグラフの構造を理解するための情報**

実際の遷移は**第二引数の関数の返り値**で決まります：

- **文字列を返す場合**: そのノードに遷移
- **`Send`オブジェクトのリストを返す場合**: 並列実行
- **`Send`オブジェクト単体を返す場合**: そのノードに遷移

---

## データベース実装

### データベース構成

このプロジェクトでは**2つのデータベース**を使用しています：

#### PostgreSQL
- **用途**: メインのデータストレージ
- **ポート**: 5433 (外部アクセス用)
- **設定**:
  ```yaml
  POSTGRES_DB: postgres
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres
  ```

#### Redis
- **用途**: メッセージブローカー・キャッシュ
- **ポート**: 6379 (内部のみ)
- **用途**: リアルタイムストリーミング用のpub-sub

### LangGraphでのDB使用目的

#### PostgreSQLの役割
- **Assistants**: エージェントの設定・定義を保存
- **Threads**: 会話スレッドの管理
- **Runs**: 実行履歴の保存
- **Thread State**: 会話状態の永続化
- **Long-term Memory**: 長期記憶の保存
- **Background Task Queue**: バックグラウンドタスクの管理（'exactly once' semantics）

#### Redisの役割
- **Pub-Sub Broker**: リアルタイムストリーミング用
- **Background Runs**: バックグラウンド実行の結果をストリーミング

### 接続設定

#### Docker Composeでの設定
```yaml
environment:
  REDIS_URI: redis://langgraph-redis:6379
  POSTGRES_URI: postgres://postgres:postgres@langgraph-postgres:5432/postgres?sslmode=disable
```

#### LangGraph設定ファイル (`langgraph.json`)
```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "http": {
    "app": "./src/agent/app.py:app"
  },
  "env": ".env"
}
```

### 実装の特徴

#### 自動的なDB管理
- **明示的なDB接続コードなし**: LangGraphが自動的にDB接続を管理
- **環境変数ベース**: `POSTGRES_URI`と`REDIS_URI`で接続情報を指定
- **スキーマ自動生成**: LangGraphが自動的にテーブル構造を作成

#### 状態管理
```python
# graph.py内で状態が自動的にDBに保存される
class OverallState(TypedDict):
    messages: list[BaseMessage]
    search_query: list[str]
    web_research_result: list[str]
    sources_gathered: list[dict]
    # ... その他の状態
```

### データフロー

1. **フロントエンド** → **LangGraph API** → **PostgreSQL** (状態保存)
2. **LangGraph** → **Redis** → **フロントエンド** (リアルタイム更新)
3. **バックグラウンドタスク** → **PostgreSQL** (結果保存)

---

## 設定管理システム

### `Configuration.from_runnable_config(config)`の解説

```python
configurable = Configuration.from_runnable_config(config)
```

このコードは、**LangGraphの設定システム**を活用して、エージェントの動作を動的に制御する仕組みです。

### `Configuration`クラスの構造

```python
class Configuration(BaseModel):
    query_generator_model: str = Field(default="gemini-2.0-flash")
    reflection_model: str = Field(default="gemini-2.5-flash") 
    answer_model: str = Field(default="gemini-2.5-pro")
    number_of_initial_queries: int = Field(default=3)
    max_research_loops: int = Field(default=2)
```

### `from_runnable_config`メソッドの動作

```python
@classmethod
def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "Configuration":
    # 1. configから"configurable"キーを取得
    configurable = (
        config["configurable"] if config and "configurable" in config else {}
    )
    
    # 2. 環境変数とconfigの両方から値を取得（優先順位: 環境変数 > config）
    raw_values: dict[str, Any] = {
        name: os.environ.get(name.upper(), configurable.get(name))
        for name in cls.model_fields.keys()
    }
    
    # 3. None値を除外
    values = {k: v for k, v in raw_values.items() if v is not None}
    
    # 4. Configurationインスタンスを作成
    return cls(**values)
```

### 設定の優先順位

1. **環境変数** (最高優先度)
2. **RunnableConfig** (中優先度)
3. **デフォルト値** (最低優先度)

### 実際の使用例

```python
# graph.py内での使用
configurable = Configuration.from_runnable_config(config)

# 設定値を使用してLLMを初期化
llm = ChatGoogleGenerativeAI(
    model=configurable.query_generator_model,  # "gemini-2.0-flash" または設定値
    temperature=1.0,
    max_retries=2,
    api_key=os.getenv("GEMINI_API_KEY"),
)
```

### 設定の動的変更

この仕組みにより、以下の方法で設定を動的に変更できます：

#### 環境変数での設定
```bash
export QUERY_GENERATOR_MODEL="gemini-2.5-flash"
export NUMBER_OF_INITIAL_QUERIES="5"
```

#### API呼び出し時の設定
```python
# フロントエンドからAPI呼び出し時に設定を渡す
{
    "configurable": {
        "query_generator_model": "gemini-2.5-flash",
        "number_of_initial_queries": 5
    }
}
```

### 利点

- **柔軟性**: 実行時に設定を変更可能
- **環境対応**: 開発・本番環境で異なる設定を使用可能
- **型安全性**: Pydanticによる型チェック
- **デフォルト値**: 設定が未指定でも動作

---

## UI部分のワークフロー可視化

AIエージェントのワークフローを動的に表現している部分は、主に以下の3つのコンポーネントで構成されています：

### 1. リアルタイムイベント処理 (`App.tsx` 30-72行)

```typescript
onUpdateEvent: (event: any) => {
  let processedEvent: ProcessedEvent | null = null;
  if (event.generate_query) {
    processedEvent = {
      title: "Generating Search Queries",
      data: event.generate_query?.search_query?.join(", ") || "",
    };
  } else if (event.web_research) {
    const sources = event.web_research.sources_gathered || [];
    const numSources = sources.length;
    const uniqueLabels = [
      ...new Set(sources.map((s: any) => s.label).filter(Boolean)),
    ];
    const exampleLabels = uniqueLabels.slice(0, 3).join(", ");
    processedEvent = {
      title: "Web Research",
      data: `Gathered ${numSources} sources. Related to: ${
        exampleLabels || "N/A"
      }.`,
    };
  } else if (event.reflection) {
    processedEvent = {
      title: "Reflection",
      data: "Analysing Web Research Results",
    };
  } else if (event.finalize_answer) {
    processedEvent = {
      title: "Finalizing Answer",
      data: "Composing and presenting the final answer.",
    };
    hasFinalizeEventOccurredRef.current = true;
  }
  if (processedEvent) {
    setProcessedEventsTimeline((prevEvents) => [
      ...prevEvents,
      processedEvent!,
    ]);
  }
}
```

**役割**: LangGraphから送信されるリアルタイムイベントを処理し、ユーザーフレンドリーな形式に変換

### 2. アクティビティタイムライン (`ActivityTimeline.tsx`)

```typescript
const getEventIcon = (title: string, index: number) => {
  if (title.toLowerCase().includes("generating")) {
    return <TextSearch className="h-4 w-4 text-neutral-400" />;
  } else if (title.toLowerCase().includes("reflection")) {
    return <Brain className="h-4 w-4 text-neutral-400" />;
  } else if (title.toLowerCase().includes("research")) {
    return <Search className="h-4 w-4 text-neutral-400" />;
  } else if (title.toLowerCase().includes("finalizing")) {
    return <Pen className="h-4 w-4 text-neutral-400" />;
  }
  return <Activity className="h-4 w-4 text-neutral-400" />;
};
```

**役割**: 
- 各ワークフローステップに適切なアイコンを表示
- タイムライン形式でプロセスの進行状況を可視化
- 折りたたみ可能なUIでユーザーエクスペリエンスを向上

### 3. チャットメッセージビュー (`ChatMessagesView.tsx` 185-198行)

```typescript
const AiMessageBubble: React.FC<AiMessageBubbleProps> = ({
  message,
  historicalActivity,
  liveActivity,
  isLastMessage,
  isOverallLoading,
  // ...
}) => {
  // Determine which activity events to show and if it's for a live loading message
  const activityForThisBubble =
    isLastMessage && isOverallLoading ? liveActivity : historicalActivity;
  const isLiveActivityForThisBubble = isLastMessage && isOverallLoading;

  return (
    <div className={`relative break-words flex flex-col`}>
      {activityForThisBubble && activityForThisBubble.length > 0 && (
        <div className="mb-3 border-b border-neutral-700 pb-3 text-xs">
          <ActivityTimeline
            processedEvents={activityForThisBubble}
            isLoading={isLiveActivityForThisBubble}
          />
        </div>
      )}
      {/* AI response content */}
    </div>
  );
};
```

**役割**: 
- AIメッセージとワークフロー進行状況を統合表示
- リアルタイム進行状況と履歴を適切に切り替え

### ワークフローの可視化フロー

1. **ユーザーがメッセージ送信** → `handleSubmit`が呼ばれる
2. **LangGraphがイベントを送信** → `onUpdateEvent`が各ステップを処理
3. **イベントがタイムラインに追加** → `setProcessedEventsTimeline`で状態更新
4. **UIがリアルタイム更新** → `ActivityTimeline`コンポーネントが表示
5. **完了時に履歴保存** → `setHistoricalActivities`で過去の活動を保存

### 表示されるワークフローステップ

- **"Generating Search Queries"** - 検索クエリ生成
- **"Web Research"** - Web検索実行（ソース数と関連ラベルを表示）
- **"Reflection"** - 結果分析
- **"Finalizing Answer"** - 最終回答作成

この仕組みにより、ユーザーはAIエージェントが何をしているかをリアルタイムで把握でき、透明性の高いAI体験を提供しています。

---

## まとめ

このプロジェクトは、LangGraphの強力な機能を活用して、複雑なAIエージェントワークフローを効率的に実装した優れた例です。特に以下の点が特徴的です：

1. **並列処理**: 複数の検索クエリを同時実行
2. **リアルタイム可視化**: ユーザーがプロセスの進行状況を把握可能
3. **柔軟な設定管理**: 環境変数やAPI呼び出し時に動的に設定変更可能
4. **自動DB管理**: LangGraphが自動的に状態管理と永続化を処理
5. **型安全性**: PydanticとTypeScriptによる堅牢な実装

これらの要素が組み合わさることで、開発者にとって保守しやすく、ユーザーにとって使いやすいAIエージェントアプリケーションが実現されています。
