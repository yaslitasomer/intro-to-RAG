# Pull the helpers ingest and rag into one place
import sys

from openai import OpenAI
from ingest import load_faq_data, build_index
from metrics import RAGWithMetrics
from db_save import save_conversation

# Create assistant
def create_assistant():
    documents = load_faq_data()
    index = build_index(documents)
    
    return RAGWithMetrics(
        index=index,
        llm_client=OpenAI(
            base_url="http://host.docker.internal:11434/v1",
            api_key="ollama"  
        )
    )
    
# Test from the command line via uv run python assistant.py
if __name__ == "__main__":
    assistant = create_assistant()

    query = "How do I join the course?"
    if len(sys.argv) > 1:
        query = sys.argv[1]

    answer = assistant.rag(query)
    print(answer)
    
    save_conversation(assistant.last_call, query, "llm-zoomcamp")
    
