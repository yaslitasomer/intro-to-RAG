import minsearch
from openai import OpenAI

openai_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  
)

def build_index(documents: list[dict], index_name : str = "faq_index") -> minsearch.Index:
    """
    Builds and populates the Minsearch index
    """
    
    index = minsearch.Index(
        text_fields=["content"],
        keyword_fields=["filename"]
    )
    index.fit(documents)
    return index


def search(query: str, index_client, num_results: int = 5) -> list[dict]:
    """
    Executes a search query against Minsearch
    """
    return index_client.search(
    query = query,
    filter_dict={},
    boost_dict={},
    num_results = num_results
    )


def build_prompt(query: str, search_results: list[dict]) -> str:
    """
    Constructs the LLM prompt using the retrieved search results as context.
    """
    prompt_template ="""
You are an expert Q&A assistant specializing in answering questions based on the provided context.
Use the context to answer the question accurately and concisely. If the answer is not found in the context, respond with "I don't know."

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
        context += f"Filename: {doc['filename']}\nContent: {doc['content']}\n\n"

    return prompt_template.format(query = query, context=context)

def llm(prompt: str) -> tuple[str, dict]:
    """
    Sends the constructed prompt to Llama model via the local Ollama.
    Returns bot the content and the token usage statistics.
    """
    response = openai_client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content":prompt}],
        temperature=0.0,
        stop=["Question:", "---", "\n\nQuestion:"]
    )
    return response.choices[0].message.content, response.usage

def ask_assistant(query: str, index_client) -> tuple[str, dict]:
    """
    Executes the end-to-ene RAG pipeline (Search -> Prompt -> Generate).
    """
    search_results = search(query, index_client)
    prompt = build_prompt(query, search_results)
    answer, usage = llm(prompt)

    return answer, usage