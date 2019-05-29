import logging
import asyncio
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientConnectorError
from config import constants
from texts_admin.models import TextsAdmin

logger = logging.getLogger(constants.logger_name)


class ARClient(object):
    """ HTTP client for sending asynchronous requests """

    url_get = '{ip}/api/result/{message_id}/'
    url_post = '{ip}/api/check/'

    def __init__(self, timeout=constants.timeout, services=constants.services):
        """
        ARClient initialization

        :param timeout: total request timeout in seconds
        :param services: dict like {service: ip}
        """

        self.responses = None
        self.session = None
        self.timeout = timeout
        self.services = services

        superuser = TextsAdmin.objects.filter(is_superuser=True).first()
        self.headers = {'X-Token': superuser.token}

    async def request_get(self, service, message_id):
        """ Get check results by get request """

        try:
            async with self.session.get(self.url_get.format(ip=self.services[service], message_id=message_id)) \
                    as response:
                return await response.json(), response.status

        except ClientConnectorError:
            logger.critical('Connection error while get request to service: {0}, id: {1}.'.format(service, message_id))
            return {'detail': 'Service unavailable.'}, 503

    async def request_post(self, service, data):
        """ Start text check by post request """

        try:
            async with self.session.post(self.url_post.format(ip=self.services[service]), json=data) as response:
                return await response.json(), response.status

        except ClientConnectorError:
            logger.critical('Connection error while post request to service: {0}, data: {1}.'.format(service, data))
            return {'detail': 'Service unavailable.'}, 503

    async def send_requests(self, parameter, gather_results):
        """
        Send asynchronous requests to all specified services and populate responses dictionary

        :param parameter: message_id (str) if gather_results=True, else data dictionary
        :param gather_results: bool,
            True - send get requests for getting a previous checking results
            False - send post requests for starting a text check
        """

        self.responses = {}
        self.session = ClientSession(headers=self.headers, timeout=ClientTimeout(total=self.timeout))

        try:
            if gather_results:
                assert isinstance(parameter, str), '"parameter" should be a string in gather_results=True case.'

                self.responses = {
                    service: await self.request_get(service, parameter)
                    for service in self.services
                }

            else:
                assert isinstance(parameter, dict), '"parameter" should be a dictionary in gather_results=False case.'

                self.responses = {
                    service: await self.request_post(service, parameter[service])
                    for service in self.services
                }

        finally:
            await self.session.close()

    def run_loop(self, parameter, gather_results=True):
        """
        Run iolopp and wait until all requests will be done

        :return: dict, service responses in format: {service: ({json data}, status code)}
        """

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_requests(parameter, gather_results))
        loop.close()
        return self.responses
