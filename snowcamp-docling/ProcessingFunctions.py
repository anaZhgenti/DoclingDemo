"""
PDF Conversion and Token Counting Functions

This module provides functions for converting PDFs to markdown format
and counting tokens using Docling and OpenAI token counting utilities.
"""
from pathlib import Path

class FileProcessor:

    @staticmethod
    def write(markdown_output, output_dir):
        """
        Write MD to the output directory.
        Args:
            markdown_output: DocumentConverter instance
            output_dir (Path): Output directory path
        """

        # Write to multiple formats with proper UTF-8 encoding
        try:
            markdown_path = output_dir / "report.md"
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_output)
            print(f"Exported to {markdown_path}")

        except Exception as e:
            print(f"Error during export: {e}")
            print("This might be due to Unicode characters in the content")

        print("Export to Markdown completed!")
    
class CountTokens:

    @staticmethod
    def format_number(num):
        """
        Format numbers in a more readable way (K, M, B).
        Args:
            num (int): Number to format
        Returns:
            str: Formatted number string
        """
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)

    @staticmethod
    def count_pdf_tokens(pdf_path, encoding):
        """
        Count tokens from PDF file content.
        Args:
            pdf_path (str): Path to the PDF file
            encoding: Encoding instance
        Returns:
            int: Token count
        """
        with open(pdf_path, 'rb') as file:
            raw_pdf_content = file.read()
            raw_text = raw_pdf_content.decode('utf-8', errors='ignore')
        tokens = encoding.encode(raw_text)
        return len(tokens)

    @staticmethod
    def count_markdown_tokens(markdown_content, encoding):
        """
        Count tokens from markdown content.
        Args:
            markdown_content (str): Markdown content string
            encoding: Encoding instance
        Returns:
            int: Token count
        """
        tokens = encoding.encode(markdown_content)
        return len(tokens)


    def compare_token_counts(self, pdf_path, markdown_content, encoding):
        """
        Compare token counts between raw PDF and parsed markdown.
        Also extracts and displays 100 characters starting at position 2000 from both.
        Args:
            pdf_path (str): Path to the PDF file
            markdown_content (str): Parsed markdown content
            encoding: Encoding instance
        Returns:
            tuple: (raw_token_count, parsed_token_count)
        """
        raw_token_count = self.count_pdf_tokens(pdf_path, encoding)
        parsed_token_count = self.count_markdown_tokens(markdown_content, encoding)

        print(f"Token count before parsing: {raw_token_count:,} ({self.format_number(raw_token_count)})")
        print(f"Token count after PDF parsing: {parsed_token_count:,} ({self.format_number(parsed_token_count)})")

        # Extract 100 characters starting at position 2000 from both
        start = 5000
        length = 300

        # Read raw PDF content for character extraction
        with open(pdf_path, 'rb') as file:
            raw_pdf_content = file.read()
            raw_text = raw_pdf_content.decode('utf-8', errors='ignore')

        # Extract from PDF
        pdf_extract = raw_text[start:start+length] if len(raw_text) > start else f"[PDF too short: only {len(raw_text)} chars]"

        # Extract from markdown
        markdown_extract = markdown_content[start:start+length] if len(markdown_content) > start else f"[Markdown too short: only {len(markdown_content)} chars]"

        print(f"\nPDF content: '{pdf_extract}'")
        print(f"\nMarkdown content: '{markdown_extract}'")

        return raw_token_count, parsed_token_count