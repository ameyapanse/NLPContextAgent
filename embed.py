import os
from langchain.vectorstores import Chroma
from langchain.text_splitter import MarkdownTextSplitter
from langchain.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader
from os import listdir
from os.path import isdir, isfile, join

from langchain.embeddings import HuggingFaceHubEmbeddings


def create_pdf_docs(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return pages


def create_md_docs(md_path, use_splitter=False):
    if use_splitter:
        return create_md_docs_splitter(md_path)
    return create_md_docs_loader(md_path)


def create_md_docs_loader(md_path):
    loader = UnstructuredMarkdownLoader(md_path, mode='elements')
    pages = loader.load_and_split()
    return pages


def create_md_docs_splitter(md_path):
    splitter = MarkdownTextSplitter()
    with open(md_path) as f:
        text = f.read()
    metadata = {
        'source': md_path.split('/')[-1]
    }
    return splitter.create_documents(texts=[text], metadatas=[metadata])


class Embedder:
    def __init__(self,
                 persist_directory='chroma_databases/db_all'):
        self.dir = persist_directory
        self.embeddings = HuggingFaceHubEmbeddings(
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
        )
        self.vectordb = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
        self.md_splitter = MarkdownTextSplitter()

    def get_vectorstore(self):
        return self.vectordb

    def embed_doc(self, docs):
        self.vectordb.add_documents(docs)
        self.vectordb.persist()

    def embed_docs_in_directory(self, path):
        data_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        for f in data_files:
            print(f)
            file_type = f.split('.')[-1]
            if file_type == 'md':
                create_docs = create_md_docs
            else:
                if file_type == 'pdf':
                    create_docs = create_pdf_docs
                else:
                    continue
            self.embed_doc(create_docs(f))

    def embed_all_documents(self, courses=None):
        if courses is None:
            courses = ['cs231n', 'cs234', 'cs324']
        for course in courses:
            self.embed_docs_in_directory(join('data', course))

if __name__ == "__main__":
    # Test md docs
    md_docs = create_md_docs('data/cs324/introduction.md')
    assert md_docs[0].metadata.get('source', '') == 'data/cs324/introduction.md'

    # Test pdf docs
    pdf_docs = create_pdf_docs('data/cs234/lecture01.pdf')
    assert pdf_docs[0].metadata.get('source', '') == 'data/cs234/lecture01.pdf'

    # Run Embedder
    from configs import set_keys
    set_keys()
    e = Embedder()
    e.embed_all_documents()

    e_cs231n = Embedder('chroma_databases/db_cs231n')
    e_cs231n.embed_all_documents(['cs231n'])

    e_cs234 = Embedder('chroma_databases/db_cs234')
    e_cs234.embed_all_documents(['cs234'])

    e_cs324 = Embedder('chroma_databases/db_cs324')
    e_cs324.embed_all_documents(['cs324'])
