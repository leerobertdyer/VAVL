import tempfile
import os
from app import supabase
import requests

def save_temp_image(image_data, extension='jpg'):
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{extension}') as temp_file:
        temp_file.write(image_data)
        return temp_file.name

def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        print('image downloaded successfully')
        return response.content
    else:
        return None
    
def upload_to_supabase(temp_file_path, upload_path):
    try:
        with open(temp_file_path, 'rb') as file:
            response = supabase.storage.from_('eventImages').upload(upload_path, file)
        os.remove(temp_file_path) 
        print('SAVED to supa!')
        return response
    except Exception as e:
        print('Error uploading to Supabase:', e)
        return None
    
def get_supabase_image_url(file_path):
    print('getting supabase image url')
    url = supabase.storage.from_('eventImages').get_public_url(file_path)
    print('url: ', url)
    return url

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

