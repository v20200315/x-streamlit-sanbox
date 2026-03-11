import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from app.llm_graph import build_graph

# Build the graph once at startup
graph = build_graph()


def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []  # list[BaseMessage]


def render_chat_history():
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            role = 'user'
        elif isinstance(msg, AIMessage):
            role = 'assistant'
        else:
            role = 'assistant'  # fallback

        with st.chat_message(role):
            st.markdown(msg.content)


def main():
    st.set_page_config(page_title='ChatGPT + LangGraph Demo', page_icon='💬')
    st.title('ChatGPT + LangGraph + Streamlit')

    st.caption('Simple demo using LangChain/LangGraph as the backend.')

    init_session_state()
    render_chat_history()

    user_input = st.chat_input('Ask ChatGPT anything:')
    if user_input:
        # Add user message to history
        user_msg = HumanMessage(content=user_input)
        st.session_state.messages.append(user_msg)

        with st.chat_message('user'):
            st.markdown(user_input)

        # Call the graph
        result_state = graph.invoke({'messages': st.session_state.messages})
        st.session_state.messages = result_state['messages']

        # Last message should be ChatGPT's answer
        ai_msg = st.session_state.messages[-1]

        with st.chat_message('assistant'):
            st.markdown(ai_msg.content)


if __name__ == '__main__':
    main()
