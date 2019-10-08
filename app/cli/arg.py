import logging
import argparse
import configparser
import app.httpreq.req
import errno

def set_vars_from_conf():
    """Set vars from configure.ini file
    """
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        app.httpreq.req.API = config.get("vars", "API")
        app.httpreq.req.CREDENTIAL = config.get("vars", "CREDENTIAL")
        app.cli.command.KEEP_LAST = int(config.get("vars", "KEEP_LAST"))
        app.cli.command.KEEP = config.get("vars", "KEEP")
    except configparser.Error as e:
        logging.error("Error in parsing configure.ini: {}".format(e))
        exit(errno.EINVAL)

def get_args():
    """Set argument to be parsed, return list of parsed argument
    
    Returns:
        [list] -- List of parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='A docker registry manager'
    )
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-d", "--dry-run", help="Output what would be deleted from the registry", action="store_true")
    parser.add_argument("-c", "--catalog", help="Output all repository from the registry <name>", action="store_true")                     
    parser.add_argument("-r", "--repository", help="Output all tags for repository <name>")     

    return parser.parse_args()
