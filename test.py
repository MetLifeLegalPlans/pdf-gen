#!/usr/bin/env python

import requests
import json
import argparse

LOCAL_URL = "http://localhost:3000"
PROD_URL = "https://pdf-gen.legalplans.com"
PROD_URL = "http://52.73.50.133"

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prod", action="store_true", default=False)
parser.add_argument("-o", "--out", default="out.html")
args = parser.parse_args()

url = PROD_URL if args.prod else LOCAL_URL

with open("data.txt") as f:
    data = json.load(f)

res = requests.post(f"{url}/api/v1/convert/?prof&download=1", json=data, timeout=120)

with open(args.out, "wb") as f:
    f.write(res.content)
