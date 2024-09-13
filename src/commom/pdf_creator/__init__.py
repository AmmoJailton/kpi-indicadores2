from fpdf import FPDF as pdf
from fpdf import XPos, YPos
from numpy import recarray

from commom.data_classes.report_content_data_class import IReportContent


class PDFGenerator:
    def __init__(self):
        pass

    @classmethod
    def from_dataframe(cls, obj_report_content: IReportContent, **kwargs) -> str:
        pdf_file = pdf()
        pdf_file.set_font("Times", size=9)

        for obj in obj_report_content.document_content:
            pdf_file.add_page(orientation="l")
            for page in obj.content:
                if type(page.content) == str:
                    pdf_file.cell(w=0, h=5, txt=page.content, align="L")
                else:
                    cls._create_table(
                        pdf=pdf_file,
                        table_data=page.content.astype(str).to_records(),
                        title=page.title,
                        cell_width="even",
                    )
                pdf_file.ln()

        pdf_file.output(f"{obj_report_content.document_file_name}")
        return f"{obj_report_content.document_file_name}"

    @classmethod
    def _get_col_widths(cls, cell_width: str, pdf: pdf, table_data, data):
        if cell_width == "even":
            if len(data) > 0:
                col_width = pdf.epw / len(data[0]) - 1
        elif cell_width == "uneven":
            col_widths = []

            for col in range(len(table_data[0])):
                longest = 0
                for row in range(len(table_data)):
                    cell_value = str(table_data[row][col])
                    value_length = pdf.get_string_width(cell_value)
                    if value_length > longest:
                        longest = value_length
                col_widths.append(longest + 4)
            col_width = col_widths

        elif isinstance(cell_width, list):
            col_width = cell_width
        else:
            col_width = int(cell_width)

        return col_width

    @classmethod
    def _create_table(
        cls,
        pdf: pdf,
        table_data: recarray,
        title="",
        data_size=10,
        title_size=12,
        align_data="L",
        align_header="L",
        cell_width="even",
        x_start="x_default",
        emphasize_data=[],
        emphasize_style=None,
        emphasize_color=(0, 0, 0),
    ):
        default_style = pdf.font_style

        if emphasize_style is None:
            emphasize_style = default_style

        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []

            for key in table_data:
                value = table_data[key]
                data.append(value)

            data = [list(a) for a in zip(*data)]
        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = pdf.font_size * 2.5

        col_width = cls._get_col_widths(cell_width=cell_width, pdf=pdf, table_data=table_data, data=data)

        pdf.set_font(size=title_size)

        if x_start == "C":
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else:
                table_width = col_width * len(table_data[0])

            margin_width = pdf.w - table_width

            center_table = margin_width / 2
            x_start = center_table
            pdf.set_x(x_start)
        elif isinstance(x_start, int):
            pdf.set_x(x_start)
        elif x_start == "x_default":
            x_start = pdf.set_x(pdf.l_margin)

        if title != "":
            pdf.multi_cell(
                0,
                line_height,
                title,
                border=0,
                align="j",
                new_x=XPos.RIGHT,
                new_y=YPos.TOP,
                max_line_height=pdf.font_size,
            )
            pdf.ln(line_height)

        pdf.set_font(size=data_size)
        y1 = pdf.get_y()

        if x_start:
            x_left = x_start
        else:
            x_left = pdf.get_x()
        x_right = pdf.epw + x_left

        if not isinstance(col_width, list):
            if x_start:
                pdf.set_x(x_start)
            for datum in header:
                pdf.multi_cell(
                    col_width,
                    line_height,
                    datum,
                    border=0,
                    align=align_header,
                    new_x=XPos.RIGHT,
                    new_y=YPos.TOP,
                    max_line_height=pdf.font_size,
                )
                x_right = pdf.get_x()
            pdf.ln(line_height)
            y2 = pdf.get_y()
            pdf.line(x_left, y1, x_right, y1)
            pdf.line(x_left, y2, x_right, y2)

            for row in data:
                if x_start:
                    pdf.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        pdf.set_text_color(*emphasize_color)
                        pdf.set_font(style=emphasize_style)
                        pdf.multi_cell(
                            col_width,
                            line_height,
                            datum,
                            border=0,
                            align=align_data,
                            new_x=XPos.RIGHT,
                            new_y=YPos.TOP,
                            max_line_height=pdf.font_size,
                        )
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font(style=default_style)
                    else:
                        pdf.multi_cell(
                            col_width,
                            line_height,
                            datum,
                            border=0,
                            align=align_data,
                            new_x=XPos.RIGHT,
                            new_y=YPos.TOP,
                            max_line_height=pdf.font_size,
                        )  # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
                pdf.ln(line_height)
        else:
            if x_start:
                pdf.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                pdf.multi_cell(
                    col_width[i],
                    line_height,
                    datum,
                    border=0,
                    align=align_header,
                    new_x=XPos.RIGHT,
                    new_y=YPos.TOP,
                    max_line_height=pdf.font_size,
                )
                x_right = pdf.get_x()
            pdf.ln(line_height)
            y2 = pdf.get_y()
            pdf.line(x_left, y1, x_right, y1)
            pdf.line(x_left, y2, x_right, y2)

            for i in range(len(data)):
                if x_start:
                    pdf.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        pdf.set_text_color(*emphasize_color)
                        pdf.set_font(style=emphasize_style)
                        pdf.multi_cell(
                            adjusted_col_width,
                            line_height,
                            datum,
                            border=0,
                            align=align_data,
                            new_x=XPos.RIGHT,
                            new_y=YPos.TOP,
                            max_line_height=pdf.font_size,
                        )
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font(style=default_style)
                    else:
                        pdf.multi_cell(
                            adjusted_col_width,
                            line_height,
                            datum,
                            border=0,
                            align=align_data,
                            new_x=XPos.RIGHT,
                            new_y=YPos.TOP,
                            max_line_height=pdf.font_size,
                        )  # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
                pdf.ln(line_height)

        y3 = pdf.get_y()

        pdf.line(x_left, y3, x_right, y3)
