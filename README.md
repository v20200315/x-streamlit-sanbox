## x-streamlit-sanbox

**A simple Streamlit frontend powered by LangChain + LangGraph and ChatGPT (OpenAI) as the LLM.**

This project demonstrates how to:

- **Use Streamlit** as a chat-style UI
- **Build an LLM workflow** with LangChain + LangGraph
- **Call ChatGPT** (via OpenAI) as the backend model

---

## Requirements

- **Python**: 3.12+ (project is configured for this)
- **uv**: for dependency management and running the app
- An **OpenAI API key** with access to your chosen ChatGPT model

---

## Installation

From the project root:

```bash
uv sync
```

This installs all dependencies defined in `pyproject.toml`.

---

## Configuration

Create a `.env` file in the project root (this file is ignored by git):

```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini
```

- **OPENAI_API_KEY**: your secret key from OpenAI
- **OPENAI_MODEL**: optional; defaults to `gpt-4.1-mini` if omitted

You can change the model later (for example, `gpt-4.1`, `gpt-4o-mini`, etc.).

---

## Project structure

```text
x-streamlit-sanbox/
  app/
    __init__.py
    config.py       # loads env vars and OpenAI config
    llm_graph.py    # LangGraph workflow that calls ChatGPT
  main.py           # Streamlit entrypoint (chat UI)
  .env              # local secrets (not committed)
  .gitignore
  pyproject.toml
  uv.lock
  README.md
```

---

## Running the app

From the project root:

```bash
uv run streamlit run main.py
```

Then open the URL printed in the terminal (typically `http://localhost:8501`).

You should see a chat interface where you can talk to ChatGPT through the LangGraph backend.

---

## Notes

- The backend logic for the LLM lives in `app/llm_graph.py`.
- Environment and model configuration live in `app/config.py`.
- You can add more nodes and tools to the graph to create richer workflows (retrieval, tools, multi-step reasoning, etc.).
