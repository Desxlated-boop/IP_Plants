"""Класс Owner (владелец растений) и функции работы с владельцами."""
from typing import List, Optional

from utils import next_id


class Owner:
    """Владелец, которому принадлежат растения."""

    def __init__(self, owner_id: int, name: str, email: str) -> None:
        """Создать объект владельца."""
        self.id = owner_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "Owner":
        """Создать владельца из словаря (данные JSON)."""
        return cls(data["id"], data["name"], data["email"])

    def __str__(self) -> str:
        """Строковое представление владельца."""
        return f"[{self.id}] {self.name} <{self.email}>"


def add_owner(owners: List[Owner], name: str, email: str) -> Owner:
    """Создать владельца и добавить его в коллекцию."""
    if not name.strip():
        raise ValueError("Имя владельца не может быть пустым.")
    owner = Owner(next_id(owners), name.strip(), email.strip())
    owners.append(owner)
    return owner


def find_owner(owners: List[Owner], query: str) -> List[Owner]:
    """Найти владельцев по части имени или e-mail."""
    query = query.lower()
    return [
        owner for owner in owners
        if query in owner.name.lower() or query in owner.email.lower()
    ]


def find_owner_by_id(
    owners: List[Owner],
    owner_id: Optional[int],
) -> Optional[Owner]:
    """Найти владельца по идентификатору."""
    for owner in owners:
        if owner.id == owner_id:
            return owner
    return None


def display_owners(owners: List[Owner]) -> None:
    """Вывести владельцев в консоль."""
    if not owners:
        print("Владельцев пока нет.")
    for owner in owners:
        print(owner)
