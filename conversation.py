from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from embed import Embedder
from langchain.memory.summary import SummarizerMixin
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.prompts.prompt import PromptTemplate


class Conversation:
    def __init__(self, debug_mode=False):
        self.embedder = Embedder()
        self.embedder.embed_all_docs()
        self.vectorstore = self.embedder.get_vectorstore()
        # self.memory = ConversationBufferMemory(memory_key="chat_history",
        #                                        return_messages=True,
        #                                        output_key='answer')
        self.llm = ChatOpenAI(
            temperature=0.0,
            model_name="gpt-3.5-turbo")

        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            output_key='answer',
            memory_key='chat_history',
            return_messages=True)

        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"include_metadata": True})

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            memory=self.memory,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            get_chat_history=lambda h: h,
            verbose=debug_mode)
        # self.chain = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0),
        #                                                    self.embedder.get_vectorstore().as_retriever(),
        #                                                    memory=self.memory,
        #                                                    max_tokens_limit=3000,
        #                                                    return_source_documents=True,
        #                                                    get_chat_history=lambda h: h,
        #                                                    qa_prompt=QA_PROMPT)
        self.debug = debug_mode

    def achat(self):
        query = input("Question : ")
        if query == 'exit' or '':
            return False
        ret = self.chain({'question': query})
        if self.debug:
            print(ret)
        print('Answer : ', ret.get('answer'))
        source_docs = ret.get('source_documents')
        lectures_home = "https://stanford-cs324.github.io/winter2022/lectures/"
        table_home = "https://github.com/Hannibal046/Awesome-LLM/blob/main/README.md#milestone-papers"
        print('References : ' )
        for sd in source_docs:
            if sd.metadata.get('file', ''):
                file = sd.metadata.get('file')
                if file != 'table':
                    title='-'.join(sd.page_content.split('\n')[0].lower().split())
                    print(lectures_home+file+'/#'+title)
                else:
                    print(table_home+file)
        return True

    def chat(self):
        continue_conversation = self.achat()
        while continue_conversation:
            continue_conversation = self.achat()
        self.summarize_conversation()

    def summarize_conversation(self):
        SUMMARIZER_TEMPLATE = """Progressively summarize the lines of conversation provided, adding onto the previous summary returning a new summary. Format the summary into bullet points. Keep the summary very short.
            EXAMPLE
            Current summary:
            The human asks what the AI thinks of artificial intelligence. The AI thinks artificial intelligence is a force for good.

            New lines of conversation:
            Human: Why do you think artificial intelligence is a force for good?
            AI: Because artificial intelligence will help humans reach their full potential.

            New summary:
             - Artificial intelligence is a force for good
             - It will help humans reach their full potential.
            END OF EXAMPLE

            Current summary:
            {summary}

            New lines of conversation:
            {new_lines}

            New summary:"""
        FINAL_SUMMARY_PROMPT = PromptTemplate(
            input_variables=["summary", "new_lines"], template=SUMMARIZER_TEMPLATE
        )
        sm = SummarizerMixin(llm=self.llm, prompt=FINAL_SUMMARY_PROMPT)
        print(sm.predict_new_summary(c.memory.chat_memory.messages, ""))


if __name__ == "__main__":
    c = Conversation(True)
    c.chat()
