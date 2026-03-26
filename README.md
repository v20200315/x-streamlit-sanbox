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
    db.py           # SQLite helpers (ingest rows)
    llm_graph.py    # LangGraph workflow that calls ChatGPT
  pages/
    01_Chat.py
    02_Data_Collector.py
  main.py           # Streamlit entrypoint (multipage home)
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

Use the sidebar to navigate between pages:

- **Chat**: talk to ChatGPT through the LangGraph backend.
- **Data collector**: upload an Excel file, preview rows, and save all rows into SQLite.

---

## Data collector (Excel → SQLite)

- **Upload**: `.xlsx` / `.xls`
- **Preview**: shows the first N rows (configurable in the sidebar)
- **Save**: inserts *all* rows into SQLite as raw JSON per row (no LLM transform)
- **Result UI**: shows a modal dialog on success/failure; after success you can click **Upload another Excel file** to reset the uploader and ingest a new file

### SQLite database location

- Default DB path is `data/app.db` (you can change it in the sidebar).
- Table name: `ingested_rows`

Schema:

- `id` INTEGER PRIMARY KEY
- `source_filename` TEXT NOT NULL
- `sheet_name` TEXT NULL
- `row_index` INTEGER NOT NULL
- `row_hash` TEXT NOT NULL (SHA-256 of canonical row JSON; used for dedupe)
- `row_json` TEXT NOT NULL
- `uploaded_at` TEXT NOT NULL (UTC ISO timestamp)

Deduplication:

- Inserts use `INSERT OR IGNORE` with a unique index on `(source_filename, sheet_name, row_hash)` to avoid duplicate rows when re-uploading the same content.

### Git ignore note

The default database directory `data/` (and `*.db` files) are ignored by git via `.gitignore`, so you won’t accidentally commit local SQLite data.

---

## Notes

- The backend logic for the LLM lives in `app/llm_graph.py`.
- Environment and model configuration live in `app/config.py`.
- You can add more nodes and tools to the graph to create richer workflows (retrieval, tools, multi-step reasoning, etc.).
