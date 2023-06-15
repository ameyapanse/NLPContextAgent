# Contextualized Conversational Agent


## Instructions:
- Install langchain, chromadb, pypdf
- 
- Run python main.py

## Solution Overview

### Base Architecture
- Get and save document embeddings from llm. Uses the OpenAI's text-embedding-ada-002 as recommended by their documentation
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
- More details below

## Capabilities
- Embedding over all the lectures and table
- Able to give contextual answers, has conversational memory
- Gives out references, but not 100%
- Generates summaries

## Weaknesses and Hacks
- The agent has to be hot wired. The first query is in-built. 
  - This is due to the ConversationalSummaryBufferMemory. But, this approach provided the best results
- The citation by the agent is flaky. I tried two ways of doing this. 
  - Adding a custom prompt to get the references directly from the llm. I was not able to make this work. 
  A way to do this is to write a custom ConversationalRetrievalChain. 
  - Using the documents retrieved for the query. A engineered solution to produce the hyperlinks to the lecture subheading
  Here, I also briefly tried to wrap the MarkdownTextSplitter to produce more relavant metadata. Next steps include adding split indices to give succint references
- The agent is slow. This is due to multiple calls to the llm.

## Data :
- Stanford LLMs Lecture Notes: https://stanford-cs324.github.io/winter2022/lectures/ (I used the markdown version of these files)
- https://github.com/Hannibal046/Awesome-LLM#milestone-papers (only the table of model architectures)

## Scalabilty:
- Currently uses Chroma's in-memory database for document embeddings. Will to to shift to a server-client model to scale
- Conversational Agent is Sequential as previous messages are used for context.
- Hit OpenAI rate limitation quite a few times during test runs
- Relies on the MarkDownTextSplitter. We will have to convert it to an interface for other data formats.