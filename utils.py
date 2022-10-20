import sys
import os
import csv
from d2lib.files import SSSFile

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

item_lib_path = resource_path('data\itemlib.csv')

#List of dictionaries
items = []

with open(item_lib_path, 'r') as file:
    reader = csv.DictReader(file)
    for item in reader:
        items.append(item)

def get_item_column(column, items):
    """
    param column = name of the column
    param items = list of dictionaries
    returns a list with the column values
    """
    item_values = []
    for item in items:
        item_values.append(item[column])
    return item_values

def get_items_by_value(column, value, items):
    """
    param column = name of the column
    param value = if value == value in column then adds the item to item_by_value
    param items = list of dictionaries
    returns a list of dictionaries of the selected column and value
    """
    item_by_value = []
    for item in items:
        if item[column] == value:
            item_by_value.append(item)
    return item_by_value

def is_rune(item_name):
    return item_name.endswith('Rune')

def get_normal_grail_func():
    """
    returns all the items - runes
    """
    normal_grail = []
    for item in items:
        if item['Item Group 0'] != 'Runes':
            normal_grail.append(item)
    return normal_grail

def not_found_items():
    """
    returns a list of not found item names
    """
    get_not_found_items = get_items_by_value('Found', 'False', items)
    return get_item_column('Item', get_not_found_items)

def normal_grail():
    """
    returns a list of item names - runes
    """
    get_normal_grail = get_normal_grail_func()
    return get_item_column('Item', get_normal_grail)

def found_items():
    """
    returns a list of found item names
    """
    get_found_items = get_items_by_value('Found', 'True', get_normal_grail_func())
    return get_item_column('Item', get_found_items)

def runes_grail():
    """
    returns a list of runes
    """
    get_runes_grail = get_items_by_value('Item Group 0', 'Runes', items)
    return get_item_column('Item', get_runes_grail)

def found_runes():
    """
    returns a list of found runes
    """
    get_runes_grail = get_items_by_value('Item Group 0', 'Runes', items)
    get_found_runes = get_items_by_value('Found', 'True', get_runes_grail)
    return get_item_column('Item', get_found_runes)
    
def normmal_grail_completed_perc():
    """
    returns an int representing the % of items found
    """
    return round((len(found_items()) / len(normal_grail())) * 100)

def runes_grail_completed_perc():
    """
    returns an int representing the % of runes found
    """
    return round((len(found_runes()) / len(runes_grail())) * 100)

def all_found():
    """
    returns a list of names with all the found items
    """
    get_all_found = get_items_by_value('Found', 'True', items)
    return get_item_column('Item', get_all_found)

def all_sets():
    """
    returns a list of names with all the sets
    """
    get_all_sets = get_items_by_value('Item Group 0', 'Sets', items)
    get_all_sets_names = get_item_column('Item Group 1', get_all_sets)
    get_all_sets_names = list(set(get_all_sets_names))
    get_all_sets_names.sort()
    return get_all_sets_names

def save_file(items):
    with open(item_lib_path, 'w', encoding='utf8', newline='') as file:
        tocsv = csv.DictWriter(file, fieldnames=items[0].keys())
        tocsv.writeheader()
        tocsv.writerows(items)

def update_item_found_status(item_name, status):
    updated_items = []
    global items
    for item in items:
        if item['Item'] == item_name:
            item['Found'] = status
        updated_items.append(item)
    items = updated_items

def update_hg_from_sss(file_path):
    """
    parses the PlugY stash and updates the items list of dictionaries
    """
    sss_file = SSSFile(file_path)
    for page in sss_file.stash:
        for item in page['items']:
            if item.is_unique or item.is_set:
                update_item_found_status(item.name, 'True')

            elif item.itype == 3 and is_rune(item.name):
                update_item_found_status(item.base_name, 'True')