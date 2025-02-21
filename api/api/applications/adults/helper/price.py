from datetime import datetime, timedelta


def calcola_ricavi_tra_date(data_inizio, data_fine, adult_price):
    total_ricavi = 0
    # data_inizio = datetime.strptime(data_inizio, "%Y-%m-%d")
    # data_fine = datetime.strptime(data_fine, "%Y-%m-%d")

    if data_inizio > data_fine:
        return 0

    differenza = data_fine - data_inizio

    for i in range(differenza.days + 1):
        data_corrente = data_inizio + timedelta(days=i)
        total_ricavi += calcola_value_by_date(data_corrente, adult_price)

    return total_ricavi


def calcola_value_by_date(date, adult_price):
    history_ordinata = sorted(adult_price["history"], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d"))

    if len(history_ordinata) == 0:
        return 0
    if date < datetime.strptime(history_ordinata[0]["timestamp"], "%Y-%m-%d").date():
        return 0
    if date >= datetime.strptime(history_ordinata[-1]["timestamp"], "%Y-%m-%d").date():
        return history_ordinata[-1]["value"]
    for i in range(0, len(history_ordinata) - 1):
        if (
            datetime.strptime(history_ordinata[i]["timestamp"], "%Y-%m-%d").date()
            <= date
            < datetime.strptime(history_ordinata[i + 1]["timestamp"], "%Y-%m-%d").date()
        ):
            return history_ordinata[i]["value"]


def calculate_intersection(start_date, end_date, entry_date, disposal_date):
    today = datetime.now().date() + timedelta(days=1)

    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").date()

    if disposal_date is not None and disposal_date != "":
        disposal_date = datetime.strptime(disposal_date, "%d/%m/%Y").date() + timedelta(days=1)
    else:
        disposal_date = today
    if entry_date is not None and entry_date != "":
        entry_date = datetime.strptime(entry_date, "%d/%m/%Y").date()
    else:
        entry_date = today

    intersection_start = max(start_date, entry_date)
    intersection_end = min(end_date, disposal_date, today)

    if intersection_start <= intersection_end:
        intersection_days = (intersection_end - intersection_start).days
    else:
        intersection_days = 0

    return intersection_start, intersection_end, intersection_days
