import pymongo
from decorate import elapsed_time, delay_time

def connect() -> None:
    global bookings, capacity
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["HallsBooking"]
    bookings = db["bookings"]
    capacity = iter(db["capacity"].find()).next()
    capacity.pop('_id')
    
def get_doc(query: dict, hall_id = None, limit =  0) -> list:
    return list(iter(bookings.find(
                {"$and":
                    [{"hallName": hall_id
                    },{"$or":
                        [{"$and": 
                            [{"startDate": {"$gte": query["startDate"]}}, 
                            {"startDate": {"$lte": query["endDate"]}}]
                        },{"$and": 
                            [{"endDate": {"$gte": query["startDate"]}}, 
                            {"endDate": {"$lte": query["endDate"]}}]
                        },{"$and":
                            [{"startDate": {"$lte": query["startDate"]}},
                            {"endDate": {"$gte": query["endDate"]}}]
                        }]
                }]}
            ).limit(limit)))

def fetch_halls(idx: int, response: list, query: dict) -> list:
    # @elapsed_time
    # @delay_time
    def inner_fetch_halls():
        doc = get_doc(query)
        query["avalaibleHalls"] = []
        occupied = set()
        for en in doc:
            occupied.add(en["hallName"])
        for k,v in capacity.items():
            if v < int(query["capacity"]) or k in occupied:
                continue
            else:
                query["avalaibleHalls"] += k,
        response[idx] = query
    
    connect()
    inner_fetch_halls()
    
def book_hall(idx: int, response: list, query: dict) -> list:
    def helper(query: dict, hall_id: str) -> bool:
        if hall_id not in capacity:
            return False
        if capacity[hall_id] < int(query["capacity"]):
            return False
        doc = get_doc(query, hall_id, 1)
        return False if doc else True
    
    # @elapsed_time
    # @delay_time
    def inner_book_hall():
        hall_id = query["hallName"]
        if hall_id:
            status = helper(query, hall_id)
        else:
            for hall_id in capacity:
                status = helper(query, hall_id)
                if status: break
        if status:
            query["hallName"] = hall_id
            bookings.insert_one(query)
            query["status"] = 'Succesfull'
        else:
            query["status"] = 'Failed'
        response[idx] = query
    connect()
    inner_book_hall()

def fetch_booking(data: dict) -> list:
    connect()
    response = []
    doc = iter(bookings.find({"startDate" : data["startDate"]}))
    for query in doc:
        query.pop("_id")
        response += query,
    return response

if __name__ == '__main__':
    connect()
    print( fetch_halls([{"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 15:29:00", "capacity":"100"}]) )
    
    print( book_hall([{"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 21:30:00", "capacity":"100", "hallName":"Hall C"}] ))