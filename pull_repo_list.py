import requests
import json
import os
import requests_cache
requests_cache.install_cache('working_cache')

keep_keys = [
    'id',
    'full_name',
    'description',
    'git_url',
    'created_at',
    'size',
    'stargazers_count',
    'watchers_count',
    'language',
    'forks_count',
    'score',
]


base_url = "https://api.github.com/search/repositories"

params = {
    "sort" :"stars",
    "order":"desc",
    "per_page":100,
}

_total_count = None

def grab(url, params):
    global _total_count
    r = requests.get(url, params=params)
    
    if r.status_code != 200:
        msg = "Exiting with status code {}".format(r.status_code)
        raise ValueError(msg)

    h = r.headers
    
    #print json.dumps(dict(r.headers),indent=2)
    if h["X-RateLimit-Remaining"] < 2:
        msg = "Rate limit hit! Exiting"
        raise ValueError(msg)

    js = json.loads(r.content)
    _total_count = js["total_count"]

    yield js

    if "Link" in h:
        link_str = h["Link"]
        next_link = [x for x in link_str.split(',') if 'rel="next"' in x]
        if next_link:
            
            link = (next_link[0].split('>;')[0]).strip('<')
            for x in grab(link,{}):
                yield x

def grab_year(year):
    date = "{year}-01-01..{year}-12-31".format(year=year)
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



year = 2010


print "Starting year", year
results = grab_year(year)
assert(_total_count == len(results))

os.system('mkdir -p data data/repos')

f_out = 'data/repos/{}.json'.format(year)
with open(f_out,'w') as FOUT:
    s = json.dumps(results,indent=2)
    FOUT.write(s)




