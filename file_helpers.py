import os, json


def load_movie_data_file(file_name):
    dict_from_file = {}
    with open(file_name, 'r') as inf:
        dict_from_file = json.load(inf)
    return dict_from_file


def create_movies_dir():
    if not os.path.exists('movies'):
        os.makedirs('movies')


def write_file(path, data):
    with open(path, 'w') as f:
        for i in data:
            f.write(i + '\n')


def write_movie_dict(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def create_file(path):
    write_file('movies/' + path, '')
    return True


def get_files(path):
    rawest_files = os.listdir(path)
    raw_files = list()
    result = list()
    if len(rawest_files) > 0:
        for _ in rawest_files:
            raw_files.append(_.replace('.json', ''))
        for _ in raw_files:
            result.append(_.replace('_timedata', ''))
        try:
            result.remove('.DS_Store')
        except ValueError:
            pass
    return result


def rem_dups(raw_list):
    new_list = list()
    for i in raw_list:
        if i not in new_list:
            new_list.append(i)
    return new_list
