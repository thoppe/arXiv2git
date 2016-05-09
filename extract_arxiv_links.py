import glob
import os
import json
import string
import collections
import tqdm

F_JSON = sorted(glob.glob("data/readme/*.json"))
F_REPO = sorted(glob.glob("data/repos/*.json"))
output_dir = 'a2g-links'

repo_lookup = {}
for f in F_REPO:
    with open(f) as FIN:
        js = json.loads(FIN.read())
    for item in js:
        repo_lookup[item['id']] = item['full_name']

def json_iterator():
    for f in F_JSON:
        with open(f) as FIN:
            raw = FIN.read()
        js = json.loads(raw)
        js['filename'] = f
        yield js

def remove_version_number(idx):
    # Remove version number
    name = idx.split('/')
    name[-1] = name[-1].split('v')[0]
    name = '/'.join(name)
    return name

def extract_arxiv_id_from_link(link):
    link = link.replace('.pdf','').replace('.ps','')

    idx = None
    if '/abs/' in link:
        idx = link.split('/abs/')[-1]
    elif '/pdf/' in link:
        idx = link.split('/pdf/')[-1]
    elif '/html/' in link:
        idx = link.split('/html/')[-1]
    elif '/ps/' in link:
        idx = link.split('/ps/')[-1]
    elif '/format/' in link:
        idx = link.split('/format/')[-1]
    elif '/refs/' in link:
        idx = link.split('/refs/')[-1]
    elif '/ftp/' in link:
        idx = link.split('/ftp/')[-1]
        idx = idx.replace('arxiv/','')
        idx = idx.replace('papers/','')

        if '.' in idx:
            idx = idx.split('/')[-1]
        else:
            tokens = idx.split('/')
            idx = '/'.join([tokens[0], tokens[2]])
    else:
        msg = "Strange link extracted {}".format(link)
        print msg

    return remove_version_number(idx)

_url_string_filter = string.lowercase + string.digits + './-'
def find_http_links(line):
    # Only keep the first link found
    if "arxiv.org/" not in line:
        return None

    def remaining_filter(s):
        sx = []
        s_itr = iter(s)

        for x in s:
            if x not in _url_string_filter:
                break
            sx.append(x)
        sx = ''.join(sx).strip('.')
        
        return sx

    matches = [
        'arxiv.org/abs',
        'arxiv.org/pdf',
        'arxiv.org/ftp',
        'arxiv.org/ps',
        'arxiv.org/format',
        'arxiv.org/html',
        'arxiv.org/refs',
    ]

    for m in matches:
        if m in line:
            s = line.split(m)[1:][0]
            iden = remaining_filter(s)
            if not iden:
                continue

            link = m+iden
            return extract_arxiv_id_from_link(link)

    # What remains are non-matching urls
    return None

def find_arxiv_link_in_str(s):
    if ':' in s:
        mark = s.split(':')[1]

        if mark and mark[0] in string.digits:
            mark = ''.join([x for x in mark if x in string.digits+'.'])
            mark = mark.strip('.')
            return remove_version_number(mark)
        if mark and mark[0] in string.lowercase:
            tokens = mark.split('/')
            if len(tokens)>1 and tokens[1][0] in string.digits:
                mark = ''.join([x for x in mark
                                if x in string.digits+'.'])
                mark = mark.strip('.')
                idx = remove_version_number(mark)
                return tokens[0]+'/'+idx

    else:
        # These might be true positives, not 100% sure
        pass
        


def find_arxiv_links(text):
    text = text.lower()

    # Hacky way to find the mirrors
    text = text.replace('arxiv-web2.library.cornell.edu','arxiv.org')
    text = text.replace('arxiv-web3.library.cornell.edu','arxiv.org')
    text = text.replace('arxiv-web4.library.cornell.edu','arxiv.org')
    text = text.replace('arxiv2.library.cornell.edu','arxiv.org')
    text = text.replace('arxiv3.library.cornell.edu','arxiv.org')
    text = text.replace('arxiv4.library.cornell.edu','arxiv.org')

    if u'arxiv' not in text:
        return []

    text = text.replace(' :', ':')
    text = text.replace(' /', '/')
    tokens = text.split()

    # Find locations of all tokens with 'arxiv'
    loc = [i for i,w in enumerate(tokens) if 'arxiv' in w]

    xid = []

    for i in loc:
        link = find_http_links(tokens[i])
        if link:
            xid.append(link)
            tokens[i] = ""
            #print link
            
        link = find_arxiv_link_in_str(tokens[i])
        if link:
            xid.append(link)
            tokens[i] = ""

    # Keep only unique items
    xid = set(xid)

    # Remove the idens with xxx (usually placeholders)
    xid = [x for x in xid if 'xxx' not in x]

    return xid


## ===---===---===---===---===---===---===---===---===---===---


AX = {
    'project'  :collections.defaultdict(list),
    'citation': collections.defaultdict(list),
}

for js in json_iterator():
                
    text_data = {}
    for key in js:
        if key not in ["read_at","id","filename"]:
            text_data[key] = js[key]

    for key in text_data:
        text = text_data[key]
        if text is None: continue
        
        xid = find_arxiv_links(text)
        repo = repo_lookup[js['id']]
        
        ax_type = 'project'
        # Code with > 5 links are classififed as citations        
        if len(xid)>5:
            ax_type = 'citation'

        for x in xid:
            AX[ax_type][x].append(repo)


            
os.system('mkdir -p data data/'+output_dir)

all_ID = set([key for key in AX[ax_type] for ax_type in AX])
all_ID = sorted(list(all_ID))

for key in tqdm.tqdm(all_ID):
    
    # Can't have slashes in filenames
    f_name = os.path.join('data',output_dir, key.replace('/','_'))

    data = {}
    
    for ax_type in AX:
        if key in AX[ax_type]:
            data[ax_type] = sorted(list(set(AX[ax_type][key])))


    with open(f_name,'w') as FOUT:
        js = json.dumps(data,indent=2)
        FOUT.write(js)




