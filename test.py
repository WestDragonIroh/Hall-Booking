import requests
import json

Base = 'http://127.0.0.1:5000/'

taskID = 'Task-2'
# data = [{"startDate":"02-06-2022 15:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100"}, {"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100"}]

data = [{"startDate":"03-06-2021 13:30:00", "endDate":"04-06-2021 14:30:00", "capacity":"100", "hallName":"Hall B"}, {"startDate":"02-06-2021 13:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100", "hallName":"Hall B"}, {"startDate":"02-06-2021 15:30:00", "endDate":"02-06-2021 16:30:00", "capacity":"100", "hallName":"Hall C"}]


args = {"taskID": taskID, "data": json.dumps(data)}

# response = requests.get(Base + taskID +'/' + json.dumps(data))

response = requests.post(Base, json = args)
print(response.json())