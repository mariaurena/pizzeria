import os
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['COMPLETED_ORDER_TABLE']
table = dynamodb.Table(table_name)

'''
 order : {
  orderId: String,
  name: String,
  address: String,
  pizzas: Array of Strings,
  delivery_status: READY_FOR_DELIVERY / DELIVERED
  timestamp: timestamp
}
'''

def save_completed_order(order):
    print('Guardar un pedido fue llamado')
    
    order['delivery_status'] = 'READY_FOR_DELIVERY'
    
    response = table.put_item(
        Item=order
    )
    
    return response

def deliver_order(order_id):
    print('Enviar una orden fue llamado')
    print('orderId:', order_id)

    try:
        response = table.update_item(
            Key={'orderId': order_id},
            ConditionExpression='attribute_exists(orderId)',
            UpdateExpression='set delivery_status = :v',
            ExpressionAttributeValues={':v': 'DELIVERED'},
            ReturnValues='ALL_NEW'
        )
        print('order delivered')
        return response.get('Attributes')
    except Exception as error:
        print('Error al entregar el pedido:', error)
        raise error