import openpyxl as op

def open_sheet(sheetName):
    wb = op.load_workbook("oussama.xlsx")
    sheet = wb[sheetName]
    return sheet


def getRow(sheetName, rowNumber):
    rowValues = []
    sheet = open_sheet(sheetName)
    max_col = sheet.max_column
 
    for i in range(1, max_col + 1):
        cell_obj = sheet.cell(row = rowNumber, column = i)
        rowValues.append(cell_obj.value)


def getColumn(sheetName, columnNumber):
    columnValues = []
    sheet = open_sheet(sheetName)
    max_row = sheet.max_column
 
    for i in range(2, max_row + 1):
        cell_obj = sheet.cell(row = i, column = columnNumber)
        columnValues.appendrowValues(cell_obj.value)


def searchByColumn(sheetName, columnNumber, searchedValue):
    result = []
    sheet = open_sheet(sheetName)
    max_row = sheet.max_row

    for i in range(2, max_row + 1):
        cell_obj = sheet.cell(row=i, column=columnNumber)
        if(cell_obj.value == searchedValue):
            result.append(getRow(sheetName, i))



# ---------------------------------- Case specific functions ------------------------------- #

def getMatriculesByCode(code):
    matricules = []
    sheet = open_sheet("Salariés")
    max_row = sheet.max_row

    for i in range(2, max_row + 1):
        cell_obj = sheet.cell(row=i, column=3)
        if(cell_obj.value == str(code)):
            matricule = sheet.cell(row=i, column=1)
            matricules.append(matricule.value)
    return matricules