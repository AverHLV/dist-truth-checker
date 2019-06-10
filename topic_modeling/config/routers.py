from config.connector import cluster_connector


class MongoRouter(object):
    """ MongoDB replica set router """

    @staticmethod
    def db_for_read(_model, **_hints):
        return cluster_connector.get_secondary()

    @staticmethod
    def db_for_write(_model, **_hints):
        return cluster_connector.get_primary() if cluster_connector.is_writable() else None

    @staticmethod
    def allow_migrate(db, _app_label, _model_name=None, **_hints):
        return db == cluster_connector.get_primary() if cluster_connector.is_writable() else False
