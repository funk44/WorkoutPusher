from datetime import date, timedelta

last_date = date.today().replace(day=1)
first_day = date.today().replace(day=1) - timedelta(days=last_date.day)

print(last_date, first_day)