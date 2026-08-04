import os 
import minsearch
from elasticsearch import Elasticsearch
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

openai_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")   
)

def build_index(documents: list[dict], backend: str = "minsearch", index_name : str = "dc_comics"):
    """
    Builds and populates the search index based on the chosen backend
    """
    if backend == "minsearch":
        index = minsearch.Index(
            text_fields=["question", "text", "section"],
            keyword_fields=["category"]
        )
        index.fit(documents)
        return index

    elif backend == "elasticsearch":
        es_client = Elasticsearch("http://127.0.0.1:9200")

        try:
            es_client.indices.create(index=index_name)
        except Exception:
            pass

        for doc in documents:
            es_client.index(index=index_name, document=doc)

        return es_client

    else:
        raise ValueError(f"Unknown backend: {backend}. Use 'minsearch' or 'elasticsearch'")

def search(query: str, index_client, backend: str = "minsearch", index_name: str = "dc_comics", num_results: int = 5) -> list[dict]:
    """
    Executes a search query against the specified backend engine
    """
    if backend == "minsearch":
        boost_dict = {"question" : 3.0, "section": 0.5}
        return index_client.search(
            query = query,
            filter_dict={},
            boost_dict=boost_dict,
            num_results = num_results
        )

    elif backend == "elasticsearch":
        search_query = {
            "size": num_results,
            "query": {
                "multi_match":{
                    "query": query,
                    "fields": ["question^3.0", "text", "section^0.5"]
                }
            }
        }
        response = index_client.search(index=index_name, body = search_query)
        return [hit["_source"] for hit in response["hits"]["hits"]]


def build_prompt(query: str, search_results: list[dict]) -> str:
    """
    Constructs the LLM prompt using the retrieved search results as context.
    """
    prompt_template = """
        You are a DC Comics lore expert. Answer the QUESTION based ONLY on the CONTEXT provided from the database.
        If the answer is not in the context, say "I don't have that information."

        QUESTION: {question}

        CONTEXT:
        {context}
        """.strip()

    context = ""
    for doc in search_results:
        context += f"Section: {doc["section"]}\nQuestion: {doc["question"]}\nFact: {doc["text"]}\n\n"

    return prompt_template.format(question = query, context=context)

def llm(prompt: str) -> str:
    """
    Sends the constructed prompt to Llama model via the Groq API.
    """
    response = openai_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content":prompt}]
    )
    return response.choices[0].message.content

def ask_assistant(query: str, index_client, backend: str = "minsearch") -> str:
    """
    Executes the end-to-ene RAG pipeline (Search -> Prompt -> Generate).
    """
    search_results = search(query, index_client, backend = backend)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)

    return answer