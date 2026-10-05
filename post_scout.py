from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    store=False,
    tools=[{"type": "web_search"}],

    input="""
Search the web specifically for recent PUBLIC LINKEDIN POSTS
from people or companies discussing hiring in Israel.

I am interested in opportunities related to:
- Business Development
- Business Operations / BizOps
- Corporate Banking
- Finance
- Strategy
- Corporate Development
- roles close to senior management or important business decision-makers

Look for posts such as:
- "We're hiring"
- "I'm hiring"
- "Join our team"
- "Looking for..."
- announcements that a team is growing
- managers personally advertising an opening
- posts describing an interesting opportunity even if the exact job title
  is unusual

Focus on early-career opportunities and reasonable stretch opportunities.

Do NOT return normal LinkedIn Jobs pages.
I specifically want LinkedIn POSTS.

For each result return:

PERSON:
COMPANY:
POST DATE:
WHAT THEY ARE HIRING FOR:
WHY IT MAY BE INTERESTING:
POST URL:

Only return posts you actually found.
Never invent a post, person, company, date, or URL.

Return up to 10 results.
"""
)

print(response.output_text)