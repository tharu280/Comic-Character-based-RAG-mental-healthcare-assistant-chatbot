import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


try:
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    print(f"Failed to load embedding model: {e}")
    exit(1)


def create_vectorstore(path, persist_path):
    if not os.path.exists(path):
        print(f" File not found: {path}")
        return

    try:
        print(f"{path}...")
        loader = TextLoader(path)
        docs = loader.load()
        if not docs:
            print(f" No documents found in {path}")
            return
    except Exception as e:
        print(f" Failed to load documents from {path}: {e}")
        return

    try:

        if "iroh_quotes" in path:
            print(" Using custom splitter for Iroh quotes")
            from langchain.text_splitter import CharacterTextSplitter
            splitter = CharacterTextSplitter(
                separator="\n\n", chunk_size=300, chunk_overlap=0
            )
        else:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=200, chunk_overlap=50
            )

        chunks = splitter.split_documents(docs)
        if not chunks:
            print(f" No chunks created for {path}")
            return
    except Exception as e:
        print(f" Failed to split documents from {path}: {e}")
        return

    try:
        print(f" Creating Vector DB for {path}...")
        vectordb = FAISS.from_documents(chunks, embedding_model)
        vectordb.save_local(persist_path)
        print(f"Vector DB saved to {persist_path}\n")
    except Exception as e:
        print(f" Failed to create or save vector DB for {path}: {e}")


create_vectorstore("iroh_quotes.txt", "vdbs/iroh")
create_vectorstore("mental_health_tips.txt", "vdbs/mental")
create_vectorstore("philosophy.txt", "vdbs/philosophy")
