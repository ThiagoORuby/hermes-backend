from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Post:
    __tablename__ = "posts"

    # init = False (campo não obrigatório na instanciação)
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    image_url: Mapped[Optional[str]]
    title: Mapped[str]
    url: Mapped[str]
    description: Mapped[str]
    date_published: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    source: Mapped[str]
    type: Mapped[Optional[str]]
