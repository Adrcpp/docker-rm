from httpreq import req
from docker.tag import Tag
from time import sleep

class Repository:
    """Represent an image in a docker repository
    
    Attribute:
        name {string} -- Name of the docker repository/image
    """

    TAG_LIST = "/tags/list"

    def __init__(self, name):
        self.name = name

    def get_tags(self) -> list: 
        """ Return tags list from a docker repository/image 
        
        Returns:
            list -- list of Tags object
        """
        rep = req.get_json("/v2/{}{}".format(self.name, self.TAG_LIST))
        tags = rep["tags"]

        # sleep(2)
        # tags = ["tag1", "tag2", "tag3", "tag4", "tag5"]
        self.list = []

        for tag in tags:
            self.list.append(Tag(self.name, tag))

        return self.list

    def print(self):
        """ Print tag name stdout
        """
        print("Tag list for " + self.name + ":")
        for tag in self.list:
            print("- " + tag.tag)