import base64

from api.applications.exports.helper.create_pdf import PDF


def pdf_template(title, subtitle, data_dict, cell_width, height, font_size, orientation):
    pdf = PDF()
    pdf.add_page(orientation=orientation)
    pdf.set_font("Times", size=font_size)
    pdf.set_fill_color(178, 194, 178)
    pdf.create_table(
        table_data=data_dict,
        title=title,
        subtitle=subtitle,
        cell_width=cell_width,
        set_row_line_height=height if len(height) > 0 else None,
        x_start="C",
    )
    pdf.ln()
    """ pdf.output :
     arg --> path #crea file pdf e lo salva nella directory indicata
     arg--> dest="S" trasforma l'output in string
     arg --> dest="D" forza il download del file
    """
    return base64.b64encode(pdf.output(dest="S")).decode()


def format_data(db, date, data, last_day):
    data_dict = []
    for el in data:
        el["name"] = el["surname"] + " " + el["name"]
        if "fiscal_code" in el:
            el["name"] = el["name"] + " (" + el["fiscal_code"] + ")"
        dat = {"name": el["name"]}
        attendances = list(
            db["minorAttendance"].find(
                {
                    "minorId": el["_id"],
                    "$expr": {"$eq": [{"$month": "$date"}, date.month]},
                }
            )
        )
        if len(attendances) > 0:
            for x in range(1, last_day):
                dat[str(x)] = check_presence(attendances, x)
            data_dict.append(dat)
    return data_dict


def check_presence(list, day):
    for x in list:
        if x["date"].day == day:
            return "x" if x["isPresent"] else "A"
    return ""


def format_header(header, last_day):
    for x in range(1, last_day):
        header[str(x)] = str(x)
    return header
