from nicegui import ui
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def calculate_cost(b):
    if  b == 0:
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
    result.set_text(f'Cost: {cost_dogs}\nBreed: {breed.value or "Not Specified"}') 
    dogs = open("cost_of_dogs.txt", "a")
    dogs.write(str(cost_dogs)+",")
    dogs.close()
    # dogs = open("cost_of_dogs.txt", "r")
    # print(dogs.read())

dark = ui.dark_mode()
with ui.row():
    weight = ui.number(label="Weight", value=0, precision=2)
    rent_fee = ui.number(label="Rent", value=0, precision=2)
    optiondogs = ['Chihuahua', 'Shih Tzu', 'Border Collie', 'Boxer', 'Cocker Spaniel', 
                  'Great Dane', 'Maltese', 'Pomeranian', 'Yorkshire Terrier', 'Saint Bernard', 
                  'Australian Shepherd', 'Basset Hound', 'Bernese Mountain Dog', 
                  'Cavalier King Charles Spaniel', 'Chow Chow', 'Dalmatian', 'French Bulldog', 
                  'Jack Russell Terrier', 'Pit Bull', 'Labrador Retriever', 'German Shepherd', 
                  'Golden Retriever', 'Bulldog', 'Poodle', 'Beagle', 'Rottweiler', 'Dachshund', 
                  'Siberian Husky', 'Doberman Pinscher', 'Samoyed']
    breed = ui.input(label='Breed', placeholder='Enter Breed', autocomplete=optiondogs)
    button_calculate = ui.button('Calculate')
    result = ui.label('Cost: 0')
    ui.switch('Dark mode').bind_value(dark)

with ui.row():
    File = pd.read_csv('FinalProject_T2/donors.csv')
    table = ui.table.from_pandas(File, pagination=5)





button_calculate.on_click(update)

ui.run()
