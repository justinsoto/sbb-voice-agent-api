from sbb_server import book_new_appointment

services = book_new_appointment()

# print("Sorting Test:")

# filtered_results = {}

# keywords = ["wash", "set"]
# for service in services:
#   for keyword in keywords:
#     service = service.lower()
#     if keyword in service and service not in filtered_results and "[" not in service:
#       filtered_results[service] = True
#       print(service)

print(services)
print(services[15])