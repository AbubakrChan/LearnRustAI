from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain

_template = """You are an AI assistant and You are trained on the book of "The rust  programming language" and you will be asked questions from this book.Answers these questions properly.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """You are an AI assistant and You are trained on the book of "The rust  programming language" and you will be asked questions from this book.Answers these questions properly.
Question: {question}
=========
{context}
=========
Answer in Markdown:"""

QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])


def get_chain(vectorstore):
    llm = OpenAI(temperature=0)
    qa_chain = ChatVectorDBChain.from_llm(
        llm,
        vectorstore,
        qa_prompt=QA_PROMPT,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    )
    return qa_chain
