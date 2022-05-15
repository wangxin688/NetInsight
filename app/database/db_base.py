import functools
import re

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base, declared_attr


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


def resolve_attr(obj, attr, default=None):
    try:
        return functools.reduce(getattr, attr.split("."), obj)
    except AttributeError:
        return default


class CustomBase:
    __repr_attrs__ = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)

    def serialize(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    @property
    def _id_str(self):
        ids = inspect(self).identity
        if ids:
            return "-".join([str(x) for x in ids] if len(ids) else str(ids[0]))
        return "None"

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__
        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError(
                    f"{self.__class__} has incorrect attribute {key} in __repr_attrs__"
                )
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, str)
            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + "..."
            if wrap_in_quote:
                value = f"'{value}'"
            values.append(value if single else f"{key}: {value}")

    def __repr__(self) -> str:
        id_str = ("#" + self._id_str) if self._id_str else ""
        return f'<{self.__class__.__name__} {id_str}{" "+self._repr_attrs_str if self._repr_attrs_str else ""}>'


Base = declarative_base(cls=CustomBase)
