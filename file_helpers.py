import os, json


def load_movie_data_file(file_name):
    dict_from_file = {}
    with open(file_name, 'r') as inf:
        dict_from_file = json.load(inf)
    return dict_from_file

def write_file(path, data):
    with open(path, 'w') as f:
        for i in data:
            f.write(i + '\n')

def write_movie_dict(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def get_files(d):
    movies = list()
    for i in d:
        movies.append(i)
    return movies

def rem_dups(raw_list):
    new_list = list()
    for i in raw_list:
        if i not in new_list:
            new_list.append(i)
    return new_list
