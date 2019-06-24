import requests
import grequests as async
import json
import glob
import logging


logging.basicConfig(level=logging.INFO)
### Methods

def hook_factory(*factory_args, **factory_kwargs):
    def response_hook(response, *request_args, **request_kwargs):
      tmp_json = response.json()
      factory_args[0][tmp_json['name']] = {
        'name': tmp_json['name'],
        'description': tmp_json['description'],
        'versions': factory_args[1]
      }
      return None
    return response_hook

### Global vars

logging.info("[I] ==> Setting global variables")
async_list = []
global_json = {}
url = "https://quay.io/api/v1/repository?public=true&namespace=biocontainers"

### Main body

logging.info("[I] ==> Beginning loop for items")
for i in glob.glob("*"):
  logging.debug("[D] ==> Enter directory {}".format(str(i)))
  all_files = glob.glob("{}/*.simg".format(i))
  all_files = sorted([item.split('/')[-1] for item in all_files], reverse=True)
  for j in all_files:
    logging.debug("[D] ==> NOT A CONTAINER {}".format(str(j)))
    if ".simg" in j:
        logging.info("[I] ==> Current container {}".format(str(j)))
        req = 'https://quay.io/api/v1/repository/biocontainers/'+i+"?public=true"
        logging.info("[I] ==> GET for {}".format(i))
        action_item = async.get(req, hooks = {'response' : [hook_factory(global_json, all_files)]})
        async_list.append(action_item)

async.map(async_list)
with open('collection.json', 'w') as f:
  json.dump(global_json, f