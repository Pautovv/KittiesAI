<p align="center">
  <span style="font-size:2.5rem; font-weight:700; vertical-align: middle;">
    KittiesAI
  </span>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python" />
  <img src="https://img.shields.io/badge/architecture-Multi--Agent%20(LangGraph)-purple.svg" alt="LangGraph" />
  <img src="https://img.shields.io/badge/VectorDB-Qdrant-red.svg" alt="Qdrant" />
  <img src="https://img.shields.io/badge/UI-Chainlit-orange.svg" alt="Chainlit" />
  <img src="https://img.shields.io/badge/LLMOps-LangSmith-black.svg" alt="LangSmith" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/light/langgraph-color.png" alt="LangGraph" height="78" style="vertical-align: middle; margin: 0 5px;"/>
  <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/light/langsmith-color.png" alt="LangSmith" height="78" style="vertical-align: middle; margin: 0 5px;"/>
  <img src="https://qdrant.tech/img/brand-resources-logos/qdrant-brandmark-red.svg" alt="Qdrant" height="40" style="vertical-align: middle; margin: 0 5px;"/>
  <img src="https://camo.githubusercontent.com/6a7901b6824c7ccc698095d878b0d1829a757bcae5a8e8ad47d913a184b51a3f/68747470733a2f2f692e696d6775722e636f6d2f596a5155534f6b2e706e67" alt="Docker" height="40" style="vertical-align: middle; margin: 0 5px;"/>
  <img src="https://avatars.githubusercontent.com/u/128686189?s=200&v=4" alt="Chainlit" height="40" style="vertical-align: middle; margin: 0 5px;"/>
</p>

<p align="center">
  <img src="dev/gif2.gif" alt="KittiesAI Demo1" width="800"/>
  <img src="dev/gif1.gif" alt="KittiesAI Demo2" width="800"/>
</p>

# About

**KittiesAI** — это продвинутая **Мульти-Агентная Система (Multi-Agent System)**, построенная на фреймворке `LangGraph`. Проект демонстрирует архитектуру распределения ролей (Separation of Concerns), где сложная задача разбивается на этапы и решается командой специализированных AI-агентов.

Система работает по принципу конвейера: от поиска сырых данных (в интернете или локальном коде) до их математической обработки в изолированной среде и финальной верстки красивого отчета.

### Команда агентов:
* **Supervisor:** мозг системы, анализирует интент юзера, отвечает на **smalltalk**, маршрутизирует задачи между агентами и следит за строгим соблюдением пайплайна с помощью встроенных **guardrails** (предохранителей от зацикливания).
* **Researcher:** специалист по поиску данных, умеет искать информацию в интернете(**Tavily API**), а так же фрагменты кода в локальной базе знаний (**RAG на Qdrant**).
* **Analyst:** программист, умеет писать **python**-скрипты для анализа данных и выполняет их в защищенной **docker**-песочнице.
* **Editor:** копирайтер, собирает сухие цифры и код от коллег и превращает их в идеально отформатированный **markdown**-отчет.

### Ключевые особенности проекта:
* **Strict Guardrails & State Management**: оркестратор защищен от бесконечных циклов и галлюцинаций (**supervisor** не может пропустить **analyst**, если нужен код, и не может завершить граф без финального отчета **editor**).
* **Hybrid RAG**: векторная БД (**Qdrant** + **FastEmbed** `multilingual-MiniLM`) позволяет **researcher** находить приватные алгоритмы в локальной кодовой базе, параллельно обращаясь к интернету.
* **Secure Sandbox Execution**: весь сгенерированный код автоматически тестируется и выполняется в изолированном **docker**-контейнере с ограничением по времени (**timeout**), памяти и без доступа к сети.
* **LLMOps Observability**: интеграция с **LangSmith** для пошагового трейсинга мыслей агентов, контроля потребления токенов и отладки графа в реальном времени.

---

# Hierarchy

```text
KittiesAI/
├── agents/                 # Промпты и логика AI-агентов
│   ├── analyst.py          # Агент-программист (Docker)
│   ├── editor.py           # Агент-копирайтер (Markdown)
│   ├── researcher.py       # Агент-поисковик (Web + RAG)
│   └── supervisor.py       # Оркестратор графа и роутер
├── core/                   # Ядро LangGraph
│   ├── graph.py            # Сборка узлов и связей (Edges)
│   └── state.py            # Типизация глобальной памяти (AgentState)
├── rag/                    # Скрипты для работы с документами
│   └── ingest.py           # Чанкинг (RecursiveCharacterTextSplitter) и загрузка в Qdrant
├── target_repo/            # Исходники для локальной базы знаний (RAG)
├── tools/                  # Инструменты агентов
│   ├── agent_tools.py      # Инициализация и @tool декораторы
│   ├── code_search.py      # Qdrant Client 
│   ├── sandbox.py          # Docker Client 
│   └── web_search.py       # Tavily Client 
├── .env                    # API ключи (Groq, Tavily, LangSmith)
├── cli.py                  # CLI интерфейс для 
├── config.py               # Инициализация LLM и переменных окружения
└──  ui.py                   # Интерфейс чата на Chainlit
```