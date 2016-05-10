# This file does k-means clustering on a set of data
# Command line arguments: # of clusters, name of file with 2D data points

import random
import sys
from matplotlib import pyplot
import numpy

# Creates a list of 2D points from the file
# Arguments: the name of the file to open
def readFile(fileName):
    inFile = open(fileName, 'r')

    points = list()

    for line in inFile:
        components = line.split()
        # X is first, Y is second
        points.append((int(components[0]), int(components[1])))
    
    inFile.close()
    return points

# Creates a list of mean points for clusters, randomly selected from the data
# Arguments: the number of clusters, the 2D points being clustered    
def initializeClusters(numClusters, points):
    clusterPoints = list()
    random.seed()
    pointIndexes = random.sample(range(len(points)), numClusters)
    
    for i in pointIndexes:
        clusterPoints.append(points[i])
        
    return clusterPoints

# Calculate the squared distance between two 2D points
# Arguments: two tuples containing (X, Y)
def calculateDistance(point1, point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2
    
# Places a point in a cluster
# Arguments: the point to place, and the center locations of the clusters
def placePoint(point, clusterCenters):
    nearestCluster = 0;
    distance = calculateDistance(point, clusterCenters[0])       
    
    for i in range(1, len(clusterCenters)):
        tempDistance = calculateDistance(point, clusterCenters[i])
        if tempDistance < distance:
            nearestCluster = i
            distance = tempDistance
            
    return nearestCluster

# Calculate the center of a cluster
# Arguments: a list of points in the cluster
def clusterCenter(cluster):
    centerX = 0
    centerY = 0
    for i in range(len(cluster)):
        centerX += cluster[i][0]
        centerY += cluster[i][1]
        
    return (centerX / len(cluster), centerY / len(cluster))

# Plot the clusters
# Arguments: a list of lists that contain points in each cluster,
# a list of center points
def plotClusters(clusters, centers):
    colors = ('red', 'orange', 'yellow', 'green', 'blue', 'cyan', 'magenta', 'purple', 'white', 'black')
    for i in range(len(clusters)):
        # Convert to numpy array
        cluster = numpy.array(clusters[i])
        pyplot.plot(cluster[:, 0], cluster[:, 1], 'o', centers[i][0], centers[i][1], '^', color=colors[i % len(colors)])
    pyplot.show()
    
def main():
    # Check the command line arguments
    if len(sys.argv) < 3:
        print("Usage: python Clustering.py numberOfClusters file.txt")
        exit()

    points = readFile(sys.argv[2])
    numClusters = int(sys.argv[1])
    if numClusters > len(points):
        print("Number of clusters must be less than or equal to number of points.")
        exit()
    elif numClusters <= 0:
        print("Number of clusters must be positive.")
        exit()
    
    # Initialize the cluster cetners
    clusterCenters = initializeClusters(numClusters, points)
    
    # Create 2D array for clusters
    clusters = None
    oldClusters = []

    # Keep going until clusters converge
    while oldClusters != clusters:
        oldClusters = clusters

        clusters = []
        for i in range(numClusters):
            clusters.append([])
            
        # Cluster each item
        for i in range(len(points)):
            clusters[placePoint(points[i], clusterCenters)].append(points[i])
        
        # Recalculate cluster centers
        clusterCenters = []
        for cluster in clusters:
            clusterCenters.append(clusterCenter(cluster))
    
    plotClusters(clusters, clusterCenters)

main()
