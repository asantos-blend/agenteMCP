import os
from dotenv import load_dotenv
from langchain_aws import ChatBedrock

load_dotenv()

def get_llm():
    return ChatBedrock(
        model_id=os.getenv("BEDROCK_MODEL_ID"),
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        model_kwargs={
            "max_tokens": 512,
            "temperature": 0
        }
    )
