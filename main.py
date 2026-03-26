import streamlit as st


def main():
    st.set_page_config(page_title='Streamlit LLM Sandbox', page_icon='💬')
    st.title('Streamlit LLM Sandbox')

    st.markdown(
        """
This app uses Streamlit **multipage** navigation.

- **Chat**: talk to ChatGPT via LangChain + LangGraph
- **Data collector**: upload an Excel file, preview it, and save all rows into SQLite
"""
    )

    st.info('Use the sidebar to open a page under “Pages”.')


if __name__ == '__main__':
    main()
