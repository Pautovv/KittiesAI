import json
from qdrant_client import QdrantClient

class CodebaseSearchTool:
    def __init__(self, collection_name: str="local_knowledge", path: str="./qdrant_local_db"):
        self.client = QdrantClient(path=path)
        self.collection_name = collection_name
        self.client.set_model("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=self.client.get_fastembed_vector_params()
            )
    
    def add_documents(self, chunks: list[dict]):
        self.client.add(
            collection_name=self.collection_name,
            documents=[chunk["text"] for chunk in chunks],
            metadata=[chunk["metadata"] for chunk in chunks],
            ids=[chunk["id"] for chunk in chunks]
        )
    
    def search(self, query: str, limit: int=3, min_score: float=0.50) -> str:
        try:
            res = self.client.query(
                collection_name=self.collection_name,
                query_text=query,
                limit=limit
            )

            points = res or []
            if not points:
                return json.dumps({"status": "empty", "source": "local_db", "results": []}, ensure_ascii=False)

            formatted = []
            for p in points:
                score = getattr(p, "score", 0.0) or 0.0
                if score < min_score:
                    continue

                payload = getattr(p, "metadata", getattr(p, "payload", {})) or {}
                formatted.append({
                    "score": float(score),
                    "file": payload.get("file", "unknown"),
                    "text": payload.get("document", payload.get("text", ""))
                })

            return json.dumps({"status": "ok", "source": "local_db", "results": formatted}, ensure_ascii=False)

        except Exception as e: return json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False)