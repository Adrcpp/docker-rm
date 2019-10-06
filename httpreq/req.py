import http.client
import json
import logging
import concurrent.futures

API = ""

def get_json(url) -> json:
    """Get a json from url
    
    Arguments:
        url {string} -- https url 
    
    Returns:
        json or None -- json
    """
    logging.debug("Url: {}".format(API + url))
    conn = http.client.HTTPSConnection(API)
    conn.request('GET', url)
    response = conn.getresponse()
    logging.debug("Status: {}".format(response.status))

    ret = None
    if response.status == http.HTTPStatus.OK:
        ret = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    conn.close()
    return ret

# async def get_json(url) -> json:
#     """Get a json from url
    
#     Arguments:
#         url {string} -- https url 
    
#     Returns:
#         json or None -- json
#     """
#     logging.debug("Url: {}".format(API + url))
#     with http.client.HTTPSConnection(API) as conn:
#         conn.request('GET', url)
#         response = conn.getresponse()
#         logging.debug("Status: {}".format(response.status))

#         ret = None
#         if response.status == http.HTTPStatus.OK:
#             ret = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

#         conn.close()
#         return ret

def get_image_ref(name, tag) -> str:
    """Get image reference (sha) from a tag's image 
    
    Arguments:
        name {string} -- Image name
        tag  {string} -- Tag name
    
    Returns:
        string -- docker sha reference of a tag's image
    """
    logging.debug("Name: {}, Tag: {}".format(name, tag))
    url = '/v2/{}/manifests/{}'.format(name, tag);

    logging.debug("Url: {}".format(API + url))
    conn = http.client.HTTPSConnection(API)
    conn.request('HEAD', url, headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'})
    response = conn.getresponse();

    logging.debug("Status: {}, Reason: {} ".format(response.status, response.reason))
    logging.debug("Docker-Content-Digest: {}".format(response.getheader("Docker-Content-Digest")))

    ret = None
    if response.status == http.HTTPStatus.OK:
        ret = response.getheader("Docker-Content-Digest")
    conn.close()

    return ret

def delete_image(image_name, reference):
    """Delete image from repository
    
    Arguments:
        image_name {string} -- Docker image name
        reference {string} -- Docker sha reference of a tag's image
    """
    url = '/v2/{}/manifest/{}'.format(image_name, reference)
    logging.debug("Url: {}, Method: DELETE".format(API + url))

    conn = http.client.HTTPSConnection(API)
    conn.request('DELETE', url)
    response = conn.getresponse()
    logging.info("Status: {}, Reason: {} ".format(response.status, response.reason))

    conn.close()