# Определяем StrEnum для order_by
from enum import StrEnum


class OrderBy(StrEnum):
    CREATED_AT = "created_at"
    ID = "id"
    BODY = "body"