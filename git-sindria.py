#!/usr/bin/env python3

import sys
import os
import subprocess
import argparse
import requests
import json
import yaml
import datetime

BASE_PATH = ''
URL = ''
TOKEN = ''
PROVIDER = ''
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

    # Subgroups supported only for gitlab - return empty list for non gitlab git provider
    # if (PROVIDER != 'gitlab' or PROVIDER != 'gitlab-self-hosted'):
    #     return []

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
        'web': data[0]['web_url']
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

# Find git provider return default if not defined
def find_provider():
    provider = find_config_by_key('sindria.provider')
    if (not provider):
        provider = 'gitlab-self-hosted'
    return provider

# Find git provider base url
def find_url():
    url = find_config_by_key('sindria.url')
    if (not url):
        if (PROVIDER == 'bitbucket'):
            url = 'https://bitbucket.org'
        elif (PROVIDER == 'github'):
            url = 'https://github.com'
        elif (PROVIDER == 'gitlab'):
            url = 'https://gitlab.com'
        else:
            print('Error during loading git sindria config, git config --global sindria.url <url>')
            sys.exit(2)
    return url

# Clone multi projects by top level group slug path or username
def clone(target, options):

    # Validate options
    available_options = [None, '-p', '--partial', '-f', '--force']
    if (not options in available_options):
        print('Option unavailable\n')
        help_clone()
        sys.exit(1)

    if (target == USER):
        # TODO: implement support personal projects for non gitlab git provider
        support_providers = ['gitlab-self-hosted', 'gitlab']
        if (not PROVIDER in support_providers):
            print('Personal projects not supported for ' + PROVIDER + ' git provider')
            sys.exit(0)

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

    # Clear already cached target with -f or --force option
    if (options == '-f' or options == '--force'):
        clear(target)

    # Create directories if not exists
    if not os.path.exists(BASE_PATH + '/' + target):
        os.makedirs(BASE_PATH + '/' + target)

    for k,project in projects.items():

        if (options == '-p'):
            if os.path.exists(BASE_PATH + '/' + target + '/' + project['path']):
                print('Project '+ project['path']+ ' already cached in this path, skip')
            else:
                subprocess.call(['git', 'clone', project['ssh'], BASE_PATH + '/' + target + '/' + project['path']])
        else:

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

            if (options == '-p'):
                if os.path.exists(BASE_PATH + '/' + target + '/' + subgroup['path'] + '/' + project_group['path']):
                    print('Subproject '+ project_group['path'] + ' already cached in this path, skip')
                else:
                    subprocess.call(['git', 'clone', project_group['ssh'], BASE_PATH + '/' + target + '/' + subgroup['path'] + '/' + project_group['path']])
            else:

                if os.path.exists(BASE_PATH + '/' + target + '/' + subgroup['path'] + '/' + project_group['path']):
                    print('One or more subproject already cached in this path, please destroy local repo cached before clone')
                    sys.exit(1)

                subprocess.call(['git', 'clone', project_group['ssh'], BASE_PATH + '/' + target + '/' + subgroup['path'] + '/' + project_group['path']])

    print('task complete')
    sys.exit(0)

# Clear local cached repos by top level group slug or username
def clear(target):
    if not os.path.exists(BASE_PATH + '/' + target):
        print('No match ' + target + ', please check if exist and try again')
        sys.exit(1)

    subprocess.call(['rm', '-Rf', BASE_PATH + '/' + target])
    print('task complete')

# Simplify git log advanced command
def log():
    return subprocess.call(['git', 'log', '--oneline', '--decorate', '--all', '--graph'])

# Simplify edit author last commit
def author(username, email):
    return subprocess.call(['git', 'commit', '--amend', '--author="'+username+' <'+email+'>"', '--no-edit'])

# Simplify release using git tag command
def release(release):
    subprocess.call(['git', 'tag', '-a', release])
    subprocess.call(['git', 'push', 'origin', release])
    print('task complete')
    sys.exit(0)

# Help message usage clone command
def help_clone():
    print('Usage: git sindria clone <target> <options>')
    print('')
    print('-h, --help\t\tPrint this message')
    print('')
    print('Available options:')
    print('')
    print('-p, --partial\t\tPartial multi clone skipping already cached repos')
    print('-f, --force\t\tForce clear already cached repos before multi clone')
    print('')
    print('Examples:')
    print('')
    print('git sindria clone devops')
    print('git sindria clone devops -p')
    print('git sindria clone devops -f')

# Help message usage global
def help():
    print('Usage: git sindria <command> <target> <options>')
    print('')
    print('-h, --help\t\tPrint this message')
    print('')
    print('Available commands:')
    print('')
    print('clone\t\tMulti clone by top level group or username')
    print('clear\t\tClear local cached repos by top level group or username')
    print('log\t\tGit log advanced')
    print('release\t\tCreate new release')
    print('')
    print('Examples:')
    print('')
    print('git sindria clone devops')
    print('git sindria clear devops')
    print('git sindria log')
    print('git sindria release 1.0.0')

# Main
def main(command):

    if (command == '-h' or command == '--help'):
        help()
    elif (command == 'clone'):
        if len(sys.argv) > 2:
            target = sys.argv[2]
            if (target == '-h' or target == '--help'):
                help_clone()
                sys.exit(1)
        else:
            help_clone()
            sys.exit(1)

        if len(sys.argv) > 3:
            options = sys.argv[3]
        else:
            options = None

        clone(target, options)
    elif (command == 'clear'):
        if len(sys.argv) > 2:
            target = sys.argv[2]
        else:
            help()
            sys.exit(1)

        clear(target)
    elif (command == 'log'):
        log()
    elif (command == 'release'):
        if len(sys.argv) > 2:
            target = sys.argv[2]
        else:
            help()
            sys.exit(1)

        release(target)
    else:
        print('command not found')
        sys.exit(0)

# Execute
if __name__ == '__main__':

    if (not find_config_by_key('sindria.path')):
        print('Error during loading git sindria config, git config --global sindria.path <path>')
        sys.exit(2)

    if (not find_config_by_key('sindria.token')):
        print('Error during loading git sindria config, git config --global sindria.token <token>')
        sys.exit(2)

    USER = find_config_by_key('user.name')
    EMAIL = find_config_by_key('user.email')

    PROVIDER = find_provider()
    URL = find_url()

    BASE_PATH = find_config_by_key('sindria.path')
    TOKEN = find_config_by_key('sindria.token')

    # Check if git provider is suppported
    available_providers = ['gitlab-self-hosted', 'gitlab', 'bitbucket']
    if (not PROVIDER in available_providers):
        print('Git provider not supported')
        sys.exit(2)

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        help()
        sys.exit(1)

    main(command)