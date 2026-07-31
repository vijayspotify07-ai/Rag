import json

from groq import Groq

from app.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def score_candidate(

    job_description: str,

    resume_text: str

):

    prompt = f"""

You are an expert technical recruiter.

Compare the candidate resume with the job description.

Return ONLY valid JSON.

Use exactly this format:

{{
    "score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "explanation": ""
}}

Rules:

- score must be between 0 and 100
- matched_skills must be an array of strings
- missing_skills must be an array of strings
- explanation must be a string

JOB DESCRIPTION:

{job_description}

CANDIDATE RESUME:

{resume_text}

"""


    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            temperature=0

        )


        result = (

            response.choices[0]

            .message

            .content

        )


        result = result.strip()


        if result.startswith("```json"):

            result = result.replace(

                "```json",

                "",

                1

            )

            result = result.replace(

                "```",

                ""

            )

            result = result.strip()


        return json.loads(result)


    except Exception as error:

        raise Exception(

            f"Groq API error: {str(error)}"

        )