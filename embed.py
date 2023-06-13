import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import MarkdownTextSplitter
from MyMDTextSplitter import MyMDTextSplitter
from os import listdir
from os.path import isfile, join
from methodtools import lru_cache

class Embedder:
    def __init__(self,
                 persist_directory='db',
                 key="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",
                 model="text-embedding-ada-002"):
        self.embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.vectordb = Chroma(persist_directory=persist_directory, embedding_function=self.embedding)
        self.md_splitter = MarkdownTextSplitter()

    def get_vectorstore(self):
        return self.vectordb

    def create_docs(self, file):
        with open(file) as f:
            text = f.read()
        return self.md_splitter.create_documents(texts=[text],metadatas=[{'file':file.split('/')[-1].split('.')[0]}])
        #return UnstructuredMarkdownLoader(file, mode="elements").load()

    def embed_doc(self, docs):
        self.vectordb.add_documents(docs)

    def embed_all_docs(self, path='data/use'):
        data_files = [join(path,f) for f in listdir(path) if isfile(join(path, f))]
        for f in data_files:
            self.embed_doc(self.create_docs(f))
        self.vectordb.persist()

if __name__ == "__main__":
    e = Embedder()
    e.embed_all_docs()

