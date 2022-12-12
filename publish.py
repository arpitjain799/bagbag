#!/opt/homebrew/bin/python3
import re 
import os 
import sys
import time
import subprocess 

if os.path.exists("version"):
    fversion = open("version").read().strip()
else:
    fversion = subprocess.getoutput("pythonPackage=bagbag;curl -Ls https://pypi.org/pypi/$pythonPackage/json | jq -r .info.version").strip()
print("current version:",fversion)

sversion = fversion.split(".")[0] + '.' + fversion.split(".")[1] + '.'
version = int(fversion.split(".")[-1])

nfversion = input("Next version ["+sversion+str(version+1)+"]: ")

if nfversion.strip() == "":
    nfversion = sversion+str(version+1)

print("Next version: " + nfversion)

open("version", "w").write(nfversion)

toml = open("pyproject.toml").read()
toml = re.sub('version = "[0-9]+\\.[0-9]+\\.[0-9]+"', 'version = "' + nfversion + '"', toml)
open("pyproject.toml", "w").write(toml)

u,p = open("ident").read().strip().split(":")

if os.system("""
set -ex 
rm dist/* -rfv
python3 -m build 
pip install ./dist/bagbag-"""+nfversion+"""-py3-none-any.whl
twine upload dist/* -u"""+u+""" -p'"""+p+"""'
docker buildx build --platform linux/amd64,linux/arm64 . -t darren2046/bagbag:"""+nfversion+""" --push 
docker buildx build --platform linux/amd64,linux/arm64 . -t darren2046/bagbag:latest --push 
docker buildx build --platform linux/amd64,linux/arm64 . -t darren2046/python:3.10-"""+nfversion+""" --push 
docker buildx build --platform linux/amd64,linux/arm64 . -t darren2046/python:3.10 --push 
""") != 0:
    sys.exit(0)

# print("Install to local system")
# while 0 != os.system('pip3 install allinone_py_lib==' + nfversion):
#     time.sleep(1)

# os.system('exec ipython')

