from config.routers import MongoClusterConnector
from api.views import ReadonlyResponse


class ReadonlyMiddleware(object):
    """ Middleware for checking primary aliveness """

    def __init__(self, get_response):
        self.get_response = get_response
        self.connector = MongoClusterConnector()

    def __call__(self, request):
        if request.method == 'POST':
            primary = self.connector.get_primary()

            if primary is None:
                return ReadonlyResponse.as_view()(request).render()

        return self.get_response(request)
