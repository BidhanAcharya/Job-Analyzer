from google import genai
import os
from model.base import KeywordsModel
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

## extract job keywords from resume summary
def job_keyword(prompt):
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            'response_schema': KeywordsModel
        }
    )
    return response.text

## summarize resume
def text_generator(prompt):
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text



