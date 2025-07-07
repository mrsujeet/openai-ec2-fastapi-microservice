from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/query")
async def get_response(request: Request):
    try:
        data = await request.json()
        user_query = data.get("query")
        if not user_query:
            return JSONResponse(content={"error": "Query not provided"}, status_code=400)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_query}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

