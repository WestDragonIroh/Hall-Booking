import json
import datetime

def data_check(taskID, data) -> list[list]:
    if type(data) == dict:
        data = [data]   
    date_formate = '%d-%m-%Y %H:%M:%S'
    good_query, bad_query = [], []
    for query in data:
        if "startDate" not in query or "endDate" not in query:
            bad_query += query,
            continue   
        try:
            start = datetime.datetime.strptime(query["startDate"], date_formate)
            end = datetime.datetime.strptime(query["endDate"], date_formate)
        except:
            bad_query += query,
            continue
        if start > end:
            bad_query += query,
            continue
        if taskID in {'Task-1', 'Task-2', 'Task-4'} and "capacity" not in query:
            bad_query += query,
            continue
        if taskID == 'Task-2' and "hallName" not in query:
            bad_query += query,
            continue
        good_query += query,
        
    return [good_query, bad_query]
        

def validate(args: dict) -> dict:
    args["Error"] = {}
    if 'taskID' not in args or args['taskID'] not in {'Task-1', 'Task-2', 'Task-3', 'Task-4'}:
        args["Error"]["TaskKeyError"] = 'Task ID is invalid'
    taskID = args['taskID']
    if 'data' not in args:
        args["Error"]["DataKeyError"] = 'Data not found'
    else:
        try:
            print(taskID , args["data"])
            data = json.loads(args["data"])
            data = data_check(taskID, data)
            args["data"] = data[0]
            if len(data[1]):
                args["Error"]["BadQueries"] = data[1] 
        except:
            args["Error"]["DataTypeError"] = 'Send data in json format'
    return args





taskID = 'Task-2'
data = [{ "startDate":"02-06-2021 13:30:00", "endDate":"02-06-2021 14:30:00", "capacity":"100"}, {"startDate":"02-06-2021 13:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100"}, {"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100"}, {"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100"}]
    
if __name__ == '__main__':
    args = {"taskID": taskID, "data": json.dumps(data)}
    validate(args)