import requests
import json

# response = requests.post(
#     "http://localhost:3000/shorten",
#     json={"url": "https://google.com"}
# )
# print("Full response:", response.text)

response = requests.delete(
    "http://localhost:3000/del",
    json = {"url": "2o5dnban"}
)
print("Full response:", response.text)

# response = requests.post(
#      "http://localhost:3000/update",
#     json = {
#         "uuid": "2o5dnban",
#         "url": "https://yahoo.com"
#     }
# )
# print("Full response:", response.text)
