from pymongo import MongoClient
from random import randint
from time import sleep
from config.settings import production


class MongoClusterConnector(object):
    """ MongoDB replica set connector """

    def __init__(self, databases=production.DATABASES, discover_timeout=0.5):
        """
        MongoClusterConnector initialization

        :param databases: django settings databases dictionary
        :param discover_timeout: timeout for discovering whole cluster by MongoClient
        """

        self.databases = [(db, databases[db]['HOST'], str(databases[db]['PORT'])) for db in databases]
        self.client = MongoClient([db[1] + ':' + db[2] for db in self.databases], replicaset='rs0')
        sleep(discover_timeout)

    def __del__(self):
        """ Destructor: close MongoClient before destruction """

        self.client.close()

    def find_alias(self, ip):
        """ Find database alias for given IP """

        for db in self.databases:
            if ip == db[1]:
                return db[0]

    def get_primary(self, return_alias=True):
        """ Find alive primary node """

        try:
            if not return_alias:
                return self.client.primary[0]

            return self.find_alias(self.client.primary[0])

        except TypeError:
            return

    def get_secondary(self):
        """ Find alive secondary node """

        primary = self.get_primary(return_alias=False)
        nodes = [node[0] for node in list(self.client.nodes)]

        if primary is None:
            return self.find_alias(nodes[randint(0, len(nodes) - 1)])

        nodes.remove(primary)
        return self.find_alias(nodes[randint(0, len(nodes) - 1)])


class MongoRouter(object):
    """ MongoDB replica set router """

    def __init__(self):
        self.connector = MongoClusterConnector()

    def db_for_read(self, _model, **_hints):
        return self.connector.get_secondary()

    def db_for_write(self, _model, **_hints):
        return self.connector.get_primary()

    def allow_migrate(self, db, _app_label, _model_name=None, **_hints):
        return db == self.connector.get_primary()
