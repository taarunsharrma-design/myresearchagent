import os
from dotenv import load_dotenv # To load the environmnetal variable from dotenv file
load_dotenv()
#API Keys

SERPER_API_KEY=os.getenv("SERPER_API_KEY")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
#AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
#AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

#Model settings
FACT_CHECK_MODEL="gpt-4o-mini"
PRIMARY_MODEL="gpt-4o-mini"
#SUMMARIZATION_MODEL=""

# workflow settings
CONFIDENCE_THRESHOLD=0.8
MAX_RETRIES=2
ADD_MAX_RESULT=2

if not SERPER_API_KEY:
    raise ValueError("Set up SERPER_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Set up OPENAI_API_KEY")

