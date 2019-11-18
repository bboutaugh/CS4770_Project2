from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import copy
#Three expected clusters: Iris Setosa, Iris Versicolor, Iris Virginica
iris = load_iris()
type(iris)


#random initialization of membership values
def random_member_init(data, clusters):
    random_val = []
    for i in range(clusters):
        arr = []
        for j in range(len(data)):
            arr.append(random.random())
        random_val.append(arr)
    print(random_val)
    return random_val

#centroid initialization
def centroid_update(data, val, fuzzy_num, clusters):
    centroids = []
    for i in range(clusters):
        centroid_vals = []
        for j in range(len(data[0])):
            x1 = 0
            x2 = 0
            for k in range(len(val[0])):
                x1 += data[k][j] * (pow(val[i][k], fuzzy_num))
                x2 += pow(val[i][k], fuzzy_num)
            centroid_val = x1 / x2
            centroid_vals.append(centroid_val)
        centroids.append(centroid_vals)
    return centroids

def find_distance(data, centroids):
    result = []
    for i in range(len(data)):
        distances = []
        for j in range(len(centroids)):
            distance = 0
            for k in range(len(data[0])):
                #print(i, ": ", data[i][k], '-', centroids[j][k])
                distance += math.pow((data[i][k] - centroids[j][k]),2)
            distances.append(pow(distance, 0.5))
            #print("after square root: ", pow(distance,0.5))
        result.append(distances)
    return result

def derive_member_val(distances, fuzzy_num):
    result = []
    for i in range(len(distances)):
        arr = []
        for j in range(len(distances[0])):
            m = 0
            for k in range(len(distances[0])):
                if distances[i][k] == 0:
                    distances[i][k] += 0.000000000001
                m += ((pow(distances[i][j], 2)) / (pow(distances[i][k], 2)))
            m = pow(m, (1 / (fuzzy_num - 1)))
            m = pow(m, -1)
            arr.append(m)
        result.append(arr)
    return result

def fcm(data, clusters):
    test_diff = 0.1
    member_val = random_member_init(data, clusters)
    test_val1 = 2
    test_val2 = 0
    for i in range(1):
    #while(abs(test_val1 - test_val2) > test_diff):
        #test_val1 = member_val[0][0]
        centroids = centroid_update(data, member_val, 2, clusters)
        distances = find_distance(data, centroids)
        member_val = derive_member_val(distances, 5)
        #test_val2 = member_val[0][0]
    return member_val

def defuzz(memberships):
    result = []
    for i in range(len(memberships)):
        for j in range(len(memberships[0])):
            if memberships[i][j] == max(memberships[i]):
                result.append(j)
    return result


if __name__ == '__main__':
    print(iris.data)
    ones = []

    for m in range(3):
        arr = []
        for j in range(len(iris.data)):
            arr.append(1.0)
        ones.append(arr)
    #d = [[0, 1], [5, 20], [10, 3]]
    #mems = [[0.7,0.2,0.5],[0.5,0.6,0.1],[0.1,0.2,0.3]]

    '''d = 
    r = [[0.8, 0.7, 0.2, 0.1],[0.2, 0.3, 0.8, 0.9]]
    d2 = [[1,3]]
    c = [[1.568, 4.051],[5.35, 8.215]]
    #print(iris.data)
    r_nums = random_member_init(d, 2)
    print(r_nums)
    arr = centroid_update(d, r, 0.02)
    print(arr)
    centroids = [[1.2, 6.79]]
    print(derive_member_val(centroids, 2))
    print(find_distance(d2,c))'''
    #print(fcm(iris.data, 3))
    data = iris.data
    member_val = random_member_init(data, 3)
    c = [[0, 0.5, 1.0, 2.0], [4.0, 5.0, 6.0, 7.0], [8.0, 9.0, 10.0, 11.0]]
    for i in range(10):
        c = centroid_update(data, member_val, 2, 3)
        distances = find_distance(data, c)
        member_val = derive_member_val(distances, 2)
    results = defuzz(member_val)
    print("centroids: ", c)
    print("distances: ", distances)
    print("membership: ", member_val)
    print ("crisp values: ", results)
    #clusters = fcm(iris.data, 3)
    #print(clusters)
    #results = defuzz(clusters)
    #print(results)
    '''cluster_id = ['cluster1','cluster2','cluster3']
    cluster1: int = results[0]
    cluster2 = results[1]
    cluster3 = results[3]
    cluster_results = [cluster1, cluster2, cluster3]
    plt.scatter(cluster_id, cluster_results)
    plt.show()'''
