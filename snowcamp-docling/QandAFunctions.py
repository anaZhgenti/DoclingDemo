def initialize_environment():
    """
    Initialize the environment by loading environment variables from config.env.
    Sets up the OpenAI API key from the configuration file.

    Note: Required packages should be installed separately via pip or requirements.txt.
    """
    import os
    from dotenv import load_dotenv

    # Load environment variables from config.env
    load_dotenv('config.env')

    # Set OpenAI API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        print("✓ Environment initialized: OPENAI_API_KEY loaded")
    else:
        print("⚠ Warning: OPENAI_API_KEY not found in config.env")


def filter_complex_metadata(documents):
    """Filter out complex metadata that Chroma can't handle"""
    from langchain_core.documents import Document

    filtered_docs = []
    for doc in documents:
        # Keep only simple metadata types
        simple_metadata = {}
        for key, value in doc.metadata.items():
            if isinstance(value, (str, int, float, bool, type(None))):
                simple_metadata[key] = value
        # Create new document with filtered metadata
        filtered_docs.append(Document(
            page_content=doc.page_content,
            metadata=simple_metadata
        ))
    return filtered_docs



def get_prompt():
    """Create and return the LangChain prompt template"""
    from langchain_core.prompts import PromptTemplate

    return PromptTemplate.from_template(
        """Here is the raw content from a PDF document:
        ---------------------
        {context}
        ---------------------
        Please answer the following question based ONLY on this content:
        Question: {input}
        Answer:
        """)


def load_pdf(file_path):
    """Load PDF content as raw text without any preprocessing"""
    import PyPDF2

    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            raw_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                raw_text += page.extract_text() + "\n"
        return raw_text
    except Exception as e:
        return f"Error loading PDF: {str(e)}"


def ask_pdf(content, question):
    """Set up an LLM chain for raw PDF content with chunking - queries each chunk separately"""
    from langchain_openai import ChatOpenAI
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # Create a document from the content
    doc = Document(page_content=content)
    
    # Split content into chunks using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=15000,
        chunk_overlap=500,
    )
    chunks = text_splitter.split_documents([doc])
    
    llm = ChatOpenAI(
        model='gpt-3.5-turbo',
        temperature=0.5,
        max_tokens=512,
    )
    
    # Query each chunk separately
    chunk_answers = []
    chunk_contexts = []
    
    try:
        for i, chunk in enumerate(chunks):
            chunk_text = chunk.page_content
            try:
                response = llm.invoke(get_prompt().format(
                    context=chunk_text,
                    input=question
                ))
                chunk_answers.append(response.content)
                chunk_contexts.append(chunk_text[:500])
            except Exception as e:
                chunk_answers.append(f"Error processing chunk {i+1}: {str(e)}")
        
        # Combine all answers
        combined_answer = "\n\n".join([f"Chunk {i+1}: {ans}" for i, ans in enumerate(chunk_answers)])
        
        return {
            "answer": combined_answer,
        }
    except Exception as e:
        return {"error": str(e), "answer": f"Error processing raw PDF: {e}"}


def load_markdown(markdown_path):
    """Load markdown file content as raw text without any preprocessing or RAG setup"""
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        return markdown_content
    except UnicodeDecodeError:
        # Try with different encodings if UTF-8 fails
        with open(markdown_path, 'r', encoding='latin-1') as f:
            markdown_content = f.read()
        return markdown_content
    except Exception as e:
        return f"Error loading markdown: {str(e)}"


def ask_markdown(content, question):
    """Ask a question to raw markdown content without RAG, with chunking - queries each chunk separately"""
    from langchain_openai import ChatOpenAI
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # Create a document from the content
    doc = Document(page_content=content)
    
    # Split content into chunks using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=15000,
        chunk_overlap=500,
    )
    chunks = text_splitter.split_documents([doc])
    
    llm = ChatOpenAI(
        model='gpt-3.5-turbo',
        temperature=0.5,
        max_tokens=512,
    )
    
    # Query each chunk separately
    chunk_answers = []
    chunk_contexts = []
    
    try:
        for i, chunk in enumerate(chunks):
            chunk_text = chunk.page_content
            try:
                response = llm.invoke(get_prompt().format(
                    context=chunk_text,
                    input=question
                ))
                chunk_answers.append(response.content)
                chunk_contexts.append(chunk_text[:500])
            except Exception as e:
                chunk_answers.append(f"Error processing chunk {i+1}: {str(e)}")
        
        # Combine all answers
        combined_answer = "\n\n".join([f"Chunk {i+1}: {ans}" for i, ans in enumerate(chunk_answers)])
        
        return {
            "answer": combined_answer
        }
    except Exception as e:
        return {"error": str(e), "answer": f"Error processing markdown: {e}"}