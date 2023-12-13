import json
import uuid
import boto3
import os
import time
from orderMetadataManager import save_completed_order  
from orderMetadataManager import deliver_order 

sqs = boto3.client('sqs', region_name=os.environ['REGION'])
QUEUE_URL = os.environ['PENDING_ORDER_QUEUE']

def hacer_pedido(event, context):

    print('HacerPedido fue llamada')

    body = json.loads(event['body'])

    order = {
        'orderId': str(uuid.uuid1()),
        'name': body['name'],
        'address': body['address'],
        'pizzas': body['pizzas'],
        'timestamp': int(time.time() * 1000)  
    }

    params = {
        'MessageBody': json.dumps(order),
        'QueueUrl': QUEUE_URL
    }

    try:
        data = sqs.send_message(**params)
        message = {
            'orderId': order,
            'messageId': data['MessageId']
        }
        return send_response(200, message)
    except Exception as err:
        return send_response(500, str(err))

def preparar_pedido(event, context):
    print('Preparar pedido fue llamada')

    order = json.loads(event['Records'][0]['body'])

    try:
        save_completed_order(order)
        return send_response(200, {'message': 'Pedido preparado exitosamente'})
    except Exception as err:
        return send_response(500, str(err))

def enviar_pedido(event, context):

    print('enviarPedido fue llamado')

    record = event['Records'][0]

    if record['eventName'] == 'INSERT':
        print('deliverOrder')

        orderId = record['dynamodb']['Keys']['orderId']['S']

        try:
            data = deliver_order(orderId)
            print(data)
        except Exception as error:
            print(error)
            raise error
    else:
        print('is not a new record')

def send_response(status_code, message):
    response = {
        'statusCode': status_code,
        'body': json.dumps(message)
    }
    return response
