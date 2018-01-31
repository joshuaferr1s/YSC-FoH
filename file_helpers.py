import os, json


def load_movie_data_file(file_name):
    dict_from_file = {}
    with open(file_name, 'r') as inf:
        dict_from_file = json.load(inf)
    return dict_from_file


def write_movie_dict(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def keys_to_list(d):
    movies = list()
    for i in d:
        movies.append(i)
    return movies