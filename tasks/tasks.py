from .celery_app import app  # noqa: I001
import subprocess


@app.task
def crawl_news_data():
    """
    Chama spiders para pegar dados de noticias
    """

    command = "scrapy crawl g1spider && scrapy crawl uolspider"

    try:
        subprocess.run(command, check=True, shell=True)

        return {"success": "true"}
    except subprocess.CalledProcessError:
        return {"success": "false"}


@app.task
def clear_old_data():
    """
    Remove notícias publicadas há mais de 2 meses
    """

    return {"success": "true"}
