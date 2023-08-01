# LearnRustAI
A chatbot designed exclusively for Bitcoin developers seeking to harness the power of Rust programming. Rust's unmatched safety, performance, and concurrency features make it a perfect fit for Bitcoin projects. With LearnRustAI, you can access instant and accurate answers from "The Rust Programming Language" book. Plus you can test your Rust knowledge with a conversational oral interview too.

# Setting UP:
### Ingest data
Ingestion of data is done over the book.txt file. Therefor, the only thing that is needed is to be done to ingest data is run python ingest_data.py

### Query data
Custom prompts are used to ground the answers in the state of the book text file.

### Running the Application
By running python app.py from the command line you can easily interact with your ChatGPT over your own data.


# Workflow:
### High Level Walkthrough
At a high level, there are two components to setting up ChatGPT over your own data: (1) ingestion of the data, (2) chatbot over the data. Walking through the steps of each at a high level here:

### Ingestion of data

![image](https://github.com/AbubakrChan/LearnRustAI/assets/89600478/3f989d50-431f-443b-ab25-27bcb87203d7)

This can be broken in a few sub steps. All of these steps are highly modular and as part of this tutorial we will go over how to substitute steps out. The steps are:

Load data sources to text: this involves loading your data from arbitrary sources to text in a form that it can be used downstream. This is one place where we hope the community will help out!
Chunk text: this involves chunking the loaded text into smaller chunks. This is necessary because language models generally have a limit to the amount of text they can deal with, so creating as small chunks of text as possible is necessary.
Embed text: this involves creating a numerical embedding for each chunk of text. This is necessary because we only want to select the most relevant chunks of text for a given question, and we will do this by finding the most similar chunks in the embedding space.
Load embeddings to vectorstore: this involves putting embeddings and documents into a vectorstore. Vecstorstores help us find the most similar chunks in the embedding space quickly and efficiently.

### Querying of Data

![image](https://github.com/AbubakrChan/LearnRustAI/assets/89600478/edf3542a-7dd1-4ca2-910a-77462becd1c3)

This can also be broken into a few steps. Again, these steps are highly modular, and mostly rely on prompts that can be substituted out. The steps are:

Combine chat history and a new question into a single standalone question. This is necessary because we want to allow for the ability to ask follow up questions (an important UX consideration).
Lookup relevant documents. Using the embeddings and vectorstore created during ingestion, we can look up relevant documents for the answer

### Ingestion of data

![image](https://github.com/AbubakrChan/LearnRustAI/assets/89600478/66f8488c-211f-43d6-b4e0-03bee3c1c366)

This section dives into more detail on the steps necessary to ingest data.


#Load Data
#Split Text
#Create embeddings and store in vectorstore
#Query data



