import os
from typing import Optional

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser
from langfuse.callback import CallbackHandler

from lib.env_vars import (
    LANGFUSE_HOST,
    LANGFUSE_PUBLIC_KEY,
    LANGFUSE_SECRET_KEY,
    OPENAI_API_KEY,
)

# from https://cloud.langfuse.com/
os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

langfuse_handler = CallbackHandler(
    secret_key=LANGFUSE_SECRET_KEY,
    public_key=LANGFUSE_PUBLIC_KEY,
    host=LANGFUSE_HOST,
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def run_llm(prompt: str, kwargs: Optional[dict] = None):
    prompt = ChatPromptTemplate.from_template(prompt)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke(kwargs, config={"callbacks": [langfuse_handler]})
