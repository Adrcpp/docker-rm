import logging
import argparse
import configparser
import httpreq.req
from docker.catalog import Catalog
from docker.tag import Tag
import concurrent.futures
from docker.repository import Repository
import time


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
        #list = catalog.get_catalog()
        list = [Repository('repo1'), Repository('repo2'), Repository('repo3'), Repository('repo2'), Repository('repo2'), Repository('repo2')]
        #catalog.print()
        #data = exec_async(list)

        data = async_task(list, "get_tags")

        for index, list_tags in enumerate(data):
            #exec_async_manifest(list_tags, index)
            async_task(list_tags, "get_manifest")


        # for repo in list:
        #     list = repo.get_tags()
        #     repo.print()

        #     for tag in list:
        #         tag.get_manifest()
        #         tag.print()

    except Exception as ex:
        logging.error(ex)


def exec_async(list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        future_to_url = {executor.submit(repo.get_tags): repo for repo in list}
        data = []
        for future in concurrent.futures.as_completed(future_to_url):
            repo = future_to_url[future]
            try:
                res = future.result()
                data.append(res)
            except Exception as exc:
                print('%r generated an exception: %s' % (repo.name, exc))
            else:
                print("Result from Future with arg:{}",repo.name)
        return data


def async_task(task_list, func_name):

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
                print("Result from Future with arg:{}", task.name)
        return data


def exec_async_manifest(list, index):
    print("Starting get manist n° {}", index)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        future_to_url = {executor.submit(tag.get_manifest): tag for tag in list}
        data = []
        for future in concurrent.futures.as_completed(future_to_url):
            tag = future_to_url[future]
            try:
                data.append(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (tag.name, exc))
            else:
                print('%r page is %d bytes' % (tag.tag, len(data)))
        print("Ending get manist n° {}", index)
        return data

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
