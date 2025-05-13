from nicegui import ui
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def calculate_cost(b):
    if b == 0:
        return 0
    elif b < 1.5:
        return 25
    elif b < 2.5:
        return 28
    elif b < 5:
        return 32
    elif b < 10:
        return 35
    else:
        return 45

def update():
    weight_value = weight.value or 0
    cost_dogs = calculate_cost(weight_value)
    breed_value = breed.value or "Not Specified"
    dog_data = pd.read_csv('dog_data.csv')
    next_id = dog_data['id'].max() + 1 if not dog_data.empty else 0
    new_data = pd.DataFrame({'Breed': [breed_value], 'Weight': [weight_value], 'Cost': [cost_dogs], 'id': [next_id]})
    dog_data = pd.concat([dog_data, new_data], ignore_index=True)
    dog_data.to_csv('dog_data.csv', index=False)
    table_dog.update_from_pandas(dog_data)

def delete_selected():
    dog_data = pd.read_csv('dog_data.csv')
    selection_list = list(map(int, dog_data['id'].isin(table_dog.selection))) #error here, need to be fixed "TypeError: only list-like objects are allowed to be passed to isin(), you passed a `str`"

    if not table_dog.selection:
        ui.notify('No selection to delete', type='warning')
        return
    dog_data = dog_data[~dog_data['id'].isin(selection_list)]
    dog_data.to_csv('dog_data.csv', index=False)
    table_dog.update_from_pandas(dog_data)
    ui.notify(f'Deleted {len(selection_list)} row(s)', type='positive')


with ui.row():
    weight = ui.number(label="Weight", value=0, precision=2)
    optiondogs = ['Chihuahua', 'Shih Tzu', 'Border Collie', 'Boxer', 'Cocker Spaniel', 
                  'Great Dane', 'Maltese', 'Pomeranian', 'Yorkshire Terrier', 'Saint Bernard', 
                  'Australian Shepherd', 'Basset Hound', 'Bernese Mountain Dog', 
                  'Cavalier King Charles Spaniel', 'Chow Chow', 'Dalmatian', 'French Bulldog', 
                  'Jack Russell Terrier', 'Pit Bull', 'Labrador Retriever', 'German Shepherd', 
                  'Golden Retriever', 'Bulldog', 'Poodle', 'Beagle', 'Rottweiler', 'Dachshund', 
                  'Siberian Husky', 'Doberman Pinscher', 'Samoyed']
    breed = ui.input(label='Breed', placeholder='Enter Breed', autocomplete=optiondogs)
    button_calculate = ui.button('Calculate')
    button_calculate.on_click(update)
    button_delete = ui.button('Delete')
    button_delete.on_click(delete_selected)

with ui.row():
    try:
        File_dog = pd.read_csv('dog_data.csv')
        table_dog = ui.table.from_pandas(File_dog, pagination=5)
        table_dog.set_selection('multiple')
    except FileNotFoundError:
        File_dog = pd.DataFrame(data={'Breed': [], 'Weight': [], 'Cost': []})
        File_dog['id'] = pd.Series([], dtype=int)
        File_dog.to_csv('dog_data.csv', mode='a', header=True, index=False)
        table_dog = ui.table.from_pandas(File_dog, pagination=5)
        table_dog.set_selection('single')
    File_donors = pd.read_csv('FinalProject_T2/donors.csv')
    table_donors = ui.table.from_pandas(File_donors, pagination=5)

ui.run()
