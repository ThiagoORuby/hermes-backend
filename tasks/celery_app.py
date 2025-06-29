from celery import Celery

from core.settings import Settings

app = Celery("tasks", broker=Settings().BROKER_URL, include=["tasks.tasks"])


app.conf.beat_schedule = {
    "crawl-news-data-every-2-hours": {
        "task": "tasks.tasks.crawl_news_data",
        "schedule": 60 * 60 * 2,
    },
}

# app.conf.timezone = "America/Sao_Paulo"
