from pymongo import MongoClient
from bson.json_util import dumps
import json
import os
import sys
import redis

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, 'common')
sys.path.append(mymodule_dir)

from utils import get_product_from_external_service
from shared import (
    NotFoundException,
    generate_ttl,
    get_cart_id,
    get_headers,
)

product_service_url = os.environ["PRODUCT_SERVICE_URL"]
mongodb_service_url = os.environ["MONGODB_SERVICE_URL"]

mongo_client = MongoClient(host=mongodb_service_url,
        port=27017,
        username='csit6000o',
        password='csit6000o')

mydb = mongo_client['cart']
mycol = mydb['items']

Pool = redis.ConnectionPool(host='127.0.0.1', port=6379,db=2, max_connections=10)
conn = redis.Redis(connection_pool=Pool)

def handle(event, context):
    """handle a request to the function
    Args:
        req (str): request body
    """
    cart_id, _ = get_cart_id(event.headers)

    pk = f"cart#{cart_id}"

    key = {
        "pk": pk,
    }


    products = dumps(list(mycol.find(key)))
    mycol.delete_many(key)
    conn.set(json.loads(products))
    return {
        "statusCode": 200,
        "headers": get_headers(cart_id),
        "body": {"products": json.loads(products)},
    }

