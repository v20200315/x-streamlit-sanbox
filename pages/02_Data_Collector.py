import json
import os
from datetime import date, datetime
from typing import Any

import pandas as pd
import streamlit as st

from app.db import get_conn, init_db, insert_rows


def _jsonable(value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    # pandas / numpy types
    if isinstance(value, pd.Timestamp):
        if pd.isna(value):
            return None
        return value.to_pydatetime().isoformat()

    if hasattr(value, 'item'):
        try:
            return value.item()
        except Exception:
            pass

    return value


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    df = df.copy()
    df = df.where(pd.notnull(df), None)
    records: list[dict[str, Any]] = df.to_dict(orient='records')
    return [{k: _jsonable(v) for k, v in row.items()} for row in records]


@st.dialog('Save succeeded')
def _success_modal(*, inserted: int, db_path: str):
    st.success(f'Saved {inserted} rows.')
    st.code(db_path)
    if st.button('Upload another Excel file'):
        st.session_state['excel_uploader_nonce'] = (
            st.session_state.get('excel_uploader_nonce', 0) + 1
        )
        st.rerun()


@st.dialog('Save failed')
def _error_modal(*, error_message: str):
    st.error('Could not save rows to the database.')
    st.code(error_message)


def main():
    st.title('Data collector')
    st.caption('Upload an Excel file, preview rows, then save all rows into SQLite.')

    db_path = st.sidebar.text_input(
        'SQLite DB path', value=os.path.join('data', 'app.db')
    )
    preview_n = st.sidebar.number_input(
        'Preview rows', min_value=1, max_value=200, value=20
    )

    uploader_key = f'excel_uploader_{st.session_state.get("excel_uploader_nonce", 0)}'
    uploaded = st.file_uploader(
        'Upload an Excel file', type=['xlsx', 'xls'], key=uploader_key
    )
    if not uploaded:
        st.info('Upload an Excel file to preview and save its rows.')
        return

    try:
        xls = pd.ExcelFile(uploaded)
    except Exception as e:
        st.error(f'Failed to read Excel file: {e}')
        return

    sheet_name = None
    if len(xls.sheet_names) > 1:
        sheet_name = st.selectbox('Sheet', options=xls.sheet_names)
    else:
        sheet_name = xls.sheet_names[0]

    try:
        df = pd.read_excel(xls, sheet_name=sheet_name)
    except Exception as e:
        st.error(f'Failed to parse sheet: {e}')
        return

    st.write(
        {'rows': int(df.shape[0]), 'columns': int(df.shape[1]), 'sheet': sheet_name}
    )
    st.dataframe(df.head(int(preview_n)), width='stretch')

    if df.shape[0] == 0:
        st.warning('This sheet has no rows to save.')
        return

    if st.button('Save to DB', type='primary'):
        try:
            with st.spinner('Saving rows to SQLite...'):
                rows = dataframe_to_records(df)

                conn = get_conn(db_path)
                try:
                    init_db(conn)
                    inserted = insert_rows(
                        conn,
                        rows,
                        source_filename=getattr(uploaded, 'name', 'uploaded.xlsx'),
                        sheet_name=str(sheet_name) if sheet_name is not None else None,
                    )
                finally:
                    conn.close()

            _success_modal(inserted=inserted, db_path=db_path)
            with st.expander('Sample saved row JSON'):
                st.code(json.dumps(rows[0], ensure_ascii=False, indent=2))
        except Exception as e:
            _error_modal(error_message=str(e))


main()
