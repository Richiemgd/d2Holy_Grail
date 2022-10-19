import sys
import os
import csv
from d2lib.files import SSSFile

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

item_lib_path = resource_path('data\Item_library.csv')

items = []

with open(item_lib_path, 'r') as file:
    reader = csv.DictReader(file)
    for item in reader:
        items.append(item)

def get_item_column(column, items):
    item_values = []
    for item in items:
        item_values.append(item[column])
    return item_values

def get_items_by_value(column, value, items):
    item_by_value = []
    for item in items:
        if item[column] == value:
            item_by_value.append(item)
    return item_by_value

def is_rune(item_name):
    return item_name.endswith('Rune')

def get_normal_grail_func():
    normal_grail = []
    for item in items:
        if item['Item Group 0'] != 'Runes':
            normal_grail.append(item)
    return normal_grail

get_not_found_items = get_items_by_value('Found', 'False', items)
get_not_found_item_names = get_item_column('Item', get_not_found_items)
get_normal_grail = get_normal_grail_func()
get_normal_grail_names = get_item_column('Item', get_normal_grail)
get_found_items = get_items_by_value('Found', 'True', get_normal_grail)
get_found_item_names = get_item_column('Item', get_found_items)
get_runes_grail = get_items_by_value('Item Group 0', 'Runes', items)
get_runes_grail_names = get_item_column('Item', get_runes_grail)
get_found_runes = get_items_by_value('Found', 'True', get_runes_grail)
get_found_rune_names = get_item_column('Item', get_found_runes)
get_normal_grail_completed_perc = round((len(get_found_item_names) / len(get_normal_grail_names)) * 100)
get_runes_grail_completed_perc = round((len(get_found_rune_names) / len(get_runes_grail_names)) * 100)
get_all_found = get_items_by_value('Found', 'True', items)
get_all_found_names = get_item_column('Item', get_all_found)
get_all_sets = get_items_by_value('Item Group 0', 'Sets', items)
get_all_sets_names = get_item_column('Item Group 1', get_all_sets)
get_all_sets_names = list(set(get_all_sets_names))
get_all_sets_names.sort()

def reload():
    global get_not_found_items, get_not_found_item_names, get_normal_grail, get_normal_grail_names, get_found_items, get_found_item_names
    global get_runes_grail, get_runes_grail_names, get_found_runes, get_found_rune_names, get_normal_grail_completed_perc, get_runes_grail_completed_perc
    global get_all_found, get_all_found_names, get_all_sets, get_all_sets_names
    get_not_found_items = get_items_by_value('Found', 'False', items)
    get_not_found_item_names = get_item_column('Item', get_not_found_items)
    get_normal_grail = get_normal_grail_func()
    get_normal_grail_names = get_item_column('Item', get_normal_grail)
    get_found_items = get_items_by_value('Found', 'True', get_normal_grail)
    get_found_item_names = get_item_column('Item', get_found_items)
    get_runes_grail = get_items_by_value('Item Group 0', 'Runes', items)
    get_runes_grail_names = get_item_column('Item', get_runes_grail)
    get_found_runes = get_items_by_value('Found', 'True', get_runes_grail)
    get_found_rune_names = get_item_column('Item', get_found_runes)
    get_normal_grail_completed_perc = round((len(get_found_item_names) / len(get_normal_grail_names)) * 100)
    get_runes_grail_completed_perc = round((len(get_found_rune_names) / len(get_runes_grail_names)) * 100)
    get_all_found = get_items_by_value('Found', 'True', items)
    get_all_found_names = get_item_column('Item', get_all_found)
    get_all_sets = get_items_by_value('Item Group 0', 'Sets', items)
    get_all_sets_names = get_item_column('Item Group 1', get_all_sets)
    get_all_sets_names = list(set(get_all_sets_names))
    get_all_sets_names.sort()

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
    sss_file = SSSFile(file_path)
    for page in sss_file.stash:
        for item in page['items']:
            if item.is_unique or item.is_set:
                update_item_found_status(item.name, 'True')

            elif item.itype == 3 and is_rune(item.name):
                update_item_found_status(item.base_name, 'True')