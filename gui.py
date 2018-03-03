import tkinter as tk
from tkinter import ttk
from time import localtime, strftime
import json, gspread
from tkinter.messagebox import showinfo
from oauth2client.service_account import ServiceAccountCredentials

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
cur_movie = ""
exists = False
early_sceening = True
movie_totals_g = dict()
movie_timedata_g = dict()


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


movie_data = load_json_file("movie_database.json")


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
        filemenu.add_command(
            label="Save settings",
            command=lambda: showinfo("Alert!", "Not implemented yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = dict()

        for F in (StartPage, Record, Report, SelectMovie):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        self.config(bg="light sky blue")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        label = tk.Label(
            self,
            text="YSC Front of House",
            font=("Comic Sans", 20),
            bg="light sky blue")
        label.grid(row=1, column=1)

        button1 = tk.Button(
            self,
            text="Record",
            command=lambda: controller.show_frame(SelectMovie),
            highlightbackground="light sky blue")
        button1.grid(row=2, column=1)
        button2 = tk.Button(
            self,
            text="Report",
            command=lambda: controller.show_frame(Report),
            highlightbackground="light sky blue")
        button2.grid(row=3, column=1)


class SelectMovie(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        self.config(bg="light sky blue")

        label = tk.Label(
            self,
            text="Select a movie to record...",
            font=LARGE_FONT,
            bg="light sky blue")
        label.grid(row=0, column=0, columnspan=5, sticky="nsew")

        self.listMovies = tk.Listbox(
            self, width=25, height=20, font=NORM_FONT, bg="#B6E3FD")
        self.listMovies.grid(
            row=1, rowspan=10, column=0, columnspan=3, sticky="nsew")
        self.scrollbar = tk.Scrollbar(
            self, bg="light sky blue", orient="vertical")
        self.scrollbar.config(command=self.listMovies.yview)
        self.scrollbar.grid(row=1, rowspan=10, column=4, sticky="nsew")

        self.listMovies.config(yscrollcommand=self.scrollbar.set)

        self.temp_mov_list = list()
        for x in movie_data:
            self.temp_mov_list.append(x)
            self.listMovies.insert(tk.END, str(" " + x))

        entry1 = tk.Entry(self, highlightbackground="light sky blue")
        entry1.grid(row=1, column=5, columnspan=2, sticky="nsew")

        button1 = tk.Button(
            self,
            text="Early",
            highlightbackground="light sky blue",
            command=
            lambda: self.recorder(temp_mov_list[listMovies.curselection()[0]], True, True)
        )
        button1.grid(row=11, column=0, sticky="nsew")
        button2 = tk.Button(
            self,
            text="Regular",
            highlightbackground="light sky blue",
            command=
            lambda: self.recorder(temp_mov_list[listMovies.curselection()[0]], True, False)
        )
        button2.grid(row=11, column=1, columnspan=4, sticky="nsew")
        button3 = tk.Button(
            self,
            text="New Early",
            highlightbackground="light sky blue",
            command=
            lambda: self.recorder(entry1.get(), self.check_ex(entry1.get()), True)
        )
        button3.grid(row=2, column=5, sticky="nsew")
        button4 = tk.Button(
            self,
            text="New Regular",
            highlightbackground="light sky blue",
            command=
            lambda: self.recorder(entry1.get(), self.check_ex(entry1.get()), False)
        )
        button4.grid(row=2, column=6, sticky="nsew")
        button5 = tk.Button(
            self,
            text="Main Menu",
            highlightbackground="light sky blue",
            command=lambda: controller.show_frame(StartPage))
        button5.grid(row=3, column=5, columnspan=2, sticky="nsew")
        button6 = tk.Button(
            self,
            text="Update",
            highlightbackground="light sky blue",
            command=self.updateMovies)
        button6.grid(row=12, column=0, columnspan=5, sticky="nsew")

    def updateMovies(self):
        self.listMovies.destroy()
        self.listMovies = tk.Listbox(
            self, width=25, height=20, font=NORM_FONT, bg="#B6E3FD")
        self.listMovies.grid(
            row=1, rowspan=10, column=0, columnspan=3, sticky="nsew")
        self.listMovies.config(yscrollcommand=self.scrollbar.set)
        self.temp_mov_list = list()
        for x in movie_data:
            self.temp_mov_list.append(x)
            self.listMovies.insert(tk.END, str(" " + x))

    def recorder(self, movie, d_exists, d_early):
        global cur_movie, exists, early_sceening
        cur_movie = movie
        exists = d_exists
        early_sceening = d_early
        self.cont.show_frame(Record)

    def check_ex(self, movie):
        global movie_data
        if movie not in movie_data:
            existence = False
        elif movie in movie_data:
            existence = True
        return existence


class Record(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="light sky blue")
        self.par = parent
        self.cont = controller
        self.movie_totals = dict()
        self.movie_timedata = dict()
        self.minute_time = ""
        self.last_time = ""
        self.movie = ""

        self.button_1 = tk.Button(
            self,
            text="Begin",
            highlightbackground="light sky blue",
            command=self.recorder)
        self.button_1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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

    def fresh_frame(self):
        self.button_1 = tk.Button(
            self,
            text="Begin",
            highlightbackground="light sky blue",
            command=self.recorder)
        self.button_1.grid(row=0, column=0)

        # Destroy Everything
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

    def recorder(self):
        self.button_1.destroy()
        global cur_movie, movie_data, exists, early_sceening
        self.movie = cur_movie
        lab_text = "Recording: {0}".format(self.movie)

        if exists:
            self.movie_totals = copy_dict(movie_data[self.movie]["final"])
            self.movie_timedata = copy_dict(movie_data[self.movie]["timedata"])
            times_a = self.get_listo(self.movie_timedata)
            self.last_time = times_a[-1]
        else:
            self.movie_totals = {
                "£3": 0,
                "£4": 0,
                "Free": 0,
                "Half-Price": 0,
                "Special": 0,
                "Total": 0
            }
            movie_data[self.movie] = dict()
            movie_data[self.movie]["final"] = dict()
            movie_data[self.movie]["timedata"] = dict()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=6)

        self.label1 = tk.Label(
            self, text=lab_text, font=("Comic Sans", 20), bg="light sky blue")
        self.label1.grid(row=0, columnspan=3)

        #### £3 ####
        self.button3 = tk.Button(
            self,
            text="£3 +",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button3.config(command=lambda: self.incr_ticket("£3"))
        self.button3.grid(row=1, column=0, sticky="nsew")
        self.button3_ = tk.Button(
            self,
            text="£3 -",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button3_.config(command=lambda: self.decr_ticket("£3"))
        self.button3_.grid(row=1, column=1, sticky="nsew")
        self.label3 = tk.Label(
            self, text=self.movie_totals["£3"], bg="light sky blue")
        self.label3.grid(row=1, column=2, sticky="w")

        #### £4 ####
        self.button4 = tk.Button(
            self,
            text="£4 +",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button4.config(command=lambda: self.incr_ticket("£4"))
        self.button4.grid(row=2, column=0, sticky="nsew")
        self.button4_ = tk.Button(
            self,
            text="£4 -",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button4_.config(command=lambda: self.decr_ticket("£4"))
        self.button4_.grid(row=2, column=1, sticky="nsew")
        self.label4 = tk.Label(
            self, text=self.movie_totals["£4"], bg="light sky blue")
        self.label4.grid(row=2, column=2, sticky="w")

        #### Free ####
        self.button5 = tk.Button(
            self,
            text="Free +",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button5.config(command=lambda: self.incr_ticket("Free"))
        self.button5.grid(row=3, column=0, sticky="nsew")
        self.button5_ = tk.Button(
            self,
            text="Free -",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button5_.config(command=lambda: self.decr_ticket("Free"))
        self.button5_.grid(row=3, column=1, sticky="nsew")
        self.label5 = tk.Label(
            self, text=self.movie_totals["Free"], bg="light sky blue")
        self.label5.grid(row=3, column=2, sticky="w")

        #### Half-Price ####
        self.button6 = tk.Button(
            self,
            text="Half +",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button6.config(command=lambda: self.incr_ticket("Half-Price"))
        self.button6.grid(row=4, column=0, sticky="nsew")
        self.button6_ = tk.Button(
            self,
            text="Half -",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button6_.config(command=lambda: self.decr_ticket("Half-Price"))
        self.button6_.grid(row=4, column=1, sticky="nsew")
        self.label6 = tk.Label(
            self, text=self.movie_totals["Half-Price"], bg="light sky blue")
        self.label6.grid(row=4, column=2, sticky="w")

        #### Special ####
        self.button7 = tk.Button(
            self,
            text="Spec +",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button7.config(command=lambda: self.incr_ticket("Special"))
        self.button7.grid(row=5, column=0, sticky="nsew")
        self.button7_ = tk.Button(
            self,
            text="Spec -",
            font=NORM_FONT,
            highlightbackground="light sky blue")
        self.button7_.config(command=lambda: self.decr_ticket("Special"))
        self.button7_.grid(row=5, column=1, sticky="nsew")
        self.label7 = tk.Label(
            self, text=self.movie_totals["Special"], bg="light sky blue")
        self.label7.grid(row=5, column=2, sticky="w")

        #### Total ####
        self.label8 = tk.Label(
            self, text="Total:", font=("Comic Sans", 15), bg="light sky blue")
        self.label8.grid(row=6, column=1, sticky="e")
        self.label9 = tk.Label(
            self,
            text=self.movie_totals["Total"],
            bg="light sky blue",
            font=("Comic Sans", 15))
        self.label9.grid(row=6, column=2, sticky="w")

        self.button1 = tk.Button(
            self,
            text="Finished",
            highlightbackground="light sky blue",
            command=self.finished)
        self.button1.grid(row=7, columnspan=2, sticky="nsew")

    def incr_ticket(self, ticket):
        self.minute_time = self.get_time()
        self.timedata_handler()
        self.movie_totals["Total"] += 1
        self.movie_totals[ticket] += 1
        self.movie_timedata[self.minute_time]["Total"] += 1
        self.movie_timedata[self.minute_time][ticket] += 1
        self.update_labels()
        self.last_time = self.minute_time

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
        return minute_time

    def get_listo(d):
        l = list()
        for i in d:
            l.append(i)
        return l

    def finished(self):
        global movie_data, movie_totals_g, movie_timedata_g
        movie_data[self.movie]["final"] = copy_dict(self.movie_totals)
        movie_totals_g = copy_dict(self.movie_totals)
        movie_data[self.movie]["timedata"] = copy_dict(self.movie_timedata)
        movie_timedata_g = copy_dict(self.movie_timedata)
        write_movie_dict("movie_database.json", movie_data)
        self.fresh_frame()
        self.cont.show_frame(Report)


class Report(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global movie_totals, movie_timedata
        self.config(bg="light sky blue")
        self.cont = controller
        self.movie_totals = fresh_dict()
        self.movie_timedata = dict()
        self.movie = ""

        self.button_1 = tk.Button(
            self,
            text="Main Menu",
            width=15,
            highlightbackground="light sky blue",
            command=self.finished)
        self.button_1.grid(row=0, column=0, columnspan=6, sticky="nsew")
        self.button_2 = tk.Button(
            self,
            text="Compile Report",
            highlightbackground="light sky blue",
            command=self.compile_report)
        self.button_2.grid(row=0, column=6, columnspan=4, sticky="nsew")
        self.button_3 = tk.Button()

        self.label11 = tk.Label()
        self.label12 = tk.Label()
        self.label13 = tk.Label()
        self.label14 = tk.Label()
        self.label15 = tk.Label()
        self.label16 = tk.Label()
        self.label17 = tk.Label()
        self.label18 = tk.Label()
        self.label19 = tk.Label()
        self.label110 = tk.Label()
        self.label111 = tk.Label()
        self.label112 = tk.Label()
        self.label113 = tk.Label()
        self.label114 = tk.Label()
        self.label115 = tk.Label()

        self.listMovies = tk.Listbox()
        self.scrollbar = tk.Scrollbar()
        self.B1 = tk.Button()
        self.B2 = tk.Button()

    def fresh_frame(self):
        self.button_1 = tk.Button(
            self,
            text="Main Menu",
            width=15,
            highlightbackground="light sky blue",
            command=lambda: self.cont.show_frame(StartPage))
        self.button_1.grid(row=0, column=0, columnspan=6, sticky="nsew")
        self.button_2 = tk.Button(
            self,
            text="Compile Report",
            highlightbackground="light sky blue",
            command=self.compile_report)
        self.button_2.grid(row=0, column=6, columnspan=4, sticky="nsew")

        self.button_3.destroy()
        self.label11.destroy()
        self.label12.destroy()
        self.label13.destroy()
        self.label14.destroy()
        self.label15.destroy()
        self.label16.destroy()
        self.label17.destroy()
        self.label18.destroy()
        self.label19.destroy()
        self.label110.destroy()
        self.label111.destroy()
        self.label112.destroy()
        self.label113.destroy()
        self.label114.destroy()
        self.label115.destroy()
        self.listMovies.destroy()
        self.scrollbar.destroy()
        self.B1.destroy()
        self.B2.destroy()

    def compile_report(self):

        self.button_2.destroy()
        self.button_3 = tk.Button(
            self,
            text="Upload to Google",
            highlightbackground="light sky blue",
            command=
            lambda: self.export_timedata(self.movie, self.movie_totals, self.movie_timedata)
        )
        self.button_3.grid(row=0, column=6, columnspan=4, sticky="nsew")

        self.listMovies = tk.Listbox(
            self, width=25, height=20, bg="#B6E3FD", font=("ariel", 12))
        self.listMovies.grid(
            row=1, rowspan=15, column=0, columnspan=5, sticky="nsew")
        self.scrollbar = tk.Scrollbar(
            self, bg="light sky blue", orient="vertical")
        self.scrollbar.config(command=self.listMovies.yview)
        self.scrollbar.grid(row=1, rowspan=15, column=5, sticky="nsew")

        self.listMovies.config(yscrollcommand=self.scrollbar.set)

        temp_mov_list = list()
        for x in movie_data:
            temp_mov_list.append(x)
            self.listMovies.insert(tk.END, str(" " + x))

        self.B1 = tk.Button(
            self, highlightbackground="light sky blue", text="Early")
        self.B1.config(command=lambda: self.display_labels(temp_mov_list[self.listMovies.curselection()[0]], True))
        self.B1.grid(row=16, column=0, columnspan=2, sticky="nsew")
        self.B2 = tk.Button(
            self, highlightbackground="light sky blue", text="Regular")
        self.B2.config(command=lambda: self.display_labels(temp_mov_list[self.listMovies.curselection()[0]], False))
        self.B2.grid(row=16, column=2, columnspan=4, sticky="nsew")

        self.display_labels(temp_mov_list[self.listMovies.size() - 1], False)

    def finished(self):
        self.fresh_frame()
        self.cont.show_frame(StartPage)

    def display_labels(self, movie, early_s):
        global movie_data

        self.clear_labels()
        self.movie = movie
        self.movie_totals = copy_dict(movie_data[movie]["final"])
        self.movie_timedata = copy_dict(movie_data[movie]["timedata"])

        self.label11 = tk.Label(
            self,
            text="Movie: {0}".format(self.movie),
            font=LARGE_FONT,
            bg="light sky blue")
        self.label11.grid(row=1, column=6, columnspan=4, sticky="w")
        self.label12 = tk.Label(
            self,
            text="£3: {0}".format(self.movie_totals["£3"]),
            bg="light sky blue")
        self.label12.grid(row=2, column=7, columnspan=3, sticky="w")
        self.label13 = tk.Label(
            self,
            text="£4: {0}".format(self.movie_totals["£4"]),
            bg="light sky blue")
        self.label13.grid(row=3, column=7, columnspan=3, sticky="w")
        self.label14 = tk.Label(
            self,
            text="£4: {0}".format(self.movie_totals["£4"]),
            bg="light sky blue")
        self.label14.grid(row=4, column=7, columnspan=3, sticky="w")
        self.label15 = tk.Label(
            self,
            text="Free: {0}".format(self.movie_totals["Free"]),
            bg="light sky blue")
        self.label15.grid(row=5, column=7, columnspan=3, sticky="w")
        self.label16 = tk.Label(
            self,
            text="Half-Price: {0}".format(self.movie_totals["Half-Price"]),
            bg="light sky blue")
        self.label16.grid(row=6, column=7, columnspan=3, sticky="w")
        self.label17 = tk.Label(
            self,
            text="Special: {0}".format(self.movie_totals["Special"]),
            bg="light sky blue")
        self.label17.grid(row=7, column=7, columnspan=3, sticky="w")
        self.label18 = tk.Label(
            self,
            text="Total: {0}".format(self.movie_totals["Total"]),
            bg="light sky blue")
        self.label18.grid(row=8, column=7, columnspan=3, sticky="w")
        if not early_s:
            pre_bets = fresh_dict()
            for key in self.movie_timedata:
                if int(key) < 31:
                    pre_bets = self.movie_timedata[key]
            self.label19 = tk.Label(
                self, text="Pre-Bets:", font=LARGE_FONT, bg="light sky blue")
            self.label19.grid(row=9, column=6, columnspan=4, sticky="w")
            self.label110 = tk.Label(
                self,
                text="£3: {0}".format(pre_bets["£3"]),
                bg="light sky blue")
            self.label110.grid(row=10, column=7, columnspan=3, sticky="w")
            self.label111 = tk.Label(
                self,
                text="£4: {0}".format(pre_bets["£4"]),
                bg="light sky blue")
            self.label111.grid(row=11, column=7, columnspan=3, sticky="w")
            self.label112 = tk.Label(
                self,
                text="Free: {0}".format(pre_bets["Free"]),
                bg="light sky blue")
            self.label112.grid(row=12, column=7, columnspan=3, sticky="w")
            self.label113 = tk.Label(
                self,
                text="Half-Price: {0}".format(pre_bets["Half-Price"]),
                bg="light sky blue")
            self.label113.grid(row=13, column=7, columnspan=3, sticky="w")
            self.label114 = tk.Label(
                self,
                text="Special: {0}".format(pre_bets["Special"]),
                bg="light sky blue")
            self.label114.grid(row=14, column=7, columnspan=3, sticky="w")
            self.label115 = tk.Label(
                self,
                text="Total: {0}".format(pre_bets["Total"]),
                bg="light sky blue")
            self.label115.grid(row=15, column=7, columnspan=3, sticky="w")

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
        sheet = spreadsheet.worksheet("Spr-Membership")
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
        else:
            worksheet = spreadsheet.add_worksheet(movie, num_of_values, 7)

        difference = len(movie_timedata) - worksheet.row_count + 1
        if difference > 0:
            worksheet.add_rows(difference)
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
        showinfo("Alert!", "Timedata upload complete.")

    def clear_labels(self):
        self.label11.destroy()
        self.label12.destroy()
        self.label13.destroy()
        self.label14.destroy()
        self.label15.destroy()
        self.label16.destroy()
        self.label17.destroy()
        self.label18.destroy()
        self.label19.destroy()
        self.label110.destroy()
        self.label111.destroy()
        self.label112.destroy()
        self.label113.destroy()
        self.label114.destroy()
        self.label115.destroy()


app = YscFoH()
app.geometry("450x400")
app.mainloop()
