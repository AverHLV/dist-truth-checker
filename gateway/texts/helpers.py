def form_services_data(responses, necessary_code):
    """
    Create services_data dictionary for displaying check results in Text detail view

    :param responses: dict, responses from tests.arclient.ARClient.run_loop()
    :param necessary_code: int, HTTP response code
    :return: dict like {service: check_result or error message}
    """

    services_data = {}

    for key in responses:
        if responses[key][1] != necessary_code:
            services_data[key] = parse_errors(responses[key][0])

        else:
            services_data[key] = responses[key][0]['check_result']

    return services_data


def parse_errors(errors):
    """ Parse response errors and return detailed errors string """

    try:
        return errors['detail']

    except KeyError:
        error_string = ''

        for key in errors:
            error_string += '{0}\n'.format(errors[key][0])

        return error_string


def get_status_repr(results):
    """
    Get string representation of Text checking status

    :param results: list of services check results (bool)
    :return: str
    """

    status = get_check_status(results)

    if status == 2:
        return 'It`s definitely truth.'

    if status == 1:
        return 'Probably it`s truth.'

    if status == -1:
        return 'No data for making decision.'

    return 'Most likely it is fake.'


def get_check_status(results):
    if isinstance(results[0], str) or isinstance(results[1], str):
        return -1

    if results[0] and results[1]:
        return 2

    if results[0] or results[1]:
        return 1

    return 0
