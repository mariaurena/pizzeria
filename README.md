# Desarrollo de una aplicación sin servidor

Siguiendo el tutorial de Marcia Villalba disponible en: https://www.udemy.com/course/serverless-en-espanol/

Usando Serveless Framework y Python como lenguaje he desarrollado un sistema para pedir pizzas con las siguientes funcionalidades:

1. Un cliente realiza un nuevo pedido.
  - Usa la lambda 'hacer_pedido' que inserta el pedido en la cola 'PENDING_ORDER_QUEUE' dónde los pedidos son procesados uno a uno.

2. El pedido se procesa.
  - Usa la lambda 'preparar_pedido' que guarda en la base de datos 'COMPLETED_ORDER_TABLE' el pedido con el estado 'READY_FOR_DELIVERY'.

3. El pedido es entregado.
  - Usa la lambda 'enviar_pedido' que cambia el estado del pedido en 'COMPLETED_ORDER_TABLE' a 'DELIVERED' usando DynamoDB streams para ello.
    
![diagrama_general](https://github.com/mariaurena/pizzeria/assets/58937944/141219ea-4606-4552-bb46-a180866eab94)

