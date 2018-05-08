import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
from time import localtime, strftime
import json, gspread
from tkinter import messagebox
from tkinter.messagebox import showinfo
from oauth2client.service_account import ServiceAccountCredentials

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
cur_movie = ""
exists = False

user_background = "light sky blue"


def load_json_file(file_name):
    dict_from_file = {}
    with open(file_name, 'r') as inf:
        dict_from_file = json.load(inf)
    return dict_from_file


def copy_dict(d):
    n_d = dict()
    for i in d:
        n_d[i] = d[i]
    return n_d


def write_movie_dict(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def fresh_dict():
    return {
        "£3": 0,
        "£4": 0,
        "Free": 0,
        "Half-Price": 0,
        "Special": 0,
        "Total": 0
    }


def import_timedata():
    global movie_data
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
    sheet = spreadsheet.worksheet("Full-List")
    headers = ["Times", "£3", "£4", "Free", "Half-Price", "Special", "Total"]
    worksheets = spreadsheet.worksheets()
    worksheets_names = list()
    for i in worksheets:
        worksheets_names.append(i.title)

    # main sheet
    cell_range = sheet.range("A2:G" + str(sheet.row_count))
    k = 0
    movies_list = list()
    finals = dict()
    temp_dict = dict()
    for cell in cell_range:
        m_k = k % 7
        if m_k == 0:
            cur_movie = cell.value
            movies_list.append(cell.value)
            temp_dict[cur_movie] = dict()
            temp_dict[cur_movie]["final"] = fresh_dict()
            temp_dict[cur_movie]["final"] = dict()
        else:
            temp_dict[cur_movie]["final"][headers[m_k]] = int(cell.value)
        k += 1
    movie_data = copy_dict(temp_dict)
    # timedata
    for movie in movies_list:
        if movie in worksheets_names:
            worksheet = spreadsheet.worksheet(movie)
            k = 0
            t_time = dict()
            cur_time = ""
            cell_range = worksheet.range("A2:G" + str(worksheet.row_count))
            k = 0
            for cell in cell_range:
                m_k = k % 7
                if m_k == 0:
                    cur_time = cell.value
                    t_time[cur_time] = fresh_dict()
                else:
                    t_time[cur_time][headers[m_k]] = int(cell.value)
                k += 1
            movie_data[movie]["timedata"] = copy_dict(t_time)
        else:
            pass

    write_movie_dict("movie_database.json", movie_data)


def user_preferences(opt):
    ## Load user preferences from the file
    global user_background

    try:
        with open("userPreferences.txt", 'r') as f:
            pass
    except FileNotFoundError:
        with open("userPreferences.txt", 'w') as f:
            pass

    if opt == "save":
        with open("userPreferences.txt", 'w') as inf:
            inf.write(user_background)
    elif opt == "load":
        with open("userPreferences.txt", 'r') as inf:
            user_background = str(inf.readline().split('\n', 1)[0])
            print(user_background)


try:
    movie_data = load_json_file("movie_database.json")
except:
    movie_data = dict()

user_preferences("load")

class YscFoH(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "YSC Front of House")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Download Data", command=import_timedata)
        filemenu.add_command(label="User Preferences", command= lambda: self.show_frame(UserPage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = dict()

        for F in (StartPage, UserPage, Record, Report, SelectMovie):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.draw()
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)

        self.label1 = tk.Label()
        self.label2 = tk.Label()
        self.button1 = tk.Button()
        self.button2 = tk.Button()

    def draw(self):
        global user_background

        self.config(bg=user_background)

        self.label1 = tk.Label(
            self,
            text="York Student Cinema",
            font=("Comic Sans", 20),
            bg=user_background)
        self.label1.grid(row=1, column=1)
        self.label2 = tk.Label(
            self,
            text="Front of House",
            font=("Comic Sans", 20),
            bg=user_background)
        self.label2.grid(row=2, column=1)
        self.button1 = tk.Button(
            self,
            text="Record",
            command=lambda: self.cont.show_frame(SelectMovie),
            highlightbackground=user_background)
        self.button1.grid(row=3, column=1)
        self.button2 = tk.Button(
            self,
            text="Report",
            command=lambda: self.cont.show_frame(Report),
            highlightbackground=user_background)
        self.button2.grid(row=4, column=1)


class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self.label1 = tk.Label()
        self.label2 = tk.Label()
        self.button1 = tk.Button()
        self.button2 = tk.Button()

    def draw(self):
        global user_background

        self.config(bg=user_background)

        self.label1 = tk.Label(
            self,
            text="User Preferences",
            font=("Comic Sans", 20),
            bg=user_background)
        self.label1.grid(row=1, column=1)
        self.button1 = tk.Button(
            self,
            text="Color Selection",
            command=self.color_select,
            highlightbackground=user_background)
        self.button1.grid(row=2, column=1)
        self.button2 = tk.Button(
            self,
            text="Main Menu",
            command=lambda: self.cont.show_frame(StartPage),
            highlightbackground=user_background)
        self.button2.grid(row=3, column=1)

    def color_select(self):
        global user_background
        c = colorchooser.askcolor()[1]
        if c is not None:
            user_background = c
        self.config(background=user_background)
        user_preferences("save")


class SelectMovie(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        self.temp_mov_list = list()
        self.label1 = tk.Label()
        self.listMovies = tk.Listbox()
        self.scrollbar = tk.Scrollbar()
        self.entry1 = tk.Entry()
        self.button1 = tk.Button()
        self.button2 = tk.Button()
        self.button3 = tk.Button()

    def draw(self):
        global user_background, movie_data

        self.config(bg=user_background)

        self.label1 = tk.Label(
            self,
            text="Select a movie to record...",
            font=LARGE_FONT,
            bg=user_background)
        self.label1.grid(row=0, column=0, columnspan=5, sticky="nsew")

        self.listMovies = tk.Listbox(
            self, width=25, height=20, font=NORM_FONT, bg="#B6E3FD")
        self.listMovies.grid(
            row=1, rowspan=10, column=0, columnspan=3, sticky="nsew")
        self.scrollbar = tk.Scrollbar(
            self, bg=user_background, orient="vertical")
        self.scrollbar.config(command=self.listMovies.yview)
        self.scrollbar.grid(row=1, rowspan=10, column=4, sticky="nsew")

        self.listMovies.config(yscrollcommand=self.scrollbar.set)

        self.temp_mov_list = list()
        for x in movie_data:
            self.temp_mov_list.append(x)
            self.listMovies.insert(tk.END, str(" " + x))

        self.entry1 = tk.Entry(self, highlightbackground=user_background)
        self.entry1.grid(row=1, column=5, columnspan=2, sticky="nsew")

        self.button1 = tk.Button(
            self,
            text="Select",
            highlightbackground=user_background,
            command=
            lambda: self.recorder(self.temp_mov_list[self.listMovies.curselection()[0]])
        )
        self.button1.grid(row=11, column=0, columnspan=5, sticky="nsew")
        self.button2 = tk.Button(
            self,
            text="New",
            highlightbackground=user_background,
            command=
            lambda: self.recorder(self.entry1.get()))
        self.button2.grid(row=2, column=5, columnspan=2, sticky="nsew")
        self.button3 = tk.Button(
            self,
            text="Main Menu",
            highlightbackground=user_background,
            command=lambda: self.cont.show_frame(StartPage))
        self.button3.grid(row=3, column=5, columnspan=2, sticky="nsew")

    def recorder(self, movie):
        global cur_movie, exists
        cur_movie = movie
        if movie not in movie_data:
            exists = False
        else:
            exists = True
        self.cont.show_frame(Record)


class Record(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        self.movie_totals = dict()
        self.movie_timedata = dict()
        self.minute_time = ""
        self.last_time = ""
        self.movie = ""

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=2)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=2)

        self.button1 = tk.Button()
        self.button3 = tk.Button()
        self.button3_ = tk.Button()
        self.button4 = tk.Button()
        self.button4_ = tk.Button()
        self.button5 = tk.Button()
        self.button5_ = tk.Button()
        self.button6 = tk.Button()
        self.button6_ = tk.Button()
        self.button7 = tk.Button()
        self.button7_ = tk.Button()

        self.label1 = tk.Label()
        self.label3 = tk.Label()
        self.label4 = tk.Label()
        self.label5 = tk.Label()
        self.label6 = tk.Label()
        self.label7 = tk.Label()
        self.label8 = tk.Label()
        self.label9 = tk.Label()

    def draw(self):
        global user_background, cur_movie, movie_data, exists
        self.config(bg=user_background)
        self.resetWidgets()
        self.movie = cur_movie
        lab_text = "{0}".format(self.movie)

        if exists:
            self.movie_totals = copy_dict(movie_data[self.movie]["final"])
            try:
                self.movie_timedata = copy_dict(movie_data[self.movie]["timedata"])
                times_a = list(self.movie_timedata.keys())
                self.last_time = times_a[-1]
            except:
                movie_data[self.movie]["timedata"] = dict()
        else:
            self.movie_totals = fresh_dict()
            movie_data[self.movie] = dict()
            movie_data[self.movie]["final"] = dict()
            movie_data[self.movie]["timedata"] = dict()

        self.label1 = tk.Label(
            self, text=lab_text, font=("Comic Sans", 20), bg=user_background)
        self.label1.grid(row=0, columnspan=5)

        #### £3 ####
        self.button3 = tk.Button(
            self,
            text="£3 +",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.incr_ticket("£3"))
        self.button3.grid(row=1, column=1, sticky="nsew")
        self.button3_ = tk.Button(
            self,
            text="£3 -",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.decr_ticket("£3"))
        self.button3_.grid(row=1, column=2, sticky="nsew")
        self.label3 = tk.Label(
            self, text=self.movie_totals["£3"], bg=user_background)
        self.label3.grid(row=1, column=3, sticky="w")

        #### £4 ####
        self.button4 = tk.Button(
            self,
            text="£4 +",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.incr_ticket("£4"))
        self.button4.grid(row=2, column=1, sticky="nsew")
        self.button4_ = tk.Button(
            self,
            text="£4 -",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.decr_ticket("£4"))
        self.button4_.grid(row=2, column=2, sticky="nsew")
        self.label4 = tk.Label(
            self, text=self.movie_totals["£4"], bg=user_background)
        self.label4.grid(row=2, column=3, sticky="w")

        #### Free ####
        self.button5 = tk.Button(
            self,
            text="Free +",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.incr_ticket("Free"))
        self.button5.grid(row=3, column=1, sticky="nsew")
        self.button5_ = tk.Button(
            self,
            text="Free -",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.decr_ticket("Free"))
        self.button5_.grid(row=3, column=2, sticky="nsew")
        self.label5 = tk.Label(
            self, text=self.movie_totals["Free"], bg=user_background)
        self.label5.grid(row=3, column=3, sticky="w")

        #### Half-Price ####
        self.button6 = tk.Button(
            self,
            text="£2 +",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.incr_ticket("Half-Price"))
        self.button6.grid(row=4, column=1, sticky="nsew")
        self.button6_ = tk.Button(
            self,
            text="£2 -",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.decr_ticket("Half-Price"))
        self.button6_.grid(row=4, column=2, sticky="nsew")
        self.label6 = tk.Label(
            self, text=self.movie_totals["Half-Price"], bg=user_background)
        self.label6.grid(row=4, column=3, sticky="w")

        #### Special ####
        self.button7 = tk.Button(
            self,
            text="Special +",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.incr_ticket("Special"))
        self.button7.grid(row=5, column=1, sticky="nsew")
        self.button7_ = tk.Button(
            self,
            text="Special -",
            font=NORM_FONT,
            highlightbackground=user_background,
            command=lambda: self.decr_ticket("Special"))
        self.button7_.grid(row=5, column=2, sticky="nsew")
        self.label7 = tk.Label(
            self, text=self.movie_totals["Special"], bg=user_background)
        self.label7.grid(row=5, column=3, sticky="w")

        #### Total ####
        self.label8 = tk.Label(
            self, text="Total:", font=("Comic Sans", 15), bg=user_background)
        self.label8.grid(row=6, column=2, sticky="e")
        self.label9 = tk.Label(
            self,
            text=self.movie_totals["Total"],
            bg=user_background,
            font=("Comic Sans", 15))
        self.label9.grid(row=6, column=3, sticky="w")

        #### Finish Button ####
        self.button1 = tk.Button(
            self,
            text="Finished",
            highlightbackground=user_background,
            command=self.finished)
        self.button1.grid(row=7, column=1, columnspan=3, sticky="nsew")

    def resetWidgets(self):
        self.button1.destroy()
        self.button3.destroy()
        self.button3_.destroy()
        self.button4.destroy()
        self.button4_.destroy()
        self.button5.destroy()
        self.button5_.destroy()
        self.button6.destroy()
        self.button6_.destroy()
        self.button7.destroy()
        self.button7_.destroy()
        self.label1.destroy()
        self.label3.destroy()
        self.label4.destroy()
        self.label5.destroy()
        self.label6.destroy()
        self.label7.destroy()
        self.label8.destroy()
        self.label9.destroy()

    def incr_ticket(self, ticket):
        self.minute_time = self.get_time()
        self.timedata_handler()
        self.movie_totals["Total"] += 1
        self.movie_totals[ticket] += 1
        self.movie_timedata[self.minute_time]["Total"] += 1
        self.movie_timedata[self.minute_time][ticket] += 1
        self.update_labels()
        self.last_time = self.minute_time
        self.cap_check()

    def decr_ticket(self, ticket):
        self.minute_time = self.get_time()
        self.timedata_handler()
        if self.movie_totals[ticket] > 0:
            self.movie_totals["Total"] -= 1
            self.movie_totals[ticket] -= 1
            self.movie_timedata[self.minute_time]["Total"] -= 1
            self.movie_timedata[self.minute_time][ticket] -= 1
        else:
            showinfo("Alert!",
                     "There are no tickets of type: {0}".format(ticket))
        self.update_labels()
        self.last_time = self.minute_time
        self.cap_check()

    def timedata_handler(self):
        if self.minute_time not in self.movie_timedata and self.last_time == "":
            self.movie_timedata[self.minute_time] = fresh_dict()
        elif self.minute_time not in self.movie_timedata and self.last_time != "":
            self.movie_timedata[self.minute_time] = copy_dict(
                self.movie_timedata[self.last_time])
        else:
            pass

    def update_labels(self):
        self.label3.config(text=self.movie_totals["£3"])
        self.label4.config(text=self.movie_totals["£4"])
        self.label5.config(text=self.movie_totals["Free"])
        self.label6.config(text=self.movie_totals["Half-Price"])
        self.label7.config(text=self.movie_totals["Special"])
        self.label9.config(text=self.movie_totals["Total"])

    def get_time(self):
        time_now = strftime("%H%M", localtime())
        minute_time = ""
        time_adjust = 1830 + (int(str(time_now)[0:2]) - 18) * 40
        minute_time = str(int(time_now) - time_adjust)
        return minute_time

    def cap_check(self):
        if self.movie_totals["Total"] == 290:
            showinfo("Alert!",
                     "We are at maximum capacity! (assuming 10 staff)")
        elif self.movie_totals["Total"] == 280:
            showinfo("Alert!", "Perform a seat check! (Approx. 10 left!")
        elif self.movie_totals["Total"] == 270:
            showinfo("Alert!", "Perform a seat check! (Approx. 20 left!")
        elif self.movie_totals["Total"] == 260:
            showinfo("Alert!", "Perform a seat check! (Approx. 30 left!")

    def finished(self):
        global movie_data
        movie_data[self.movie]["final"] = copy_dict(self.movie_totals)
        movie_data[self.movie]["timedata"] = copy_dict(self.movie_timedata)
        write_movie_dict("movie_database.json", movie_data)
        self.fresh_frame()
        self.cont.show_frame(Report)


class Report(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global movie_totals, movie_timedata
        self.cont = controller
        self.movie_totals = fresh_dict()
        self.movie_timedata = dict()
        self.movie = ""

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=0)

        self.button1 = tk.Button() # Main Menu button
        self.button2 = tk.Button() # Upload to Google button
        self.button3 = tk.Button() # Select button

        self.listMovies = tk.Listbox()  # Movie list
        self.scrollbar = tk.Scrollbar() # Scrollbar for Movie list

        self.label1 = tk.Label()   # Move Name label
        self.label2 = tk.Label()   # £3 label
        self.label3 = tk.Label()   # £4 label
        self.label4 = tk.Label()   # Free label
        self.label5 = tk.Label()   # Half-Price label
        self.label6 = tk.Label()   # Special label
        self.label7 = tk.Label()   # Total label

    def resetLabels(self):
        self.label1.destroy()   # Move Name label
        self.label2.destroy()   # £3 label
        self.label3.destroy()   # £4 label
        self.label4.destroy()   # Free label
        self.label5.destroy()   # Half-Price label
        self.label6.destroy()   # Special label
        self.label7.destroy()   # Total label

    def draw(self):
        global user_background, movie_data

        self.config(bg=user_background)
        self.resetLabels()

        ## Render the buttons to the screen ##
        self.button1 = tk.Button(
            self,
            text="Main Menu",
            highlightbackground=user_background,
            command=self.finished)
        self.button1.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.button2 = tk.Button(
            self,
            text="Upload to Google",
            highlightbackground=user_background,
            command=
            lambda: self.export_timedata(self.movie, self.movie_totals, self.movie_timedata)
        )
        self.button2.grid(row=0, column=2, sticky="nsew")
        self.button3 = tk.Button(
            self, highlightbackground=user_background, text="Select", command=lambda: self.display_labels(temp_mov_list[self.listMovies.curselection()[0]]))
        self.button3.grid(row=8, column=0, columnspan=2, sticky="nsew")

        ## Display the current database ##
        self.listMovies = tk.Listbox(
            self, height=21, bg="#B6E3FD", font=("ariel", 12))
        self.listMovies.grid(
            row=1, rowspan=7, column=0, sticky="nsew")
        self.scrollbar = tk.Scrollbar(
            self, bg=user_background, orient="vertical", command=self.listMovies.yview)
        self.scrollbar.grid(row=1, rowspan=7, column=1, sticky="nsew")
        self.listMovies.config(yscrollcommand=self.scrollbar.set)

        temp_mov_list = list()
        for x in movie_data:
            temp_mov_list.append(x)
            self.listMovies.insert(tk.END, str(" " + x))

        ## Display the lastest movie details ##
        self.display_labels(temp_mov_list[self.listMovies.size() - 1])

    def finished(self):
        self.cont.show_frame(StartPage)

    def display_labels(self, movie):
        global movie_data

        sIndent = "        "

        self.resetLabels()
        self.movie = movie
        self.movie_totals = copy_dict(movie_data[movie]["final"])
        try:
            self.movie_timedata = copy_dict(movie_data[movie]["timedata"])
        except KeyError:
            self.movie_timedata = dict()

        self.label1 = tk.Label(
            self,
            text="Movie: {0}".format(self.movie),
            font=LARGE_FONT,
            bg=user_background)
        self.label1.grid(row=1, column=2, sticky="w")
        self.label2 = tk.Label(
            self,
            text="{0}£3: {1}".format(sIndent, self.movie_totals["£3"]),
            bg=user_background)
        self.label2.grid(row=2, column=2, sticky="w")
        self.label3 = tk.Label(
            self,
            text="{0}£4: {1}".format(sIndent, self.movie_totals["£4"]),
            bg=user_background)
        self.label3.grid(row=3, column=2, sticky="w")
        self.label4 = tk.Label(
            self,
            text="{0}Free: {1}".format(sIndent, self.movie_totals["Free"]),
            bg=user_background)
        self.label4.grid(row=4, column=2, sticky="w")
        self.label5 = tk.Label(
            self,
            text="{0}Half-Price: {1}".format(sIndent, self.movie_totals["Half-Price"]),
            bg=user_background)
        self.label5.grid(row=5, column=2, sticky="w")
        self.label6 = tk.Label(
            self,
            text="{0}Free: {1}".format(sIndent, self.movie_totals["Free"]),
            bg=user_background)
        self.label6.grid(row=6, column=2, sticky="w")
        self.label7 = tk.Label(
            self,
            text="{0}Total: {1}".format(sIndent, self.movie_totals["Total"]),
            bg=user_background)
        self.label7.grid(row=7, column=2, sticky="w")

    def export_timedata(self, movie, finals, movie_timedata):
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
        sheet = spreadsheet.worksheet("Full-List")
        headers = [
            "Times", "£3", "£4", "Free", "Half-Price", "Special", "Total"
        ]
        worksheets = spreadsheet.worksheets()
        worksheets_names = list()
        for i in worksheets:
            worksheets_names.append(i.title)

        # main sheet
        try:
            cell = sheet.find(movie)
            cell_range = sheet.range(
                "B" + str(cell.row) + ":G" + str(cell.row))
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
        if messagebox.askyesno("YSC Helper", "Would you like to update the minute report?"):

            num_of_values = len(movie_timedata) + 1

            if movie in worksheets_names:
                worksheet = spreadsheet.worksheet(movie)
            else:
                worksheet = spreadsheet.add_worksheet(movie, num_of_values, 7)

            difference = len(movie_timedata) - worksheet.row_count + 1
            if difference > 0:
                worksheet.add_rows(difference)

            work_cells = worksheet.range("A1:G" + str(num_of_values))
            k = 0
            l = 0
            cur_time = ""
            timedata_k = list(movie_timedata.keys())
            for cell in work_cells:
                m_k = k % 7
                if k < 7:
                    cell.value = headers[k]
                elif m_k == 0:
                    cell.value = timedata_k[m_k]
                    cur_time = timedata_k[m_k]
                else:
                    cell.value = movie_timedata[cur_time][headers[m_k]]
                k += 1

            worksheet.update_cells(work_cells)
        showinfo("Alert!", "Upload complete.")


app = YscFoH()
app.geometry("450x400")
app.mainloop()
