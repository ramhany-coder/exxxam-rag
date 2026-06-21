from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from prompts import *
from dotenv import load_dotenv
from models import *
load_dotenv()

embedder = HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

llm = ChatOpenAI(
    model=OLLAMA_MODEL,
    api_key="ollama",
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)

vbd_q = Chroma(
embedding_function=embedder,
persist_directory="python_q_emb"
)

def rewritter_agent (state:State) :
    query = state.get("query")
    hist = state.get("chat_history")

    messages = [
        SystemMessage(content=rewrite_system_prompt),
        HumanMessage(content=rewrite_human_prompt(query=query,conversation_history=hist))
    ]

    response = llm.invoke(messages)

    return {
        "rewritten_query" : response.text
    }

def retrival_agent (state:State) :
    query = state.get("rewritten_query")

    ret = vbd_q.as_retriever(kwargs=5)

    content = ret.invoke(query)

    return {
        "content": content
    }

def responser_agent(state:State):
    query = state.get("rewritten_query")
    content = state.get("content")

    messages = [
        SystemMessage(content=responser_system_prompt)
        , HumanMessage(content=responser_human_prompt(query=query,context=content))
    ]

    result = llm.invoke(messages)

    return{
        "response":result.text
    }