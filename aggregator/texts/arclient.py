import logging
import asyncio
import aiohttp
from aiohttp import client_exceptions
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

        self.session = None
        self.responses = {}
        self.timeout = timeout
        self.services = services

        # send requests tracing

        self.trace_config = aiohttp.TraceConfig()
        self.trace_config.on_request_end.append(self.on_request_end)

        # request custom headers

        superuser = TextsAdmin.objects.filter(is_superuser=True).first()
        self.headers = {'X-Token': superuser.token}

    @staticmethod
    async def on_request_end(_session, _trace_config_ctx, params):
        """ Invoke when a request ended """

        logger.info('{0} {1} {2}'.format(params.method, params.url, params.response.status))

    async def request_get(self, service, message_id):
        """ Get check results by get request """

        async with self.session.get(self.url_get.format(ip=self.services[service], message_id=message_id)) as response:
            return await response.json(), response.status

    async def request_post(self, service, data):
        """ Start text check by post request """

        async with self.session.post(self.url_post.format(ip=self.services[service]), json=data) as response:
            return await response.json(), response.status

    async def send_requests(self, parameter, gather_results):
        """
        Send asynchronous requests to all specified services and populate responses dictionary

        :param parameter: message_id (str) if gather_results=True, else data dictionary
        :param gather_results: bool,
            True - send get requests for getting a previous checking results
            False - send post requests for starting a text check
        """

        if gather_results:
            assert isinstance(parameter, str), '"parameter" should be a string in gather_results=True case.'

        else:
            assert isinstance(parameter, dict), '"parameter" should be a dictionary in gather_results=False case.'

        self.session = aiohttp.ClientSession(
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            trace_configs=[self.trace_config]
        )

        try:
            for service in self.services:
                request_type = 'None'

                try:
                    if gather_results:
                        request_type = 'GET'
                        self.responses[service] = await self.request_get(service, parameter)

                    else:
                        request_type = 'POST'
                        self.responses[service] = await self.request_post(service, parameter[service])

                except asyncio.TimeoutError:
                    logger.critical('Timeout error while request to service: {0}, {1}'.format(service, request_type))

                    self.responses[service] = (
                        {'detail': 'Request timeout occured. Please re-submit your request later.'}, 408
                    )

                except client_exceptions.ClientConnectorError:
                    logger.critical('Connection error while request to service: {0}, {1}'.format(service, request_type))
                    self.responses[service] = {'detail': 'Service unavailable.'}, 503

                except client_exceptions.ClientOSError:
                    logger.critical('Connection reset while request to service: {0}, {1}'.format(service, request_type))
                    self.responses[service] = {'detail': 'Connection reset by peer. Try again.'}, 520

                except client_exceptions.ServerDisconnectedError:
                    logger.critical('Server refused the request to service: {0}, {1}'.format(service, request_type))
                    self.responses[service] = {'detail': 'Service refused the request.'}, 444

                except client_exceptions.ContentTypeError:
                    logger.critical('Server response has unexpected mime type: {0}, {1}'.format(service, request_type))
                    self.responses[service] = {'detail': 'Service returned unexpected data format. Try later.'}, 415

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
