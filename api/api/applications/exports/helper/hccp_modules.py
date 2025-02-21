from datetime import datetime, timedelta

from bson import ObjectId

from api.applications.auth.helper.user import get_user
from api.applications.exports.helper.export import pdf_template


class Export:
    @classmethod
    def export_type(cls, type, module, db, date, *args, **kwargs):
        return getattr(cls, f"export_{type}")(module, db, date, *args, **kwargs)

    @classmethod
    def export_cleaning(cls, module, db, date, *args, **kwargs):
        today = datetime.now()
        if date is not None:
            today = datetime.combine(datetime.strptime(date, "%m/%Y"), datetime.min.time())
        nxt_mnth = today.replace(day=28) + timedelta(days=4)
        last = nxt_mnth - timedelta(days=nxt_mnth.day)
        header = {
            "day": "Giorno",
            "floor_cleaning": "Pavimento",
            "wallpaper_cleaning": "Parati",
            "window_cleaning": "Vetrine",
            "counter_cleaning": "Bancone",
            "tools_cleaning": "Utensili",
            "operator": "Operatore",
        }
        data_dict = cls.format_data(cls, db, str(module["_id"]), header, today, (last.day + 1))
        data_dict.insert(0, header)
        return {
            "file": pdf_template(
                "DISPENSA",
                f"OPERAZIONI DI PULIZIA DEL MESE {today.strftime('%m')} ANNO {today.strftime('%Y')}",
                data_dict,
                28,
                [],
                10,
                "P",
            )
        }

    @classmethod
    def export_kitchen_cleaning(cls, module, db, date, *args, **kwargs):
        today = datetime.now()
        if date is not None:
            today = datetime.combine(datetime.strptime(date, "%m/%Y"), datetime.min.time())
        nxt_mnth = today.replace(day=28) + timedelta(days=4)
        last = nxt_mnth - timedelta(days=nxt_mnth.day)
        header = {
            "day": "Giorno",
            "floor_cleaning": "Pavimento",
            "surfaces_cleaning": "Piani Lav.",
            "equipment_cleaning": "Attrezzature",
            "window_cleaning": "Finestre",
            "sinks_cleaning": "Lavelli",
            "operator": "Operatore",
        }
        data_dict = cls.format_data(cls, db, str(module["_id"]), header, today, (last.day + 1))
        data_dict.insert(0, header)
        return {
            "file": pdf_template(
                "CUCINA",
                f"OPERAZIONI DI PULIZIA DEL MESE {today.strftime('%m')} ANNO {today.strftime('%Y')}",
                data_dict,
                28,
                [],
                10,
                "P",
            )
        }

    @classmethod
    def export_fridge_check(cls, module, db, date, *args, **kwargs):
        today = datetime.now()
        if date is not None:
            today = datetime.combine(datetime.strptime(date, "%m/%Y"), datetime.min.time())
        nxt_mnth = today.replace(day=28) + timedelta(days=4)
        last = nxt_mnth - timedelta(days=nxt_mnth.day)
        header = {
            "day": "Giorno",
            "fridge1": "Frigo 1",
            "fridge2": "Frigo 2",
            "fridge3": "Frigo 3",
            "fridge4": "Frigo 4",
            "fridge5": "Frigo 5",
            "fridge6": "Frigo 6",
            "hour": "Orario",
            "operator": "Operatore",
        }
        data_dict = []
        data_dict = cls.format_fridge_data(cls, db, module, data_dict, today, (last.day + 1))

        data_dict.insert(0, header)
        return {
            "file": pdf_template(
                "SCHEDA TEMPERATURA RILEVATA",
                f"MESE {today.strftime('%m')} ANNO {today.strftime('%Y')}",
                data_dict,
                20,
                [],
                10,
                "P",
            )
        }

    def format_fridge_data(self, db, module, data_dict, now, last_day):
        for x in range(1, last_day):
            day = datetime.combine(now.date().replace(day=x), datetime.min.time())
            next_day = day + timedelta(1)
            data = db["tasks"].find_one(
                {
                    "resource.module": str(module["_id"]),
                    "start": {"$gte": day, "$lte": next_day},
                }
            )
            if data:
                hour = self.get_hours(self, data["log"]) if "log" in data else ""
                if data["status"] == "done":
                    operator = get_user(db, data["operator"]) if "operator" in data else ""
                    data_dict.append(
                        {
                            "day": str(x),
                            "fridge1": "X",
                            "fridge2": "X",
                            "fridge3": "X",
                            "fridge4": "X",
                            "fridge5": "X",
                            "fridge6": "X",
                            "hour": hour,
                            "operator": f"{operator['surname']} {operator['name']}" if operator else "",
                        }
                    )
                continue
            data_dict.append(
                {
                    "day": str(x),
                    "fridge1": "",
                    "fridge2": "",
                    "fridge3": "",
                    "fridge4": "",
                    "fridge5": "",
                    "fridge6": "",
                    "hour": "",
                    "operator": "",
                }
            )
        return data_dict

    @staticmethod
    def get_hours(self, log):
        log = log[-1]
        return log["date"].strftime("%H:%M")

    def format_data(self, db, id, header, now, last_day):
        data_dict = []
        for x in range(1, last_day):
            day = datetime.combine(now.date().replace(day=x), datetime.min.time())
            next_day = day + timedelta(1)
            data = list(db["tasks"].find({"resource.module": id, "start": {"$gte": day, "$lte": next_day}}))
            dat = {"day": str(x)}
            for el in header:
                if el != "day":
                    dat[el] = self.get_data(self, db, el, data)
                if el == "operator":
                    operator = get_user(db, data[0]["operator"]) if len(data) > 0 and "operator" in data else ""
                    dat[el] = f"{operator['surname']} {operator['name']}" if operator else ""
            data_dict.append(dat)
        return data_dict

    def get_data(self, db, type, data):
        if len(data) > 0:
            el = ""
            for element in data:
                el = (
                    "  -  "
                    if not element["status"] == "done"
                    else self.check_resource_type(self, db, type, element["resource"])
                )
                if el:
                    return el
                else:
                    continue
            return el
        else:
            return ""

    @staticmethod
    def check_resource_type(self, db, type, element):
        el = list(
            db["settings"].aggregate(
                [
                    {
                        "$match": {
                            "type": "task",
                            "settings.hccpModules._id": ObjectId(element["module"]),
                            "settings.hccpModules.modules._id": ObjectId(element["type"]),
                        }
                    },
                    {"$unwind": "$settings"},
                    {"$unwind": "$settings.hccpModules"},
                    {"$unwind": "$settings.hccpModules.modules"},
                    {
                        "$match": {
                            "type": "task",
                            "settings.hccpModules.modules._id": ObjectId(element["type"]),
                        }
                    },
                    {"$project": {"settings.hccpModules": 1}},
                ]
            )
        )
        if el[0]["settings"]["hccpModules"]["modules"]["name"] == type:
            return "X"
        else:
            return ""
