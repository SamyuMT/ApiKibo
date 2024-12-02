from pymongo import MongoClient
from bson.binary import UuidRepresentation

class ConnectionMongo:

    def __init__(self):
        # Nombre de la base de datos
        db = "dbkibo"

        # Conectar a MongoDB
        connection = MongoClient("mongodb://localhost:27017/",
                                 UuidRepresentation="standard")
        self.con = connection[db]
        
        # Verificar la conexión listando las bases de datos
        try:
            databases = connection.list_database_names()
            print(f"Conectado a MongoDB. Bases de datos disponibles: {databases}")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {str(e)}")

