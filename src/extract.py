import os
import requests
import logging
import docx2txt
import PyPDF2
import pandas as pd
from .utils import *

__all__ = ["File", "Extractor"]


class File:
    def __init__(self, path: str, name: str, content: str):
        self.path = path
        self.name = name
        self.content = content


class Extractor:
    def __init__(self, path: str):
        self.base_path = path

    def extract(self):
        if self.is_directory():
            return self.get_directory_content(path=self.base_path)
        else:
            return self.extract_from_file(path=self.base_path)

    def file_name(self, path) -> str:
        return os.path.basename(path)

    def is_directory(self) -> bool:
        return os.path.isdir(self.base_path)

    def get_directory_content(self, path: str) -> str:
        file_contents = []
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                file_contents.extend(self.extract_from_file(file_path))
        return file_contents

    def extract_from_file(self, path: str) -> str:
        content = ""
        if self.is_docx_file(path):
            content = self.read_docx_file(path)
        elif self.is_xlsx_file(path):
            content = self.read_xlsx_file(path)
        elif self.is_xls_file(path):
            content = self.read_xls_file(path)
        elif self.is_csv_file(path):
            content = self.read_csv_file(path)
        elif self.is_pdf_file(path):
            content = self.read_pdf_file(path)
        elif self.is_website(path):
            content = self.read_website(path)
        else:
            content = self.read_file(path)

        split_content = self.split(content)

        result = []
        for content in split_content:
            result.append(
                File(
                    path=path,
                    name=self.file_name(path),
                    content=str(self.strip(content)),
                )
            )

        return result

    def read_file(self, path) -> str:
        try:
            with open(path, "r") as f:
                return f.read(10000)
        except FileNotFoundError:
            logging.error(f"File not found: {path}")
            return None
        except Exception as e:
            logging.error(f"Error reading file: {path}, {e}")
            return None

    def is_docx_file(self, path) -> bool:
        return path.endswith(".docx")

    def read_docx_file(self, path: str) -> str:
        try:
            return docx2txt.process(path)
        except Exception as e:
            logging.error(f"Error reading docx file: {path}, {e}")
            return None

    def is_xlsx_file(self, path) -> bool:
        return path.endswith(".xlsx")

    def read_xlsx_file(self, path: str) -> str:
        try:
            return pd.read_excel(path).to_string()
        except Exception as e:
            logging.error(f"Error reading xlsx file: {path}, {e}")
            return None

    def is_xls_file(self, path) -> bool:
        return path.endswith(".xls")

    def read_xls_file(self, path: str) -> str:
        try:
            return pd.read_excel(path).to_string()
        except Exception as e:
            logging.error(f"Error reading xls file: {path}, {e}")
            return None

    def is_csv_file(self, path) -> bool:
        return path.endswith(".csv")

    def read_csv_file(self, path: str) -> str:
        try:
            return pd.read_csv(path).to_string()
        except Exception as e:
            logging.error(f"Error reading csv file: {path}, {e}")
            return None

    def is_pdf_file(self, path) -> bool:
        return path.endswith(".pdf")

    def read_pdf_file(self, path: str) -> str:
        try:
            pdfReader = PyPDF2.PdfReader(path)
            content = ""
            for i in range(len(pdfReader.pages)):
                pageObj = pdfReader.pages[i]
                content += pageObj.extract_text()

            return content
        except Exception as e:
            logging.error(f"Error reading pdf file: {path}, {e}")
            return None

    def is_website(self, path) -> bool:
        return (
            path.startswith("http")
            or path.startswith("https")
            or path.startswith("www")
            or path.startswith("ftp")
            or path.startswith("ftps")
        )

    def read_website(self, path: str) -> str:
        try:
            response = requests.get(path)
            return response.text
        except Exception as e:
            logging.error(f"Error reading website: {path}, {e}")
            return None

    def strip(self, content: str) -> str:
        if content is None:
            return None
        return content

    def split(self, content: str) -> list[str]:
        if content is None:
            return None

        result = []
        while is_token_overflow(content, model="text-embedding-3-small"):
            result.append(content[:10000])
            content = content[10000:]

        result.append(content)
        return result
