# DOCKER REGISTRY MANAGER

Originally intended for cleaning image tag's in a Nexus snapshot registry. Keeping latest tag and the last 3 tags.

# Usage :

edit configure.ini:

- API        - Your registry URL (only domain name ex: domain.com)
- CREDENTIAL - Your credential in base64 (you can found it in ~/.docker/config.json)
- KEEP       - Tag you want to keep (default: latest)
- KEEP_LAST  - Number of tag you want to keep (default: 3)

`
python docker-rm
`

# Option :

  -h, --help            show this help message and exit  
  -v, --verbose         increase output verbosity  
  -d, --dry-run         Output what would be deleted from the registry  
  -c, --catalog         Output all repository from the registry <name>  
  -r REPOSITORY, --repository REPOSITORY  
  Output all tags for repository <name>   