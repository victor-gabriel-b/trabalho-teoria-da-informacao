import matplotlib
import matplotlib.pyplot as plt
from math import log

filename = "logs/lzm24_compression.txt"

with open(filename, "r") as file:
    lines = file.readlines()


x_ind = []
y_ind = []
sum = 0
last_size = 0
last_size_location = 0
skipped = 1

"""
for l in lines[:-1]:
    line_xy = l[:-1].split(",")

    if int(line_xy[1]) != last_size:
        print((int(line_xy[1])-last_size))
        avg = (int(line_xy[1])-last_size)/(100*(skipped))
        for i in range(last_size_location, int(line_xy[0])+1, 100):
            x_ind.append(i)
            y_ind.append(avg)
        skipped = 1
        last_size = int(line_xy[1])
        last_size_location = int(line_xy[0])
    else:
        skipped += 1
"""

last = 0
for l in lines[:-1]:
    line_xy = l[:-1].split(",")
    avg = 8*int(line_xy[1])/int(line_xy[0])
    if int(line_xy[1]) == last:
        continue
    last = int(line_xy[1])
    x_ind.append(int(line_xy[0]))
    y_ind.append(avg)


plt.xlabel("N")
plt.ylabel("Comprimento Médio até N")
plt.plot(x_ind, y_ind)
plt.savefig("grafico.png")