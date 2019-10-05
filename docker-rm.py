import logging
import argparse
import configparser
import httpreq.req
from docker.catalog import Catalog
from docker.tag import Tag

def main():

    config = configparser.ConfigParser()
    config.read("config.ini")

    httpreq.req.API = config.get("vars", "API")

    #Argument parser
    parser = argparse.ArgumentParser(
        description='A docker repository handler'
    )

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    parser.add_argument("-d", "--dry-run", help="Output what would be deleted from the registry",
                        action="store_true")

    parser.add_argument("-r", "--repository", help="Output all repository name",
                        action="store_true")     
    
    parser.add_argument("-t", "--tag", help="Output all tags for repository  <name>")                     

    args = parser.parse_args()
    ##############


    # Set logging 
    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.info("Verbose output.")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    ##############

    
    try:
        catalog = Catalog()
        list = catalog.get_catalog()
        catalog.print()

        for repo in list:
            list = repo.get_tags()
            repo.print()

            for tag in list:
                tag.get_manifest()
                tag.print()

    except Exception as ex:
        logging.error(ex)

main()