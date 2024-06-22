import base64
import string
import json
import uuid
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
dynamodb_table = dynamodb.Table('usuarios')
s3 = boto3.client("s3")

usuarios_path = '/usuarios'

def lambda_handler(event, context):
    print('Request event: ', event)
    response = None
   
    try:
        http_method = event.get('httpMethod')
        path = event.get('path')

        if http_method == 'GET' and path == usuarios_path:
            response = mostrar_usuarios()
        elif http_method == 'POST' and path == usuarios_path:
            response = guardar_usuarios(json.loads(event['body']))
        else:
            response = build_response(404, '404 Not Found')

    except Exception as e:
        print('Error:', e)
        response = build_response(400, 'Error processing request')
   
    return response


# Mostrar los usuarios
def mostrar_usuarios():
    try:
        scan_params = {
            'TableName': dynamodb_table.name
        }
        return build_response(200, scan_dynamo_records(scan_params, []))
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])

def scan_dynamo_records(scan_params, item_array):
    response = dynamodb_table.scan(**scan_params)
    item_array.extend(response.get('Items', []))
   
    if 'LastEvaluatedKey' in response:
        scan_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        return scan_dynamo_records(scan_params, item_array)
    else:
        return {'id': item_array}

# Guardar los datos de usuario
def guardar_usuarios(request_body):
    try:
        # Decodificar la imagen (Base64)
        imagen_decodificada = base64.b64decode(request_body.get('imagen'))
        
        # Renombrar la imagen con un nombre aleatorio
        nombre_imagen = ''.join(str(uuid.uuid4()))
        
        # Guardar la ruta y subir la imagen al bucket
        nombre_bucket = 'lotus-storage'
        region_s3 = '.s3.us-east-2.'
        url_imagen = 'https://' + nombre_bucket + region_s3 + 'amazonaws.com' + '/' + nombre_imagen + '.png'
        
        s3.put_object(Bucket=nombre_bucket, Key='imagenes/'+nombre_imagen+'.png', Body=imagen_decodificada)
        
        
        # Filtrar solo los campos requeridos
        usuario = {
            'id': request_body.get('id'),
            'nombre': request_body.get('nombre'),
            'correo': request_body.get('correo'),
            'edad': int(request_body.get('edad', 0)),  # Convertir a entero
            'imagen': url_imagen 
        }
        dynamodb_table.put_item(Item=usuario)
        
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': usuario
        }
        
        return build_response(200, body)
    
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Check if it's an int or a float
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        # Let the base class default method raise the TypeError
        return super(DecimalEncoder, self).default(obj)

def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }