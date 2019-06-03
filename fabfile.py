from fabric import Connection
from os import environ


def deploy(host, user, password, image):
    """ Deploy Django app from docker container on specified host """

    connection = Connection(host=host, port=22, user=user, connect_kwargs={'password': password})
    connection.run('docker pull {0}'.format(image))
    connection.run('docker stop $(docker ps -a -q)')

    connection.run(
        '''
            docker run -p 8000:8000 {0} /bin/bash -c "
            git pull --depth=1 origin dev;
            python manage.py collectstatic --settings=config.settings.production;
            uwsgi uwsgi.ini" &
        '''.format(image))

    connection.close()


if __name__ == '__main__':
    host_user = environ['USER']
    passw = environ['PASSWORD']

    params = {
        'aggregator0': {'host': environ['AGG0'], 'user': host_user, 'password': passw, 'image': 'averhlv/aggregator'},
        'aggregator1': {'host': environ['AGG1'], 'user': host_user, 'password': passw, 'image': 'averhlv/aggregator'},
        'seo': {'host': environ['SEO'], 'user': host_user, 'password': passw, 'image': 'averhlv/seo'},
        'topic': {'host': environ['TOPIC'], 'user': host_user, 'password': passw, 'image': 'averhlv/topic'}
    }

    for service in params:
        print('\n{0} deploy started\n'.format(service))
        deploy(**params[service])
        print('\n{0} deployed\n'.format(service))
