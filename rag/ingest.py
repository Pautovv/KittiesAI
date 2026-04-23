import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from tools.code_search import CodebaseSearchTool

def ingest_repository(repo_path: str, collection_name: str = "local_knowledge"):
    print(f"Начинаем индексацию репозитория: {repo_path}")
    
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=1000,
        chunk_overlap=200
    )
    
    db = CodebaseSearchTool(collection_name=collection_name)
    chunks_to_insert = []
    chunk_id = 1

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()

                    docs = python_splitter.create_documents([code])
                    
                    for doc in docs:
                        chunks_to_insert.append({
                            "id": chunk_id,
                            "text": doc.page_content,
                            "metadata": {"file": file_path}
                        })
                        chunk_id += 1
                except Exception as e:
                    print(f"Ошибка чтения {file_path}: {e}")

    if chunks_to_insert:
        db.add_documents(chunks_to_insert) 
        print(f"Успешно загружено {len(chunks_to_insert)} чанков в коллекцию {collection_name}")
    else: print("Код не найден.")

if __name__ == "__main__":
    ingest_repository("./target_repo")