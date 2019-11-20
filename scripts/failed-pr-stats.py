import os
import pickle
import requests
from dateutil.parser import parse

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

API_ENDPOINT = 'https://api.github.com'
PR_ENDPOINT = API_ENDPOINT + '/repos/getpelican/pelican/pulls?sort=created&state=all&direction=desc&page={}'
MAX_PAGE = 10
DATA_FILE = 'statuses.pkl'
HEADERS = {'Authorization': 'token {}'.format(os.getenv('GITHUB_TOKEN', ''))}

def get_pr_statuses():
  statuses = []
  
  if os.path.isfile(DATA_FILE):
    print('reading cached data')
    with open(DATA_FILE, 'rb') as f:
      statuses = pickle.load(f)

    return statuses

  for page in range(1, MAX_PAGE + 1):
    print('fetching page {}/{}'.format(page, MAX_PAGE))
    resp = requests.get(PR_ENDPOINT.format(page), headers=HEADERS)
    prs = resp.json()

    for pr in prs:
      created_at = parse(pr['created_at'])

      statuses_resp = requests.get(pr['statuses_url'], headers=HEADERS)
      stats = statuses_resp.json()
      for status in stats:
        if 'travis ci' in status['description'].lower() and status['state'] != 'pending':
          statuses.append((created_at, status['state']))
  
  print('saving data...')
  with open(DATA_FILE, 'wb') as f:
    pickle.dump(statuses, f)
  print('done')

  return statuses


if __name__ == '__main__':
  statuses = get_pr_statuses()

  years = {}
  for status in statuses:
    year = status[0].year
    if year not in years.keys():
      years[year] = {'success': 0, 'total': 0}

    if status[1] == 'success':
      years[year]['success'] += 1

    years[year]['total'] += 1

  data = []
  for k, v in years.items(): 
    ratio = 1.0 - float(v['success'])/v['total']
    data.append((k, ratio))

  data = sorted(data, key=lambda x:x[0])
  x = [d[0] for d in data]
  y = [d[1] for d in data]
  plt.bar(x, y)
  plt.ylim(0, .45)
  plt.show()

