import os
import tarfile
from fabric import Connection
from base64 import b64decode


def tar_dir(path, tar_name):
    """ Compress given folder to .tar.gz """

    with tarfile.open(tar_name, 'w:gz') as tar_handle:
        for root, dirs, files in os.walk(path):
            for file in files:
                if '.csv' not in file:
                    tar_handle.add(os.path.join(root, file))


def save_secret(name, secret):
    """ Save service secret decoded from environment variable """

    with open(name + '/config/secret.json', 'w', encoding='utf8') as file:
        file.write(b64decode(secret).decode('utf8'))

    print('\n{0} secret saved\n'.format(name))


def deploy(host, user, password, image, name, _secret):
    """ Deploy Django app from docker container on specified host """

    tar_dir(name, name + '.tar.gz')

    connection = Connection(host=host, port=22, user=user, connect_kwargs={'password': password})
    connection.run('rm -rf {0} && rm -f {1}'.format(name, name + '.tar.gz'))
    connection.put(name + '.tar.gz', remote=name + '.tar.gz')
    connection.run('tar -xvzf ' + name + '.tar.gz')
    connection.run('docker pull {0}'.format(image))
    connection.run('docker stop $(docker ps -a -q)')

    connection.run(
        '''
            docker run -d -p 8000:8000 -v ~/{1}:/dist-truth-checker/{1} {0} /bin/bash -c "
            python manage.py collectstatic --settings=config.settings.production;
            uwsgi uwsgi.ini"
        '''.format(image, name))

    connection.close()


if __name__ == '__main__':
    host_user = os.environ['USER']
    passw = os.environ['PASSWORD']

    params = {
        'aggregator0': {'host': os.environ['AGG0'], 'user': host_user, 'password': passw, 'image': 'averhlv/aggregator',
                        'name': 'aggregator', 'secret': os.environ['AGG_SECRET']},
        'aggregator1': {'host': os.environ['AGG1'], 'user': host_user, 'password': passw, 'image': 'averhlv/aggregator',
                        'name': 'aggregator', 'secret': os.environ['USER']},
        'seo': {'host': os.environ['SEO'], 'user': host_user, 'password': passw, 'image': 'averhlv/seo',
                'name': 'seo_analysis', 'secret': os.environ['SEO_SECRET']},
        'topic': {'host': os.environ['TOPIC'], 'user': host_user, 'password': passw, 'image': 'averhlv/topic',
                  'name': 'topic_modeling', 'secret': os.environ['TOPIC_SECRET']}
    }

    for service in params:
        save_secret(params[service]['name'], params[service]['secret'])
        print('\n{0} deploy started\n'.format(service))
        deploy(**params[service])
        print('\n{0} deployed\n'.format(service))
