import sys
import json

print("Hello World")

def Verarbeite(Liste):
    print(Liste)
    print(sum(Liste))

# if __name__ == "__main__":
ListStr = sys.argv[1]
List = json.loads(ListStr)
Verarbeite(List)