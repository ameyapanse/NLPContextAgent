# Contextualized Conversational Agent


## Instructions:
- Install langchain, chromadb, pypdf
- Run python main.py

## Solution Overview

## Capabilities
- Embedding over all the lectures and table
- Able to give contextual answers, has conversational memory
- Gives out references, but not 100%
- Generates summaries

### Base Architecture
- Get and save document embeddings from llm. Uses the HuggingFaceHub's GPT-2 as recommended by their documentation
- Pick top-k documents according to the similarity score w.r.t the query embeddings.
- Pass these docs as context along with the query to the model

### Conversational History
- Uses a conversation prompt
- Keep a history of previous messages. Summarize the history and add as context
- Chained the ConversationalSummaryMemoryBuffer, Similarity Retriver and Converastional Retrival fto achieve this 
- Tried the stuff, refine and map-reduce chains. Map reduce and refine require muliple calls to the llm.

### Conversation Summary
- Uses the message history and a custom summarization prompt to generate the summary
- Uses a seperate instance of SummarizerMixin object for summarization. Using the same instance for both querying and summarization worsened results on both.

### Source Citation
- Uses the retrived documents as references


## Data :
- Stanford LLMs Lecture Notes: https://stanford-cs324.github.io/winter2022/lectures/
- Stanford CNN Lecture Notes : https://cs231n.github.io/
- Stanford RL Lecture Notes  : https://github.com/tallamjr/stanford-cs234/tree/master/slides

