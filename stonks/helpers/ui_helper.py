import os
import pathlib
import json

from tempfile import NamedTemporaryFile
import streamlit as st
from helpers import pdf_helper, vector_db_helper


def upload_docs():
    uploaded_file = st.file_uploader(
        "upload PDFs", accept_multiple_files=False, type=["pdf"]
    )
    if uploaded_file is not None:
        fup(uploaded_file)


@st.cache_resource(show_spinner=False)
def getDbClient():
    return vector_db_helper.VectorDbHelper(persist_to_disk=True)


def getTemporaryStoragePath():
    temp_file_path = os.path.join(os.getcwd(), "stonks/storage/tempFiles")
    pathlib.Path(temp_file_path).mkdir(parents=True, exist_ok=True)
    return temp_file_path


@st.cache_data(experimental_allow_widgets=True, show_spinner=False)
def fup(uploaded_file):
    # st doesn't give path of the file and hence the following workaround using temp file
    temp_file_path = getTemporaryStoragePath()

    with NamedTemporaryFile(dir=temp_file_path, suffix=".pdf", delete=False) as f:
        f.write(uploaded_file.read())

        with st.spinner(text="Extracting text from Pdf..."):
            # extract text from pdf
            pdf_text_content_list = pdf_helper.extract_content_from_url(
                os.path.join(temp_file_path, f.name)
            )

            with st.expander("See extracted text"):
                st.code("\n".join(pdf_text_content_list))

            # generate embeddings and save to vector db
            with st.spinner(text="Generating Embeddings and saving to disk..."):
                vectorDb = getDbClient()
                vectorDb.generate_embeddings_and_save_to_db(pdf_text_content_list)


def chat_with_vector_store(show_chat_history: bool):
    """"""
    st.title("Vector Db Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if show_chat_history:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.code(message["content"])

    # React to user input
    if prompt := st.chat_input("Write query here"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # get nearest embeddings from vector store using similarity search
        vectorDb = vector_db_helper.VectorDbHelper()
        vdb_response = vectorDb.dbStore().similarity_search_with_score(prompt, k=3)

        # convert to json for readability
        response = (
            json.dumps(vdb_response, cls=CustomEncoder, indent=4)
            .replace("\\n\\n", "\\\n")
            .replace("\\", "")
        )

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.code(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


def init(title="ठटायो  🤔💸 🤕", show_chat_history=True):
    """"""
    st.set_page_config(page_title=title, page_icon="💸")
    st.header("ठटायो  🤔💸 🤕")
    upload_docs()
    chat_with_vector_store(show_chat_history)


class CustomEncoder(json.JSONEncoder):
    """"""

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)
