from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI,VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
import os 
from dotenv import load_dotenv
from pprint import pprint
import openai
import sys

load_dotenv()
path=os.getcwd()
embeddings = OpenAIEmbeddings()
def load_from_txt():
    # 加载文件夹中的所有txt类型的文件
    loader = DirectoryLoader(path, glob='**/*.txt')
    # # 将数据转成 document 对象，每个文件会作为一个 document
    documents = loader.load()
    # 初始化加载器
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # 切割加载的 document
    split_docs = text_splitter.split_documents(documents)
    # 初始化 openai 的 embeddings 对象
    embeddings = OpenAIEmbeddings()
    # 持久化数据
    docsearch = Chroma.from_documents(split_docs, embeddings, persist_directory=f"{path}/vector_store")
    docsearch.persist()

def get_from_db(question):
    # Now we can load the persisted database from disk, and use it as normal. 
    docsearch = Chroma(persist_directory=f"{path}/vector_store", embedding_function=embeddings)
    docs = docsearch.similarity_search(question,k=1)
    return docs[0].page_content.strip().replace('\n','')


def generate_text(prompt):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一個遊戲客服專員，請你模仿客服溫柔的語氣，並且依照我提供的參考資料回答，不知道就說不清楚，不要亂回答。 "},
            {"role": "user", "content": prompt + "請你參考以下資訊回答,{}".format(get_from_db(prompt)) }
        ], 
        # prompt=prompt,
        max_tokens=1024,
        temperature=0.1,
        n=1,
        stop="END",
        timeout=15,
        # context=context
    )

    return response['choices'][0]['message']['content']
if __name__ == "__main__":
    print(generate_text(sys.argv[1]))
