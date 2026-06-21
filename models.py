from typing import Optional , Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict) :
    query : str
    rewritten_query : Optional[str]
    chat_history : Annotated[str,add_messages]
    content : Optional[list[str]]
    response : Optional[str]