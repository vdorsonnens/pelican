import os, sys

from git import Repo
from travispy import TravisPy

PELICAN = 'pelican'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TOKEN_FILE = '.travistoken'

def get_pelican_repo():
  # get the parent of the current directory
  repo_path = os.path.dirname(DIR_PATH)
  return Repo(repo_path)


def get_travis_token():
  token_path = os.path.join(DIR_PATH, TOKEN_FILE)
  if os.path.isfile(token_path):
    return read_token_file(token_path)
  
  print('You need your TravisCI token to authenticate with the API')
  print('Find it at this address: https://travis-ci.org/account/preferences')
  
  token = ''
  while token == '':
    token = input('Your token: ')
  
  write_token_file(token_path, token)

  return token

def read_token_file(path):
  token = ''
  with open(path) as f:
    token = f.read()

  return token

def write_token_file(path, token):
  with open(path, 'w+') as f:
    f.write(token)

if __name__ == '__main__':
  # get the pelican repo and read the configuration
  repo = get_pelican_repo()
  reader = repo.config_reader()
  
  # build the remote repo name with the github user, ex: vdorsonnens/pelican
  reader.read()
  github_username = reader.get_value('user', 'name')
  remote_repo = '/'.join([github_username, PELICAN])

  # connect to travis-ci
  token = get_travis_token()
  travis_client = TravisPy(token)
  travis_repo = travis_client.repo(remote_repo)

  success = False
  if travis_repo.active:
    print('Repository is already enabled')
    sys.exit(0)

  else:
    print('Enabling repo...')
    success = travis_repo.enable()


  if success:
    print('Operation successful')
    sys.exit(0)
  

  print('Failed operation')
  sys.exit(1)
