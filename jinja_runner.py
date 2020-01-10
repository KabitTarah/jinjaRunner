import json
import jinja2
import sys
import os
print()

h = False
if len(sys.argv) < 3:
    h = True
elif sys.argv[1] in ["--help", "-h", "/?", "/h"]:
    h = True
if h:
    print("jinja_runner.py requires two arguments:")
    print("   (1) site-code (e.g. ppx1)")
    print("   (2) template file")
    print()
    print("Important Files in this directory:")
    print("   globals.json      - Holds global variables applied to all sites, (accessed with literal \"global\" and variable")
    print("                       key \"global.<variable>\")")
    print("   sites.json        - Holds site specific variables, ex:")
    print("                       \"sitecode\": {")
    print("                            \"someVar\": \"SomeValue\"")
    print("                       }")
    print("   secrets.json      - Holds hidden global secrets (accessed with literals \"global\" and \"secret\" and variable")
    print("                       key \"global.secret.<variable>\"). Variables should return the original variable text, ex:")
    print("                       \"SecretVar\": \"{{ global.secret.SecretVar }}\"")
    print("   site_secrets.json - Holds hidden site specific secrets. Variables should return the original text, as for secrets.json and uses")
    print("                       the same format as sites.json (accessed with literal \"secret\" and key: \"secret.<variable>\")")
    print("Important Files in ~/.secrets/ (recommend setting this directiory chmod 700, and these files chmod 600)")
    print("   secrets.json      - Holds visible secrets. The format is the same as for secrets.json in the main directory")
    print("   site_secrets.json - Holds visible site specific secrets. The format is the same as site_secrets.json in the main directory")
    print()
    print(f"{len(sys.argv)-1} arguments were given: {sys.argv[1:]}", file=sys.stderr)
    print()
    exit(0)

site = sys.argv[1]
secretsite = site
template_fname = sys.argv[2]

secrets_file = ''.join([os.path.expanduser('~'),"/.secrets/secrets.json"])
if not os.path.isfile(secrets_file):
    secrets_file = "secrets.json"
siteSecrets_file = ''.join([os.path.expanduser('~'),"/.secrets/site_secrets.json"])
if not os.path.isfile(siteSecrets_file):
    siteSecrets_file = "site_secrets.json"
    # Use a default name for the default secrets file
    secretsite = "site"

if not os.path.isfile(template_fname):
    print(f"ERROR: missing template file '{template_fname}'", file=sys.stderr)
    exit(1)

vars_dic = dict()

# site specific variables loaded from "sites.json"
if not os.path.isfile('sites.json'):
    print("WARNING: missing file 'sites.json' in local dir", file=sys.stderr)
else:
    with open('sites.json','r') as f:
        sites_dic = json.loads(f.read())
    if site in sites_dic.keys():
        # "secret" is an invalid key name
        sites_dic[site].pop('secret',"")
        # "global" is an invalid key name
        sites_dic[site].pop('global',"")
        vars_dic.update(sites_dic[site])
    else:
        print(f"WARNING: site {site} not found in 'sites.json'", file=sys.stderr)

# global variables loaded from gloabls.json"
if not os.path.isfile('globals.json'):
    print("WARNING: missing file 'globals.json' in local dir", file=sys.stderr)
else:
    with open('globals.json','r') as f:
        global_dic = json.loads(f.read())
    # "secret" is an invalid key name
    global_dic.pop("secret","")
    vars_dic['global'] = global_dic
    
# secret variables loaded from secrets_file
if not os.path.isfile(secrets_file):
    print(f"WARNING: missing file '{secrets_file}' in local dir and ~/.secrets", file=sys.stderr)
else:
    with open(secrets_file,'r') as f:
        secrets_dic = json.loads(f.read())
    vars_dic['global']['secret'] = secrets_dic

# site specific secret variables loaded from siteSecrets_file
if not os.path.isfile(siteSecrets_file):
    print(f"WARNING: missing file '{siteSecrets_file}' in local dir and ~/.secrets'", file=sys.stderr)
else:
    with open(siteSecrets_file,'r') as f:
        siteSecrets_dic = json.loads(f.read())
    if site in siteSecrets_dic.keys():
        vars_dic['secret'] = siteSecrets_dic[site]
    else:
        print(f"WARNING: site {site} not found in '{siteSecrets_file}'", file=sys.stderr)

split_fname = template_fname.split('/')
fdir = '/'.join(split_fname[0:-1])
template_fname = split_fname[-1]

loader = jinja2.FileSystemLoader(fdir)
env =  jinja2.Environment(loader=loader)
template = env.get_template(template_fname)
print(template.render(vars_dic))

