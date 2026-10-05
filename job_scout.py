from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()


def find_jobs():

    response = client.responses.create(
        model="gpt-5.6-luna",
        store=False,
        tools=[{"type": "web_search"}],

        input="""
Search the web for currently open jobs in Israel.

Focus on:
- Business Development
- Business Operations / BizOps
- Corporate Banking
- Strategic Finance
- Strategy

Prioritize LinkedIn, but also search company career pages and other
reputable job sources.

Include junior and early-career roles as well as attractive stretch roles.
A stretch role should be only moderately above the candidate's current level.

Exclude jobs with Senior, Sr., Lead, Head, Director, VP, or Vice President
in the title.

Exclude jobs that explicitly require fluency or native-level proficiency
in a language other than Hebrew or English.

Do not automatically exclude "Manager" roles. Include them only when the
experience requirements suggest they could realistically be an early-career
stretch opportunity.

Find up to 10 jobs.

IMPORTANT:
For every job, open the actual job posting.

Only include a job if you can retrieve enough information about BOTH:
1. The main responsibilities.
2. The main requirements / qualifications.

If you cannot retrieve both, exclude the job from the results.

Never evaluate relevance based only on the job title.
Do not invent missing information.

Return ONLY a JSON array in this exact structure:

[
  {
    "company": "Company name",
    "position": "Job title",
    "location": "Location",
    "url": "Direct URL",
    "job_description": "Responsibilities and requirements found in the posting"
  }
]
"""
    )

    text = response.output_text.strip()

    # Remove Markdown code fences if the model adds them
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]

    return json.loads(text)


if __name__ == "__main__":
    jobs = find_jobs()

    print(f"Found {len(jobs)} jobs.\n")

    for job in jobs:
        print(job["company"], "-", job["position"])