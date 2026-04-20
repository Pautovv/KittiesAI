from langchain_core.tools import tool
from tools.sandbox import DockerSandbox
from tools.web_search import WebSearchTool

sandbox_instance = DockerSandbox()
web_search_instance = WebSearchTool()

@tool
def execute_python_code(code: str) -> str:
    """
    Полезно для выполнения Python-кода, математических вычислений, 
    анализа данных (pandas) или построения алгоритмов.
    Ожидает на вход строку с Python-кодом.
    Возвращает результат выполнения (stdout) или ошибку (stderr).
    """
    res = sandbox_instance.execute_code(code)
    return f"Status: {res['status']}\nStdout: {res['stdout']}\nStderr: {res['stderr']}"

@tool
def search_internet(query: str) -> str:
    """
    Полезно для поиска актуальной информации в интернете, 
    новостей, статей, документации или фактов.
    Ожидает на вход поисковой запрос.
    Возвращает текстовую сводку найденной информации.
    """
    return web_search_instance.search(query)