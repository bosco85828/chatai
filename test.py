from dotenv import load_dotenv
import os 
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import pinecone


load_dotenv()

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY=os.getenv('PINECONE_API_KEY')

pinecone.init(
  api_key=PINECONE_API_KEY,
  environment="us-central1-gcp"
)
loader = DirectoryLoader('~/Desktop/script/chatai/', glob='**/*.txt')
documents = loader.load()
embeddings = OpenAIEmbeddings()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# 切割加载的 document
split_docs = text_splitter.split_documents(documents)

index_name="bill-test"
# 持久化数据
docsearch = Pinecone.from_texts([t.page_content for t in split_docs], embeddings, index_name=index_name)

# 加载数据
docsearch = Pinecone.from_existing_index(index_name,embeddings)

query = "科大讯飞今年第一季度收入是多少？"
# docs = docsearch.similarity_search(query, include_metadata=True)
docs = docsearch.similarity_search(query)

llm = OpenAI(temperature=0)
chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
chain.run(input_documents=docs, question=query)


# llm = OpenAI(model_name="text-davinci-003",max_tokens=1024)
# llm("怎么评价人工智能")