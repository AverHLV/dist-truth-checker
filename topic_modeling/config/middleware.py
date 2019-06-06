from django.shortcuts import redirect
from django.urls import reverse
from config.routers import MongoClusterConnector


class ReadonlyMiddleware(object):
    """ Middleware for checking primary aliveness """

    def __init__(self, get_response):
        self.get_response = get_response
        self.connector = MongoClusterConnector()

    def __call__(self, request):
        if request.method == 'POST':
            primary = self.connector.get_primary()

            if primary is None:
                return redirect(reverse('readonly'))

        return self.get_response(request)
