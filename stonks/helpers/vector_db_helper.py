from langchain.docstore.document import Document
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

import chromadb


class VectorDbHelper:
    """Helper class to generate and manage embeddings using Vector Db"""

    model_name = ""
    _persist_to_disk = False
    _persist_directory = ""
    _persistent_client = None
    _embedding_function = None

    def __init__(
        self,
        model="all-MiniLM-L6-v2",
        persist_directory="./chroma_db",
        persist_to_disk=False,
    ) -> None:
        """"""
        self.model_name = model
        self._persist_directory = persist_directory
        self._persist_to_disk = persist_to_disk
        self.init_client()

    def init_client(self) -> None:
        """"""
        self._embedding_function = SentenceTransformerEmbeddings(
            model_name=self.model_name
        )
        self.persistent_client = chromadb.PersistentClient()

    def generate_embeddings_and_save_to_db(
        self, contents: list
    ) -> Chroma:
        """"""
        docs = []
        for content in contents:
            docs.append(Document(page_content=content, metadata={"source": "local"}))  
        return Chroma.from_documents(docs, self._embedding_function, persist_directory=self._persist_directory)
    
    def dbStore(self) -> Chroma:
        """"""
        return Chroma(embedding_function = self._embedding_function, persist_directory=self._persist_directory)