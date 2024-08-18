from pymongo.mongo_client import MongoClient

connect_string = f"mongodb+srv://tommypang04:e45Id0SpuuOQdqEK@medscan-mentor.ghuae.mongodb.net/?retryWrites=true&w=majority&appName=MedScan-Mentor"
client = MongoClient(connect_string)
db = client['MedScan-Mentor']

def insert_into_collection(collection_name, data):
    try:
        create_collection_if_not_exists(collection_name)
        db[collection_name].insert_one(data.to_dict())
    except Exception as e:
        print(e)

def delete_from_collection_if_exists(collection_name, query):
    create_collection_if_not_exists(collection_name)
    db[collection_name].delete_one(query)

def update_collection(collection_name, new_data):
    try:
        create_collection_if_not_exists(collection_name)
        db[collection_name].update_one({"username": new_data.username}, new_data.__dict__)
    except Exception as e:
        print(e)

def find_from_collection(collection_name, query):
    try:
        create_collection_if_not_exists(collection_name)
        document = db[collection_name].find_one(query)
        if (document is None):
            return None
        document['_id'] = str(document['_id'])
        return document
    except Exception as e:
        print(e)
        return None

def create_collection_if_not_exists(collection_name):
    try:
        collection_names = db.list_collection_names()
        if collection_name not in collection_names:
            db.create_collection(collection_name)
            print(f"Created the '{collection_name}' collection.")
    except Exception as e:
        print(f"Error creating collection: {e}")

