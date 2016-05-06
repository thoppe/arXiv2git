import requests
import json
import requests_cache
requests_cache.install_cache('working_cache')

year = 2014

url = "https://api.github.com/search/repositories"

params = {
    "sort" :"stars",
    "order":"desc",
    "per_page":100,
}

date = "{year}-01-01..{year}-12-31".format(year=year)
q = ' '.join([
    "arxiv org",
    "in:description,readme",
    "created:{date}".format(date=date),
    "fork:false",
])

params['q'] = q

def grab(params):
    
    r = requests.get(url, params=params)
    assert(r.status_code == 200)

    h = r.headers
    #print json.dumps(dict(r.headers),indent=2)
    print h["X-RateLimit-Remaining"]
    print h["Link"]

    return json.loads(r.content)


js = grab(params)

print js['total_count']
print js['incomplete_results']
print len(js['items'])
print js.keys()


