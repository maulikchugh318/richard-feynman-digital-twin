import argparse

from logger import app_logger


def run_health_check():
    app_logger.info("System healthy")


def ingest_data():
    from rag.ingest import ingest_documents

    ingest_documents()


def run_streamlit():
    import os

    os.system("streamlit run ui/chat_page.py")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        choices=[
            "check",
            "ingest",
            "app"
        ]
    )

    args = parser.parse_args()

    if args.command == "check":
        run_health_check()

    elif args.command == "ingest":
        ingest_data()

    elif args.command == "app":
        run_streamlit()


if __name__ == "__main__":
    main()