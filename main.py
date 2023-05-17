from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.vectorstores import Chroma
from embed import Embedder
from langchain.embeddings.openai import OpenAIEmbeddings

import os
from os import listdir
from os.path import isfile, join
from langchain.chains.question_answering import load_qa_chain

os.environ['OPENAI_API_KEY'] = "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"

# Embed Docs
embedder = Embedder()
embedder.embed_all_docs()
db = embedder.get_vectorstore()

def single_query(query='What are some milestone model architectures and papers in the last few years?'):
    relevant_docs = db.similarity_search(query, 5)
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    return chain({"input_documents": relevant_docs, "question": query})




