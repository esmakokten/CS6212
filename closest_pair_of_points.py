#!/usr/bin/env python3
import math
import timeit
import matplotlib.pyplot as plt

# Function to calculate the Euclidean distance between two points
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Function to read n points from the file
# The same set of points is used for the sake of measurements
def read_points_from_file(filename, n):
    points = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[:n]:
            x, y = map(float, line.strip().split(','))
            points.append((x, y))
    return points


# Function to find the closest pair of points using the Divide and Conquer approach
def closest_pair(points):
    n = len(points)
    
    # Base case: If there are fewer than 2 points, return infinity.
    if n <= 1:
        return float('inf'), None, None
    
    # If there are only two points, return their distance and the points themselves
    if n == 2:
        return distance(points[0], points[1]), points[0], points[1]
    
    # The points are sorted by their x-coordinate, select the median as the splitting point.
    mid = n // 2

    # Divide the points into left and right halves
    left_half = points[:mid]
    right_half = points[mid:]
    
    # Recursively find the closest pairs in the left and right halves
    min_dist_left, pair_left1, pair_left2 = closest_pair(left_half)
    min_dist_right, pair_right1, pair_right2 = closest_pair(right_half)
    
    # Find the minimum distance among the two halves
    if min_dist_left < min_dist_right:
        min_dist = min_dist_left
        closest_pair1 = pair_left1
        closest_pair2 = pair_left2
    else:
        min_dist = min_dist_right
        closest_pair1 = pair_right1
        closest_pair2 = pair_right2
    
    # Find the points in the "strip" that may have a closer pair
    strip = [point for point in points if abs(point[0] - points[mid][0]) < min_dist]
    
    # Sort the strip by their y-coordinates
    # Time complexity of sort() is O(n log n) for average and worst cases
    strip.sort(key=lambda x: x[1])
    
    # Check for closer pairs in the strip
    for i in range(len(strip)):
        # There can only be maximum of 6 points should be checked
        for j in range(i+1, min(i+7, len(strip))): 
            dist = distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair1 = strip[i]
                closest_pair2 = strip[j]
    
    return min_dist, closest_pair1, closest_pair2

# This function finds closest pair brute force, It is only used to verify the DC algorithm
def closest_pair_bruteforce(points):
    n = len(points)
    if n < 2:
        return None, float('inf')
    
    min_distance = float('inf')
    closest_pair = None

    for i in range(n - 1):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            if dist < min_distance:
                min_distance = dist
                closest_pair = (points[i], points[j])

    return closest_pair, min_distance


if __name__ == "__main__":

    filename = "random_points.txt"  # Replace with the actual filename
    # Specify the array of number of points you want to read
    max_n = 100000  # Maximum value of n
    step = 5000 # Step size for n
    n_values = range(0, max_n+1, step)  # Generate dynamic n values
    #n_values = [1,10,100,1000,10000,100000]

    execution_times = []
    theoretical_times = []
    linear_times = []
    print(f"| n           | execution_time | theoretical_time ")
    
    for n in n_values:
        if n == 0 :
            n=1
        # Call the function to read the points from the file
        points = read_points_from_file(filename, n)
        sorted_points = sorted(points, key=lambda x: x[0])

        execution_time = timeit.timeit(lambda: closest_pair(sorted_points), number=1)
        execution_times.append(execution_time)

        theoretical_time = n * math.log(n,2) / 1400000  # O(n log n) in microseconds
        theoretical_times.append(theoretical_time)

        linear_time = n / 1400000  # O(n log n) in microseconds
        linear_times.append(linear_time)


        print(f"| {n}       | {execution_time:.6f}       | {theoretical_time:.6f} ")


    #Create a graph
    plt.plot(n_values, execution_times, marker='o', linestyle='-', label='Actual Execution Time')
    plt.plot(n_values, theoretical_times, marker='x', linestyle='--', label='Theoretical O(n log n)')
    plt.plot(n_values, linear_times, marker='*', linestyle='--', label='Theoretical O(n)')
    plt.xlabel('Number of Points (n)')
    plt.ylabel('Time (microseconds)')
    plt.title('Execution Time vs. Theoretical Complexity')
    plt.legend()
    plt.grid(True)
    plt.show()