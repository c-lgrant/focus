import os

import httpx
from fastapi import FastAPI
from google import genai
from google.genai import types
from pydantic import BaseModel

from src.db_session import get_session
from src.function_calling import query_database
from src.system_instructions import system_instructions

app = FastAPI()

db = get_session()


class TextInput(BaseModel):
    text: str


@app.post("/query-text")
async def process_text(input: TextInput):
    #couldnt find spec for v1.0
    doc_data = httpx.get("https://focus.finops.org/wp-content/uploads/2024/11/FOCUS-spec-v1_1.pdf").content
    config = {
        "tools": [query_database],
        "system_instruction": system_instructions,
    }

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    response = client.models.generate_content(
        model=os.getenv("MODEL_ID"),
        config=config,
        contents=[
            "Spec Sheet",
            types.Part.from_bytes(data=doc_data,mime_type='application/pdf'),
            input.text
        ]
    )
    print(response.text)

    answer = {"answer": response.text, "queries": []}
    for function in response.automatic_function_calling_history:
        if function.role == "model":
            for part in function.parts:
                if "function_call" in part.model_fields_set:
                    if "args" in part.function_call.model_fields_set:
                        answer["queries"].append(part.function_call.args.get("query"))
    return answer
