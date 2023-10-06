#!/usr/bin/env python3
import random

def generate_random_points(n):
    points = []
    for _ in range(n):
        x = random.randint(0, 100000)  # Adjust the range as needed
        y = random.randint(0, 100000)  # Adjust the range as needed
        points.append((x, y))
    return points

def save_points_to_file(points, filename):
    with open(filename, 'w') as file:
        for x, y in points:
            file.write(f"{x}, {y}\n")

n = 10000000  # You can change this value to generate a different number of points
random_points = generate_random_points(n)
filename = "random_points.txt"  # Change the filename as needed
save_points_to_file(random_points, filename)

