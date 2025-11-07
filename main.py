from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json

# Import your agent function
from agent import generate_post_data

app = FastAPI(
    title="Demanual AI Post Generator",
    description="API for generating LinkedIn posts from recent news."
)

# 1. Define Input JSON model
class TopicRequest(BaseModel):
    topic: str

# 2. Define Output JSON model
class PostResponse(BaseModel):
    topic: str
    news_sources: List[str]
    linkedin_post: str
    image_suggestion: Optional[str] = None

@app.post("/generate-post", response_model=PostResponse)
def create_post(request: TopicRequest):
    
    # 3. Call your agent
    # This will return a JSON *string*
    json_string_output = generate_post_data(request.topic)
    
    if not json_string_output:
        raise HTTPException(status_code=500, detail="Agent returned no output")

    # 4. Parse the JSON string from the agent
    try:
        data = json.loads(json_string_output)
    except json.JSONDecodeError:
        print(f"Agent Output (Not JSON): {json_string_output}")
        raise HTTPException(status_code=500, detail="Failed to parse agent's JSON output")

    if data.get("error"):
        raise HTTPException(status_code=500, detail=f"Agent Error: {data['error']}")

    # 5. Format and return the final Pydantic model
    response = PostResponse(
        topic=request.topic,
        news_sources=data.get("news_sources", []),
        linkedin_post=data.get("linkedin_post", "No post generated."),
        image_suggestion=data.get("image_suggestion", None)
    )
    return response

@app.get("/")
def read_root():
    return {"message": "Welcome! Go to /docs for the API."}