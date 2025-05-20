from typing import Optional
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app, ui
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

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

    def plot_to_base64(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return img_base64

    def load_maintenance_costs():
        try:
            with open('maintenance.txt', 'r') as f:
                line = f.read().strip()
                parts = [float(x) for x in line.split(',')]
                return parts if len(parts) == 3 else [0.0, 0.0, 0.0]
        except:
            return [0.0, 0.0, 0.0]

    def save_maintenance_costs(food, medical, toys):
        with open('maintenance.txt', 'w') as f:
            f.write(f'{food},{medical},{toys}')

    def refresh_dashboard():
        food = food_cost.value or 0
        medical = medical_cost.value or 0
        toys = toys_cost.value or 0
        save_maintenance_costs(food, medical, toys)

        dog_df = pd.read_csv('dog_data.csv')
        dog_df['Cost'] = dog_df['Weight'].apply(calculate_cost)
        total_dog_cost = dog_df['Cost'].sum() * 4
        donor_df = pd.read_csv('donors.csv')
        total_donation = donor_df['donation'].sum()
        total_cost = total_dog_cost + food + medical + toys
        status.clear()
        chart_container.clear()
        with status:
            ui.label(f'Total 4-week Cost: ${total_cost:.2f}')
            ui.label(f'Total Donations: ${total_donation:.2f}')
            ui.label('Donations are enough!' if total_donation >= total_cost else 'Donations are not enough!')\
                .classes('text-lg text-positive' if total_donation >= total_cost else 'text-lg text-negative')
        with chart_container:   
            labels = ['Donations', 'Dog Maintenance', 'Food', 'Medical', 'Toys']
            values = [total_donation, total_dog_cost, food, medical, toys]
            colors = ['green', 'orange', 'gold', 'red', 'purple']
            fig1, ax1 = plt.subplots()
            ax1.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
            ax1.set_title('Donations vs Costs')
            ui.image(f'data:image/png;base64,{plot_to_base64(fig1)}').classes('w-96 h-auto')

            if not donor_df.empty:
                fig2, ax2 = plt.subplots()
                ax2.hist(donor_df['donation'], bins=10, color='blue', edgecolor='black')
                ax2.set_title('Donation Distribution')
                ui.image(f'data:image/png;base64,{plot_to_base64(fig2)}').classes('w-80 h-auto')

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

    def delete():
        selected_rows = table_dog.selected
        if not selected_rows:
            ui.notify('No selection to delete', type='warning')
            return
        selected_ids = [x['id'] for x in selected_rows]
        dog_data = pd.read_csv('dog_data.csv')
        dog_data = dog_data[~dog_data['id'].isin(selected_ids)]
        dog_data.to_csv('dog_data.csv', index=False)
        table_dog.update_from_pandas(dog_data)
        ui.notify(f'Deleted {len(selected_ids)} row(s)', type='positive')

    def logout():
        app.storage.user.clear()
        ui.navigate.to('/login')

    food_default, medical_default, toys_default = load_maintenance_costs()

    with ui.row():
        ui.label("Dashboard").classes('text-2xl')
        food_cost = ui.number(label='Food Cost', value=food_default, format='%.2f')
        medical_cost = ui.number(label='Medical Cost', value=medical_default, format='%.2f')
        toys_cost = ui.number(label='Toys Cost', value=toys_default, format='%.2f')
        ui.button('Refresh Dashboard', on_click=refresh_dashboard)

    status = ui.row()
    chart_container = ui.row()

    refresh_dashboard()

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
        ui.button('Append', on_click=update)
        ui.button('Delete', on_click=delete)

    with ui.row():
        try:
            File_dog = pd.read_csv('dog_data.csv')
            table_dog = ui.table.from_pandas(File_dog, pagination=5,on_select=lambda x: ui.notify(f'selected: {x.selection}'),title="Dogs")
            table_dog.set_selection('single')
        except FileNotFoundError:
            File_dog = pd.DataFrame(data={'Breed': [], 'Weight': [], 'Cost': []})
            File_dog['id'] = pd.Series([], dtype=int)
            File_dog.to_csv('dog_data.csv', mode='a', header=True, index=False)
            table_dog = ui.table.from_pandas(File_dog, pagination=5)
            table_dog.set_selection('single')

        File_donors = pd.read_csv('donors.csv')
        table_donors = ui.table.from_pandas(File_donors, pagination=5,title='Doners')


ui.run(storage_secret='skcp8J9Ccrkw4YWbVNWR9w==')
