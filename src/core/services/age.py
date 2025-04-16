from datetime import date


def calculate_age(date_of_birth: date) -> int:
    today = date.today()
    age = today - date_of_birth
    return age.days // 365
