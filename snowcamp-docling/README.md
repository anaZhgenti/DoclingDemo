# PDF vs Markdown Q&A Demo with Docling

A demonstration project that compares the performance of Large Language Models (LLMs) when processing raw PDF documents versus properly formatted Markdown documents. This project showcases why proper document preprocessing is essential for optimal LLM performance.

## Overview

This project demonstrates the significant difference in LLM performance when answering questions from:
1. **Raw PDF**: Basic PyPDF2 text extraction with minimal preprocessing
2. **Formatted Markdown**: Proper document conversion using Docling, with intelligent chunking and processing

The key insight: Raw PDF extraction often produces poorly formatted text that confuses LLMs, while properly converted Markdown preserves document structure and improves answer quality.

## Features

- 📄 **PDF to Markdown Conversion**: Uses IBM's Docling library for intelligent PDF conversion
- 🔍 **Question-Answering Comparison**: Side-by-side comparison of Q&A performance on PDF vs Markdown
- 🧩 **Intelligent Chunking**: Uses LangChain's RecursiveCharacterTextSplitter with 15k character chunks
- 🔄 **Automatic Module Reloading**: Jupyter notebook automatically picks up changes to Python modules
- 📊 **Full Document Processing**: Processes entire documents by querying each chunk separately

## Prerequisites

- Python 3.13 recommended
- OpenAI API key
- Jupyter Notebook or JupyterLab

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create a `config.env` file in the project root
   - Add your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Project Structure

```
snowcamp-docling/
├── converter.ipynb              # PDF to Markdown conversion notebook
├── questions-and-answers.ipynb # Q&A comparison notebook
├── QandAFunctions.py           # Question-answering utility functions
├── ProcessingFunctions.py      # PDF conversion and file processing utilities
├── config.env                  # Environment variables (create this)
├── requirements.txt            # Python dependencies
├── report.pdf                  # Sample PDF document
└── result/
    └── report.md               # Converted Markdown output
```

## Usage

### Step 1: Convert PDF to Markdown

Open `converter.ipynb` and run the cells. This will:
- Use Docling to convert `report.pdf` to Markdown
- Save the output to `result/report.md`

### Step 2: Compare Q&A Performance

Open `questions-and-answers.ipynb` and run all cells. This notebook:
- Loads the raw PDF and converted Markdown
- Asks the same question to both formats

## Key Functions

### QandAFunctions.py

- `load_pdf(file_path)`: Extracts text from PDF using PyPDF2
- `ask_pdf(content, question)`: Queries raw PDF content using chunking
- `load_markdown(markdown_path)`: Loads Markdown file content
- `ask_markdown_simple(content, question)`: Queries Markdown content using chunking
- `initialize_environment()`: Loads OpenAI API key from config.env

### ProcessingFunctions.py

- `FileProcessor.write()`: Writes Markdown output to file with proper encoding
- `CountTokens`: Utilities for token counting (little bonus)

## How It Works

### Chunking Strategy

Both PDF and Markdown processing use:
- **Chunk Size**: 15,000 characters
- **Chunk Overlap**: 500 characters
- **Splitter**: LangChain's RecursiveCharacterTextSplitter

### Processing Flow

1. **Document Loading**: Content is loaded from PDF or Markdown file
2. **Chunking**: Content is split into manageable chunks
3. **Querying**: Each chunk is queried separately with the same question
4. **Combining**: Answers from all chunks are combined into a final response

This approach ensures:
- ✅ Full document coverage (no content is skipped)
- ✅ Respects token limits (each chunk fits within model limits)
- ✅ Better context preservation (chunking at natural boundaries)

## Configuration

### Model Settings

Default model (in `QandAFunctions.py`):
- Model: `gpt-3.5-turbo`

You can modify these in the `ask_pdf()` and `ask_markdown()` functions.

## Dependencies

Key libraries used:
- **docling**: IBM's document conversion library
- **langchain**: LLM application framework
- **langchain-openai**: OpenAI integration for LangChain
- **langchain-text-splitters**: Text chunking utilities
- **PyPDF2**: PDF text extraction
- **openai**: OpenAI API client
- **python-dotenv**: Environment variable management

See `requirements.txt` for the complete list.

## Tips

1. **Automatic Reloading**: The notebook uses `%autoreload 2` to automatically pick up changes to `QandAFunctions.py`. Just save your changes and re-run cells!

2. **Full Answers**: The notebook displays full answers without clipping, so you can see complete responses from all chunks.

3. **Error Handling**: Both functions handle errors gracefully and continue processing other chunks if one fails.

## Results

The results demonstrate the importance of proper document preprocessing before feeding content to LLMs.

## License

This is a demonstration project. Please check individual library licenses for production use.

## Contributing

This is a demo project, but suggestions and improvements are welcome!

## Acknowledgments

- [IBM Docling for document conversion capabilities](https://github.com/docling-project/docling)
- [LangChain for LLM application framework](https://www.langchain.com/)
- [OpenAI for the GPT models](https://openai.com/fr-FR/)
- A huge thank you to [Cedric Clyburn](https://github.com/cedricclyburn) for inspiring this project

