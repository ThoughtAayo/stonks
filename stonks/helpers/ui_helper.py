import os

import streamlit as st
from tempfile import NamedTemporaryFile
from helpers import pdf_helper, vector_db_helper

def upload_docs():
    uploaded_file = st.file_uploader(
        "upload PDFs", accept_multiple_files=False, type=["pdf"])
    if uploaded_file is not None:
        fup(uploaded_file)

@st.cache_resource
def getDbClient():
    return vector_db_helper.VectorDbHelper(persist_to_disk=True)


@st.cache_data(show_spinner=False, experimental_allow_widgets=True)
def fup(uploaded_file):
    # st doesn't give path of the file and hence the following workaround using temp file
    tempFilePath = "./tempFiles"
    with NamedTemporaryFile(dir=tempFilePath, suffix=".pdf", delete=False) as f:
        f.write(uploaded_file.read())
        with st.spinner(text="Extracting text from Pdf..."):
            # extract text from pdf
            pdf_text_content_list = pdf_helper.extract_content_from_url(os.path.join(tempFilePath,f.name))      
            with st.expander("See extracted text"):       
                st.code("\n".join(pdf_text_content_list))
            
            # generate embeddings and save to vector db
            with st.spinner(text="Generating Embeddings and saving to disk..."):
                vectorDb = getDbClient()
                vectorDb.generate_embeddings_and_save_to_db(pdf_text_content_list)

def chat_with_vector_store():
    st.title("Vector Db Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Write query here"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # get nearest embeddings from vector store using similarity search
        vectorDb = vector_db_helper.VectorDbHelper()
        vdb_response = vectorDb.dbStore().similarity_search(prompt)
        response = f"Vector Db: {vdb_response[0].page_content}"
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


def init():
    """"""
    st.set_page_config(page_title="ठटायो Stonks ", page_icon=":bird:")
    st.header("ठटायो Stonks :bird:")
    upload_docs()
    chat_with_vector_store()