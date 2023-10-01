import json
from textwrap import dedent
from typing import Optional


def get_initial_prompt(
    resume: str,
    job_description: str,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
):
    """
    intitialize the session.
    """
    metadata_template = {
        "candidate_name": "string",
        "recruiter_name": "string (invent a realistic recruiter name)",
        "company_name": "string",
        "job_title": "string",
        "job_description_summary": "string (just one sentence)",
        "candidate_description_summary": "string (just one sentence)",
        "minimum_posted_salary": "integer",
        "maximum_posted_salary": "integer",
        "match_score": "float (a number from 0 to 1, indicating the general level of qualification of the candidate with respect to the role. 0 is unqualified, 1 is the best possible candidate who's overqualified. 0.5 is satisfactory meeting all minimum requirements.)",
        "initial_offer_email": "string (this is the brief plaintext email the candidate received prior to this conversation, giving them an initial job offer including the position and an appropriate starting salary consistent with the match_score)",
    }

    prompt = dedent(
        f"""
        You are going to simulate a conversation as a recruiter from a company discussing an offer with a candidate. This is not an interview, it is a salary negotiation. This interaction is verbal and should be realistic, professional, courteous, yet conversational. You should NOT return any templated text (such as [name]) in the "message" from this point forward.

        Candidate information:
        ```
        {sanitize(resume)}
        ```

        job_description
        ```
        {sanitize(job_description)}
        ```

    """
    )

    if salary_min:
        prompt += f"Disregard any salary in the job post and use the value for minimum published salary: ${salary_min}\n"

    if salary_max:
        prompt += f"Disregard any salary in the job post and use the value for maximum published salary: ${salary_max}\n"

    prompt += dedent(
        f"""
        Before we begin, please output some metadata about the conversation in JSON. This should be the structure of your next response. if no salary range was given, you should estimate a realistic salary range.
        ```
        {json.dumps(metadata_template)}
        ```
    """
    )
    return prompt


def get_second_prompt():
    prompt = """Great. Now welcome your candidate and begin the conversation. From this point forward, all your responses should be JSON formatted to match the template `{"message": "string"}`. When the conversation is over and it's time to hang up, you can add a field to your response `{"message": "string", "event": "interview_finished"}`. Remember to be professional and courteous, but realistically conversational."""
    return prompt


def sanitize(text):
    return text.replace("```", "")


def get_final_prompt():
    prompt = """The interview is now complete. Based on the above conversation history, please provide a detailed summary and feedback focusing on the user's behavior and performance in this mock salary negotiation. Evaluate the clarity and effectiveness of communication, justification for the desired salary, handling of objections, and overall negotiation strategy. Additionally, provide constructive feedback on areas of improvement and recommend strategies or resources to enhance negotiation skills."""
    return prompt


if __name__ == "__main__":
    from scrape import parse_url

    candidate = parse_url("https://s3.amazonaws.com/nicbor.com/sample_resume.html")
    jd = parse_url("https://s3.amazonaws.com/nicbor.com/sample_job_description.html")
    print(get_initial_prompt(candidate, jd, 100000, 200000))
    print(get_second_prompt())
    print(get_final_prompt())
