import tempfile
import os
from app import supabase
import requests

def save_temp_image(image_data, extension='jpg'):
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as temp_file:
        temp_file.write(image_data)
        return temp_file.name

def download_image(image_url):
    if image_url.startswith('/RecordBin'):
        return None 
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    else:
        return None
    
def upload_to_supabase(temp_file_path, upload_path):
    try:
        with open(temp_file_path, 'rb') as file:
            response = supabase.storage.from_('eventImages').upload(upload_path, file)
        os.remove(temp_file_path) 
        return response
    except Exception as e:
        print('Error uploading to Supabase:', e)
        return None
    
def get_supabase_image_url(file_path):
    url = supabase.storage.from_('eventImages').get_public_url(file_path)
    return url