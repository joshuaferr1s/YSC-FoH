import gspread
from oauth2client.service_account import ServiceAccountCredentials


def export_timedata(movie, movie_timedata, finals):
    # use creds to create a client to interact with the Google Drive API
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)
    client = gspread.authorize(creds)

    # open required spreadhseet and worksheet
    spreadsheet = client.open('YSC-foh')
    sheet = client.open("YSC-foh").worksheet('Spr-Membership')
    headers = ['Times', '£3', '£4', 'Free', 'Half-Price', 'Special', 'Total']
    worksheets = spreadsheet.worksheets()
    worksheets_names = list()
    for i in worksheets:
        worksheets_names.append(i.title)

    try:
        cell = sheet.find(movie)
        cell_range = sheet.range('B' + str(cell.row) + ':G' + str(cell.row))
        k = 1
        for cell in cell_range:
            cell.value = finals[headers[k]]
            k += 1
        sheet.update_cells(cell_range)
        print('Spr-Membership sheet updated. (maybe)')
    except:
        new_row = [
            movie, finals['£3'], finals['£4'], finals['Free'],
            finals['Half-Price'], finals['Special'], finals['Total']
        ]
        sheet.append_row(new_row)
        print('Spr-Membership sheet updated. (maybe)')

    try:
        if movie not in worksheets_names:
            worksheet = spreadsheet.add_worksheet(movie, 100, 7)
            print('Created a new worksheet for ' + movie)
        else:
            print('Overwriting previous data for ' + movie)
            worksheet = spreadsheet.worksheet(movie)

        cell_list = worksheet.range('A1:G1')
        k = 0
        for cell in cell_list:
            cell.value = headers[k]
            k += 1
        worksheet.update_cells(cell_list)

        print('Exporting timedata')
        cells = ['B', 'C', 'D', 'E', 'F', 'G']
        k = 2
        for i in movie_timedata:
            worksheet.update_acell('A' + str(k), str(i))
            cell_list = worksheet.range('B' + str(k) + ':G' + str(k))
            for cell in cell_list:
                cell.value = movie_timedata[i][worksheet.acell(
                    cells[cell.col - 2] + '1').value]
            worksheet.update_cells(cell_list)
            k += 1
    except:
        print('Could not create/update movie spreadsheet.')
    print('Finished exporting timedata')
