import base64
from datetime import date, datetime, timedelta

from bson import ObjectId
from flask import jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

from api.applications.auth.helper.user import get_user
from api.applications.exports.helper.adult import (
    archive_adult_information_sheet,
    generate_adult_information_sheet,
)
from api.applications.exports.helper.export import (
    format_data,
    format_header,
    pdf_template,
)
from api.applications.exports.helper.hccp_modules import Export
from api.applications.exports.helper.logbook import generate_logbook
from api.applications.exports.helper.minor import (
    archive_minor_information_sheet,
    generate_ai_report_pdf,
    generate_minor_information_sheet,
)
from api.applications.minors.helper.minor import get_minor
from api.middleware.mongo import get_mongo


def exports_export_medication_get():
    db = get_mongo().cx.get_default_database()
    query = {}
    if len(request.args) > 0:
        today = datetime.combine(date.today(), datetime.min.time())
        subquery = {"$lte": today} if request.args.get("expired") == "true" else {"$gte": today}
        query = {"expiration_date": subquery}
        if request.args.get("disposed_of"):
            query["disposed_of"] = bool(request.args.get("disposed_of"))
    data_dict = list(
        db["medication"].find(
            query,
            {
                "_id": 0,
                "name": 1,
                "lotto": 1,
                "amount": 1,
                "expiration_date": 1,
                "disposed_of": 1,
            },
        )
    )
    for data in data_dict:
        data["amount"] = str(data["amount"])
        data["expiration_date"] = data["expiration_date"].strftime("%d/%m/%Y")
        data["disposed_of"] = "SI" if data["disposed_of"] else "No"
    data_dict.insert(
        0,
        {
            "name": "Nome",
            "lotto": "Lotto",
            "amount": "Quantità",
            "expiration_date": "Data di scadenza",
            "disposed_of": "Smaltito",
        },
    )

    return {"file": pdf_template("Farmaci", "", data_dict, 40, [], 10, "P")}


def exports_export_operators_get():
    db = get_mongo().cx.get_default_database()
    query = {}
    subquery = {}
    if len(request.args) > 0:
        if request.args.get("start_date"):
            start_date = datetime.combine(
                datetime.strptime(request.args.get("start_date"), "%d/%m/%Y"),
                datetime.min.time(),
            )
            subquery["$gte"] = start_date
        if request.args.get("end_date"):
            end_date = datetime.combine(
                datetime.strptime(request.args.get("end_date"), "%d/%m/%Y"),
                datetime.min.time(),
            )
            end_date += timedelta(days=1)
            subquery["$lte"] = end_date
        if request.args.get("start_date") or request.args.get("end_date"):
            query["start_date"] = subquery
        if request.args.get("operator"):
            query["userId"] = ObjectId(request.args.get("operator"))
    data_dict = list(db["attendance"].find(query, {"_id": 0, "start_date": 1, "userId": 1, "end_date": 1, "type": 1}))
    attendance_type = {
        "green": "Fisica",
        "red": "Rifiutata",
        "grey": "Manuale",
        "blue": "Accettata",
    }
    for data in data_dict:
        data["date"] = data["start_date"].strftime("%d/%m/%Y")
        data["start_date"] = data["start_date"].strftime("%H:%M")
        data["end_date"] = data["end_date"].strftime("%H:%M") if data["end_date"] is not None else "In corso"
        operator = get_user(db, data["userId"])
        del data["userId"]
        if operator:
            data["name"] = f"{operator['surname']} {operator['name']}"
            data["role"] = operator["role"]["label"] if "role" in operator else ""
        else:
            data["name"] = ""
            data["role"] = ""
        data["type"] = attendance_type[data["type"]]
    data_dict = list(filter(lambda x: x["name"] != "", data_dict))
    data_dict.insert(
        0,
        {
            "date": "Data",
            "name": "Nominativo",
            "role": "Ruolo",
            "start_date": "Entrata",
            "end_date": "Uscita",
            "type": "Tipologia Timbratura",
        },
    )
    return {"file": pdf_template("Registro presenze operatori", "", data_dict, 30, [], 10, "P")}


def exports_export_minors_get():
    db = get_mongo().cx.get_default_database()
    today = datetime.now()
    if len(request.args) > 0:
        today = datetime.combine(datetime.strptime(request.args.get("date"), "%m/%Y"), datetime.min.time())
    data_dict = list(db["children"].find({}, {"_id": 1, "name": 1, "surname": 1, "fiscal_code": 1}))
    nxt_mnth = today.replace(day=28) + timedelta(days=4)
    last = nxt_mnth - timedelta(days=nxt_mnth.day)
    data_dict = format_data(db, today, data_dict, (last.day + 1))
    header = {"name": "Minore"}
    header = format_header(header, (last.day + 1))
    data_dict.insert(0, header)

    column_width = [8 for x in range(1, (last.day + 1))]
    column_width.insert(0, 40)
    first = today
    if first.day != 1:
        first = datetime.combine(date.today(), datetime.min.time())
        first = first.replace(day=1)
    return {
        "file": pdf_template(
            f"Registro presenze minori ( {first.strftime('%d/%m/%Y')}-{last.strftime('%d/%m/%Y')} )",
            "",
            data_dict,
            column_width,
            [],
            7,
            "L",
        )
    }


def exports_export_minor_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    data_dict = db["children"].find_one({"_id": ObjectId(arg)}, {"_id": 1, "info_sheet": 1})
    if "info_sheet" in data_dict:
        return {"file": generate_minor_information_sheet(data_dict["info_sheet"])}
    else:
        return {"file": generate_minor_information_sheet(None)}


def exports_export_minor_ai_get(minor_id):
    db = get_mongo().cx.get_default_database()
    data_dict = db["children"].find_one({"_id": ObjectId(minor_id)}, {"_id": 1, "info_sheet": 1})
    if "info_sheet" in data_dict:
        return {"file": generate_ai_report_pdf(data_dict["info_sheet"])}
    else:
        return {"file": generate_ai_report_pdf(None)}


def exports_archive_minor_get():
    db = get_mongo().cx.get_default_database()
    sheets = list(db["minor_info_sheets"].find({}, {"pdf_data": 0}))
    return sheets


def exports_archive_minor_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    sheet = db["minor_info_sheets"].find_one({"_id": ObjectId(arg)})
    pdf_data = sheet["pdf_data"]
    decoded_data = base64.b64decode(pdf_data)
    return decoded_data


# Get Operator Report
def exports_operator_report_get(reportId):
    db = get_mongo().cx.get_default_database()
    sheet = db["operator_reports"].find_one({"_id": ObjectId(reportId)})
    pdf_data = sheet["pdf_data"]
    decoded_data = base64.b64decode(pdf_data)
    return decoded_data


def exports_archive_adult_get():
    db = get_mongo().cx.get_default_database()
    sheets = list(db["adult_info_sheets"].find({}, {"pdf_data": 0}))
    return sheets


def exports_archive_adult_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    sheet = db["adult_info_sheets"].find_one({"_id": ObjectId(arg)})
    pdf_data = sheet["pdf_data"]
    decoded_data = base64.b64decode(pdf_data)
    return decoded_data


def exports_archive_minor_arg_post(arg):
    db = get_mongo().cx.get_default_database()
    info_children = db["children"].find_one({"_id": ObjectId(arg)})
    data_dict = db["children"].find_one({"_id": ObjectId(arg)}, {"_id": 1, "info_sheet": 1})

    if "info_sheet" in data_dict:
        if data_dict.get("info_sheet").get("semestral_comunication").get("date"):
            result = archive_minor_information_sheet(db, info_children, data_dict["info_sheet"])
        else:
            return {"error: unable to archive document, no date": False}, 404
    else:
        return {"error: unable to archive document, no infosheet": False}, 404
    if result.acknowledged:
        return {"success": True}
    else:
        return {"error: unable to archive document": False}, 404


def exports_archive_adult_arg_post(arg):
    db = get_mongo().cx.get_default_database()
    info_adult = db["adults"].find_one({"_id": ObjectId(arg)})
    data_dict = db["adults"].find_one({"_id": ObjectId(arg)}, {"_id": 1, "info_sheet": 1})
    if "info_sheet" in data_dict:
        if data_dict.get("info_sheet").get("semestral_comunication").get("date"):
            result = archive_adult_information_sheet(db, info_adult, data_dict["info_sheet"])
        else:
            return {"error: unable to archive document, no date": False}, 404
    else:
        return {"error: unable to archive document, no infosheet": False}, 404
    if result.acknowledged:
        return {"success": True}
    else:
        return {"error: unable to archive document": False}, 404


def exports_export_call_logs_get():
    db = get_mongo().cx.get_default_database()
    query = {}
    subquery = {}
    if len(request.args) > 0:
        if request.args.get("start_date"):
            start_date = datetime.combine(
                datetime.strptime(request.args.get("start_date"), "%d/%m/%Y"),
                datetime.min.time(),
            )
            subquery["$gte"] = start_date
        if request.args.get("end_date"):
            end_date = datetime.combine(
                datetime.strptime(request.args.get("end_date"), "%d/%m/%Y"),
                datetime.min.time(),
            )
            end_date += timedelta(days=1)
            subquery["$lte"] = end_date
        if request.args.get("start_date") or request.args.get("end_date"):
            query["date"] = subquery
        if request.args.get("operator"):
            query["creation_user"] = ObjectId(request.args.get("operator"))
        if request.args.get("minor"):
            query["minors"] = ObjectId(request.args.get("minor"))
    data_dict = list(
        db["callLogs"].find(
            query,
            {
                "_id": 0,
                "date": 1,
                "creation_user": 1,
                "minors": 1,
                "phone_call_issuer": 1,
                "notes": 1,
            },
        )
    )
    set_height = []
    for data in data_dict:
        data["hour"] = data["date"].strftime("%H:%M")
        data["date"] = data["date"].strftime("%d/%m/%Y")
        operator = get_user(db, data["creation_user"])
        del data["creation_user"]
        if operator:
            data["operator"] = (
                operator["companyName"]
                if (operator["type"] == "admin" or operator["type"] == "superadmin")
                else f"{operator['surname']} {operator['name']}"
            )
        else:
            data["operator"] = ""
        minors = ""
        for minor in data["minors"]:
            minor = get_minor(db, minor)
            if minor:
                minors += f"{minor['surname']} {minor['name']} \n"
        data["minors"] = minors
        set_height.append((5 * len(data["notes"]) / 60) if (len(data["notes"]) / 60) > 1 else 13)
    data_dict.insert(
        0,
        {
            "date": "Data",
            "hour": "Ora",
            "minors": "Minore/i destinatari",
            "phone_call_issuer": "Emittente telefonata",
            "notes": "Note particolari",
            "operator": "Operatore",
        },
    )
    columns_width = [20, 15, 30, 20, 90, 30]
    return {"file": pdf_template("Registro telefonate", "", data_dict, columns_width, set_height, 10, "P")}


def exports_export_hccp_arg_get(type, date):
    if type.strip() != "":
        db = get_mongo().cx.get_default_database()
        hccp_modules = db["settings"].find_one({"type": "task"}, {"settings.hccpModules": 1})
        if hccp_modules:
            module = [item for item in hccp_modules["settings"]["hccpModules"] if item["_id"] == ObjectId(type)]
            if module[0]:
                return Export.export_type(
                    module[0]["name"],
                    module[0],
                    db,
                    date if date.strip() != "" else None,
                )
        else:
            raise NotFound()
    else:
        return jsonify([])


def exports_export_logbook_get(date):
    db = get_mongo().cx.get_default_database()
    day = datetime.now()
    if date.strip() != "":
        day = datetime.combine(datetime.strptime(date, "%d/%m/%Y"), datetime.min.time())
    else:
        day = datetime.combine(day, datetime.min.time())
    logbooks = db["logbook"].find({"date": day})
    _id = ObjectId(request.args.get("operator")) if request.args.get("operator") else None
    if logbooks:
        return {"file": generate_logbook(db, day, logbooks, _id)}
    else:
        return {"file": generate_logbook(db, day, None, None)}


def exports_export_accounting_post(body):
    data_dict = []
    stringa_iva = f'IVA ({body["valore_iva"]}%)'
    dict_intestazione = {"tipo": " ", "imponibile": "Imponibile", "iva": stringa_iva, "total": "Importo Totale"}
    dict_entrate = {
        "tipo": "Entrate",
        "imponibile": str(body["imponibile"][0]),
        "iva": str(body["iva"][0]),
        "total": str(body["total"][0]),
    }
    dict_uscite = {
        "tipo": "Uscite",
        "imponibile": str(body["imponibile"][1]),
        "iva": str(body["iva"][1]),
        "total": str(body["total"][1]),
    }
    dict_differenza = {
        "tipo": "Differenza",
        "imponibile": str(body["imponibile"][2]),
        "iva": str(body["iva"][2]),
        "total": str(body["total"][2]),
    }

    data_dict.append(dict_intestazione)
    data_dict.append(dict_entrate)
    data_dict.append(dict_uscite)
    data_dict.append(dict_differenza)

    periodo = body.get("periodo")

    if periodo:
        return {"file": pdf_template("Rendicontazione - " + body.get("periodo"), "", data_dict, 40, [], 10, "P")}
    else:
        return {"file": pdf_template("Rendicontazione", "", data_dict, 40, [], 10, "P")}


def exports_export_adults_get():
    db = get_mongo().cx.get_default_database()
    today = datetime.now()
    if len(request.args) > 0:
        today = datetime.combine(datetime.strptime(request.args.get("date"), "%m/%Y"), datetime.min.time())
    data_dict = list(db["adults"].find({}, {"_id": 1, "name": 1, "surname": 1, "fiscal_code": 1}))
    nxt_mnth = today.replace(day=28) + timedelta(days=4)
    last = nxt_mnth - timedelta(days=nxt_mnth.day)
    data_dict = format_data(db, today, data_dict, (last.day + 1))
    header = {"name": "Adulto"}
    header = format_header(header, (last.day + 1))
    data_dict.insert(0, header)

    column_width = [8 for x in range(1, (last.day + 1))]
    column_width.insert(0, 40)
    first = today
    if first.day != 1:
        first = datetime.combine(date.today(), datetime.min.time())
        first = first.replace(day=1)
    return {
        "file": pdf_template(
            f"Registro presenze adulti ( {first.strftime('%d/%m/%Y')}-{last.strftime('%d/%m/%Y')} )",
            "",
            data_dict,
            column_width,
            [],
            7,
            "L",
        )
    }


def exports_export_adult_arg_get(arg):
    db = get_mongo().cx.get_default_database()
    data_dict = db["adults"].find_one({"_id": ObjectId(arg)}, {"_id": 1, "info_sheet": 1})
    if data_dict is None:
        raise BadRequest("Adulto non esiste")
    if "info_sheet" in data_dict:
        return {"file": generate_adult_information_sheet(data_dict["info_sheet"])}
    else:
        return {"file": generate_adult_information_sheet(None)}
