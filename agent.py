import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

# 1. --- Define Tools & Model ---
search_tool = TavilySearch(max_results=3, time_range="week")

# ▼▼▼▼▼ THIS IS THE FIX ▼▼▼▼▼
# Using "gemini-2.0-flash", which is a free-tier model
# and is referenced in v1beta API examples.
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
# ▲▲▲▲▲ END THE FIX ▲▲▲▲▲


# 2. --- Define Prompts ---
prompt_template = """
You are an AI assistant that generates LinkedIn posts based on recent news.

INSTRUCTIONS:
- You will be given a topic and a set of recent news search results.
- Synthesize the key information from the search results.
- Generate a professional and engaging LinkedIn-style post (200-400 characters, 1st person).
- Extract the 2-3 most important source URLs from the search results.
- Provide an optional image suggestion (a simple description).

TOPIC:
{topic}

SEARCH RESULTS:
{search_results}

FINAL RESPONSE FORMAT:
You MUST output your final answer as a single, valid JSON object with no
other text before or after it.

Example:
{{
    "news_sources": ["url1", "url2"],
    "linkedin_post": "The AI world is buzzing! Recent developments in... [generated text]",
    "image_suggestion": "A graphic showing AI growth"
}}

JSON OUTPUT:
"""

prompt = PromptTemplate.from_template(prompt_template)


# 3. --- Define the Chain (The "Alternate Way") ---
def format_search_results(tavily_output: dict):
    results_list = tavily_output.get('results', [])
    return "\n---\n".join([f"URL: {res['url']}\nContent: {res['content']}" for res in results_list])


# This runnable will fetch the search results
fetch_results_chain = (
    (lambda input: {"query": input["topic"]})
    | search_tool
    | format_search_results
)

# This is the main chain
chain = (
    RunnablePassthrough.assign(
        search_results=fetch_results_chain
    )
    | {
        "prompt_str": (lambda input: prompt.format(topic=input["topic"], search_results=input["search_results"]))
    }
    | (lambda input: input["prompt_str"])
    | llm
    | StrOutputParser()
    | JsonOutputParser()
)


# 4. --- Create the Function for FastAPI ---

def generate_post_data(topic: str):
    try:
        response_json = chain.invoke({"topic": topic})
        return json.dumps(response_json)
    except Exception as e:
        print(f"Error in chain execution: {e}")
        return json.dumps({"error": str(e)})


# 5. --- Test this file directly ---

if __name__ == "__main__":
    topic = "Latest advancements in electric vehicle batteries"
    print(f"--- Testing chain with topic: {topic} ---")
    
    print("--- Testing search_tool with {'query': topic} ---")
    results = search_tool.invoke({"query": topic})
    print("--- Raw Search Results (is a dict) ---")
    print(results)
    
    print("\n--- Generating full post... ---")
    final_result_string = generate_post_data(topic)
    
    print("--- Chain Result (JSON String) ---")
    print(final_result_string)
    
    print("\n--- Parsed Python Dictionary ---")
    print(json.loads(final_result_string))