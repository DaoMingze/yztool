import json
import re

re.compile(r"\\r\\n  +")

with open("1402详细信息.json", "r", encoding="utf-8") as f:
    a = json.load(f)


b = []
c = []
for x in range(len(a)):
    for y in range(len(a[x])):
        a[x][y] = a[x][y].strip()

with open("test.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(a))
