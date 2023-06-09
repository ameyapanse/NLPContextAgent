# Contextualized Conversational Agent


## Instructions:
- Install langchain, chromadb, pypdf
- Make sure your keys are in keys/openai_api_key and keys/huggingfacehub_api_token
- Run python main.py


## Capabilities
- Embedding over all the lectures and table
- Able to give contextual answers, has conversational memory
- Gives out references, but not 100%
- Generates summaries

## Solution Overview

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


### Google Forms for Agent Evaluation
- CS324 Responder Link https://forms.gle/9QmBkhvvQjavJbM87
- CS234 Responder Link https://forms.gle/VUsxfj8fP5pE8VVY6
- CS231n Responder Link https://forms.gle/ASBXgqv6H9JogpRN8
- Mix Data Responder Link https://forms.gle/i1anmawfDdFzFUraA

