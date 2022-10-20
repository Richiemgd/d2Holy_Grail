import PySimpleGUIQt as sg
import utils as hg
import cube_recipes as cr
import sys

# This bit gets the taskbar icon working properly in Windows
if sys.platform.startswith('win'):
    import ctypes
    if sys.argv[0].endswith('.exe') == False:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation')

sg.theme('DarkAmber')

font = ('Avqest', 11, 'bold')
sg.set_options(font=font)

def item_ui(slot, type):
    if slot != 'Sets':
        all_same_slot = hg.get_items_by_value('Item Group 1', slot, hg.items)
        quality_slot = hg.get_items_by_value('Item Group 2', type, all_same_slot)
        item_list = hg.get_item_column('Item', quality_slot)
    else:
        set_items = hg.get_items_by_value('Item Group 1', type, hg.items)
        item_list = hg.get_item_column('Item', set_items)

    unique_item_layout = [[sg.Text(f'{type}')]]
    unique_item_layout += [[sg.Checkbox(name, enable_events=True,
                                        key=f'{name} checkBox')] for name in item_list]
    return unique_item_layout

def item(slot):
    item = [[sg.Text(slot, justification='c')],
            [sg.Column(item_ui(slot, 'Normal')), sg.Column(
                item_ui(slot, 'Exceptional')), sg.Column(item_ui(slot, 'Elite'))]
            ]
    return item

def update_stats():
    hg.save_file(hg.items)
    window['-ITEMS-'].Update(
    f'Normal Grail {hg.normmal_grail_completed_perc()}% completed: {len(hg.found_items())} of {len(hg.normal_grail())} items found')
    window['-RUNES-'].Update(
        f'Runes Grail {hg.runes_grail_completed_perc()}% completed: {len(hg.found_runes())} of {len(hg.runes_grail())} runes found')
    window['-NOT_FOUND_ITEMS-'].Update(hg.not_found_items())

circlets = [[sg.Text('Circlet', justification='c')],
            [sg.Column(item_ui('Circlet', 'Exceptional')), sg.Column(item_ui('Circlet', 'Elite'))]]

empty_layout = []

unique_armor = [[sg.Column(item('Chest')), sg.Column(item('Gloves')), sg.Column(item('Shield'))],
                [sg.Column(item('Belt')), sg.Column(item('Boots')), sg.Column(item('Helm'))],
                [sg.Column(circlets), sg.Column(empty_layout), sg.Column(empty_layout)]]

unique_weapons_1 = [[sg.Column(item('Axe 1H')), sg.Column(item('Axe 2H')), sg.Column(item('Bow'))],
                    [sg.Column(item('Club 1H')), sg.Column(
                        item('Club 2H')), sg.Column(item('Crossbow'))],
                    [sg.Column(item('Dagger')), sg.Column(item('Polearm'))]]

javeline = [[sg.Text('Javeline')],
            [sg.Column(item_ui('Javelin', 'Elite'))]]

unique_weapons_2 = [[sg.Column(item('Scepter')), sg.Column(item('Spear')), sg.Column(item('Staff'))],
                    [sg.Column(item('Sword 1H')), sg.Column(
                        item('Sword 2H')), sg.Column(item('Throwing'))],
                    [sg.Column(javeline), sg.Column(item('Wand'))]]

jewelry = [[sg.Text('Jewelry', justification='c')],
           [sg.Column(item_ui('Jewelry', 'Amulets')), sg.Column(item_ui('Jewelry', 'Rings'))]]

d2_classes = [[sg.Text('Classes', justification='c')],
              [sg.Column(item_ui('Classes', 'Amazon')), sg.Column(
                  item_ui('Classes', 'Assasin')), sg.Column(item_ui('Classes', 'Barbarian'))],
              [sg.Column(item_ui('Classes', 'Druid')), sg.Column(
                  item_ui('Classes', 'Necromancer')), sg.Column(item_ui('Classes', 'Sorceress'))],
              [sg.Column(item_ui('Classes', 'Paladin'))]]

charms = [[sg.Text('Charms')],
          [sg.Column(item_ui('Charms', 'All'))]]

facet = [[sg.Text('Rainbow Facet (Jewel)', justification='c')],
         [sg.Column(item_ui('Rainbow Facet (Jewel)', 'Die')), sg.Column(item_ui('Rainbow Facet (Jewel)', 'Level Up'))]]

unique_misc = [[sg.Column(jewelry), sg.Column(d2_classes)],
               [sg.Column(charms), sg.Column(facet)]]

sets1 = [[sg.Text('Sets', justification='c')],
         [sg.Column(item_ui('Sets', f'{name}')) for name in hg.all_sets()[0:6]],
         [sg.Column(item_ui('Sets', f'{name}')) for name in hg.all_sets()[6:12]],
         [sg.Column(item_ui('Sets', f'{name}')) for name in hg.all_sets()[12:18]]]
 
sets2 = [[sg.Text('Sets', justification='c')],
         [sg.Column(item_ui('Sets', f'{name}')) for name in hg.all_sets()[18:24]],
         [sg.Column(item_ui('Sets', f'{name}')) for name in hg.all_sets()[24:30]],
         [sg.Column(item_ui('Sets', "Trang-Oul's Avatar")), sg.Column(item_ui('Sets', "Vidala's Rig"))]]

runes = [[sg.Text('Runes', justification='c')]]
runes += [[sg.Checkbox(name, enable_events=True,
                       key=f'{name} checkBox')] for name in hg.runes_grail()]

stats = [[sg.Text('Holy Grail', justification='c')],
         [sg.Text(key='-ITEMS-')],
         [sg.Text(key='-RUNES-')],
         [sg.Text('Add your PlugY stash to the Holy Grail')],
         [sg.Input(disabled=True, enable_events=True, key='-FILEBROWSER-'),
          sg.FilesBrowse(file_types=(('SSS Files', '*.sss'),), size=(10, 1)),
          sg.Button('Upload', size=(10, 1))],
         [sg.Text('Add an item to the Holy Grail')],
         [sg.Input(enable_events=True, key='-SEARCHBOX-'), sg.Button('Add Item',
                                                                     size=(10, 1))],
         [sg.Listbox(hg.not_found_items(), enable_events=True,
                     key='-NOT_FOUND_ITEMS-')]
         ]

recipes = [[sg.Text('Cube Recipes', justification='c')],
           [sg.Text('Search Recipe')],
           [sg.Input(enable_events=True, key='-SEARCHBOX2-')],
           [sg.Listbox(cr.recipes, enable_events=True, key='-RECIPES-')]
           ]

layout = [[sg.TabGroup([[
    sg.Tab('Holy Grail', stats),
    sg.Tab('Unique Armor', unique_armor),
    sg.Tab('Unique Weapons 1', unique_weapons_1),
    sg.Tab('Unique Weapons 2', unique_weapons_2),
    sg.Tab('Unique Misc', unique_misc),
    sg.Tab('Sets 1', sets1),
    sg.Tab('Sets 2', sets2),
    sg.Tab('Runes', runes),
    sg.Tab('Cube Recipes', recipes)]],
    tab_location='top',
    selected_title_color='#705e52',
    background_color='#2c2825',
)]
]

window = sg.Window('Holy Grail', layout, finalize=True, resizable=True, location=(0, 0), icon=hg.resource_path('data\hgicon.ico'))

[window[f'{name} checkBox'].Update(True) for name in hg.all_found()]

while True:             # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == '-FILEBROWSER-':
        filename = values['-FILEBROWSER-']
        window['-FILEBROWSER-'].Update(filename)
    if event.endswith('checkBox'):
        values = values[event]
        event = event.split(' checkBox')[0]
        hg.update_item_found_status(event, str(values))
        update_stats()
    if event == 'Upload':
        try:
            filename
        except NameError:
            sg.popup('Fist, browse a file!')
        if 'filename' in locals() and len(filename) > 0:
            hg.update_hg_from_sss(filename)
            update_stats()
            [window[f'{name} checkBox'].Update(True) for name in hg.all_found()]
            sg.popup('Holy grail updated!')
    if event == '-SEARCHBOX-':
        search = values['-SEARCHBOX-'].lower()
        new_values = [x for x in hg.not_found_items() if search in x.lower()]
        window['-NOT_FOUND_ITEMS-'].update(new_values)
    else:
        window['-NOT_FOUND_ITEMS-'].update(hg.not_found_items())
    if event == '-NOT_FOUND_ITEMS-' and len(values['-NOT_FOUND_ITEMS-']):
        item_selected = values['-NOT_FOUND_ITEMS-']
        item_name = item_selected[0]
        window['-SEARCHBOX-'].Update(item_name)
    if event == 'Add Item' and 'item_name' in locals():
        sg.popup('Item added to the Holy Grail', item_name)
        window[f'{item_name} checkBox'].Update(True)
        hg.update_item_found_status(item_name, 'True')
        update_stats()
    if event == '-SEARCHBOX2-':
        search = values['-SEARCHBOX2-'].lower()
        new_values = [x for x in cr.recipes if search in x.lower()]
        window['-RECIPES-'].update(new_values)
    else:
        window['-RECIPES-'].update(cr.recipes)
window.close()
