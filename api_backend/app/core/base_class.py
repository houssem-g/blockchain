from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr  # type: ignore


@as_declarative()
class Base:
    id: Any
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
