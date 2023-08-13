# Multi-Pdf-Chat
A moderate python project regarding making a chat-bot with LLMs &amp; LangChain.

This project first gets data from uploaded pdfs on a web-interface created with streamlit.
Then the pdf files are processed into mono-string and broken into chunks. These are converted into vector-embeddings and stored in a vector store.
For my project I used FAISS-cpu as vector store &amp; execution on local machine. 

Then the user queries are embedded similarly and relevant results from corpus (broken phrases) are passed through an LLM (I used google's flan-t5-xxl).
The history is stored using streamlit's session vars, and latter used to find context of a query. 

