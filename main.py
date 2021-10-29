import codecs

from fastapi import FastAPI, File, UploadFile,Request
import pandas as pd
import numpy as n
from pathlib import Path
import shutil
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, legal, letter
import csv
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")
#getting work directory
cwd = os.getcwd()

@app.get("/home",response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse("home.html", {"request":request})


 # at last, the bottom of the file/module
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5049)
# app.get("/",response_class=HTMLResponse)
# def index(request:Request):
#     return {"message":"HElloworld"}
#     return """<html>
#   <head>
#     <title>Report Generator</title>
#   </head>
#   <body>
#     <h1>Upload .csv Fiel</h1>
#     <form action="/submitForm" method="post" enctype="multipart/form-data">
#       <input type= "file" name="csv_file">
#       <input type="submit" value="Generate report">
#     </form>
#   </body>
# </html>
# """


@app.post("/submitForm")
async def upload_file(csv_file:UploadFile = File(...)):
    #Pdf layout

    table_style = TableStyle(
        [
            ('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]
    )
    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']

    style_config = getSampleStyleSheet()
    style_config = style_config["BodyText"]
    style_config.wordWrap = 'CJK'


    readFile = csv.DictReader(codecs.iterdecode(csv_file.file,'utf-8'))
    dataList = list(readFile)
    #print(dataList)
    headers = dataList[0]
    #print(headers)
    for record in range(1,len(dataList)):
        file_records = dataList[record]
        print((file_records))

        data = list()
        nullRecords = list()
        records = list()
        headers = list()
        count = 0

        for line in file_records:
            if line == "":
                nullRecords.append(line)
            else:
                records.append(line)
                headers.append(count)
                data.append([str(headers[count]),str(line)])
            count += 1
    return {"fileName":csv_file.filename}