#!/usr/bin/env python3

import sys
import os
import subprocess
import requests
import json
import yaml
import datetime

BASE_PATH = ''
URL = ''
TOKEN = ''
USER = ''
EMAIL = ''

# Parse git config into dict
def config():
    config = dict()
    cmd = subprocess.check_output(['git', 'config', '--list'])
    string = "".join(chr(x) for x in cmd)

    i = 0
    for line in string.splitlines():
        list = line.split("=")

        entry = {
            list[0]: list[1]
        }

        config[i] = entry
        i += 1

    return config


# Get current datetime
def now():
  current = datetime.datetime.now()
  now = current.strftime("%Y-%m-%d %H:%M:%S")
  return now

# Load yaml file
def load(file):
  with open(file, 'r') as f:
    try:
      data = yaml.load(f, Loader=yaml.FullLoader)
    except yaml.YAMLError as e:
      print(e)
      sys.exit(1)
  return data

# Save yaml file
def save(file, data):
  with open(file, 'w') as f:
    try:
      yaml.dump(data, f)
    except yaml.YAMLError as e:
      print(e)
      sys.exit(1)
  return True

# Get all groups data
def get_groups():
    batch_size = 100
    url = '{0}/api/v4/groups?top_level_only=1&per_page={1}'.format(URL, batch_size)
    headers = {'PRIVATE-TOKEN': TOKEN}
    request = requests.get(url, headers=headers)
    response = request.json()
    return response

# Get subgroups by group id
def get_subgroups(id):
    batch_size = 100
    url = '{0}/api/v4/groups/{1}/subgroups?per_page={2}'.format(URL, id, batch_size)
    headers = {'PRIVATE-TOKEN': TOKEN}
    request = requests.get(url, headers=headers)
    response = request.json()
    return response

# Get all projects of a group by group id
def get_projects_group(id):
    batch_size = 100
    url = '{0}/api/v4/groups/{1}/projects?&per_page={2}'.format(URL, id, batch_size)
    headers = {'PRIVATE-TOKEN': TOKEN}
    request = requests.get(url, headers=headers)
    response = request.json()
    return response

# Get all projects data
def get_projects(page):
    batch_size = 100
    url = '{0}/api/v4/projects?per_page={1}&page={2}'.format(URL, batch_size, page)
    headers = {'PRIVATE-TOKEN': TOKEN}
    request = requests.get(url, headers=headers)
    response = request.json()
    return response

# Get all users data
def get_users():
    url = '{0}/api/v4/users'.format(URL)
    headers = {'PRIVATE-TOKEN': TOKEN}
    request = requests.get(url, headers=headers)
    response = request.json()
    return response

# Get user data by username
def get_user(username):
    url = '{0}/api/v4/users?username={1}'.format(URL, username)
    headers = {'PRIVATE-TOKEN': TOKEN}
    request = requests.get(url, headers=headers)
    response = request.json()
    return response

# Get user projects by user id
def get_user_projects(id):
    batch_size = 100
    url = '{0}/api/v4/users/{1}/projects?per_page={2}'.format(URL, id, batch_size)
    headers = {'PRIVATE-TOKEN': TOKEN}
    request = requests.get(url, headers=headers)
    response = request.json()
    return response

# Fetch groups git data
def fetch_groups():
    data = dict()
    groups = get_groups()

    i = 0
    for value in groups:
        group = {
            'id': value['id'],
            'web': value['web_url'],
            'name': value['name'],
            'path': value['path'],
            'full_name': value['full_name'],
            'full_path': value['full_path'],
            'parent_id': value['parent_id']
        }

        data[i] = group
        i += 1

    return data


# Fetch subgroups of a top level group git data by group id
def fetch_subgroups(id):
    data = dict()
    subgroups = get_subgroups(id)

    i = 0
    for value in subgroups:
        subgroup = {
            'id': value['id'],
            'web': value['web_url'],
            'name': value['name'],
            'path': value['path'],
            'full_name': value['full_name'],
            'full_path': value['full_path'],
            'parent_id': value['parent_id']
        }

        data[i] = subgroup
        i += 1

    return data

# Fetch projects of a group by group id or projects of a user if passed as second argument
def fetch_projects_group_or_user(id, username = None):
    data = dict()
    if (username == None):
        projects = get_projects_group(id)
    else:
        projects = get_user_projects(id)

    i = 0
    for value in projects:
        project = {
            'id': value['id'],
            'name': value['name'],
            'path': value['path'],
            'web': value['web_url'],
            'http': value['http_url_to_repo'],
            'ssh': value['ssh_url_to_repo']
        }

        data[i] = project
        i += 1

    return data


# Fetch all projects git data
def fetch_projects():
    tmp = dict()
    data = dict()

    for i in range(0,2):
        projects = get_projects(i+1)
        j = 0
        for value in projects:

            repo = {
                'id': value['id'],
                'name': value['name'],
                'path': value['path'],
                'web': value['web_url'],
                'http': value['http_url_to_repo'],
                'ssh': value['ssh_url_to_repo']
            }

            tmp[j] = repo
            j +=1

        data[i] = tmp

    return data

# Fetch specific user git data by username
def fetch_user_by_username(username):
    data = get_user(username)

    user = {
        'id': data[0]['id'],
        'name': data[0]['name'],
        'username': data[0]['username'],
        'avatar': data[0]['avatar_url'],
        'web': data[0]['web_url'],
        'is_admin': data[0]['is_admin']
    }

    return user

# Find group by slug path
def find_group_by_slug(slug):
    match = None
    groups = fetch_groups()
    for k,group in groups.items():
        if (group['path'] == slug):
            match = group
    return match

# Find config entry by key
def find_config_by_key(key):
    for k,entry in config().items():
        if key in entry:
            return entry[key]
    return False

# Clone multi projects by top level group slug path or username
def clone(target):

    if (target == USER):
        user = fetch_user_by_username(USER)
        id = user['id']
        projects = fetch_projects_group_or_user(id, user['username'])
    else:
        group = find_group_by_slug(target)

        if (group == None):
            print('No match ' + target + ', please check if exist and try again')
            sys.exit(1)

        id = group['id']
        projects = fetch_projects_group_or_user(id)

    # Create directories if not exists
    if not os.path.exists(BASE_PATH + '/' + target):
        os.makedirs(BASE_PATH + '/' + target)

    for k,project in projects.items():

        if os.path.exists(BASE_PATH + '/' + target + '/' + project['path']):
            print('One or more project already cached in this path, please destroy local repo cached before clone')
            sys.exit(1)

        subprocess.call(['git', 'clone', project['ssh'], BASE_PATH + '/' + target + '/' + project['path']])

    if (target == USER):
        print('No support subgroups for personal projects, done')
        sys.exit(0)

    subgroups = fetch_subgroups(id)

    if (len(subgroups) == 0):
        print('there\'s no subproject for this target, done')
        sys.exit(0)

    for k,subgroup in subgroups.items():

        if not os.path.exists(BASE_PATH + '/' + target + '/' + subgroup['path']):
            os.makedirs(BASE_PATH + '/' + target + '/' + subgroup['path'])

        projects_group = fetch_projects_group_or_user(subgroup['id'])

        for k,project_group in projects_group.items():

            if os.path.exists(BASE_PATH + '/' + target + '/' + subgroup['path'] + '/' + project_group['path']):
                print('One or more project already cached in this path, please destroy local repo cached before clone')
                sys.exit(1)

            subprocess.call(['git', 'clone', project_group['ssh'], BASE_PATH + '/' + target + '/' + subgroup['path'] + '/' + project_group['path']])

    print('task complete')
    sys.exit(0)

# Clear local cached repos by top level group slug or username
def clear(target):
    if os.path.exists(BASE_PATH + '/' + target):
        subprocess.call(['rm', '-Rf', BASE_PATH + '/' + target])
    print('task complete')
    sys.exit(0)

def main(command, target):

    if (command == 'clone'):
        clone(target)
    elif (command == 'clear'):
        clear(target)
    else:
        print('command not found')
        sys.exit(0)


if __name__ == '__main__':

    if (not find_config_by_key('sindria.path')):
        print('Error during loading git sindria config, git config --global sindria.path <path>')
        sys.exit(2)

    if (not find_config_by_key('sindria.url')):
        print('Error during loading git sindria config, git config --global sindria.url <url>')
        sys.exit(2)

    if (not find_config_by_key('sindria.token')):
        print('Error during loading git sindria config, git config --global sindria.token <token>')
        sys.exit(2)

    BASE_PATH = find_config_by_key('sindria.path')
    URL = find_config_by_key('sindria.url')
    TOKEN = find_config_by_key('sindria.token')
    USER = find_config_by_key('user.name')
    EMAIL = find_config_by_key('user.email')

    command = sys.argv[1]
    target = sys.argv[2]
    main(command, target)