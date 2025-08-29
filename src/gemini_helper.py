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



def analyze_resume(job_description: str, resume_text: str):
    prompt = f"""
    Analyze the following resume against the provided job description. Evaluate the resume's strengths and weaknesses in the context of the role's requirements.
    Provide the analysis in JSON format with these fields:
    - matchScore (integer 0-100)
    - summary (string)
    - strengths (array of strings)
    - improvements (array of strings)

    Job Description:
    ---
    {job_description}
    ---

    Resume Text:
    ---
    {resume_text}
    ---
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text



