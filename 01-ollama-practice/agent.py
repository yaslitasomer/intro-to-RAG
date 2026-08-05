import json
from openai import OpenAI
from rag import search

openai_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# 1. TOOL DEFINITION: Simplified to prevent schema hallucination
search_tool = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Searches the DC Comics database for facts.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string" # Removed the long description here to prevent model confusion
                }
            },
            "required": ["query"]
        }
    }
}

# 2. HELPER: The bridge that converts the JSON command returned by the model into a real Python function
def make_call(tool_call, index_client):
    args = json.loads(tool_call.function.arguments)
    
    # --- BULLETPROOF DEFENSIVE PROGRAMMING ---
    raw_query = args.get("query", "")
    search_query = ""
    
    if isinstance(raw_query, dict):
        # If the model regurgitates the schema, extract the actual search term from "value"
        if "value" in raw_query:
            search_query = str(raw_query["value"])
        else:
            # Fallback just in case it uses a different key
            search_query = str(list(raw_query.values())[0]) if raw_query else ""
    else:
        # Guarantee it is cast to a string type
        search_query = str(raw_query)
        
    print(f" -> Sanitized query sent to database: '{search_query}'")
    # -----------------------------------------
    
    # If the model wants to "search", we trigger our search function from rag.py
    if tool_call.function.name == "search":
        # IMPORTANT: We are passing 'search_query' here, not args["query"]
        result = search(query=search_query, index_client=index_client)
        
    result_json = json.dumps(result, indent=2)
    
    # Returning the response in the standard OpenAI/Ollama tool message format
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result_json,
    }
    
# 3. AGENT LOOP: The main loop where the model thinks and takes action
def agent_loop(instructions: str, question: str, index_client, model="llama3.2") -> str:
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": question}
    ]
    
    it = 1
    max_iterations = 5 # Infinite loop prevention for memory and CPU safety
    last_answer = "Could not find an answer."

    while it <= max_iterations:
        print(f"\n[Iteration #{it}] Model is thinking...")
        
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=[search_tool],
            temperature=0.0
        )
        
        response_message = response.choices[0].message
        messages.append(response_message)
        
        # If the model wants to use a tool (make a search):
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                print(f" -> Executing Search: {tool_call.function.arguments}")
                tool_output = make_call(tool_call, index_client)
                messages.append(tool_output) # Add the search result to the model's memory
        
        # If the model does not want to search (found the answer):
        else:
            print(" -> Final Answer Generated.")
            last_answer = response_message.content
            break
            
        it += 1
        
    return last_answer