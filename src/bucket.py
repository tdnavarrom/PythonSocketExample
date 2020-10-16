import os

class Bucket:

    def __init__(self, id):
        self.dir_path = os.path.join(os.getcwd(),'buckets/'+str(id))
        self.id = id
        self.objects = []

    def create_object():
        pass

    def list_objects():
        pass

    def delete_object():
        pass