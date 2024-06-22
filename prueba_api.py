import requests
import random
import string
import uuid
import names

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
        'id': random_uuid,
        'nombre': random_nombre,
        'correo': random_correo,
        'edad': random_edad
    }

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

# Number of random data entries to generate and post
NUM_ENTRIES = 10

# Generate and post random data entries
for _ in range(NUM_ENTRIES):
    random_data = generate_random_data()
    post_data_to_api(random_data)
