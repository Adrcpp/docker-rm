# DOCKER REGISTRY MANAGER

Originally intended for cleaning image tag's in a Nexus snapshot registry. Keeping latest tag and the last 3 tags.

# Usage :

edit configure.ini:

Add your registry URL

`
python docker-rm
`

# Option :

  -h, --help         show this help message and exit  
  -v, --verbose      increase output verbosity  
  -d, --dry-run      Output what would be deleted from the registry  
  -r, --repository   Output all repository name  
  -t TAG, --tag TAG  Output all tags for repository <name>  