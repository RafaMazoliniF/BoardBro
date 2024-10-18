import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context. Talk to me like a friend that is explaning me the game rules:

{context}

---

Answer the question based on the above context: {question}

Use "bro" instead of friend.
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
    results = db.similarity_search_with_score(query_text, k=7)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    #formatted_response = f"Response: {response_text}\nSources: {sources}"
    
    formatted_response = f"Response: {response_text}"
    
    return response_text


if __name__ == "__main__":
    main()
