import logging
from app.docker.catalog import Catalog
from app.docker.tag import Tag
from app.docker.repository import Repository
from app.async_task.async_task import async_task

KEEP = "latest"
KEEP_LAST = 3

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