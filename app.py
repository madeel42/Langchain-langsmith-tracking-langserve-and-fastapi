from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv
from streamlit.errors import StreamlitSecretNotFoundError

load_dotenv()

try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except (StreamlitSecretNotFoundError, KeyError, TypeError):
    openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error(
        "Missing OPENAI_API_KEY. Set it in a .env file or in Streamlit secrets."
    )
    st.stop()

os.environ["OPENAI_API_KEY"] = openai_api_key

## langsmith tracking (optional)
try:
    langchain_api_key = st.secrets["LANGCHAIN_API_KEY"]
except (StreamlitSecretNotFoundError, KeyError, TypeError):
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

## prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer the user's question."),
        ("human", "Question: {question}"),
    ]
)

## streamlit framework
st.title("Langchain demo with openai Api")
input_text = st.text_input("Search the topic u want")

##open ai llm

llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()
chain= prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))
