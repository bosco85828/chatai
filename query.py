from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI,VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
import os 
from pprint import pprint
import openai
import sys
from tgbot import send_msg
from sqldb import insert_info , get_maxid ,change_info , insert_token 

path=os.getcwd()
embeddings = OpenAIEmbeddings()

def load_from_txt(merchant,prompt,completion):
    
    try : 
        _id= int(get_maxid(f"{merchant}_train")) + 1 
    
    except Exception as err :
        _id=1
        print({_id:err}) 

    print('now:{}'.format(_id))
    data=prompt + '\n' + completion

    original_doc = Document(page_content=data)
    # 初始化 openai 的 embeddings 对象
    embeddings = OpenAIEmbeddings()
    # 持久化数据
    docsearch = Chroma.from_documents(
        documents=[original_doc], 
        embedding=embeddings,
        persist_directory=f"{path}/{merchant}"
        )
    
    docsearch.persist()

    try : insert_info(f"{merchant}_train",prompt,completion)
    except Exception as err : 
        send_msg({'insert_info':err})

def load_from_dir_id(merchant,_id):
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
    num=[ f"doc_{_id}_{i}" for i in range(len(split_docs))] 

    # docsearch = Chroma.from_documents([split_docs], embeddings,ids=["doc_{}_{}".format(_id,num)],  persist_directory=f"{path}/{merchant}")
    docsearch = Chroma.from_documents(split_docs, embeddings,ids=num,  persist_directory=f"{path}/{merchant}")
    docsearch.persist()
    

def load_from_dir(merchant):
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
    docsearch = Chroma.from_documents(split_docs, embeddings,  persist_directory=f"{path}/{merchant}")
    docsearch.persist()

def change_data(merchant,prompt,completion,_id):
    try : 
        data=prompt + '\n' + completion
        original_doc = Document(page_content=data)
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma(persist_directory=f"{path}/{merchant}", embedding_function=embeddings)
        
        docsearch.update_document(document_id="doc_{}".format(_id), document=original_doc)
        docsearch.persist()
        # change_info(f"{merchant}_train",prompt,completion,_id)

    
    except Exception as err : 
        print(err)




def get_from_db(question,merchant):

    if os.path.exists(f"{path}/{merchant}") : 
        # print('exist')
        # Now we can load the persisted database from disk, and use it as normal. 
        docsearch = Chroma(persist_directory=f"{path}/{merchant}", embedding_function=embeddings)
        try : docs = docsearch.similarity_search(question,k=1)
        except Exception as err : 
            send_msg({"get_from_db":err})
            docs = None

    else : 
        # print('not exist')
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
    print('now:' + os.getenv('OPENAI_API_KEY'))
    try : insert_token(f"{merchant}_token",response['usage']['total_tokens'],prompt,response['choices'][0]['message']['content'])
    except Exception as err : 
        send_msg({"insert_token":err})

    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    # load_from_dir_id('JLB_seasonal','seasonal')
    # load_from_txt('TEST2','明天早餐要吃什麼','還不知道')
    # print(generate_text('客服您好，請問該如何修改密碼','test777'))
    print(change_data('JLB_seasonal','3天後天氣如何','陰天','seasonal_0'))
    # print(generate_text('晚餐要吃什麼','JLB'))
    # load_from_dir('TEST_5','test1')
    # print(change_data('TEST_5','20天後的天氣如何','陰天','test1'))
    pass


