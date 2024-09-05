from ass1.ErrorInjection import *
from ass2.Sender import *

with open("ass2/data.txt") as f:
    while True:
        data=f.readline()
        if not data:
            break
        print(data)
        data=framing(data,0)
        print(insertError(data,3))