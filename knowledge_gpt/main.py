import streamlit as st

from knowledge_gpt.components.sidebar import sidebar

from knowledge_gpt.ui import (
    wrap_doc_in_html,
    is_query_valid,
    is_file_valid,
    is_open_ai_key_valid,
    display_file_read_error,
)

from knowledge_gpt.core.caching import bootstrap_caching

from knowledge_gpt.core.parsing import read_file
from knowledge_gpt.core.chunking import chunk_file
from knowledge_gpt.core.embedding import embed_files
from knowledge_gpt.core.qa import query_folder
from knowledge_gpt.core.utils import get_llm
from io import BytesIO
from hashlib import md5



EMBEDDING = "openai"
VECTOR_STORE = "faiss"
MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]

# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="Vink GPT", page_icon="🍕", layout="wide")
st.header("🍕Vink GPT")

# Enable caching for expensive functions
bootstrap_caching()

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")


if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )



# Path to your specific file
#article_path = '/Users/dejvid/fromGit/knowledge_gpt/knowledge_gpt/core/oslo_top_50.txt'  
article_path = '/mount/src/knowledge_gpt/knowledge_gpt/core/oslo_top_50.txt' # Update the path as needed


# Load the specific file
with open(article_path, 'rb') as file:
    file_content = file.read()

# Create a BytesIO object from the file content
bytes_data = BytesIO(file_content)

# Mock-up file object
class MockUploadedFile:
    def __init__(self, name, bytes_data):
        self.name = name
        self.bytes_data = bytes_data
        self.size = len(bytes_data.getvalue())  # Size might be required for some operations

    def read(self):
        # Reset the pointer to the beginning of the file each time before reading
        self.bytes_data.seek(0)
        return self.bytes_data.read()

    def close(self):
        self.bytes_data.close()

    def getvalue(self):
        # For methods that might use getvalue instead of read
        return self.bytes_data.getvalue()

    def seek(self, offset, whence=0):
        # This might be required if your process seeks within the file
        self.bytes_data.seek(offset, whence)

    @property
    def closed(self):
        # This property might be checked by some functions
        return self.bytes_data.closed


# Instantiate the mock-up file object
uploaded_file = MockUploadedFile('oslo_top_50.txt', bytes_data)

# Use the `uploaded_file` in the same way as if it was returned by `st.file_uploader`
try:
    # Ensure that read_file expects a file object with a 'name' attribute
    file = read_file(uploaded_file)
    # ...
except Exception as e:
    display_file_read_error(e, file_name=uploaded_file.name)
    st.stop()


model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

with st.expander("Advanced Options"):
    return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = st.checkbox("Show parsed contents of the document")


if not uploaded_file:
    st.stop()

try:
    file = read_file(uploaded_file)
except Exception as e:
    display_file_read_error(e, file_name=uploaded_file.name)

chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)

if not is_file_valid(file):
    st.stop()


if not is_open_ai_key_valid(openai_api_key, model):
    st.stop()


with st.spinner("Indexing document... This may take a while⏳"):
    folder_index = embed_files(
        files=[chunked_file],
        embedding=EMBEDDING if model != "debug" else "debug",
        vector_store=VECTOR_STORE if model != "debug" else "debug",
        openai_api_key=openai_api_key,
    )

with st.form(key="qa_form"):
    query = st.text_area("In English, ask a question about the [Vink Article](https://vink.aftenposten.no/artikkel/onOkVa/her-er-oslos-hotteste-restauranter-akkurat-na) on the hottest restaurants in Oslo right now")
    submit = st.form_submit_button("Submit")


if show_full_doc:
    with st.expander("Document"):
        # Hack to get around st.markdown rendering LaTeX
        st.markdown(f"<p>{wrap_doc_in_html(file.docs)}</p>", unsafe_allow_html=True)


if submit:
    if not is_query_valid(query):
        st.stop()

    # Output Columns
    answer_col, sources_col = st.columns(2)

    llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)
    result = query_folder(
        folder_index=folder_index,
        query=query,
        return_all=return_all_chunks,
        llm=llm,
    )

    with answer_col:
        st.markdown("#### Answer")
        st.markdown(result.answer)

    with sources_col:
        st.markdown("#### Sources")
        for source in result.sources:
            st.markdown(source.page_content)
            st.markdown(source.metadata["source"])
            st.markdown("---")
