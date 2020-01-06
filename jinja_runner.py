import json
import jinja2
import sys
import os

secrets_file = ''.join([os.path.expanduser('~'),"/.secrets/secrets.json"])
if not os.path.isfile(secrets_file):
    secrets_file = "secrets.json"

h = False
if len(sys.argv) < 3:
    h = True
elif sys.argv[1] in ["--help", "-h", "/?", "/h"]:
    h = True
if h:
    print()
    print("jinja_runner.py requires two arguments:")
    print("   (1) site-code (e.g. xmpl1)")
    print("   (2) template file")
    print()
    print(f"{len(sys.argv)-1} arguments were given: {sys.argv[1:]}")
    print()
    exit(0)

if not os.path.isfile(secrets_file):
    print()
    print(f"missing file '{secrets_file}' in local dir and/or ~/.secrets")

site = sys.argv[1]
fname = sys.argv[2]

if not os.path.isfile('sites.json'):
    print()
    print("Missing sites.json variable file!")
    print()
    exit(1)
if not os.path.isfile(fname):
    print()
    print(f"Template '{fname}' not found!")
    print()
    exit(1)

with open('sites.json','r') as f:
    var_dic = json.loads(f.read())
with open(secrets_file,'r') as f:
    secrets = json.loads(f.read())
if site in var_dic.keys():
    site_dic = var_dic[site]
    site_dic.update(secrets)
else:
    print()
    print(f"Site {site} not found in variable file!")
    print()
    exit(1)

split_fname = fname.split('/')
fdir = '/'.join(split_fname[0:-1])
fname = split_fname[-1]

loader = jinja2.FileSystemLoader(fdir)
env =  jinja2.Environment(loader=loader)
template = env.get_template(fname)
print(template.render(site_dic))
