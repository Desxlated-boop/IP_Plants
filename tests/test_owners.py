"""Тесты класса Owner и функций работы с владельцами."""
import pytest

from models import Owner
from models.owners import add_owner, find_owner, find_owner_by_id


def test_owner_creation_and_str():
    owner = Owner(1, "Анна", "anna@example.com")
    assert owner.id == 1
    assert owner.name == "Анна"
    assert "anna@example.com" in str(owner)


def test_owner_from_data():
    owner = Owner.from_data(
        {"id": 2, "name": "Иван", "email": "ivan@example.com"}
    )
    assert isinstance(owner, Owner)
    assert owner.id == 2


def test_add_and_find_owner():
    owners = []
    first = add_owner(owners, "Анна", "anna@example.com")
    second = add_owner(owners, "Иван", "ivan@example.com")
    assert (first.id, second.id) == (1, 2)
    assert find_owner(owners, "ИВАН") == [second]
    assert find_owner_by_id(owners, 1) is first
    assert find_owner_by_id(owners, 99) is None


def test_add_owner_empty_name_rejected():
    with pytest.raises(ValueError):
        add_owner([], "  ", "x@example.com")
