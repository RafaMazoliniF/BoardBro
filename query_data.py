import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import os
from langchain_community.llms import DeepInfra
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from get_embedding_function import get_embedding_function

os.environ["DEEPINFRA_API_TOKEN"] = 'vECEnkhLpRW64z6ZvKK5CSU8AwzqAkBT'
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context.

{context}

Answer the question based on the above context: {question}
"""


def main():
        
    # Create CLI.
    while True:
        query_text = str(input("> "))
        response = query_rag(query_text)
        print(response)   


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=4)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = DeepInfra(model_id="mistralai/Mistral-7B-Instruct-v0.3")
    response_text = model.invoke(prompt)    
    
    return response_text


if __name__ == "__main__":
    main()
