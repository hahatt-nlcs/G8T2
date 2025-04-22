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

def delete_row():
    df = pd.read_csv('dog_data.csv') 
    df = df[df['s'] != 22]
    df.to_csv('dog_data.csv', index=False)

def update():
    weight_value = weight.value or 0
    cost_dogs = calculate_cost(weight_value)
    breed_value = breed.value or "Not Specified"  
    new_data_dog = pd.DataFrame({'Breed': [breed_value], 'Weight': [weight_value], 'Cost': [cost_dogs]})
    new_data_dog.to_csv('dog_data.csv', mode='a', header=False, index=False)
    updated_file_dog = pd.read_csv('dog_data.csv')
    # sum_cost = updated_file_dog['Cost'].sum()
    # result_sum.set_text(f'Cost: {sum_cost}') 
    table_dog.update_from_pandas(updated_file_dog)
    




with ui.row():
    weight = ui.number(label="Weight", value=0, precision=2)
    # rent_fee = ui.number(label="Rent", value=0, precision=2)
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
    result_sum = ui.label('Sum_Cost: 0')


with ui.row():
    try:
        File_dog = pd.read_csv('dog_data.csv')
        table_dog = ui.table.from_pandas(File_dog, pagination=5)
        table_dog.set_selection('single')
    except FileNotFoundError:
        File_dog = pd.DataFrame(columns=['Breed', 'Weight', 'Cost'])
        table_dog = ui.table.from_pandas(File_dog, pagination=5)   
    File_donors = pd.read_csv('FinalProject_T2/donors.csv')
    table_donors = ui.table.from_pandas(File_donors, pagination=5)


ui.run()
