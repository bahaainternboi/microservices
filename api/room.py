import uuid
from flask_injector import inject
from elasticsearchsetup.elasticsearch import elasticSearchIndex

class Room(object):
    @inject
    def post(self, indexer: elasticSearchIndex, room: dict) -> dict:
        if indexer.existsbyurl(room['url']):
            return room, 409
        room['id']= str(uuid.uuid4())

        if not indexer.index(room):
            return {"error": "Room not saved"}, 400

        return room, 201

class_instance = Room()

