from time import localtime, strftime
from file_helpers import *


def report(movie, movie_data_dict, movie_timedata):
    # Create a dictionary for each minute where there exists a record.
    # Also create dictionaries for specific intervals to measure.
    minute_report = dict()
    last_minute = ''
    pre_bets = {
        '£3': 0,
        '£4': 0,
        'Free': 0,
        'Half-Price': 0,
        'Special': 0,
        'Total': 0
    }

    for curr in movie_timedata:
        try:
            curr_time = curr.split('_')[0]
            curr_ticket = curr.split('_')[1]
            if int(curr_time) < 1900:
                curr_time_min = str(int(curr_time) - 1830)
            else:
                curr_time_min = str(int(curr_time) - 1870)

            if curr_time_min not in minute_report and last_minute == '':
                minute_report[curr_time_min] = {
                    '£3': 0,
                    '£4': 0,
                    'Free': 0,
                    'Half-Price': 0,
                    'Special': 0,
                    'Total': 0
                }
            else:
                minute_report[curr_time_min] = dict(minute_report[last_minute])

            if curr_ticket.split(' ')[0] == 'Added':
                minute_report[curr_time_min][curr_ticket.split(' ')[1]] += 1
                minute_report[curr_time_min]['Total'] += 1
            else:
                minute_report[curr_time_min][curr_ticket.split(' ')[1]] -= 1
                minute_report[curr_time_min]['Total'] -= 1
        except IndexError:
            break

        last_minute = curr_time_min

    for key in minute_report:
        if int(key) < 31:
            pre_bets['£3'] = minute_report[key]['£3']
            pre_bets['£4'] = minute_report[key]['£4']
            pre_bets['Free'] = minute_report[key]['Free']
            pre_bets['Half-Price'] = minute_report[key]['Half-Price']
            pre_bets['Special'] = minute_report[key]['Special']
            pre_bets['Total'] = minute_report[key]['Total']

    dividor = '-' * (len('Movie: ' + movie) + 4)
    print('Movie: ' + movie)
    print(dividor)
    print('End of the night')
    for key in movie_data_dict:
        print(key + ': ' + str(movie_data_dict[key]))
    print(dividor)
    print('At 7:00')
    for key in pre_bets:
        print(key + ': ' + str(pre_bets[key]))
    print(dividor)
    try:
        multiplier = movie_data_dict['Total'] / pre_bets['Total']
        print('Multiplier: ' + str(multiplier))
    except ZeroDivisionError:
        multiplier = 'Division by zero error when calculating multiplier'
        print(multiplier)

    report_data_path = 'movies/' + movie + '_report.txt'
    create_file(movie + '_report.txt')
    append_to_file(report_data_path, 'Movie: ' + movie)
    append_to_file(report_data_path, dividor)
    append_to_file(report_data_path, 'End of the night')
    for key in movie_data_dict:
        append_to_file(report_data_path,
                       key + ': ' + str(movie_data_dict[key]))
    append_to_file(report_data_path, dividor)
    append_to_file(report_data_path, 'At 7:00')
    for key in pre_bets:
        append_to_file(report_data_path, key + ': ' + str(pre_bets[key]))
    append_to_file(report_data_path, dividor)
    append_to_file(report_data_path, 'Multiplier: ' + str(multiplier))
    append_to_file(report_data_path, dividor)
    append_to_file(report_data_path, 'Each minute:')
    for key in minute_report:
        append_to_file(report_data_path, key + ': ' + str(minute_report[key]))
    print(dividor)
    print(dividor)
    print('This report has been saved to ' + report_data_path)
    try:
        input("Press Enter to continue...")
    except SyntaxError:
        pass


def record(exists, movie):
    recording = True
    movie_data_dict = dict()
    movie_timedata = list()
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
        #Load past data
        try:
            movie_data_dict = load_movie_data('movies/' + movie + '.json')
        except FileNotFoundError:
            movie_data_dict = {
                '£3': 0,
                '£4': 0,
                'Free': 0,
                'Half-Price': 0,
                'Special': 0,
                'Total': 0
            }
        try:
            movie_timedata = file_to_list('movies/' + movie + '_timedata.txt')
        except FileNotFoundError:
            pass
    else:
        create_file(movie + '.json')
        create_file(movie + '_timedata.txt')
        movie_data_dict = {
            '£3': 0,
            '£4': 0,
            'Free': 0,
            'Half-Price': 0,
            'Special': 0,
            'Total': 0
        }

    while recording:
        # Capacity Check
        capacity_messages = {
            250: 'We are very close to Capacity!',
            260: 'We are very very very close to Capacity!',
            270: 'Temporarily Close The Doors!'
        }
        if movie_data_dict['Total'] in capacity_messages:
            print('\n' * 20)
            print(capacity_messages[movie_data_dict['Total']])
            try:
                input('Press Enter to continue...')
            except SyntaxError:
                pass
        # Counter
        dividor = '-' * (len('£3: ' + str(movie_data_dict['£3']) + ' | £4: ' +
                             str(movie_data_dict['£4']) + ' | Free: ' + str(
                                 movie_data_dict['Free']) + ' | Half-Price: ' +
                             str(movie_data_dict['Half-Price']) +
                             ' | Total: ' + str(movie_data_dict['Total'])))
        scene_splitter = '#' * (
            len('£3: ' + str(movie_data_dict['£3']) + ' | £4: ' +
                str(movie_data_dict['£4']) + ' | Free: ' +
                str(movie_data_dict['Free']) + ' | Half-Price: ' + str(
                    movie_data_dict['Half-Price']) + ' | Total: ' + str(
                        movie_data_dict['Total'])))
        print(dividor)
        print('Movie: ' + movie)
        print('£3: ' + str(movie_data_dict['£3']) + ' | £4: ' + str(
            movie_data_dict['£4']) + ' | Free: ' + str(movie_data_dict['Free'])
              + ' | Half-Price: ' + str(movie_data_dict['Half-Price']) +
              ' | Special: ' + str(movie_data_dict['Special']) + ' | Total: ' +
              str(movie_data_dict['Total']))
        print(dividor)
        print('Recording Mode')
        print('(3) £3')
        print('(4) £4')
        print('(f) Free')
        print('(h) Half-Price')
        print('(s) Special')
        print('To remove x, type xr.')
        print('* stop')
        change = input('> ')
        print(scene_splitter)
        print(scene_splitter)

        date_time_now = strftime("%H%M", localtime())

        if change == 'stop':
            recording = False
        elif change in ticket_type:
            if ticket_type[change].split(' ')[0] == 'Added':
                movie_data_dict['Total'] += 1
                movie_data_dict[ticket_type[change].split(' ')[1]] += 1
                print(ticket_type[change])
            else:
                if movie_data_dict[ticket_type[change].split(' ')[1]] > 0:
                    movie_data_dict[ticket_type[change].split(' ')[1]] -= 1
                    movie_data_dict['Total'] -= 1
                    print(ticket_type[change])
                else:
                    print('There are no customers that bought a ' +
                          ticket_type[change].split(' ')[1] + ' ticket.')
            movie_timedata.append(date_time_now + '_' + ticket_type[change])
        else:
            print('Invalid Input.')

    write_movie_dict('movies/' + movie + '.json', movie_data_dict)
    write_file('movies/' + movie + '_timedata.txt', movie_timedata)
    return movie_data_dict, movie_timedata


# Initialization
running = True
create_movies_dir()

# Main Loop
while running:
    movie_data_dict = dict()
    movies_recorded = rem_dups(get_files('movies/'))
    print('')
    print('YSC Front of House')
    print('* record')
    if len(movies_recorded) > 0:
        print('* report')
    print('* quit')
    choice = input('> ')
    if choice == 'record':
        if len(movies_recorded) > 0:
            print('Movies already Recorded:')
            for i in movies_recorded:
                print('* ' + i)
        print('What movie would you like to record?')
        movie = input('> ')
        if movie in movies_recorded:
            print('Loading previous data.')
            movie_data_dict, movie_timedata = record(True, movie)
        else:
            movie_data_dict, movie_timedata = record(False, movie)
        print('Would you like to make a report of the screening?')
        print('* yes')
        print('* no')
        selection = input('> ')
        if selection == 'yes':
            report(movie, movie_data_dict, movie_timedata)
        elif selection == 'no':
            pass
        else:
            print('Invalid Input.')
    elif choice == 'report' and len(movies_recorded) > 0:
        print('Movies already Recorded:')
        running_sub = True
        while running_sub:
            for i in movies_recorded:
                print('* ' + i)
            print('For which movie would you like to make a report?')
            movie = input('> ')
            if movie in movies_recorded:
                print('Loading previous data.')
                movie_data_dict = load_movie_data('movies/' + movie + '.json')
                movie_timedata = file_to_list(
                    'movies/' + movie + '_timedata.txt')
                report(movie, movie_data_dict, movie_timedata)
                running_sub = False

            elif movie == 'quit':
                running_sub = False
            else:
                print('You must select a movie with pre-existing data.')
    elif choice == 'quit':
        running = False
    else:
        print('Invalid Input.')
        try:
            input("Press Enter to continue...")
        except SyntaxError:
            pass
