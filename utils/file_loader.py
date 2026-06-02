from pathlib import Path
from pypdf import PdfReader


class FileLoader:

    @staticmethod
    def load_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)

    @staticmethod
    def load_txt(file_path: str) -> str:
        return Path(file_path).read_text(
            encoding="utf-8",
            errors="ignore"
        )

    @classmethod
    def load_document(cls, file_path: str) -> str:

        path = Path(file_path)

        if path.suffix.lower() == ".pdf":
            return cls.load_pdf(file_path)

        if path.suffix.lower() == ".txt":
            return cls.load_txt(file_path)

        raise ValueError(
            f"Unsupported file type: {path.suffix}"
        )