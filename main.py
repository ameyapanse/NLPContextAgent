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

os.environ['OPENAI_API_KEY'] = "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"

# Embed Docs
embedder = Embedder()
embedder.embed_all_docs()

