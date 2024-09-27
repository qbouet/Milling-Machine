"""
File prints matrix of 1s and 0s to a .txt file in the shape of a house and a stick-figure
Equations for the lines were made in Desmos for easier visualisation and quicker editing
"""
import math

FILE_NAME = "matrix.txt"

# Initialize a 2D matrix with dimensions 70x70, filled with zeros
matrix = []
for row in range(700):
    column = []
    for number in range(700):
        column.append(0)
    matrix.append(column)

# FORMAT EXAMPLE:
# for x in range(start x position, end x position):
#    Equation
#    matrix[y position from top (e.g. 690 is 10 from bottom) - int(y)][x] = 1  # Adjusted row indexing

# First equation: y=x/2+300 {10<x<250}
for x in range(10, 250):
    y = x / 2 + 300
    matrix[500 - int(y)][x] = 1  # Adjusted row indexing

# Second equation: y=-x/2+550 {250<x<490}
for x in range(250, 490):
    y = -x / 2 + 550
    matrix[500 - int(y)][x] = 1

# Third equation: x=50 {0<y<325}
for y in range(425):
    matrix[600 - y][50] = 1

# Fourth equation: x=450 {0<y<325}
for y in range(425):
    matrix[600 - y][450] = 1

# 5th equation: x=150 {0<y<200}
for y in range(160):
    matrix[600 - y][150] = 1

# 6th equation: x=350 {0<y<200}
for y in range(160):
    matrix[600 - y][350] = 1

# 5th equation: y=0 {50<y<450}
for x in range(50, 450):
    y = 100
    matrix[700 - y][x] = 1

# x=250 {160<y<212}
for y in range(158, 212):
    x = 250
    matrix[700 - y][x] = 1

# y=x/3+110 {225<x<250}
for x in range(225, 250):
    y = x / 3 + 110
    matrix[700 - int(y)][x] = 1

# y=-x/1.5+360 {250<x<290}
for x in range(250, 290):
    y = -x / 1.5 + 360
    matrix[700 - int(y)][x] = 1

# y=-x/1.1 + 389.5 {200<x<225}
for x in range(200, 225):
    y = -x / 1.1 + 389.5
    matrix[700 - int(y)][x] = 1

# y=-3x+910 {250<x<270}
for x in range(250, 270):
    y = -3 * x + 910
    matrix[700 - int(y)][x] = 1

# Semi-Circle outline (arch): (x-250)^{2}+(y-200)^{2}=100^{2} {y<=200}
center_x, center_y = 250, 250  # Define the center coordinates
radius = 100
num_points = 700  # Increased number of points for a smoother circle
for point in range(num_points):
    angle = 2 * math.pi * point / num_points  # Calculate angle for the current point in radians
    x = int(center_x + radius * math.cos(angle))  # Calculate x&y coordinates using polar->Cartesian conversion.
    y = int(center_y + radius * math.sin(angle))
    if 0 <= x < 700 and 250 <= y < 700:
        matrix[690 - y][x] = 1

# Circle outline (head): (x-250)^{2}+(y-240)^{2}=28^{2}
center_x, center_y = 250, 240
radius = 28
num_points = 500  # Increased number of points for a smoother circle
for point in range(num_points):
    angle = 2 * math.pi * point / num_points
    x = int(center_x + radius * math.cos(angle))
    y = int(center_y + radius * math.sin(angle))
    if 0 <= x < 700 and 0 <= y < 700:
        matrix[700 - y][x] = 1

# These last two lines (Legs) have a steeper gradient and results in gaps in the line. Therefore, this code fills in the spaces
# with 1s between to two bounds

# y= -3x+910 {250<x<270}
x = 250
yi = 0  # initial y position
yf = -3 * x + 910  # final y position
for x in range(250, 270):
    try:
        yi = yf
        yf = -3 * x + 908
        matrix[700 - yf][x] = 1
        while yi != yf:
            if yi > yf:
                yi += -1
            elif yi < yf:
                yi += 1
            matrix[700 - yi][x] = 1

    except IndexError:
        break

# y= 3x-590 {230<x<250}
x = 230
yi = 0
yf = 3 * x - 590
for x in range(230, 250):
    try:
        yi = yf
        yf = 3 * x - 590
        matrix[700 - yf][x] = 1
        while yi != yf:
            if yi > yf:
                yi += -1
            elif yi < yf:
                yi += 1
            matrix[700 - yi][x] = 1

    except IndexError:
        break

# Open a file for writing and save the matrix data to the file
out_file = open(FILE_NAME, 'w')
for row in matrix:
    for value in row:
        out_file.write(str(value))
        out_file.write(",")
    out_file.write("\n")
out_file.close()
