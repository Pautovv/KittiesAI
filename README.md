```
KittiesAI/
├── .env                    
├── main.py                 # Точка входа (запуск графа в консоли)
├── app_ui.py               # Продвинутый UI на базе Chainlit
├── config.py               # Инициализация LLM и интеграция с LangSmith
├── core/                   
│   ├── state.py            # Global State (общая память для всех агентов)
│   └── graph.py            # Сборка MAS-графа (узлы и связи)
├── agents/                 # ИИ-Сотрудники
│   ├── __init__.py
│   ├── supervisor.py       # Менеджер (Решает, кто работает следующим)
│   ├── researcher.py       # Искатель (Использует web_search)
│   ├── analyst.py          # Аналитик (Использует sandbox для расчетов/графиков)
│   └── editor.py           # Редактор (Критик, факт-чекер и писатель отчета)
└── tools/                  # Инструменты
    ├── sandbox.py          # DockerSandbox
    └── web_search.py       # TavilyClient
```