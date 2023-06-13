import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import MarkdownTextSplitter
from langchain.document_loaders import PyPDFLoader
from MyMDTextSplitter import MyMDTextSplitter
from os import listdir
from os.path import isfile, join
from methodtools import lru_cache

from langchain.embeddings import HuggingFaceHubEmbeddings

class Embedder:
    def __init__(self,
                 persist_directory='hfembeddb',
                 key="",
                 model="text-embedding-ada-002"):
        os.environ['OPENAI_API_KEY'] = "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"
        os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
        # self.embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.embeddings = HuggingFaceHubEmbeddings(
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
        
        # self.embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.vectordb = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
        self.md_splitter = MarkdownTextSplitter()

    def get_vectorstore(self):
        return self.vectordb

    def create_docs(self, file):
        with open(file) as f:
            text = f.read()
        return self.md_splitter.create_documents(texts=[text],metadatas=[{'file':file.split('/')[-1].split('.')[0]}])
        #return UnstructuredMarkdownLoader(file, mode="elements").load()

    def create_pdf_docs(self, pdf_path):
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        return pages

    def embed_doc(self, docs):
        self.vectordb.add_documents(docs)

    def embed_pdf_doc(self, docs):
        self.vectordb.from_documents(docs,embedding=self.embeddings)

    def embed_all_docs(self, path='data/use'):
        data_files = [join(path,f) for f in listdir(path) if isfile(join(path, f))]
        for f in data_files:
            if f.split('.')[-1] == 'md':
                self.embed_doc(self.create_docs(f))
            else:
                if f.split('.')[-1] == 'pdf':
                    self.embed_pdf_doc(self.create_pdf_docs(f))
        self.vectordb.persist()

if __name__ == "__main__":
    e = Embedder()
    e.embed_all_docs()

