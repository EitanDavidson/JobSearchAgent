from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

from agents.job_scout import find_jobs
from database.job_database import setup_database, job_exists, save_job

load_dotenv()
client = OpenAI()
setup_database()

# Read candidate information
career_profile = Path(
    "config/career_profile.md"
).read_text(encoding="utf-8")

candidate_profile = Path(
    "config/candidate_profile.md"
).read_text(encoding="utf-8")


def evaluate_job(job):

    response = client.responses.create(
        model="gpt-5.6-luna",
        store=False,
            tools=[{"type": "web_search"}],

        input=f"""
You are evaluating a job opportunity for a candidate.

CAREER GOALS:
{career_profile}

CANDIDATE FACTS:
{candidate_profile}

JOB POSTING:
Company: {job["company"]}
Position: {job["position"]}
Location: {job["location"]}
URL: {job["url"]}

{job["job_description"]}

RULES:
1. Use only information contained above.
2. Never invent candidate experience, job responsibilities, or company facts.
3. If information is unavailable, write "Unknown".
4. Missing experience is not automatically a reason to reject a job.
5. Stretch opportunities should be considered when they offer strong career value.
6. Distinguish career attractiveness from current qualification fit.
7. Do not infer responsibilities that are not stated.

COMPANY EVALUATION:
Use web search to briefly research the employer.

Evaluate the company as a career platform based on:
- Scale, reputation, and position in its industry
- Quality of business exposure and network
- Learning and future career opportunities
- Whether it is a strong established platform OR an attractive smaller
  company that may provide unusually high responsibility and growth

Do not automatically prefer a large company over a smaller company.

When evaluating COMPANY PLATFORM, evaluate the actual employer,
not the job board, recruiter, staffing agency, or website where the
job was found.

If the actual employer cannot be identified, write:
COMPANY PLATFORM: Unknown

CAREER FIT EVALUATION:

When calculating CAREER FIT, consider four major dimensions:

1. Professional Skills
Concrete, transferable skills such as financial analysis, modeling,
credit analysis, commercial analysis, negotiation, or other valuable
professional capabilities.

2. Business Exposure
Exposure to companies, customers, markets, business models,
commercial decisions, and how businesses actually operate.

3. Ownership & Breadth
Responsibility for meaningful outcomes and initiatives.
Prefer roles with broad responsibility over roles limited mainly to
narrow analysis, repetitive tasks, coordination, or support.

4. Decision-Maker Proximity
Meaningful exposure to senior executives, important decisions,
and the reasoning behind those decisions.

The ideal role combines several of these dimensions.

Do NOT give a very high Career Fit score simply because a role develops
excellent technical skills if the role is narrow, has little ownership,
or offers little exposure to important decision-making.

Likewise, do NOT give a very high Career Fit score simply because a role
offers executive exposure if it mainly consists of coordination and
project management without developing concrete professional skills.

Return:

CAREER FIT: X/100

QUALIFICATION FIT: X/100

COMPANY PLATFORM: X/100

Explain in 1-2 bullets why this company is or is not a strong platform
for the candidate's future career.

PROFESSIONAL SKILL RISK: Low / Medium / High

Assess the risk that the candidate could spend 1-2 years in this role
gaining exposure and coordination experience but leave without strong,
concrete professional skills.

DECISION: Apply / Consider / Skip

WHY:
- Maximum 3 short bullets.

GAPS:
- Only important gaps or mandatory requirements not met.

Keep the evaluation concise.
"""
    )

    return response.output_text


print("Searching for jobs...\n")

jobs = find_jobs()

print(f"Found {len(jobs)} jobs.")
print("Evaluating jobs...\n")

report = []

new_jobs = [job for job in jobs if not job_exists(job["url"])]

print(f"{len(new_jobs)} new jobs to evaluate.\n")

for number, job in enumerate(new_jobs[:10], start=1):

    print(
        f"Evaluating {number}/{min(len(new_jobs), 10)}: "
        f"{job['company']} - {job['position']}"
    )

    evaluation = evaluate_job(job)

    report.append(
        f"""
============================================================
{number}. {job['company']} - {job['position']}
Location: {job['location']}
URL: {job['url']}
============================================================

{evaluation}
"""
    )

    save_job(
        job,
        datetime.now().strftime("%Y-%m-%d")
    )

# Create report file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
report_path = Path("reports") / f"job_report_{timestamp}.txt"

report_path.write_text(
    "\n".join(report),
    encoding="utf-8"
)

print("\nDone!")
print(f"Report saved to: {report_path}")