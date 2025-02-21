import base64
from datetime import timedelta

from bson import ObjectId
from fpdf import FPDF, HTMLMixin

from api.applications.auth.helper.user import get_user
from api.applications.minors.helper.minor import get_minor
from api.font import FONT_DEJAVU_SANS_CONDENSED
from api.utils.generic import get_shift


class PDF(FPDF, HTMLMixin):
    def section_1(self, date, title):
        self.cell(
            0,
            h=5,
            txt=date.strftime("%d/%m/%Y"),
            border=0,
            ln=0,
            align="",
            fill=False,
            link="",
        )
        self.set_font(size=16)
        self.set_x(80)
        self.cell(
            0,
            h=5,
            txt=title,
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        self.set_font(size=11)

    def section_2(self, title, tasks, x, y):
        self.set_y(y)
        self.set_x(x)
        self.cell(
            0,
            h=5,
            txt=title,
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        x += 5
        turno_mattina = [dizionario for dizionario in tasks if dizionario["shifts"].lower() == "mattina"]
        turno_pomeriggio = [dizionario for dizionario in tasks if dizionario["shifts"].lower() == "pomeriggio"]
        turno_sera = [dizionario for dizionario in tasks if dizionario["shifts"].lower() == "sera"]
        for task in turno_mattina:
            y += 10
            self.set_y(y)
            self.set_x(x)
            self.cell(
                0,
                h=5,
                txt="Mattina",
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            y += 10
            self.line(x, y, x + 2, y)
            self.set_y(y - 3)
            self.set_x(x + 10)
            self.cell(
                0,
                h=5,
                txt=task["title"],
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_font(size=9)
            self.set_y(y - 3)
            self.set_x(x + 110)
            self.cell(
                0,
                h=5,
                txt="Operatore: ",
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_y(y - 3)
            self.set_x(x + 130)
            self.cell(
                0,
                h=5,
                txt=task["operator"],
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_font(size=8)

            self.set_y(y + 2)
            self.set_x(x + 10)
            x, y = self.get_description_chunks(x, y, task["description"], 109)

            if "minors" in task and task["minors"].strip() != "":
                self.set_y(y + 4)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Minori : {task['minors']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if "minor" in task and task["minor"].strip() != "":
                self.set_y(y + 5)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Minore : {task['minor']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if "resource" in task and task["resource"].strip() != "":
                self.set_y(y + 4)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Modulo HCCP : {task['resource']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if "notes" in task and task["notes"].strip() != "":
                self.set_y(y + 8)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Note : {task['notes']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            self.set_font(size=11)
            y += 3
        for task in turno_pomeriggio:
            y += 14
            self.set_y(y)
            self.set_x(x)
            self.cell(
                0,
                h=5,
                txt="Pomeriggio",
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            y += 10
            self.line(x, y, x + 2, y)
            self.set_y(y - 3)
            self.set_x(x + 10)
            self.cell(
                0,
                h=5,
                txt=task["title"],
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_font(size=9)
            self.set_y(y - 3)
            self.set_x(x + 110)
            self.cell(
                0,
                h=5,
                txt="Operatore: ",
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_y(y - 3)
            self.set_x(x + 130)
            self.cell(
                0,
                h=5,
                txt=task["operator"],
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_font(size=8)

            self.set_y(y + 2)
            self.set_x(x + 10)
            x, y = self.get_description_chunks(x, y, task["description"], 109)

            if "minors" in task and task["minors"].strip() != "":
                self.set_y(y + 4)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Minori : {task['minors']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if "minor" in task and task["minor"].strip() != "":
                self.set_y(y + 5)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Minore : {task['minor']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if "resource" in task and task["resource"].strip() != "":
                self.set_y(y + 4)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Modulo HCCP : {task['resource']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if "notes" in task and len(task["notes"]) != 0:
                self.set_y(y + 8)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Note : {task['notes']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            self.set_font(size=11)
            y += 3
        for task in turno_sera:
            y += 14
            self.set_y(y)
            self.set_x(x)
            self.cell(
                0,
                h=5,
                txt="Pomeriggio",
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            y += 10
            self.line(x, y, x + 2, y)
            self.set_y(y - 3)
            self.set_x(x + 10)
            self.cell(
                0,
                h=5,
                txt=task["title"],
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_font(size=9)
            self.set_y(y - 3)
            self.set_x(x + 110)
            self.cell(
                0,
                h=5,
                txt="Operatore: ",
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_y(y - 3)
            self.set_x(x + 130)
            self.cell(
                0,
                h=5,
                txt=task["operator"],
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_font(size=8)

            self.set_y(y + 2)
            self.set_x(x + 10)
            x, y = self.get_description_chunks(x, y, task["description"], 109)

            if "minors" in task and task["minors"].strip() != "":
                self.set_y(y + 4)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Minori : {task['minors']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if "minor" in task and task["minor"].strip() != "":
                self.set_y(y + 5)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Minore : {task['minor']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if "resource" in task and task["resource"].strip() != "":
                self.set_y(y + 4)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Modulo HCCP : {task['resource']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            if "notes" in task and task["notes"].strip() != "":
                self.set_y(y + 8)
                self.set_x(x + 12)
                self.cell(
                    0,
                    h=5,
                    txt=f"Note : {task['notes']}",
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
            self.set_font(size=11)
            y += 3

        return x - 5, y + 20

    def section_3(self, title, notes, x, y):
        # self.set_y(y)
        # self.set_x(x)
        # self.cell(
        #     0,
        #     h=5,
        #     txt=title,
        #     border=0,
        #     ln=1,
        #     align="",
        #     fill=False,
        #     link="",
        # )
        x += 5
        turno_mattina = [dizionario for dizionario in notes if dizionario["shifts"].lower() == "mattina"]
        turno_pomeriggio = [dizionario for dizionario in notes if dizionario["shifts"].lower() == "pomeriggio"]
        turno_sera = [dizionario for dizionario in notes if dizionario["shifts"].lower() == "sera"]

        y += 10
        self.set_y(y)
        self.set_x(x)
        self.set_font(size=11)
        self.cell(
            0,
            h=5,
            txt="Mattina:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )
        for note in turno_mattina:
            if y + 6 > 275:
                self.add_page()
                y = 10
            self.set_y(y)

            self.set_y(y + 6)
            self.set_x(x + 5)
            self.set_font(size=10)
            self.cell(
                0,
                h=5,
                txt="Operatore: ",
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_y(y + 6)
            self.set_x(x + 20 + 5)
            self.set_font(size=10)
            self.cell(
                0,
                h=5,
                txt=note["operator"],
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            if y + 11 > 275:
                self.add_page()
                y = 10
            self.set_y(y)
            self.set_y(y + 11)
            self.set_x(x + 5)
            self.set_font(size=9)
            x, y = self.get_description_chunks(x, y + 17, note["notes"], 158)
            # self.cell(
            #     0,
            #     h=5,
            #     txt=f"      {note['notes']}",
            #     border=0,
            #     ln=1,
            #     align="",
            #     fill=False,
            #     link="",
            # )
            # y += 10

        y += 10
        self.set_y(y)
        self.set_x(x)
        self.set_font(size=11)
        self.cell(
            0,
            h=5,
            txt="Pomeriggio:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )

        for note in turno_pomeriggio:
            if y + 6 > 275:
                self.add_page()
                y = 10
            self.set_y(y)

            self.set_y(y + 6)
            self.set_x(x + 5)
            self.set_font(size=10)
            self.cell(
                0,
                h=5,
                txt="Operatore: ",
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_y(y + 6)
            self.set_x(x + 20 + 5)
            self.set_font(size=10)
            self.cell(
                0,
                h=5,
                txt=note["operator"],
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            if y + 11 > 275:
                self.add_page()
                y = 10
            self.set_y(y)
            self.set_y(y + 11)
            self.set_x(x + 5)
            self.set_font(size=9)
            x, y = self.get_description_chunks(x, y + 17, note["notes"], 158)
            # self.cell(
            #     0,
            #     h=5,
            #     txt=f"      {note['notes']}",
            #     border=0,
            #     ln=1,
            #     align="",
            #     fill=False,
            #     link="",
            # )
            # y += 10

        y += 10
        self.set_y(y)
        self.set_x(x)
        self.set_font(size=11)
        self.cell(
            0,
            h=5,
            txt="Sera:",
            border=0,
            ln=1,
            align="",
            fill=False,
            link="",
        )

        for note in turno_sera:
            if y + 6 > 275:
                self.add_page()
                y = 10
            self.set_y(y)

            self.set_y(y + 6)
            self.set_x(x + 5)
            self.set_font(size=10)
            self.cell(
                0,
                h=5,
                txt="Operatore: ",
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            self.set_y(y + 6)
            self.set_x(x + 20 + 5)
            self.set_font(size=10)
            self.cell(
                0,
                h=5,
                txt=note["operator"],
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            if y + 11 > 275:
                self.add_page()
                y = 10
            self.set_y(y)
            self.set_y(y + 11)
            self.set_x(x + 5)
            self.set_font(size=9)
            x, y = self.get_description_chunks(x, y + 17, note["notes"], 158)
            # self.cell(
            #     0,
            #     h=5,
            #     txt=f"      {note['notes']}",
            #     border=0,
            #     ln=1,
            #     align="",
            #     fill=False,
            #     link="",
            # )
            # y += 10

        self.set_y(y + 17)
        self.set_x(x)
        # x, y = self.get_description_chunks(x - 10, y + 17, note["notes"], 109)
        x -= 10
        y += 17
        if y > 275:
            self.add_page()
            y = 10
        self.set_y(y)
        x += 10
        self.set_font(size=11)

    def get_description_chunks(self, x, y, desc, n):
        words = desc.split()  # Dividi la descrizione in una lista di parole
        line = ""  # Inizializza una stringa per rappresentare la riga corrente
        for word in words:
            if self.get_string_width(line + " " + word) <= n:  # Controlla se la parola si adatta nella riga corrente
                line += " " + word  # Aggiungi la parola alla riga corrente
            else:
                self.cell(
                    0,
                    h=5,
                    txt=line.strip(),  # Rimuovi eventuali spazi vuoti all'inizio e alla fine della riga
                    border=0,
                    ln=1,
                    align="",
                    fill=False,
                    link="",
                )
                y += 5
                self.set_x(x + 5)
                line = word  # Inizia una nuova riga con la parola attuale

        # Stampa l'ultima riga rimanente, se presente
        if line:
            self.cell(
                0,
                h=5,
                txt=line.strip(),  # Rimuovi eventuali spazi vuoti all'inizio e alla fine della riga
                border=0,
                ln=1,
                align="",
                fill=False,
                link="",
            )
            y += 5
            self.set_x(x + 5)

        if y > 275:
            y -= 275

        return x, y

    def create_document(self, db, date, infos, _id):
        self.section_1(date, "Diario di bordo")
        x, y = 20, 20
        notes_to_print = []
        notes = []
        for info in infos:
            if info:
                # if "notebook_tasks" in info:
                #     notebook_tasks.append(get_notebook_tasks(db, info["notebook_tasks"], info["date"], _id))
                # if "tasks" in info:
                #     tasks.append(get_tasks(db, info["tasks"], _id))
                if "notes" in info:
                    notes.append(get_notes(db, info["notes"], info["shift"], _id))

        # if len(notebook_tasks) > 0:
        #     for sublist in notebook_tasks:
        #         notebook_tasks_to_print += sublist
        # x, y = self.section_2("Mansioni portate a termine", notebook_tasks_to_print, x, y)
        # if len(tasks) > 0:
        #     for sublist in tasks:
        #         tasks_to_print += sublist
        # x, y = self.section_2("Consegne portate a termine", tasks_to_print, x, y)
        if len(notes) > 0:
            for sublist in notes:
                notes_to_print += sublist
        self.section_3("Note: ", notes_to_print, x, y)


def generate_logbook(db, date, info=None, _id=None):
    pdf = PDF()
    pdf.add_page()
    pdf.add_font(fname=FONT_DEJAVU_SANS_CONDENSED)
    pdf.set_font("DejaVuSansCondensed", size=11)
    # pdf.set_font("Helvetica", "", 11)
    pdf.set_margins(13, 5)
    pdf.create_document(db, date, info, _id)
    return base64.b64encode(pdf.output(dest="S")).decode()


def get_notebook_tasks(db, tasks, date, _id):
    notebook_tasks = []
    for task in tasks:
        # notebook_task = db["notebookTasks"].find_one({"_id": task})
        notebook_task = db["notebookTasks"].find_one({"_id": task.get("id")})
        if notebook_task:
            notebook_task["title"] = notebook_task["title"].strip("|| ")
            notebook_task["title"] = notebook_task["title"].strip(" ||")
            notebook_task["notes"] = task.get("notes") if task.get("notes") else []
            notebook_task["minors"] = get_minors(db, notebook_task["minors"] if "minors" in notebook_task else [])
            next_day = date + timedelta(1)
            log = db["notebookLog"].find_one(
                {
                    "task": task.get("id"),
                    "date": {"$gte": date, "$lte": next_day},
                    "status": "done",
                }
            )
            if log:
                notebook_task["shifts"] = log["shifts"]
                operator = get_user(db, log["operator"])
                if (operator and _id is not None and operator["_id"] == _id) or (operator and _id is None):
                    notebook_task["operator"] = (
                        f"{operator['surname']} {operator['name']}" if "name" in operator else operator["companyName"]
                    )
                    notebook_tasks.append(notebook_task)
    return notebook_tasks


def get_minors(db, minors):
    task_minors = ""
    for minor in minors:
        minor = get_minor(db, ObjectId(minor))
        if minor:
            task_minors += "" if task_minors == "" else ","
            task_minors += f"{minor['surname']} {minor['name']}"
    return task_minors


def get_tasks(db, tasks, _id):
    log_tasks = []
    for task in tasks:
        log_task = db["tasks"].find_one({"_id": task.get("id")})
        if log_task:
            operator = get_user(db, log_task["operator"]) if "operator" in log_task else None
            if operator:
                log_task["operator"] = (
                    f"{operator['surname']} {operator['name']}" if "name" in operator else operator["companyName"]
                )
            else:
                log_task["operator"] = ""
            if "minor" in log_task:
                minor = get_minor(db, log_task["minor"])
                log_task["minor"] = f"{minor['surname']} {minor['name']}" if minor else ""
            if "resource" in log_task:
                log_task["resource"] = get_resource(db, log_task["resource"])
            log_task["notes"] = task.get("notes") if task.get("notes") else []
            log_task["shifts"] = get_shift(log_task["start"])
            if (operator and _id is not None and operator["_id"] == _id) or (operator and _id is None):
                log_tasks.append(log_task)
    return log_tasks


def get_resource(db, resource):
    src = ""
    result = list(
        db["settings"].aggregate(
            [
                {
                    "$match": {
                        "type": "task",
                        "settings.hccpModules._id": ObjectId(resource["module"]),
                    }
                },
                {"$unwind": "$settings"},
                {"$unwind": "$settings.hccpModules"},
                {
                    "$match": {
                        "type": "task",
                        "settings.hccpModules._id": ObjectId(resource["module"]),
                    }
                },
                {"$project": {"settings.hccpModules": 1}},
            ]
        )
    )
    if len(result) > 0:
        src += result[0]["settings"]["hccpModules"]["label"]
        for element in result[0]["settings"]["hccpModules"]["modules"]:
            if element["_id"] == ObjectId(resource["type"]):
                src += f" {element['label']}"
    return src


def get_notes(db, notes, shift, _id):
    log_notes = []
    for note in notes:
        note["shifts"] = shift
        operator = get_user(db, note["operator"])
        if (operator and _id is not None and operator["_id"] == _id) or (operator and _id is None):
            note["operator"] = (
                f"{operator['surname']} {operator['name']}" if "name" in operator else operator["companyName"]
            )
            log_notes.append(note)
    return log_notes
