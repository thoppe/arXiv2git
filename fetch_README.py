import json
import os
import time
import glob
import codecs
import unidecode
from calendar import monthrange
from datetime import date

current_year = date.today().year
current_month = date.today().month

from utils import get_login_params
login_params = get_login_params()

os.system('mkdir -p data data/readme')

clone_cmd = 'git clone --depth 1 {url} {dest}'

def repo_iter():
    gb = os.path.join('data','repos','*.json')
    F_REPO = glob.glob(gb)

    for f in F_REPO:
        with open(f) as FIN:
            js = json.loads(FIN.read())
        for item in js:
            yield item

def get_filename(id):
    return os.path.join('data','readme','{}.json'.format(id))

def update_needed(id):
    f_readme = get_filename(id)
    if not os.path.exists(f_readme):
        return True
    return False

def gather_readme(item):

    # Clear the space
    os.system('rm -rf tmp')

    # Clone the repo
    cmd = clone_cmd.format(url=item["git_url"],dest="tmp")
    os.system(cmd)

    # Find the matching files
    F_README = [x for x in os.listdir('tmp')
                if 'readme' in x.lower()
                and 'html' not in x.lower()]

    data = {}
    for f in F_README:
        f = os.path.join('tmp',f)

        if os.path.isdir(f):
            continue
        
        with codecs.open(f,'r','utf-8') as FIN:
            raw = FIN.read()
            val = unidecode.unidecode(raw)
            data[os.path.basename(f)] = val

    # Clear the space
    os.system('rm -rf tmp')
    
    return data
    

for r in repo_iter():

    id = r['id']
    if not update_needed(id):
        print "Skipping", id
        continue

    print "Cloning", id
       
    data = gather_readme(r)
    data["description"] = r["description"]
    data['id'] = r['id']
    data['read_at'] = int(time.time())

    js = json.dumps(data,indent=2)

    with codecs.open(get_filename(id),'w','utf-8') as FOUT:
        FOUT.write(js)

    print "Sleeping", 2
    time.sleep(2)
