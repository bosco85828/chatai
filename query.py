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
from tgbot import send_msg

load_dotenv()
path=os.getcwd()
embeddings = OpenAIEmbeddings()
def load_from_txt(merchant):

    # 加载文件夹中的所有txt类型的文件
    loader = DirectoryLoader(f"{path}/{merchant}-rawdata/", glob='*.txt')

    # # 将数据转成 document 对象，每个文件会作为一个 document
    documents = loader.load()
    # 初始化加载器
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # 切割加载的 document
    split_docs = text_splitter.split_documents(documents)
    # 初始化 openai 的 embeddings 对象
    embeddings = OpenAIEmbeddings()
    # 持久化数据
    docsearch = Chroma.from_documents(split_docs, embeddings, persist_directory=f"{path}/{merchant}")
    docsearch.persist()

def get_from_db(question,merchant):
    # Now we can load the persisted database from disk, and use it as normal. 
    docsearch = Chroma(persist_directory=f"{path}/{merchant}", embedding_function=embeddings)
    try : docs = docsearch.similarity_search(question,k=1)
    except Exception as err : 
        send_msg(err)
        docs = None

    if docs : 
        print(docs)
        print(docs[0].page_content.strip().replace('\n',''))
        return docs[0].page_content.strip().replace('\n','')
    
    else : 
        return None


def generate_text(prompt,merchant):
    while True : 
        try : 
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个中国的游戏客服专员，请你模仿客服温柔的语气，用简体中文回覆，并且依照我提供的参考资料回答，不知道就说不清楚，不要乱回答，再次强调，不管提问者的语言为何，都请你使用简体中文回覆。 "},
                    {"role": "user", "content": prompt + "请你参考以下资讯并且使用简体中文回答,{}".format(get_from_db(prompt,merchant)) }
                ], 
                # prompt=prompt,
                max_tokens=1024,
                temperature=0.1,
                n=1,
                stop="END",
                timeout=30,
                # context=context
            )

            break

        except Exception as err :
            send_msg(err)
            continue 

    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    # load_from_txt()
    print(generate_text(sys.argv[1]))

