import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter 
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS, Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub
from constants import *
import click
import torch
from htmlTemplates import *





def pdf_to_text(pdfs):
    text = ""
    for pdf in pdfs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    return text 


def text_to_chunks(text):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
    chunks = splitter.split_text(text=text)
    return chunks

def get_vector_store(chunks, device_type):
    # embeddings = OpenAIEmbeddings()
    model_name = "hkunlp/instructor-xl"
    model_kwargs = {'device': device_type}
    encode_kwargs = {'normalize_embeddings': True}
    embeddings = HuggingFaceInstructEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
    
    # db = Chroma.from_documents(
    #     chunks,
    #     embeddings,
    #     persist_directory=PERSIST_DIRECTORY,
    #     client_settings=CHROMA_SETTINGS,
    # )
    # db.persist()
    # db = None
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    print("embeddings done")
    return vector_store, True

def get_conv_chain(vector_store):
    # llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever= vector_store.as_retriever(),
        memory = memory
    )
    return conversation_chain



# @click.command()
# @click.option(
#     "--device_type",
#     default="cuda" if torch.cuda.is_available() else "cpu",
#     type=click.Choice(
#         [
#             "cpu",
#             "cuda",
#             "ipu",
#             "xpu",
#             "mkldnn",
#             "opengl",
#             "opencl",
#             "ideep",
#             "hip",
#             "ve",
#             "fpga",
#             "ort",
#             "xla",
#             "lazy",
#             "vulkan",
#             "mps",
#             "meta",
#             "hpu",
#             "mtia",
#         ],
#     ),
#     help="Device to run on. (Default is cuda)",
# )

def handle_userinput(question):
    res = st.session_state.conversation({'question': question})
    st.session_state.chat_history = res['chat_history']
    # st.write(res)
    for i,msg in enumerate(st.session_state.chat_history):
        if i % 2==0:
            st.write(user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)

def main(device_type="cuda"):
    load_dotenv()
    st.set_page_config(page_title="Anubhab's Chatting", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)
  

    # initialise session states
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "knowledge_base" not in st.session_state:
        st.session_state.knowledge_base = False

    st.header("Chat with multiple pdfs :books:")
    question = st.text_input("Ask a question about your documents:")
                            #  disabled=not st.session_state.knowledge_base )
    # if not st.session_state.knowledge_base :
    #     st.write("First train the KB on your pdfs")

    if question : 
        print("user Q is " , question)
        # if st.session_state.conversation == None:
        #     st.write("No Knowledge base yet")
        # else:
        #     handle_userinput(question)
        if st.session_state.knowledge_base  :
            handle_userinput(question)
        else:
            st.write("No Knowledge base yet")

    # st.write(user_template.replace("{{MSG}}", "hello Robot"), unsafe_allow_html=True)
    # st.write(bot_template.replace("{{MSG}}", "hello Human"), unsafe_allow_html=True)

     
    with st.sidebar:
        st.subheader("your documents")
        pdfs = st.file_uploader("Upload pdfs here ", 
                         accept_multiple_files=True,
                         type=['pdf'])
        if st.button("Process"):
            with st.spinner("Processing"):
                # 1. get pdf text extracted
                raw_text = pdf_to_text(pdfs)
                print("raw text size : ", len(raw_text))

                # 2. get text embedings
                text_chunks = text_to_chunks(raw_text)
               
                print("Raw text divided into ", len(text_chunks), " chunks ")

                # 3. create vector store
                print("Now creating embeddings & vector storage ... ")
                vector_store, st.session_state.knowledge_base = get_vector_store(text_chunks, "cpu")
                print("Knowlwdge base is ready : address of vectorSpace ", vector_store)
                

                # conversation chain
                st.session_state.conversation = get_conv_chain(vector_store)






if __name__ == '__main__':
    main()