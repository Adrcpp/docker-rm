import concurrent.futures
import logging

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
