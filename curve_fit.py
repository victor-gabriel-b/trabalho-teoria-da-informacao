from scipy.optimize import curve_fit
from math import e, log
import numpy as np

FILENAME = "logs/lzm24_compression.txt"
with open(FILENAME, "r") as file:
    lines = file.readlines()

x_values, y_values = [], []
for line in lines:
    line_xy = line[:-1].split(",")
    x_values.append(int(line_xy[0]))
    y_values.append(int(line_xy[1])*8/(int(line_xy[0])))

minimo = min(x_values)
maximo = max(x_values)
for i in range(len(x_values)):
    x_values[i] = (x_values[i]-(minimo-1))/(maximo-(minimo-1))

def objective(x, a, b, c):
    return (a * (x ** (-b * e)) + c)

popt, _ = curve_fit(objective, x_values, y_values)
print(popt)

print(y_values[-1])