import shelve
import os

SHELF_FILE = os.path.dirname(os.path.abspath(__file__)) + '/params.shelf'


def open_shelf():
    return shelve.open(SHELF_FILE)


# Revtrieve params
def get_shelf():
    try:
        shelf = open_shelf()
        return_var = dict(shelf)
    finally:
        shelf.close()

    return return_var


def edit_shelf(add_mod):
    try:
        shelf = open_shelf()
        shelf.update(add_mod)
    finally:
        shelf.close()


def set_shelf(new_shelf):
    try:
        shelf = open_shelf()
        shelf.clear()
        shelf.update(new_shelf)
    finally:
        shelf.close()


# Get values:
def get_key(dict_key):
    try:
        shelf = open_shelf()
        return_var = shelf[dict_key]
    finally:
        shelf.close()

    return return_var


def get_annoy():
    DICT_KEY = 'ANNOY'
    get_key(DICT_KEY)
