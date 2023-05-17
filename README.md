# Natural Language Query Agent

Utilizes LLMs and open-source vector indexing and storage frameworks to answer simple questions over a small set of lecture notes and a table of LLM architectures.

## Data :
- Stanford LLMs Lecture Notes: https://stanford-cs324.github.io/winter2022/lectures/ (create conversational intelligence over 3-4 lectures of your choosing, but be sure to include the introduction lecture)
- https://github.com/Hannibal046/Awesome-LLM#milestone-papers (only the table of model architectures)


## Steps:
- Read up langchain, chroma documentation
- Install the required packages
- Get .md files from git for data
- Import data into chroma
- Play around
- Test out openapi key
- Get query embedding
- Get topk similarity scores with data
- Generate final query
- Citations ? Add meta data to md files, see if chroma does it automatically
  - Again similarity?
  - Check api response, maybe helpful
- Conversational ? Seems like langchain openai has an api. 
- Create cli/python wrapper
- Summary ? Keep the conversation handy. Then generate summary
- Scaling plan. Think about this
- Clean README, pipreq