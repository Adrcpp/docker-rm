from httpreq import req
from docker.repository import Repository

class Catalog:
    """Represent all the image name of a docker registry
    
    Attribute:
        name {string} -- Name of the docker registry
        list {dict}   -- List of Repository object
    """

    CATALOG = "/v2/_catalog"

    def __init__(self):
        pass

    def get_catalog(self):
        """Retrieve all image name - create a list of Repository object
        
        Returns:
            list (dict) -- list of Repository object
        """

        rep = req.get_json(self.CATALOG)
        repoList = rep["repositories"]

        self.list = []

        for repo in repoList:
            self.list.append(Repository(repo))

        return self.list

    def print(self):
        """Print all image name
        """
        print("Repository list: ")
        for repo in self.list:
            print("- " + repo.name)