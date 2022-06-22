
import json
import requests
import re
import os

from datetime import datetime


# based on code found in ghost forum https://forum.ghost.org/t/api-db-access-point/22250


# TODO: have this config from a file 

def get_config(config_file):

    config = {}
    config['myblog'] = {}
    config['myblog']['user_name'] = ''   # add your user name here
    config['myblog']['user_password'] = ''  # add your password here
    config['myblog']['ghost_url']="https://myblog.ghost.io" # amend this to point to your ghost blog url

    return config

config = get_config('')
option = {'server':'myblog'}
server = 'myblog'


def authenticate(config, server):
    data = {
        'username': config[server]['user_name'],
        'password': config[server]['user_password']
    }
    url = '{}/ghost/api/v3/admin/session/'.format(
        config[server]['ghost_url'])

    session = requests.Session()
    r = session.post(
        url=url,
        data=data)

    if r.status_code != 201:
        "Cannot connect to server"
        exit(1)

    return session


def export(session, config, server):
    url = '{}/ghost/api/v3/admin/db/?include=mobiledoc_revisions'.format(
        config[server]['ghost_url'])
    r = session.get(url)
    if r.status_code == 401:
        "Cannot connect to server to get post"
        exit(1)
    elif r.status_code == 200:
        return r.json()


def write_json(f_path, server, data):
    now = datetime.now().utcnow()
    f_name = now.strftime(
        '{}/{}_%Y-%m-%d-%H-%M-%S.json'.format(
            f_path, server))
    with open(f_name, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":

    session = authenticate(config, option['server'])

    json_export = export(session, config, option['server'])

    ghost_url = config[option['server']]['ghost_url']
    url = re.compile(r"https?://(www\.)?")
    ghost_url_name = url.sub('', ghost_url).strip().strip('/')
    ghost_url_name = ghost_url_name.replace('.', '_')

    cwd = os.getcwd()
    write_json(cwd, ghost_url_name, json_export)



