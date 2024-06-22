import requests
import random
import string
import uuid
import names
import base64
import os

# Replace with your API endpoint URL
API_ENDPOINT = 'https://g53car1hxj.execute-api.us-east-2.amazonaws.com/v1/usuarios'

# Function to generate random data with UUID and integer Edad
def generate_random_data():
    # Generate random UUID
    random_uuid = str(uuid.uuid4())
    
    # Generate random Nombre (name) using the names library
    random_nombre = names.get_full_name()
    
    # Generate random Correo (email)
    random_correo = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10))) + '@example.com'
    
    # Generate random Edad (age) as integer
    random_edad = random.randint(18, 80)
    
    return {
        'nombre': random_nombre,
        'correo': random_correo,
        'edad': random_edad
    }

# Function to encode an image to base64
def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

# Function to make POST request to API endpoint
def post_data_to_api(data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        print(f"Data posted successfully: {data}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting data: {e}")
        if response:
            print(response.content)  # Print response content for debugging

# Generate random data
random_data = generate_random_data()

# Encode image to base64
image_path = os.path.join(os.path.dirname(__file__), 'xmat.png')  # Use the image located in the same directory
encoded_image = encode_image_to_base64(image_path)

# Add the base64 encoded image to the data
random_data['imagen'] = encoded_image

# Post the data with the image
post_data_to_api(random_data)
