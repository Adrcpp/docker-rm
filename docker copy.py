import sys
import urllib.request
import urllib.parse
import http.client 
import json
from pprint import pprint

API = "nexus.nova-technology.fr"
CATALOG = "/v2/_catalog"
TAG_LIST = "/tags/list"
PORT = "8182"


def main():
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    jsonResp = getJson(CATALOG)
    pprint(jsonResp)

    if jsonResp and "repositories" in jsonResp: 
        repoList = jsonResp["repositories"]
        for repo in repoList:
            rep = Repository(repo)
            rep.getTags()
        #     data = getTags(repo)
        #     tags = data["tags"]

        #     if tags:
        #         for tag in tags:
        #             getImageRef(repo, tag)   
    else:
        print('ERROR')
    #getImageRef('teamlink', 'latest')
    #deleteImage()
    #printJson( getJson(API + "/sherlock-frt-snapshot" + TAG_LIST) )


def getJson(url):
    print("getJson : -> " + API + url)
    conn = http.client.HTTPSConnection(API)
    conn.request('GET', url)
    response = conn.getresponse();
    print("Response: ", response.status)

    if response.status == http.HTTPStatus.OK:
        return json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    return None

def printJson(data):
    print(json.dumps(data, indent=4, sort_keys=True))

def getTags(name):
    return getJson("/v2/" + name + TAG_LIST)

def cleanTags(tags):
    return

def deleteImage(imageName, reference):
    url = '/v2' + imageName + '/manifest/' + reference
    conn = http.client.HTTPSConnection(API)
    conn.request('DELETE', url)
    response = conn.getresponse();
    print(response.status, response.reason)

def getImageRef(name, tag):
    print("Name: " + name + " Tag: " + tag)
    url = "/v2/" + name + '/manifests/' + tag 
    conn = http.client.HTTPSConnection(API)

    conn.request('HEAD', url, headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'})
    response = conn.getresponse();
    print(response.status, response.reason)
    print(response.getheader("Docker-Content-Digest"))

    if response.status == http.HTTPStatus.ACCEPTED:
        return response.getheader("Docker-Content-Digest")
    
    # curl -v -H "Accept: application/vnd.docker.distribution.manifest.v2+json" -X HEAD https://registry.example.com/v2/derek/busybox/manifests/latest

main()