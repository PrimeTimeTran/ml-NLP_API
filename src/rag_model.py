# https://huggingface.co/learn/cookbook/rag_zephyr_langchain
# 1. Use langchain
import locale
locale.getpreferredencoding = lambda: "UTF-8"

# 2. Use Github
from getpass import getpass
ACCESS_TOKEN = getpass("YOUR_GITHUB_PERSONAL_TOKEN")

# 3. Load issues
from langchain.document_loaders import GitHubIssuesLoader
loader = GitHubIssuesLoader(repo="huggingface/peft", access_token=ACCESS_TOKEN, include_prs=False, state="all")
docs = loader.load()

# 4. Split into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=30)
chunked_docs = splitter.split_documents(docs)

# 5. Create the embeddings + retriever
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
db = FAISS.from_documents(chunked_docs, HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5"))

# We need a way to return(retrieve) the documents given an unstructured query. 
# For that, we’ll use the as_retriever method using the db as a backbone:
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# 6. Load quantized model
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
model_name = "HuggingFaceH4/zephyr-7b-beta"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16
)
model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 7. Setup the LLM chain
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_core.output_parsers import StrOutputParser
text_generation_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.2,
    do_sample=True,
    repetition_penalty=1.1,
    return_full_text=True,
    max_new_tokens=400,
)
llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
prompt_template = """
<|system|>
Answer the question based on your knowledge. Use the following context to help:
{context}
</s>
<|user|>
{question}
</s>
<|assistant|>
"""
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)
llm_chain = prompt | llm | StrOutputParser()

# 8. Combine the llm_chain with the retriever to create a RAG chain.
from langchain_core.runnables import RunnablePassthrough
retriever = db.as_retriever()
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | llm_chain

# 9. Compare the results
question = "How do you combine multiple adapters?"




# First, let’s see what kind of answer we can get with just the model itself, no context added:
llm_chain.invoke({"context": "", "question": question})


rag_chain.invoke(question)

