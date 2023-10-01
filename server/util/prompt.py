import json
from textwrap import dedent
from typing import Optional

def get_initial_prompt(resume: str, job_description: str, salary_min: Optional[int] = None, salary_max: Optional[int] = None):
    """
    intitialize the session.
    """
    metadata_template = {
        "candidate_name": "string",
        "job_title": "string",
        "job_description_summary": "string (just one sentence)",
        "candidate_description_summary": "string (just one sentence)",
        "minimum_posted_salary": "integer",
        "maximum_posted_salary": "integer"
    }

    prompt = dedent(f"""
        You are going to act as a recruiter for an employer who's discussing an offer with a candidate. At this point, the candidate has already been given an initial job offer. You will be professional and courteous, yet conversational as this interaction is verbal. This should be as realistic as possible.

        Candidate information:
        ```
        {sanitize(resume)}
        ```

        job_description
        ```
        {sanitize(job_description)}
        ```

    """)

    if salary_min:
        prompt += f"Disregard any salary in the job post and use the value for minimum published salary: ${salary_min}\n"

    if salary_max:
        prompt += f"Disregard any salary in the job post and use the value for maximum published salary: ${salary_max}\n"

    prompt += dedent(f"""
        Before we begin, please output some metadata about the conversation in JSON. This should be the structure of your next response. if no salary range was given, you should estimate a realistic salary range.
        ```
        {json.dumps(metadata_template)}
        ```
    """)
    return prompt

def sanitize(text):
    return text.replace("```", "")


if __name__ == '__main__':
    from scrape import parse_doc
    candidate = parse_doc("https://s3.amazonaws.com/nicbor.com/sample_resume.html")
    jd = parse_doc("https://s3.amazonaws.com/nicbor.com/sample_job_description.html")
    print(get_initial_prompt(candidate, jd, 100000, 200000))
