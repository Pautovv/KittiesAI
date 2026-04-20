import os, json
from tavily import TavilyClient

class WebSearchTool:
    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
    def search(self, query: str, max_res: int = 3) -> str:
        try:
            response = self.client.search(query=query, max_results=max_res)
            items = []
            for r in response.get("results", []):
                items.append({
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "url": r.get("url", "")
                })

            if not items:
                return json.dumps({
                    "status": "empty",
                    "source": "web",
                    "query": query,
                    "results": []
                }, ensure_ascii=False)

            return json.dumps({
                "status": "ok",
                "source": "web",
                "query": query,
                "results": items
            }, ensure_ascii=False)

        except Exception as e:
            return json.dumps({
                "status": "error",
                "source": "web",
                "query": query,
                "error": str(e)
            }, ensure_ascii=False)
            