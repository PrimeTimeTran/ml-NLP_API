# 1. Install dependencies
# !pip install -q torch transformers accelerate bitsandbytes sentence-transformers unstructured[all-docs] langchain chromadb langchain_community

# 2. Collect documents
# !mkdir -p "./documents"
# !wget https://www.gov.nl.ca/ecc/files/env-protection-pesticides-business-manuals-applic-chapter7.pdf -O "./documents/env-protection-pesticides-business-manuals-applic-chapter7.pdf"
# !wget https://ipm.ifas.ufl.edu/pdfs/Citrus_IPM_090913.pptx -O "./documents/Citrus_IPM_090913.pptx"
# !wget https://www.gutenberg.org/ebooks/45957.epub3.images -O "./documents/45957.epub"
# !wget https://blog.fifthroom.com/what-to-do-about-harmful-garden-and-plant-insects-and-pests.html -O "./documents/what-to-do-about-harmful-garden-and-plant-insects-and-pests.html"

# 3. Unstructured data preprocessing
# Optional cell to reduce the amount of logs
import logging
logger = logging.getLogger("unstructured.ingest")
logger.root.removeHandler(logger.root.handlers[0])

# 4. Optionally, you can also choose a destination for the processed documents - this 
# could be MongoDB, Pinecone, Weaviate, etc. In this notebook, we’ll keep everything local.
import os
from unstructured.ingest.connector.local import SimpleLocalConfig
from unstructured.ingest.interfaces import PartitionConfig, ProcessorConfig, ReadConfig
from unstructured.ingest.runner import LocalRunner
output_path = "./local-ingest-output"
runner = LocalRunner(
    processor_config=ProcessorConfig(
        # logs verbosity
        verbose=True,
        # the local directory to store outputs
        output_dir=output_path,
        num_processes=2,
    ),
    read_config=ReadConfig(),
    partition_config=PartitionConfig(
        partition_by_api=True,
        api_key="YOUR_UNSTRUCTURED_API_KEY",
    ),
    connector_config=SimpleLocalConfig(
        input_path="./documents",
        # whether to get the documents recursively from given directory
        recursive=False,
    ),
)
runner.run()
# !brew install poppler
# !brew install tesseract

# 5. Import element objects from these json files.
from unstructured.staging.base import elements_from_json
elements = []
for filename in os.listdir(output_path):
    filepath = os.path.join(output_path, filename)
    elements.extend(elements_from_json(filepath))

# 6. You can also optionally choose to combine consecutive text elements 
# such as list items, for instance, that will together fit within chunk size limit.
from unstructured.chunking.title import chunk_by_title
chunked_elements = chunk_by_title(
    elements,
    # maximum for chunk size
    max_characters=512,
    # You can choose to combine consecutive elements that are too small
    # e.g. individual list items
    combine_text_under_n_chars=200,
)

# 7. The chunks are ready for RAG. To use them with LangChain, you 
# can easily convert Unstructured elements to LangChain documents.
from langchain_core.documents import Document
documents = []
for chunked_element in chunked_elements:
    metadata = chunked_element.metadata.to_dict()
    metadata["source"] = metadata["filename"]
    del metadata["languages"]
    documents.append(Document(page_content=chunked_element.text, metadata=metadata))

# 8. Setting up the retriever
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import utils as chromautils
# ChromaDB doesn't support complex metadata, e.g. lists, so we drop it here.
# If you're using a different vector store, you may not need to do this
docs = chromautils.filter_complex_metadata(documents)
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})


# 9. 
