import matplotlib
import matplotlib.pyplot as plt

filename = "ppm_compression.txt"

with open(filename, "r") as file:
    lines = file.readlines()


x_ind = []
y_ind = []
sum = 0
last_size = 0
last_size_location = 0
skipped = 1


for l in lines[:-1]:
    line_xy = l[:-1].split(",")

    if int(line_xy[1]) != last_size:
        avg = (int(line_xy[1])-last_size)/100*(skipped)
        for i in range(last_size_location, int(line_xy[0])+1, 100):
            x_ind.append(i)
            y_ind.append(avg)
        skipped = 1
        last_size = int(line_xy[1])
        last_size_location = int(line_xy[0])
    else:
        skipped += 1


"""
for l in lines[:-1]:
    line_xy = l[:-1].split(",")
    avg = int(line_xy[1])/int(line_xy[0])
    x_ind.append(int(line_xy[0]))
    y_ind.append(avg)
"""
plt.xlabel("N")
plt.ylabel("Comprimento Médio (ultimos 100 simbolos)")
plt.plot(x_ind, y_ind)
plt.savefig("grafico.png")