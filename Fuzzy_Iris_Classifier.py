from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import random
import math
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
    print(len(random_val))
    return random_val

#centroid initialization
def centroid_update(data, val, fuzzy_num, clusters):
    centroids = []
    data_len = len(data[0])
    for i in range(clusters):
        centroid_vals = []
        for j in range(4):
            x1 = 0
            x2 = 0
            for k in range(len(data)):
                x1 += data[k][j] * (val[i][k] + fuzzy_num)
                x2 += (val[i][k] + fuzzy_num)
            centroid_val = x1 / x2
            centroid_vals.append(centroid_val)
        centroids.append(centroid_vals)
    return centroids

def find_distance(data, centroids):
    result = []
    for i in range(len(data)):
        distance = 0
        distances = []
        for j in range(len(centroids)):
            for k in range(len(data[0])):
                distance += math.pow((data[i][k] - centroids[j][k]),2)
            distances.append(pow(distance,0.5))
        result.append(distances)
    return result

def derive_member_val(distances, fuzzy_num):
    result = []
    for i in range(len(distances)):
        arr = []
        for j in range(len(distances[0])):
            m = 0
            for k in range(len(distances[0])):
                m += (pow(distances[i][j], 2) / pow(distances[i][k], 2))
            val = pow(m, (1/ (fuzzy_num - 1)))
            mem = pow(val, -1)
            arr.append(mem)
        result.append(arr)
    return result

def fcm(data, clusters):
    test_diff = 0.2
    member_val = random_member_init(data, clusters)
    test_val1 = 2
    test_val2 = 0
    while(abs(test_val1 - test_val2) > test_diff):
        test_val1 = member_val[0][0]
        centroids = centroid_update(data, member_val, 0.5, clusters)
        distances = find_distance(data, centroids)
        member_val = derive_member_val(distances, 2)
        test_val2 = member_val[0][0]
    return member_val


if __name__ == '__main__':
    '''d = [[1,3],[2,5],[4,8],[7,9]]
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
    clusters = fcm(iris.data, 3)
    plt.plot(clusters)
    plt.show()