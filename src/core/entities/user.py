from datetime import date, datetime


class User:
    def __init__(
        self,
        name: str,
        surname: str,
        date_of_birth: date,
        username: str,
        password: str,
        age: int | None = None,
        is_active: bool | None = True,
        id: int | None = None,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.age = age
        self.username = username
        self.password = password
        self.is_active = is_active
        self.created_at = created_at

    def deactivate(self):
        self.is_active = False
