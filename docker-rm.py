import logging
import argparse
import configparser
import httpreq.req
import time
import errno
import concurrent.futures
from docker.catalog import Catalog
from docker.tag import Tag
from docker.repository import Repository

KEEP_LAST = 3
KEEP = "latest"

def main():
    
    set_vars_from_conf()
    args = get_args()

    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.info("Verbose output.")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    if args.catalog:
        logging.debug("Catalog")
        show_catalog()

    elif args.repository:
        logging.debug("Reposirory : {}".format(args.repository))
        show_tags(args.repository)

    elif args.dry_run:
        logging.debug("Dry Run:")
        dry_run()

    else :
        logging.debug("Delete:")
        exec_del(True)


def set_vars_from_conf():
    """Set vars from configure.ini file
    """
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        httpreq.req.API = config.get("vars", "API")
        httpreq.req.CREDENTIAL = config.get("vars", "CREDENTIAL")
        KEEP_LAST = config.get("vars", "KEEP_LAST")
        KEEP = config.get("vars", "KEEP")
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


def show_catalog():
    """ Print catalog
    """
    catalog = Catalog()
    list = catalog.get_catalog()
    print("Repository :")
    for repo in list:
        print ("  - {}".format(repo.name))


def show_tags(repository: str):
    """Print tags of a repository
    
    Arguments:
        repository {str} -- repository name
    """
    data = async_task([Repository(repository)], "get_tags")
    print("Tag list for repository : {}".format(repository))
    for tag in data[0]:
        print("  - {}".format(tag.tag))


def dry_run():
    """ Dry run - print tag to that would be deleted
    """
    exec_del(False)


def exec_del(delete: bool):
    """Delete repository tag
    """
    try:
        catalog = Catalog()
        list = catalog.get_catalog()
        data = async_task(list, "get_tags")

        keep_tag = Tag("", KEEP)
        for list_tags in data:
            
            if keep_tag in list_tags:
                list_tags.remove(keep_tag)

            if len(list_tags) > KEEP_LAST:
                last_index = len(list_tags) - KEEP_LAST
                remove_or_print(delete, list_tags[:last_index])

    except Exception as ex:
        logging.error(ex)


def remove_or_print(delete: bool, list_tags: list):
    """ Print or delete tag from repository
    
    Arguments:
        delete    {bool} -- If true delete tag, else just print
        list_tags {list} -- Tag list to delete/print
    """
    if delete:
        list_remove = async_task(list_tags, "retrieve_manifest")
        async_task(list_remove, "delete")
    else:
        print("Would be deleted: ")
        for tag in list_tags:
            print("- {}:{}".format(tag.name, tag.tag))


def async_task(task_list: list, func_name: str):
    """Execute the function of each objects in the list asynchronously
       in 5 threads

    Arguments:
        task_list {list} -- List of object (Repository or Tag)
        func_name {str}  -- The function to be executed (ex: Repository.get_tag())
    
    Returns:
        [list] -- List of objects
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_task = {}
        for task in task_list:
            func = getattr(task, func_name)
            future_task.update( { executor.submit(func): task } )

        data = []
        for future in concurrent.futures.as_completed(future_task):
            task = future_task[future]
            try:
                res = future.result()
                data.append(res)
            except Exception as exc:
                print('generated an exception: %s' % (exc))
            else:
                logging.debug("Result from {} of {}".format(func_name, task.name))
        return data


if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    logging.debug(f"{__file__} executed in {elapsed:0.2f} seconds.")