from typing import Optional
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app, ui
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

passwords = {'user1': 'pass1', 'user2': 'pass2'}

unrestricted_page_routes = {'/login'}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                return RedirectResponse(f'/login?redirect_to={request.url.path}')
        return await call_next(request)


app.add_middleware(AuthMiddleware)



@ui.page('/login')
def login(redirect_to: str = '/login') -> Optional[RedirectResponse]:
    def try_login() -> None:
        if passwords.get(username.value) == password.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.navigate.to('/')  
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)
    return None

@ui.page('/')
def main():
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
        selected_ids = lambda x: x.selected_ids
        print(f'Selected IDs: {selected_ids}')
        if isinstance(selected_ids, str):
            selected_ids = [selected_ids]
        if not selected_ids:
            ui.notify('No selection to delete', type='warning')
            return
        dog_data = pd.read_csv('dog_data.csv')
        dog_data = dog_data[~dog_data['id'].isin(selected_ids)]
        dog_data.to_csv('dog_data.csv', index=False)
        table_dog.update_from_pandas(dog_data)
        ui.notify(f'Deleted {len(selected_ids)} row(s)', type='positive')
    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')
    with ui.row().classes('absolute right-20'):
        ui.label(f'Welcome {app.storage.user["username"]} !').classes('text-2xl')
        ui.button(on_click=logout, icon='logout').props('outline round')
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
            table_dog = ui.table.from_pandas(File_dog, pagination=5,on_select=lambda x: ui.notify(f'selected: {x.selection}'))
            table_dog.set_selection('single')
        except FileNotFoundError:
            File_dog = pd.DataFrame(data={'Breed': [], 'Weight': [], 'Cost': []})
            File_dog['id'] = pd.Series([], dtype=int)
            File_dog.to_csv('dog_data.csv', mode='a', header=True, index=False)
            table_dog = ui.table.from_pandas(File_dog, pagination=5)
            table_dog.set_selection('single')
        File_donors = pd.read_csv('FinalProject_T2/donors.csv')
        table_donors = ui.table.from_pandas(File_donors, pagination=5)



ui.run(storage_secret='skcp8J9Ccrkw4YWbVNWR9w==')
