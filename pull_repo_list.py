import requests
import json
import os
import time
from calendar import monthrange
from datetime import date
import itertools

current_year = date.today().year
current_month = date.today().month
#import requests_cache
#requests_cache.install_cache('working_cache')

from utils import get_login_params
login_params = get_login_params()

keep_keys = [
    'id',
    'full_name',
    'description',
    'git_url',
    'created_at',
    'pushed_at',
    'updated_at',
    'size',
    'stargazers_count',
    'watchers_count',
    'language',
    'forks_count',
]

base_url = "https://api.github.com/search/repositories"

params = {
    "sort" :"created",
    "order":"desc",
    "per_page":100,
}
params.update(login_params)


_total_count = None

def grab(url, params):
    global _total_count
    r = requests.get(url, params=params)
    h = r.headers
    
    if r.status_code != 200:
        print h
        msg = "Exiting with status code {}".format(r.status_code)
        raise ValueError(msg)
    
    current_time  = int(time.time())
    remaining_req = int(h["X-RateLimit-Remaining"])
    
    if remaining_req < 2:
        delta = int(h["X-RateLimit-Reset"]) - current_time + 2
        print "Rate limit hit! Holding...", delta
        time.sleep(delta)
        
    js = json.loads(r.content)
    _total_count = js["total_count"]

    if _total_count > 1000:
        msg = "Search broken with > 1000 results, need refined query..."
        raise SyntaxError(msg)

    yield js

    if "Link" in h:
        link_str = h["Link"]
        next_link = [x for x in link_str.split(',') if 'rel="next"' in x]
        if next_link:
            
            link = (next_link[0].split('>;')[0]).strip('<')
            for x in grab(link,{}):
                yield x

def grab_range(year,month):
    
    date = "{year}-{month:02d}-01..{year:02d}-{month:02d}-{day:02d}"
    date = date.format(year=year,
                       month=month,
                       day=monthrange(year,month)[1])
    
    q = ' '.join([
        "arxiv",
        "in:description,readme",
        "created:{date}".format(date=date),
        "fork:false",
    ])

    params['q'] = q              
    INPUT_ITR = grab(base_url, params)

    results = []
    for k,page in enumerate(INPUT_ITR):
       
        print "Grabbed {: 3d} items from page {}".format(len(page["items"]),k)

        for item in page["items"]:
            results.append(reduce_item(item))

    return results

def reduce_item(item):
    data = {}
    for key in keep_keys:
        data[key] = item[key]
    return data



os.system('mkdir -p data data/repos')

years = range(2007, current_year+1)
months = range(1,13)

INPUT_ITR = itertools.product(years,months)

for year,month in INPUT_ITR:

    # Stop if past the present
    if year == current_year:
        if month > current_month:
            break
              
    print "Starting year/month", year, month

    results = grab_range(year,month)
    assert(_total_count == len(results))
    print " {} results found".format(len(results))

    f_out = 'data/repos/{}_{}.json'.format(year,month)
    with open(f_out,'w') as FOUT:
        s = json.dumps(results,indent=2)
        FOUT.write(s)
