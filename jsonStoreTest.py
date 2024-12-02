from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.app import App
import os

# Determine the storage path
if platform == 'android' or platform == 'ios':
    store_path = App.get_running_app().user_data_dir
else:
    store_path = '.'

# Create or open a JsonStore in the appropriate directory
store = JsonStore(os.path.join(store_path, 'data.json'))

# Save data
#store.put('user1', name='Alice', age=25)

# Retrieve and print data
user1 = store.get('user1')
print(f"Name: {user1['name']}, Age: {user1['age']}")
