import json
from openai import OpenAI
from rag import search

openai_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# 1. TOOL DEFINITION
search_tool = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Searches the database for relevant information. Use this to find answers.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": ["query"]
        }
    }
}

# 2. HELPER: Converts and cleans up queries safely
def make_call(raw_query, index_client):
    search_query = ""
    
    if isinstance(raw_query, dict):
        if "value" in raw_query:
            search_query = str(raw_query["value"])
        else:
            search_query = str(list(raw_query.values())[0]) if raw_query else ""
    else:
        search_query = str(raw_query)
        
    print(f" -> Sanitized query sent to database: '{search_query}'")
    
    results = []
    if search_query:
        results = search(query=search_query, index_client=index_client, num_results=3)
        
    return json.dumps(results, indent=2)
    
# 3. AGENT LOOP: Bulletproof wrapper handling both native calls and text-based Llama JSON fallbacks
def agent_loop(instructions: str, question: str, index_client, model="llama3.2") -> tuple[str, int]:
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": question}
    ]
    
    it = 1
    max_iterations = 10 
    last_answer = "Could not find an answer."
    search_call_count = 0

    while it <= max_iterations:
        print(f"\n[Iteration #{it}] Model is thinking...")
        
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=[search_tool],
            temperature=0.0
        )
        
        response_message = response.choices[0].message
        
        # A) Native Tool Call (OpenAI style)
        if response_message.tool_calls:
            messages.append(response_message)
            for tool_call in response_message.tool_calls:
                search_call_count += 1
                print(f" -> Executing Native Search: {tool_call.function.arguments}")
                
                args = json.loads(tool_call.function.arguments)
                raw_query = args.get("query", "")
                
                tool_output_content = make_call(raw_query, index_client)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output_content
                })
                
        # B) Text-Based Fallback (When Llama 3.2 outputs the JSON tool call as raw text content)
        elif response_message.content and response_message.content.strip().startswith("{"):
            content_text = response_message.content.strip()
            try:
                content_json = json.loads(content_text)
                if "name" in content_json or "parameters" in content_json or "query" in content_json:
                    search_call_count += 1
                    print(f" -> Caught text-based tool call from Llama 3.2.")
                    
                    params = content_json.get("parameters", content_json)
                    raw_query = params.get("query", "agentic loop")
                    
                    tool_output_content = make_call(raw_query, index_client)
                    
                    messages.append(response_message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": "fallback_tool_id",
                        "content": tool_output_content
                    })
                    it += 1
                    continue
            except json.JSONDecodeError:
                pass
            
            # If it's just regular text response
            print(" -> Final Answer Generated.")
            last_answer = response_message.content
            break
            
        # C) Final Normal Text Answer
        else:
            print(" -> Final Answer Generated.")
            last_answer = response_message.content
            break
            
        it += 1
        
    return last_answer, search_call_count