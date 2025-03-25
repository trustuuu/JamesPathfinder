import streamlit as st
from langchain.storage import LocalFileStore
from langchain.document_loaders import UnstructuredFileLoader, UnstructuredExcelLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler

st.set_page_config(
    page_title="Pathfinder!",
    page_icon="😍"
)
st.title("Please ask to AI about Yoon-Suk Chang")

st.markdown("""
Welcome!
            Use this chatbot to ask questions to an AI about Yoon-Suk Chang.
""")

if 'initialized' not in st.session_state:
    # Run the command or function you want to execute only once
    st.session_state.initialized = True
    st.session_state["messages"] = []

class ChatCallbackHandler(BaseCallbackHandler):
    message = ""

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)


llm = ChatOpenAI(temperature=0.1, streaming=True,callbacks=[ChatCallbackHandler()])
def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Answer the question using ONLY the following context. If you don't know the answer just say you don't know. DON'T make anything up.
            
            Context: {context}
            """,
        ),
        ("human", "{question}"),
    ]
)

@st.cache_data(show_spinner=f"Embedding file......")
def embed_file(file):
    file_path = f"./{file}"
    cache_dir = LocalFileStore(f"./.cache/embeddings/{file}")
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
        
    docs = loader.load_and_split(text_splitter=splitter)
    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    vectorstore = FAISS.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()
    return retriever

def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if(save):
        save_message(message, role)

def paint_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"], False)


# with st.sidebar:
#     file = st.file_uploader("Upload a .txt .pdf .xlsx or .docx file", type=["pdf", "txt", "docx", "xlsx"])

retriever = embed_file("Resume(YSChang_ATS).pdf")
send_message("I'm ready! Ask away!", "ai", save=False)

paint_history()
message = st.chat_input("Ask anything about Yoon-Suk Chang...")
if message:
    send_message(message, "human")
    chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )
    with st.chat_message("ai"):
        response = chain.invoke(message)
