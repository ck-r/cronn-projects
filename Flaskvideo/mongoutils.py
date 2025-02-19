import pymongo


def get_client_and_db():
    client = pymongo.MongoClient()
    db = client.video_site
    return client, db