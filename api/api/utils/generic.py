import datetime


def get_dayofweek(data):
    if isinstance(data, str):  # Se data è una stringa, convertila in un oggetto datetime
        data_datetime = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
    elif isinstance(data, datetime.datetime):  # Se data è già un oggetto datetime, usa direttamente quello
        data_datetime = data
    else:
        raise ValueError("Il parametro data deve essere una stringa o un oggetto datetime")
    giorni_settimana_italiano = {0: "lun", 1: "mar", 2: "mer", 3: "gio", 4: "ven", 5: "sab", 6: "dom"}
    giorno_settimana = giorni_settimana_italiano[data_datetime.weekday()]
    return giorno_settimana


def get_shift(data):
    hour = data.hour
    if 8 <= hour < 14:
        return "Mattina"
    elif 14 <= hour < 20:
        return "Pomeriggio"
    else:
        return "Sera"
