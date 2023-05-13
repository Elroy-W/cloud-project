import json
import os
import redis   

dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir, 'common/product_list.json'), 'r') as product_list:
    product_list = json.load(product_list)

Pool = redis.ConnectionPool(host='127.0.0.1', port=6379,db=0, max_connections=10)
conn = redis.Redis(connection_pool=Pool)
i=0
for value in product_list.items():
   conn.set(i+1,json.dumps(value))

for key in conn.keys():
    data = json.loads(conn.get(key))

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}

def handle(event, context):
    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": {"products": product_list},
    }

