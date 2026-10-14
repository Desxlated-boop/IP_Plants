"""Класс WateringLog (запись о поливе) и функции журнала поливов."""
from datetime import date
from typing import List

from utils import next_id

from .plants import DATE_FORMAT, Plant


class WateringLog:
    """Запись журнала: когда и какое растение полили."""

    def __init__(
        self,
        log_id: int,
        plant: Plant,
        watered_on: str,
        note: str = "",
    ) -> None:
        """Создать запись о поливе."""
        self.id = log_id
        self.plant = plant
        self.watered_on = watered_on
        self.note = note

    def __str__(self) -> str:
        """Строковое представление записи."""
        text = f"{self.watered_on}: {self.plant.name}"
        if self.note:
            text += f" ({self.note})"
        return text


def add_watering(
    logs: List[WateringLog],
    plant: Plant,
    watered_on: date,
    note: str = "",
) -> WateringLog:
    """Добавить запись о поливе и обновить дату полива растения."""
    log = WateringLog(
        next_id(logs),
        plant,
        watered_on.strftime(DATE_FORMAT),
        note,
    )
    logs.append(log)
    if log.watered_on >= plant.last_watered:
        plant.water(watered_on)
    return log


def find_waterings_for_plant(
    logs: List[WateringLog],
    plant_id: int,
) -> List[WateringLog]:
    """Вернуть записи журнала для одного растения (новые первыми)."""
    own = [log for log in logs if log.plant.id == plant_id]
    return sorted(own, key=lambda log: log.watered_on, reverse=True)


def sort_waterings(logs: List[WateringLog]) -> List[WateringLog]:
    """Отсортировать журнал: новые записи первыми."""
    return sorted(logs, key=lambda log: log.watered_on, reverse=True)


def display_waterings(logs: List[WateringLog]) -> None:
    """Вывести журнал поливов в консоль."""
    if not logs:
        print("Журнал поливов пуст.")
    for log in sort_waterings(logs):
        print(log)
