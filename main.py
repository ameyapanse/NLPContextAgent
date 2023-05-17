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



from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.agents import initialize_agent

def conversation(q1,q2):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), db.as_retriever(), memory=memory)
    print(conversation_chain({'question': q1})['answer'])
    print(conversation_chain({'question': q2})['answer'])


if __name__ == '__main__':
    ret = []
    for q in ['What are some milestone model architectures and papers in the last few years?',
              "What are the layers in a transformer block?",
              "Tell me about datasets used to train LLMs and how they’re cleaned"]:
        ret.append(single_query(q))
    print(ret)
    print('---Conversation agent---')
    q1 = "What are some milestone model architectures and papers in the last few years?"
    q2 = 'Are there any published by NVIDIA?'
    conversation(q1,q2)