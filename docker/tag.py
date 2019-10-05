from httpreq import req

class Tag:
    """Represent an image in a docker repository
    
    Attribute:
        name {string} -- Name of the docker's repository/image
        tag  {string} -- Name of the docker's image tag
    """
    def __init__(self, name, tag):
        self.name = name
        self.tag = tag
        self.sha = ""

    def get_manifest(self):
        """ Retrieve the sha reference of the tag from manifest
        
        Returns:
            sha (string) -- sha reference of the tag
        """
        self.sha = req.get_image_ref(self.name, self.tag)
      
        return self.sha

    def delete(self):
        """ Delete image tag
        """
        req.delete_image(self.name, self.tag)

    def print(self):
        """Print tag info
        """
        print("Repository: {}, Tag: {}, Sha: {}".format(self.name, self.tag, self.sha))