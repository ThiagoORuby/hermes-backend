# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from datetime import datetime

from dateutil import parser
from itemadapter.adapter import ItemAdapter

from core.database import get_session
from core.models import Post


class NewsScrapperPipeline:
    def process_item(self, item, spider):  # noqa: PLR6301
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == "type":
                value = adapter.get(field_name)
                if value:
                    adapter[field_name] = value.lower()
            if field_name == "description":
                value = adapter.get(field_name)
                if not value:
                    adapter[field_name] = ""
            if field_name == "date_published":
                value = adapter.get(field_name)
                if value and type(value) is not datetime:
                    adapter[field_name] = parser.isoparse(value)
        return item


class PostgresPipeline:
    def __init__(self):
        self.session = next(get_session())

    def process_item(self, item, spider):
        if self.session.query(Post).filter_by(url=item["url"]).first():
            print("Has already been saved")
            return item

        post = Post(**item)

        self.session.add(post)
        self.session.commit()

        return item

    def close_spider(self, spider):
        self.session.close()
