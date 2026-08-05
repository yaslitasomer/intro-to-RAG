import minsearch
from openai import OpenAI

openai_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  
)

def build_index(documents: list[dict], index_name : str = "dc_comics"):
    """
    Builds and populates the Minsearch index
    """
    
    index = minsearch.Index(
        text_fields=["question", "text", "section"],
        keyword_fields=["category"]
    )
    index.fit(documents)
    return index


def search(query: str, index_client, num_results: int = 5) -> list[dict]:
    """
    Executes a search query against Minsearch
    """
    
    boost_dict = {"question" : 3.0, "section": 0.5}
    return index_client.search(
        query = query,
        filter_dict={},
        boost_dict=boost_dict,
        num_results = num_results
    )


def build_prompt(query: str, search_results: list[dict]) -> str:
    """
    Constructs the LLM prompt using the retrieved search results as context.
    """
    prompt_template ="""
You are an expert Q&A assistant specializing in DC Comics lore. 
Answer the QUESTION based ONLY on the provided CONTEXT.

CRITICAL INSTRUCTIONS:
1. Provide the answer directly and concisely.
2. Do NOT include introductory phrases, conversational text, or repeat the question.
3. STOP GENERATING TEXT IMMEDIATELY after providing the answer.

Context:
{context}

Question: {query}
Answer: 
""".strip()

    context = ""
    for doc in search_results:
        context += f"Section: {doc["section"]}\nQuestion: {doc["question"]}\nFact: {doc["text"]}\n\n"

    return prompt_template.format(query = query, context=context)

def llm(prompt: str) -> str:
    """
    Sends the constructed prompt to Llama model via the local Ollama.
    """
    response = openai_client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content":prompt}],
        temperature=0.0,
        stop=["Question:", "---", "\n\nQuestion:"]
    )
    return response.choices[0].message.content

def ask_assistant(query: str, index_client) -> str:
    """
    Executes the end-to-ene RAG pipeline (Search -> Prompt -> Generate).
    """
    search_results = search(query, index_client)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)

    return answer