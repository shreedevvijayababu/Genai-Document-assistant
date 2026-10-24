import streamlit as st
from app.core.config import SUPPORTED_FILE_TYPES
from app.agents.orchestrator import answer_question
from app.services import vector_store
from app.utils.guardrails import validate_question
from app.utils.helpers import ingest_uploads

st.set_page_config(page_title="Document Assistant", page_icon="📄", layout="centered")
st.title("Document Assistant")
st.caption("Upload documents, then ask questions. Answers are grounded in your files.")

uploaded = st.file_uploader("Upload documents", type=SUPPORTED_FILE_TYPES, accept_multiple_files=True)

col1, col2 = st.columns(2)
if col1.button("Index documents") and uploaded:
    with st.spinner("Reading and indexing..."):
        done, errors = ingest_uploads(uploaded)
    for d in done:
        st.success(f"Indexed {d}")
    for e in errors:
        st.error(e)
if col2.button("Clear knowledge base"):
    vector_store.reset()
    st.info("Knowledge base cleared.")

st.divider()
question = st.text_input("Ask a question about your documents:")
if st.button("Ask", type="primary"):
    ok, msg = validate_question(question)
    if not ok:
        st.warning(msg)
    else:
        try:
            with st.spinner("Agents are working..."):
                result = answer_question(question)
            st.markdown(result["answer"])
            if result["sources"]:
                st.caption("Sources: " + ", ".join(result["sources"]))
            st.caption("Validator: " + ("answer supported by documents" if result["validated"] else "not verified"))
            with st.expander("Agent trace"):
                st.write(f"Planner search query: {result['query']}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
