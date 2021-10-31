import codecs
from fastapi import FastAPI, File, UploadFile,Request
import csv
import  os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import *
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet


app = FastAPI()

templates = Jinja2Templates(directory="templates")
#getting work directory
cwd = os.getcwd()

@app.get("/home",response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse("home.html", {"request":request})


@app.post("/submitForm")
async def upload_file(csv_file:UploadFile = File(...)):
    #reading data from csv in a list
    readFile = csv.reader(codecs.iterdecode(csv_file.file,'utf-8'))
    dataList = list(readFile)
    print(readFile)


    element = []

    style = getSampleStyleSheet()
    normalStyle = style["Normal"]
    #making pdf table
    #[(starting_column,starting_row), (ending_column, ending_row)]

    all_cells = [(0, 0), (-1, -1)]
    header = [(0, 0), (-1, 0)]
    column0 = [(0, 0), (0, -1)]
    column1 = [(1, 0), (1, -1)]
    column2 = [(2, 0), (2, -1)]
    column3 = [(3, 0), (3, -1)]
    column4 = [(4, 0), (4, -1)]
    column5 = [(5, 0), (5, -1)]
    column6 = [(6, 0), (6, -1)]

    table_style = TableStyle(
        [
            ('VALIGN', all_cells[0], all_cells[1], 'TOP'),
            ('LINEBELOW', header[0], header[1], 1, colors.black),
            ('ALIGN', column0[0], column0[1], 'LEFT'),
            ('ALIGN', column1[0], column1[1], 'LEFT'),
            ('ALIGN', column2[0], column2[1], 'LEFT'),
            ('ALIGN', column3[0], column3[1], 'RIGHT'),
            ('ALIGN', column4[0], column4[1], 'LEFT'),
            ('ALIGN', column5[0], column5[1], 'LEFT'),
            ('ALIGN', column6[0], column6[1], 'LEFT'),
        ]
    )

    #column widths
    columnWidht = [
        3.7 * cm,
        3.7 * cm,
        3.7 * cm,
        3.7 * cm,
        3.7 * cm,
        3.7 * cm,
        6 * cm,
    ]
    for index, row in enumerate(dataList):

        for column, value in enumerate(row):
            try:
                if column != 6 or index == 0:
                    dataList[index][column] = value.strip("'[]()")
                else:
                    dataList[index][column] = Paragraph(value, style["Normal"])
            except ValueError:
                pass

    table = Table(dataList, colWidths=columnWidht)
    table.setStyle(table_style)
    #print(table)
    element.append(table)
    fileName = cwd + '\\' + 'Demo Report.pdf'

    print(element)

    create_pdf = SimpleDocTemplate(fileName,pagesize=letter,rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=28)
    create_pdf.build(element)
    print('Demo Report Generated')


    return {"Report_Genrated":csv_file.filename}