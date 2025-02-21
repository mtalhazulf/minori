from fpdf import FPDF


class PDF(FPDF):
    def create_table(
        self,
        table_data,
        title="",
        subtitle="",
        data_size=10,
        title_size=12,
        align_data="L",
        align_header="L",
        cell_width="even",
        set_row_line_height=None,
        x_start="x_default",
        emphasize_data=[],
        emphasize_style=None,
        emphasize_color=(0, 0, 0),
    ):
        """
        table_data:
                    list of lists with first element being list of headers
        title:
                    (Optional) title of table (optional)
        data_size:
                    the font size of table data
        title_size:
                    the font size fo the title of the table
        align_data:
                    align table data
                    L = left align
                    C = center align
                    R = right align
        align_header:
                    align table data
                    L = left align
                    C = center align
                    R = right align
        cell_width:
                    even: evenly distribute cell/column width
                    uneven: base cell size on lenght of cell/column items
                    int: int value for width of each cell/column
                    list of ints: list equal to number of columns with the widht of each cell / column
        x_start:
                    where the left edge of table should start
        emphasize_data:
                    which data elements are to be emphasized - pass as list
                    emphasize_style: the font style you want emphaized data to take
                    emphasize_color: emphasize color (if other than black)

        """
        default_style = self.font_style
        if emphasize_style is None:
            emphasize_style = default_style

        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == "even":
                col_width = (
                    self.epw / len(data[0]) - 1
                )  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == "uneven":
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])):  # for every row
                    longest = 0
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4)  # add 4 for padding
                col_width = col_widths

                # compare columns

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        header = table_data[0]
        data = table_data[1:]

        multiple = 3.5 if self.font_size > 3 else 5
        line_height = self.font_size * multiple  # row height

        col_width = get_col_widths()
        self.set_font(size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == "C":
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else:  # need to multiply cell width by number of cells to get table width
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from pdf width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2  # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == "x_default":
            x_start = self.set_x(self.l_margin)

        # TABLE CREATION #

        # add title
        if title != "":
            self.multi_cell(
                0,
                line_height,
                title,
                border=0,
                align="C",
                ln=3,
                max_line_height=self.font_size,
            )
            self.ln(line_height)  # move cursor back to the left margin

        if subtitle != "":
            self.multi_cell(
                0,
                line_height,
                subtitle,
                border=0,
                align="C",
                ln=3,
                max_line_height=self.font_size,
            )
            self.ln(line_height)  # move cursor back to the left margin

        self.ln()  # put space between title and table
        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if not isinstance(col_width, list):  # columns same sizes
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(
                    col_width,
                    line_height,
                    header[datum],
                    border=1,
                    align=align_header,
                    ln=3,
                    max_line_height=self.font_size,
                    fill=True,
                )
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)
            for row in data:
                if x_start:  # not sure if I need this
                    self.set_x(x_start)
                for dat in header:
                    if dat in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(
                            col_width,
                            line_height,
                            row[dat],
                            border=1,
                            align=align_data,
                            ln=3,
                            max_line_height=self.font_size,
                        )
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(
                            col_width,
                            line_height,
                            row[dat],
                            border=1,
                            align=align_data,
                            ln=3,
                            max_line_height=self.font_size,
                        )  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin

        else:  # columns with different sizes   (TO FIX)
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[list(header.keys())[i]]
                self.multi_cell(
                    col_width[i],
                    line_height,
                    datum,
                    border=1,
                    align=align_header,
                    ln=3,
                    max_line_height=self.font_size,
                    fill=True,
                )
                x_right = self.get_x()
            self.ln(line_height)  # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left, y1, x_right, y1)
            self.line(x_left, y2, x_right, y2)
            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                if set_row_line_height:
                    line_height = set_row_line_height[i]
                for i in range(len(header)):
                    datum = row[list(header.keys())[i]]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(
                            adjusted_col_width,
                            line_height,
                            datum,
                            border=1,
                            align=align_data,
                            ln=3,
                            max_line_height=self.font_size,
                        )
                        self.set_text_color(0, 0, 0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(
                            adjusted_col_width,
                            line_height,
                            datum,
                            border=1,
                            align=align_data,
                            ln=3,
                            max_line_height=self.font_size,
                        )  # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height)  # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left, y3, x_right, y3)
