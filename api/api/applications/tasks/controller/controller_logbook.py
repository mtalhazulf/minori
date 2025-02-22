import base64
from datetime import date, datetime, timedelta

from bson import ObjectId

from api.applications.auth.helper.user import get_user
from api.applications.exports.helper.minor import generate_ai_report_pdf
from api.applications.tasks.helper.logbook import update_logbook
from api.middleware.mongo import get_mongo
from api.utils import jsonify_mongo
from api.utils.openai import generate_report


def tasks_logbook_get(days_or_date):
    db = get_mongo().cx.get_default_database()
    today = datetime.combine(date.today(), datetime.min.time())
    end = today + timedelta(1)
    try:
        start = today - timedelta(int(days_or_date))
    except ValueError:
        start = datetime.strptime(days_or_date, "%Y-%m-%d")
        end = start + timedelta(1)
    query = {"date": {"$gte": start, "$lt": end}}
    logs = list(db["logbook"].find(query))
    if logs:
        for log in logs:
            log["date"] = log["date"].strftime("%Y-%m-%d %H:%M:%S")
            if "notes" in log:
                for note in log["notes"]:
                    operator = get_user(db, ObjectId(note["operator"]))
                    if operator:
                        note["operator"] = operator
                    else:
                        note["operator"] = None
            if "tasks" in log:
                for task in log["tasks"]:
                    operator = get_user(db, ObjectId(task["operator"]))
                    if operator:
                        task["operator"] = operator
                    else:
                        task["operator"] = None
            if "notebook_tasks" in log:
                for notebook_task in log["notebook_tasks"]:
                    operator = get_user(db, ObjectId(notebook_task["operator"]))
                    if operator:
                        notebook_task["operator"] = operator
                    else:
                        notebook_task["operator"] = None
        return jsonify_mongo(logs)
    else:
        return jsonify_mongo({})


def tasks_operator_report_get(operator_id, start_date, end_date):
    db = get_mongo().cx.get_default_database()

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    tasks_query = {"operator": ObjectId(operator_id), "creation_date": {"$gte": start, "$lte": end}}
    tasks = list(db["tasks"].find(tasks_query))

    logbook_query = {
        "date": {"$gte": start, "$lte": end},
        "$or": [{"tasks.operator": ObjectId(operator_id)}, {"notebook_tasks.operator": ObjectId(operator_id)}],
    }
    logbook_entries = list(db["logbook"].find(logbook_query))

    # print("\n\n\n######@@@@@@@@@########")
    # print(logbook_entries)
    # print("\n\n\n ######@@@@@@@@@######## \n\n\n ")
    if len(logbook_entries) == 0:
        return jsonify_mongo({
            "success": False,
            "message": "Nessuna voce del registro trovata per l'intervallo di date e l'operatore selezionati."
        })
    for task in tasks:
        task["creation_date"] = task["creation_date"].strftime("%Y-%m-%d %H:%M:%S")
        if "log" in task:
            for log_entry in task["log"]:
                log_entry["date"] = log_entry["date"].strftime("%Y-%m-%d %H:%M:%S")

        task["notes"] = []

        for entry in logbook_entries:
            if "tasks" in entry:
                for logbook_task in entry["tasks"]:
                    if logbook_task["id"] == task["_id"] and "notes" in logbook_task:
                        task["notes"].append(
                            {"date": entry["date"].strftime("%Y-%m-%d %H:%M:%S"), "note": logbook_task["notes"]}
                        )
            if "notebook_tasks" in entry:
                for notebook_task in entry["notebook_tasks"]:
                    if notebook_task["id"] == task["_id"] and "notes" in notebook_task:
                        task["notes"].append(
                            {"date": entry["date"].strftime("%Y-%m-%d %H:%M:%S"), "note": notebook_task["notes"]}
                        )

    for entry in logbook_entries:
        entry["date"] = entry["date"].strftime("%Y-%m-%d %H:%M:%S")
        if "tasks" in entry:
            entry["tasks"] = [task for task in entry["tasks"] if task["operator"] == ObjectId(operator_id)]
        if "notebook_tasks" in entry:
            entry["notebook_tasks"] = [
                task for task in entry["notebook_tasks"] if task["operator"] == ObjectId(operator_id)
            ]

    # Get operator details
    operator = get_user(db, ObjectId(operator_id))

    tasks_details = {
        "start_date": start_date,
        "end_date": end_date,
        "tasks": tasks,
        "logbook_entries": logbook_entries,
        "total_tasks": len(tasks),
        "total_logbook_entries": len(logbook_entries),
    }

    # Call OpenAI API
    ai_report = generate_report(tasks_details)


    print("\n\n\n######@@@@@@@@@########")
    print(ai_report)
    print("\n\n\n ######@@@@@@@@@######## \n\n\n ")


    # Generate PDF
    pdf_content = generate_ai_report_pdf(
        {"operator": operator, "start_date": start_date, "end_date": end_date, "ai_report": ai_report}
    )

    # Store in MongoDB
    report_document = {
        "operator_id": ObjectId(operator_id),
        "name": f"{operator['name']} {operator['surname']}",
        "pdf_data": pdf_content,
        "pdf_creation_date": datetime.now(),
        "pdf_selected_date_range": {"start": start_date, "end": end_date},
    }

    result = db["operator_reports"].insert_one(report_document)

    if result.acknowledged:
        return jsonify_mongo(
            {
                "success": True,
                "report_id": str(result.inserted_id),
                "message": "Operator report generated and stored successfully.",
            }
        )
    else:
        return jsonify_mongo({"success": False, "message": "Failed to store the operator report."}), 500


def tasks_report_get(report_id):
    db = get_mongo().cx.get_default_database()
    report = db["operator_reports"].find_one({"_id": ObjectId(report_id)})
    if report:
        pdf_data = report["pdf_data"]
        decoded_data = base64.b64decode(pdf_data)
        return decoded_data
    else:
        return jsonify_mongo({"success": False, "message": "Report not found."}), 404


def tasks_reports_get():
    db = get_mongo().cx.get_default_database()
    reports = list(db["operator_reports"].find({}, {"pdf_data": 0}))
    return reports


def tasks_logbook_put(body):
    db = get_mongo().cx.get_default_database()
    if body["notes"]:
        task_id = ObjectId(body.get("task")) if "task" in body else None
        update_logbook(db, task_id, "notes", body["date"], body["shift"], body["notes"])
