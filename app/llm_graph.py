from typing import List, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from app.config import openai_config


class ChatState(TypedDict):
    messages: List[BaseMessage]


def get_llm() -> ChatOpenAI:
    # Uses ChatGPT via OpenAI
    return ChatOpenAI(
        model=openai_config.model,
        api_key=openai_config.api_key,
        temperature=0.2,
    )


def llm_node(state: ChatState) -> ChatState:
    """Single graph node that calls ChatGPT with the chat history."""
    llm = get_llm()
    response = llm.invoke(state['messages'])
    # Append the AI's reply to the message list
    return {'messages': state['messages'] + [response]}


def build_graph():
    """Compile and return a simple single-node chat graph."""
    graph = StateGraph(ChatState)

    graph.add_node('chatgpt', llm_node)
    graph.set_entry_point('chatgpt')
    graph.add_edge('chatgpt', END)

    return graph.compile()
