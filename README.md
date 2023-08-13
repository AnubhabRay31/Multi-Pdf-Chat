# Multi-Pdf-Chat
A moderate python project regarding making a chat-bot with LLMs &amp; LangChain.

This project first gets data from uploaded pdfs on a web-interface created with streamlit.
Then the pdf files are processed into mono-string and broken into chunks. These are converted into vector-embeddings and stored in a vector store.
For my project I used FAISS-cpu as vector store &amp; execution on local machine. 

Then the user queries are embedded similarly and relevant results from corpus (broken phrases) are passed through an LLM (I used google's flan-t5-xxl).
The history is stored using streamlit's session vars, and latter used to find context of a query. 

## Below are some screenshots of the UI and VS Code screen
![1](https://github.com/AnubhabRay31/Multi-Pdf-Chat/assets/76247904/02c70993-058f-46c3-94d5-15cd18b88a6e)

![2](https://github.com/AnubhabRay31/Multi-Pdf-Chat/assets/76247904/dbec39e3-3117-4467-a846-60d3b81576d0)

![3](https://github.com/AnubhabRay31/Multi-Pdf-Chat/assets/76247904/2b4f8d14-88b1-49cf-a815-1ef91eb58fb6)
