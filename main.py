import win32api
import json
import mongo
import multiprocessing as MP
from decorate import elapsed_time

compare = lambda x1, x2, y1, y2: ((x1 >= y1) and (x1 <= y2)) or ((x2 >= y1) and (x2 <= y2)) or ((x1 <= y1) and (x2 >= y2))

# print(compare(1,3,0,0))

def capacity_compare(X: int, Y: int) -> bool:
    if X <= Y:
        return False
    capacity = mongo.capacity
    for _, v in capacity.items():
        x = X/v
        y = Y/v
        if (x > 1) ^ (y > 1):
            return False
    return True
        
# @elapsed_time
def filter_query(data: list[dict]) -> tuple[list]:
    for query in data:
        if "hallName" not in query:
            query["hallName"] = None
    cur , wait = [], []
    for i in range(len(data)):
        for j in range(i+1,  len(data)):
            if (data[i]["hallName"] == data[j]["hallName"]) and compare(data[i]["startDate"], data[i]["endDate"], data[j]["startDate"], data[j]["endDate"]):
                if capacity_compare(int(data[i]["capacity"]), int(data[j]["capacity"])):
                    data[i], data[j] = data[j], data[i]
                wait += data[i],
                break
        else:
            cur += data[i],
    # print("Cur :- \n",cur,"\nWait :- \n", wait,'\n')
    return cur, wait

# @elapsed_time
def create_process(target: callable, response: list, data: list[dict]) -> list:
    p = []
    for idx, query in enumerate(data):
        p += MP.Process(target = target, args =(idx, response, query, )),
        p[idx].start()
    for i in p:
        i.join()
        i.close()
    return response

# @elapsed_time
def main(taskID: str, data: list[dict]) -> list:
    mongo.connect()
    if type(data) != list:
        data = [data]
    match taskID:
        case 'Task-1':
            response = create_process(mongo.fetch_halls, MP.Manager().list([0]*len(data)), data)
            # [print("Available halls between {} and {} for capacity {} are {} \n".format(res["startDate"], res["endDate"], res["capacity"], res["avalaibleHalls"])) for res in response]
            
        case 'Task-2' | 'Task-4':
            cur, wait = filter_query(data)
            response = []
            while len(cur):
                res = create_process(mongo.book_hall, MP.Manager().list([0]*len(cur)), cur)
                print('', res, '')
                # [print("{} booking of {} for capacity {} from {} to {} \n".format(r["status"], r["hallName"], r["capacity"], r["startDate"], r["endDate"])) for r in res]
                response += res
                cur, wait = filter_query(wait)
            
        case 'Task-3':
            response = mongo.fetch_booking(data)
            # [print(res) for res in response]
        case _ :
            return "Bad Request"
    return list(response)

#Testing
# taskID = 'Task-1'
# data = [{"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100"}, {"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100"}]

# taskID = 'Task-2'
# data = [{"startDate":"02-06-2021 13:30:00", "endDate":"02-06-2021 14:30:00", "capacity":"100", "hallName":"Hall B"}, {"startDate":"02-06-2021 13:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100", "hallName":"Hall B"}, {"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100", "hallName":"Hall C"}]


taskID = 'Task-2'
data = [{"startDate":"02-06-2021 13:30:00", "endDate":"02-06-2021 14:30:00", "capacity":"100"}, {"startDate":"02-06-2021 13:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"110"}, {"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"90"}]

# if __name__ == '__main__':
    # arguments = win32api.GetCommandLine().split('main.py')[1]
    # try:
    #     taskID = arguments[:arguments.index('[')].strip()
    #     data = json.loads(arguments[arguments.index('['):])
    # except:
    #     taskID = arguments[:arguments.index('{')].strip()
    #     data = [json.loads(arguments[arguments.index('{'):])]
    
    # response = main(taskID, data)
    # print(response)