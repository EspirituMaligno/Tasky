from datetime import date


def calculate_age(date_of_birth: date) -> int:
    today = date.today()
    return today.year - date_of_birth.year
