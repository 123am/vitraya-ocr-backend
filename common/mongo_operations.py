from base import *


mongo_client=MongoClient('mongodb+srv://%s:%s@cluster0.3odaop8.mongodb.net' % ("amitgadia29", "amitgadia29"))

db_mongo_client=mongo_client["vitraya_ocr"]

def insertion(coll_name,data):
    coll_mongo_client=db_mongo_client[coll_name]
    coll_mongo_client.insert_one(data)
    return {
        "status":200,
        "msg":"",
        "data":[]
    }


def finding_aggregate(coll_name,data):
    coll_mongo_client=db_mongo_client[coll_name]
    resp_data=coll_mongo_client.aggregate(data)
    return {
        "status":200,
        "msg":"",
        "data":list(resp_data)
    }
    
def real_deleting(coll_name,data):
    coll_mongo_client=db_mongo_client[coll_name]
    resp_data=coll_mongo_client.delete_one(data)
    return {
        "status":200,
        "msg":"",
        "data":[]
    }

def real_deleting_many(coll_name,data):
    coll_mongo_client=db_mongo_client[coll_name]
    resp_data=coll_mongo_client.delete_many(data)
    return {
        "status":200,
        "msg":"",
        "data":[]
    }
