import json
with open("workflow_result_ip_2_layers.json") as f:
    data = json.load(f)
print(data.keys())
for i in data.keys():
    print(i)
    print(data[i].keys())
print("*"*20)
print(data['qcbm-opt-89f98337-b059-437f-81b8-3b025a55c031-2467666868']['qcbm-optimization-results'].keys())
print("*"*20)
print(data['qcbm-opt-89f98337-b059-437f-81b8-3b025a55c031-2467666868']['qcbm-optimization-results'])