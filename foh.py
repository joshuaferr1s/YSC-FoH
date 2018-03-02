import gspread
from decimal import *
from time import localtime, strftime
from file_helpers import *
from oauth2client.service_account import ServiceAccountCredentials


def existing_movies(movies_recorded):
    print(dividor)
    for i in movies_recorded:
        print("* " + i)
    print(dividor)


def format_display(d):
    output_text = ""
    for i in d:
        if output_text != "":
            output_text += " | "
        else:
            pass
        output_text = output_text + str(i) + ": " + str(d[i])
    print(output_text)


def fresh_dict():
    return {"£3": 0, "£4": 0, "Free": 0, "Half-Price": 0, "Special": 0, "Total": 0}


def copy_dict(d):
    n_d = dict()
    for i in d:
        n_d[i] = d[i]
    return n_d


def export_timedata(movie, movie_timedata, finals):
    # use credentials to create a client to interact with the Google Drive API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "client_secret.json", scope)
    client = gspread.authorize(creds)

    # open required spreadhseet and worksheet
    spreadsheet = client.open("YSC-foh")
    sheet = spreadsheet.worksheet("Spr-Membership")
    headers = ["Times", "£3", "£4", "Free", "Half-Price", "Special", "Total"]
    worksheets = spreadsheet.worksheets()
    worksheets_names = list()
    for i in worksheets:
        worksheets_names.append(i.title)

    # main sheet
    try:
        cell = sheet.find(movie)
        cell_range = sheet.range("B" + str(cell.row) + ":G" + str(cell.row))
        k = 1
        for cell in cell_range:
            cell.value = finals[headers[k]]
            k += 1
        sheet.update_cells(cell_range)
    except:
        new_row = [
            movie, finals["£3"], finals["£4"], finals["Free"],
            finals["Half-Price"], finals["Special"], finals["Total"]
        ]
        sheet.append_row(new_row)

    # timedata
    num_of_values = len(movie_timedata) + 1
    cell_tops = {
        1: "£3",
        2: "£4",
        3: "Free",
        4: "Half-Price",
        5: "Special",
        6: "Total"
    }

    if movie in worksheets_names:
        worksheet = spreadsheet.worksheet(movie)
        print("Overwriting previous data for {0}.".format(movie))
    else:
        worksheet = spreadsheet.add_worksheet(movie, num_of_values, 7)
        print("Created a new worksheet for {0}.".format(movie))

    difference = len(movie_timedata) - worksheet.row_count + 1
    print(difference)
    if difference > 0:
        worksheet.add_rows(difference)
    print(num_of_values)
    work_cells = worksheet.range("A1:G" + str(num_of_values))
    k = 0
    t_d_t = 0
    cur_time = ""
    l = 0
    timedata_k = list(movie_timedata.keys())
    for cell in work_cells:
        if k < 7:
            cell.value = headers[k]
        elif k % 7 == 0:
            cell.value = timedata_k[t_d_t]
            cur_time = timedata_k[t_d_t]
            t_d_t += 1
            l += 1
        else:
            cell.value = movie_timedata[cur_time][cell_tops[l]]
            if l == 6:
                l = 0
            else:
                l += 1
        k += 1

    worksheet.update_cells(work_cells)
    print("Timedata upload complete.")


def report(movie, movie_totals, movie_timedata, early_screening=False):
    global dividor

    print(dividor)
    print("Movie: {0}".format(movie))
    print(dividor)
    print("End of the night:")
    format_display(movie_totals)
    print(dividor)
    if not early_sceening:
        pre_bets = fresh_dict()
        for key in movie_timedata:
            if int(key) < 31:
                pre_bets = movie_timedata[key]
        print("Before bets:")
        format_display(pre_bets)
        print(dividor)
        try:
            multiplier = Decimal(movie_totals["Total"]) / int(pre_bets["Total"])
            print("Multiplier: {0}".format(str(multiplier)))
        except ZeroDivisionError:
            print("There were no customers before 7:00 and so no multiplier.")
        print(dividor)
    print("\nWould you like to upload this data to the Google Sheet?")
    print("* yes")
    print("* no")
    choice = input("> ").lower()

    if choice == "yes":
        export_timedata(movie, movie_timedata, movie_totals)
    else:
        pass


def warning_messages(total):
    warnings = {
        250: "We are nearing full.",
        260: "Prepare to start warning customers.",
        270: "Temporarily close the doors and do a seat count."
    }
    if total in warnings:
        print("\n" * 20)
        print(warnings[total])
        try:
            input("Press Enter to continue...")
        except SyntaxError:
            pass


def record(exists, movie, early_sceening=False):
    global movie_data, dividor
    scene_splitter = "#" * 69
    recording = True
    minute_time = "0"
    last_time = ""
    movie_totals = dict()
    movie_timedata = dict()
    ticket_type = {
        "3": "Added £3",
        "3r": "Removed £3",
        "4": "Added £4",
        "4r": "Removed £4",
        "f": "Added Free",
        "fr": "Removed Free",
        "h": "Added Half-Price",
        "hr": "Removed Half-Price",
        "s": "Added Special",
        "sr": "Removed Special"
    }

    if exists:
        # load previous data to continue recording
        movie_totals = copy_dict(movie_data[movie]["final"])
        movie_timedata = copy_dict(movie_data[movie]["timedata"])
    else:
        movie_data[movie] = dict()
        movie_data[movie]["final"] = dict()
        movie_data[movie]["timedata"] = dict()
        movie_totals = fresh_dict()

    while recording:

        warning_messages(movie_totals["Total"])

        print(dividor)
        print("Movie: {0}".format(movie))
        format_display(movie_totals)
        print(dividor)
        print("Recording Mode:")
        print("(3) £3")
        print("(4) £4")
        print("(f) Free")
        print("(h) Half-Price")
        print("(s) Special")
        print("To remove x, type xr.")
        print("* stop")
        ticket = input("> ")

        print(scene_splitter)
        print(scene_splitter)
        time_now = strftime("%H%M", localtime())

        if ticket == "stop":
            recording = False
        elif ticket in ticket_type:
            if early_sceening:
                if int(time_now) < 1800:
                    minute_time = str(int(time_now) - 1790)
                else:
                    minute_time = str(int(time_now) - 1830)
            else:
                if int(time_now) < 1900:
                    minute_time = str(int(time_now) - 1830)
                elif int(time_now) >= 1900 and int(time_now) < 2000:
                    minute_time = str(int(time_now) - 1870)
                else:
                    minute_time = str(int(time_now) - 1910)

            if minute_time not in movie_timedata and last_time == "":
                movie_timedata[minute_time] = fresh_dict()
            elif minute_time not in movie_timedata and last_time != "":
                movie_timedata[minute_time] = copy_dict(movie_timedata[last_time])
            else:
                pass

            if ticket_type[ticket].split(" ")[0] == "Added":
                movie_totals["Total"] += 1
                movie_totals[ticket_type[ticket].split(" ")[1]] += 1
                movie_timedata[minute_time]["Total"] += 1
                movie_timedata[minute_time][ticket_type[ticket].split(" ")[
                    1]] += 1
                print("{0} -- {1}".format(time_now, ticket_type[ticket]))
            else:
                if movie_totals[ticket_type[ticket].split(" ")[1]] > 0:
                    movie_totals["Total"] -= 1
                    movie_timedata[minute_time]["Total"] -= 1
                    movie_totals[ticket_type[ticket].split(" ")[1]] -= 1
                    movie_timedata[minute_time][ticket_type[ticket].split(" ")[
                        1]] -= 1
                    print("{0} -- {1}".format(time_now, ticket_type[ticket]))
                else:
                    print("There are no customers who have bought a {0} ticket.".format(ticket_type[ticket].split(" ")[1]))
            last_time = minute_time

        else:
            print("Invalid input: {0}.".format(ticket))

    movie_data[movie]["final"] = copy_dict(movie_totals)
    movie_data[movie]["timedata"] = copy_dict(movie_timedata)
    write_movie_dict("movie_database.json", movie_data)

    return movie_totals, movie_timedata


# Initialization
running = True
dividor = "-" * 69

# Main Loop
while running:
    try:
        movie_data = load_movie_data_file("movie_database.json")
    except:
        movie_data = dict()
    movie_total = dict()
    movies_recorded = list(movie_data.keys())
    early_sceening = False

    print("\nYSC Front of House")
    print("* record")
    if len(movies_recorded) > 0:
        print("* report")
    print("* quit")
    choice = input("> ").lower()

    if choice == "quit":
        running = False
    elif choice == "record":
        print(dividor)
        existing_movies(movies_recorded)
        print(dividor)
        print("What movie would you like to record?")
        movie = input("> ")
        print("Is this an early screening?")
        print("* y")
        print("* n")
        early_sceening_in = input("> ")

        if early_sceening_in == "y":
            early_sceening = True
        else:
            early_sceening = False

        if movie in movies_recorded:
            print("Loading previous movie data...")
            movie_total, movie_timedata = record(True, movie, early_sceening)
        else:
            movie_total, movie_timedata = record(False, movie, early_sceening)

        print("Would you like to compile a report of this screening?")
        print("* yes")
        print("* no")
        report_choice = input("> ")

        if report_choice == "yes":
            report(movie, movie_total, movie_timedata, early_sceening)
        elif report_choice == "no":
            pass
        else:
            print("Invalid input: {0}.".format(report_choice))

    elif choice == "report" and len(movies_recorded) > 0:
        print("Movies in the database:")
        existing_movies(movies_recorded)
        print(dividor)
        print("Which movie would you like to compile a report for?")
        movie = input("> ")

        print("Was this an early screening?")
        print("* yes")
        print("* no")
        early_sceening_in = input("> ")

        if early_sceening_in == "yes":
            early_screening = True
        else:
            early_screening = False

        if movie in movies_recorded:
            movie_totals = copy_dict(movie_data[movie]["final"])
            movie_timedata = copy_dict(movie_data[movie]["timedata"])
            report(movie, movie_totals, movie_timedata, early_sceening)
        else:
            pass

    else:
        print("Invalid input: {0}.".format(choice))
