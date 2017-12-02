from time import localtime, strftime
from file_helpers import *
from spreading import *


def report(movie, movie_totals, movie_timedata, early_screening = False):
    dividor = '-'*69

    print(dividor)
    print('Movie: ' + movie)
    print(dividor)
    print('End of the night:')
    print('£3: ' + str(movie_totals['£3']) + ' | £4: ' + str(
            movie_totals['£4']) + ' | Free: ' + str(movie_totals['Free'])
              + ' | Half-Price: ' + str(movie_totals['Half-Price']) +
              ' | Special: ' + str(movie_totals['Special']) + ' | Total: ' +
              str(movie_totals['Total']))
    print(dividor)
    if not early_sceening:
        pre_bets = {
            '£3': 0,
            '£4': 0,
            'Free': 0,
            'Half-Price': 0,
            'Special': 0,
            'Total': 0
        }
        for key in movie_timedata:
            if int(key) < 31:
                pre_bets['£3'] = movie_timedata[key]['£3']
                pre_bets['£4'] = movie_timedata[key]['£4']
                pre_bets['Free'] = movie_timedata[key]['Free']
                pre_bets['Half-Price'] = movie_timedata[key]['Half-Price']
                pre_bets['Special'] = movie_timedata[key]['Special']
                pre_bets['Total'] = movie_timedata[key]['Total']
        print('Before bets:')
        print('£3: ' + str(pre_bets['£3']) + ' | £4: ' + str(
            pre_bets['£4']) + ' | Free: ' + str(pre_bets['Free'])
              + ' | Half-Price: ' + str(pre_bets['Half-Price']) +
              ' | Special: ' + str(pre_bets['Special']) + ' | Total: ' +
              str(pre_bets['Total']))
        print(dividor)
        try:
            multiplier = int(movie_totals['Total']) / int(pre_bets['Total'])
            print('Multiplier: ' + str(multiplier))
        except ZeroDivisionError:
            multiplier = 'There were no customers before 7:00 and so no multiplier.'
            print(multiplier)
        print(dividor)
    print('')
    print('Would you like to upload this data to the Google Sheet?')
    print('* yes')
    print('* no')
    choice = input('> ')

    if choice == 'yes':
        export_timedata(movie, movie_timedata, movie_totals)
    else:
        pass

def load_movie_data(movie):
    movie_totals = dict()
    movie_timedata = dict()
    try:
        movie_totals = load_movie_data_file('movies/' + movie + '.json')
    except FileNotFoundError:
        movie_totals = {
            '£3': 0,
            '£4': 0,
            'Free': 0,
            'Half-Price': 0,
            'Special': 0,
            'Total': 0
        }
    try:
        movie_timedata = load_movie_data_file('movies/' + movie + '_timedata.json')
    except FileNotFoundError:
        pass

    return movie_totals, movie_timedata

def warning_messages(total):
    warnings = {
        250 : 'We are nearing full.',
        260 : 'Prepare to start warning customers.',
        270 : 'Temporarily close the doors and do a seat count.'
    }
    if total in warnings:
            print('\n' * 20)
            print(warnings[total])
            try:
                input('Press Enter to continue...')
            except SyntaxError:
                pass

def record(exists, movie, early_sceening = False):

    recording = True
    minute_time = '0'
    movie_totals = dict()
    movie_timedata = dict()
    ticket_type = {
        '3': 'Added £3',
        '3r': 'Removed £3',
        '4': 'Added £4',
        '4r': 'Removed £4',
        'f': 'Added Free',
        'fr': 'Removed Free',
        'h': 'Added Half-Price',
        'hr': 'Removed Half-Price',
        's': 'Added Special',
        'sr': 'Removed Special'
    }
    
    if exists:
        # load previous data to continue recording
        movie_totals, movie_timedata = load_movie_data(movie)
    else:
        # create new dictionaries for recording
        create_file(movie + '.json')
        create_file(movie + '_timedata.json')
        movie_totals = {
            '£3': 0,
            '£4': 0,
            'Free': 0,
            'Half-Price': 0,
            'Special': 0,
            'Total': 0
        }

    while recording:

        warning_messages(movie_totals['Total'])
        dividor = '-'*69
        scene_splitter = '#'*69

        print(dividor)
        print('Movie: ' + movie)
        print('£3: ' + str(movie_totals['£3']) + ' | £4: ' + str(
            movie_totals['£4']) + ' | Free: ' + str(movie_totals['Free'])
              + ' | Half-Price: ' + str(movie_totals['Half-Price']) +
              ' | Special: ' + str(movie_totals['Special']) + ' | Total: ' +
              str(movie_totals['Total']))
        print(dividor)
        print('Recording Mode:')
        print('(3) £3')
        print('(4) £4')
        print('(f) Free')
        print('(h) Half-Price')
        print('(s) Special')
        print('To remove x, type xr.')
        print('* stop')
        ticket = input('> ')

        print(scene_splitter)
        print(scene_splitter)
        time_now = strftime("%H%M", localtime())
        last_time = ''

        if ticket == 'stop':
            recording = False
        elif ticket in ticket_type:
            if time_now not in movie_timedata and last_time == '':
                movie_timedata[minute_time] = {
                    '£3': 0,
                    '£4': 0,
                    'Free': 0,
                    'Half-Price': 0,
                    'Special': 0,
                    'Total': 0
                }
            elif time_now not in movie_timedata and last_time != '':
                movie_timedata[minute_time] = movie_timedata[last_time]

            if early_sceening:
                if time_now < 1800:
                    minute_time = str(int(time_now) - 1790)
                else:
                    minute_time = str(int(time_now) - 1830)
            else:
                if time_now < 1900:
                    minute_time = str(int(time_now) - 1830)
                else:
                    minute_time = str(int(time_now) - 1870)

            if ticket_type[ticket].split(' ')[0] == 'Added':
                movie_totals['Total'] += 1
                movie_timedata[minute_time]['Total'] += 1
                movie_totals[ticket_type[ticket].split(' ')[1]] += 1
                movie_timedata[minute_time][ticket_type[ticket].split(' ')[1]] += 1
                print(time_now + ' -- ' + ticket_type[ticket])
            else:
                if movie_totals[ticket_type[ticket].split(' ')[1]] > 0:
                    movie_totals['Total'] -= 1
                    movie_timedata[minute_time]['Total'] -= 1
                    movie_totals[ticket_type[ticket].split(' ')[1]] -= 1
                    movie_timedata[minute_time][ticket_type[ticket].split(' ')[1]] -= 1
                    print(time_now + ' -- ' + ticket_type[ticket])
                else:
                    print('There are no customers who have bought a ' +
                        ticket_type[ticket].split(' ')[1] + ' ticket.')
            last_time = time_now

        else:
            print('Invalid input: ' + ticket + '.')
        
    write_movie_dict('movies/' + movie + '.json', movie_totals)
    write_movie_dict('movies/' + movie + '_timedata.json', movie_timedata)

    return movie_totals, movie_timedata


# Initialization
running = True
create_movies_dir()

# Main Loop
while running:
    movie_total = dict()
    movies_recorded = rem_dups(get_files('movies/'))
    early_sceening = False

    print('')
    print('YSC Front of House')
    print('* record')
    if len(movies_recorded) > 0:
        print('* report')
    print('* quit')
    choice = input('> ').lower()

    if choice == 'quit':
        running = False
    elif choice == 'record':
        print('What movie would you like to record?')
        movie = input('> ')
        print('Is this an early screening?')
        print('* y')
        print('* n')
        early_sceening_in = input('> ')

        if early_sceening_in == 'y':
            early_sceening = True
        else:
            early_sceening = False

        if movie in movies_recorded:
            print('Loading previous movie data...')
            movie_total, movie_timedata = record(True, movie, early_sceening)
        else:
            movie_total, movie_timedata = record(False, movie, early_sceening)

        print('Would you like to compile a report of this screening?')
        print('* yes')
        print('* no')
        report_choice = input('> ')

        if report_choice == 'yes':
            report(movie, movie_total, movie_timedata, early_sceening)
        elif report_choice == 'no':
            pass
        else:
            print('Invalid input: ' + report + '.')

    elif choice == 'report' and len(movies_recorded) > 0:
        print('Movies in the database:')
        for i in movies_recorded:
            print('* ' + i)
        print('Which movie would you like to compile a report for?')
        movie = input('> ')

        print('Was this an early screening?')
        print('* yes')
        print('* no')
        early_sceening_in = input('> ')

        if early_sceening_in == 'yes':
            early_screening = True
        else:
            early_screening = False

        if movie in movies_recorded:
            movie_total, movie_timedata = load_movie_data(movie)
            report(movie, movie_total, movie_timedata, early_sceening)
        else:
            pass

    else:
        print('Invalid input: ' + choice + '.')
        try:
            input("Press Enter to continue...")
        except SyntaxError:
            pass
