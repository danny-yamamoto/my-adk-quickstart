import requests
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv(override=True)


# セッション管理キー
STATE_CURRENT_TEXT = "current_text"
STATE_EVAL1 = "evaluation1"
STATE_EVAL2 = "evaluation2"
STATE_EVAL_AGGREGATED = "evaluation_aggregated"

# モデル
# model = LiteLlm(model="openai/gpt-4o")
model = "gemini-2.0-flash"

# ペルソナ
persona1 = "技術ゴリゴリのデータサイエンティスト。生成AIやLLMに関心が高い"
persona2 = "エンジニア。バズ狙いの誇張したワードは嫌い"


def fetch_articles() -> list[str]:
    url = "https://zenn-api.vercel.app/api/trendTech"
    response = requests.get(url).json()
    return [article["title"] for article in response]


reference_texts = fetch_articles()


# テキスト生成Agent
initial_writer_agent = LlmAgent(
    name="InitialWriterAgent",
    model=model,
    description="Agent to generate initial text.",
    instruction=f"""
あなたは優れたコピーライターです。候補のキャッチコピーを5個程度考えてください。
タイトル以外は出力しないでください。
なお、他のライターたちは以下のようなキャッチコピーで評価を得ていますので参考にしてください: {reference_texts}
""",  # `reference_texts` には参考にするべきキャッチコピーを与える
    output_key=STATE_CURRENT_TEXT,
)


def word_counter(word: str) -> int:
    """
    文字列の長さを返す関数
    """
    return len(word)


# 評価Agent1
evaluator1_agent_in_loop = LlmAgent(
    name="EvaluatorAgent1",
    model=model,
    description="Agent to evaluate the generated text based on persona.",
    instruction=f"""
# あなたのペルソナ
{persona1}

# Task
ライターが考えたキャッチコピーを評価します。
{{current_text}} のキャッチコピーを以下の1-4点で評価し、評価結果を理由とともに出力してください。
4: いいねを押したい, 3: 読んでみたい, 2: 特に何とも思わない, 1: 面白くない

キャッチコピーが不適切な場合は、厳しく評価してください。
また、キャッチコピーの長さを `word_counter` ツールで計算し、40文字を超えている場合は、長すぎるのでその旨を理由に書いて1点減点してください。
""",  # `persona1` にこのエージェントのペルソナを指定
    output_key=STATE_EVAL1,
    tools=[word_counter],
)

# 評価Agent2
evaluator2_agent_in_loop = LlmAgent(
    name="EvaluatorAgent2",
    model=model,
    description="Agent to evaluate the generated text based on persona.",
    instruction=f"""
# あなたのペルソナ
{persona2}

# Task
ライターが考えたキャッチコピーを評価します。
{{current_text}} のキャッチコピーを以下の1-4点で評価し、評価結果を理由とともに出力してください。
4: いいねを押したい, 3: 読んでみたい, 2: 特に何とも思わない, 1: 面白くない

キャッチコピーが不適切な場合は、厳しく評価してください。
また、キャッチコピーの長さを `word_counter` ツールで計算し、40文字を超えている場合は、長すぎるのでその旨を理由に書いて1点減点してください。
""",
    output_key=STATE_EVAL2,
    tools=[word_counter],
)

# 評価集約Agent
evaluation_aggregator_agent_in_loop = LlmAgent(
    name="EvaluationAggregatorAgent",
    model=model,
    description="Agent to aggregate evaluations from multiple evaluators.",
    instruction=f"""
{{current_text}}という各キャッチコピーにつき、以下の評価がつきました。

# {persona1} からの評価
{{evaluation1}}

# {persona2} からの評価
{{evaluation2}}

これらの評価を、キャッチコピーごとにまとめ直して出力してください。
""",
    output_key=STATE_EVAL_AGGREGATED,
)


def exit_loop(tool_context):
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    return {}


# テキスト改善Agent
refiner_agent_in_loop = LlmAgent(
    name="RefinerAgent",
    model=model,
    description="Agent to refine the text based on the evaluation.",
    instruction=f"""
あなたは優れたコピーライターです。
あなたが以前考えたキャッチコピーは{{current_text}}ですが、これに対して、以下の評価がつきました (それぞれ4点満点)。

# 評価
{{evaluation_aggregated}}

# Task
評価結果をキャッチコピーごとによく読み、まずは「評価者全員が"4点 (いいねを押したい) "と評価したコピー」が存在するかを判定してください。
* もし存在するなら、 `exit_loop` ツールを実行してください。
* そうでなければ、評価を改善するためにキャッチコピーをブラッシュアップし、改善したキャッチコピーを出力してください (最大5個)。

なお、他のライターたちは以下のようなキャッチコピーで評価を得ていますので参考にしてください: {reference_texts}
""",
    tools=[exit_loop],
    output_key=STATE_CURRENT_TEXT,
)

refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[
        evaluator1_agent_in_loop,
        evaluator2_agent_in_loop,
        evaluation_aggregator_agent_in_loop,
        refiner_agent_in_loop,
    ],
    max_iterations=5,  # 5回で停止
)

root_agent = SequentialAgent(
    name="TextGenerationAgent",
    sub_agents=[initial_writer_agent, refinement_loop],
    description="Agent to manage a sequence of tasks related to text generation.",
)
