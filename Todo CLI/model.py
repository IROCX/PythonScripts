from datetime import datetime


class Todo:
    def __init__(
        self,
        task,
        category,
        dateAdded=None,
        dateCompleted=None,
        status=None,
        position=None,
    ) -> None:

        self.task = task
        self.category = category
        self.dateAdded = dateAdded if dateAdded else datetime.now().isoformat()
        self.dateCompleted = dateCompleted
        self.status = status if status else 0  # 0 - open & 1 - complete
        self.position = position

    def __repr__(self) -> str:
        return f"{self.task} {self.category} {self.dateAdded} {self.dateCompleted} {self.status} {self.position}"
