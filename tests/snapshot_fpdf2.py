# Each PDF generated will have different /ID field within metadata
# but visually identical

from fpdf import FPDF


def generate_fpdf2(data, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("times", size=14)

    with pdf.table(borders_layout="SINGLE_TOP_LINE") as table:
        for row in data:
            table_row = table.row()
            for cell in row:
                table_row.cell(cell)

    pdf.output(output_file)
    return output_file


data = [
    ["Header1", "Header2", "Header3"],
    ["Row1Cell1", "Row1Cell2", "Row1Cell3"],
    ["Row2Cell1", "Row2Cell2", "Row2Cell3"],
    ["Row3Cell1", "Row3Cell2", "Row3Cell3"],
    ["Row4Cell1", "Row4Cell2", "Row4Cell3"],
    ["Row5Cell1", "Row5Cell2", "Row5Cell3"],
]
