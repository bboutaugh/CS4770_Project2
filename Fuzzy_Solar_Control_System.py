
import matplotlib.pyplot as plt
from tabulate import tabulate
#Fuzzy Trapezoidal Membership Fuzzifiers
def trapezoidal_member_function(size,lower_a, upper_a, upper_b, lower_b):
        fuzzy_arr = []
        for x in range(size):
            fuzzy_arr.append(max(min((x - lower_a)/(upper_a - lower_a),1,(lower_b - x)/(lower_b - upper_b)),0))
        return fuzzy_arr

#Power Variable Fuzzifiers##--------------------------------------------------------------------------------------------

#Fuzzifier based on a very low range of 0 - 15 mA and a definitively very low range of 0-5
def trapezoidal_power_fuzzifier_low(data):
    fuzzy_val = max(min(1, (25 - data) / 5), 0)
    return fuzzy_val

#Fuzzifier based on a moderate range of 20-35 mA and a definitively moderate range of 25-30
def trapezoidal_power_fuzzifier_moderate(data):
    fuzzy_val = max(min((data - 20) / 5, 1, (45 - data) / 5), 0)
    return fuzzy_val

#Fuzzifier based on a very high range of 40 and beyond mA and a definitively very high range of 55 and beyond
def trapezoidal_power_fuzzifier_high(data):
    fuzzy_val = max(min((data - 40) / 5, 1), 0)
    return fuzzy_val

#Exposure Fuzzifiers##--------------------------------------------------------------------------------------------------

def trapezoidal_exposure_fuzzifier_small(data):
    fuzzy_val = max(min(1, (35 - data) / 5), 0)
    return fuzzy_val


def trapezoidal_exposure_fuzzifier_regular(data):
    fuzzy_val = max(min((data - 30) / 5, 1, (60 - data) / 10), 0)
    return fuzzy_val


def trapezoidal_exposure_fuzzifier_large(data):
    fuzzy_val = max(min((data - 70) / 10, 1), 0)
    return fuzzy_val

#Radius Fuzzifiers##----------------------------------------------------------------------------------------------------

def trapezoidal_radius_fuzzifier_small(data):
    fuzzy_arr = []
    for i in range(len(data)):
        fuzzy_arr.append(max(min(1, (3 - data[i]) / 2), 0))
    return fuzzy_arr


def trapezoidal_radius_fuzzifier_regular(data):
    fuzzy_arr = []
    for i in range(len(data)):
        fuzzy_arr.append(max(min((data[i] - 2) , 1, (6 - data[i]) / 2), 0))
    return fuzzy_arr


def trapezoidal_radius_fuzzifier_large(data):
    fuzzy_arr = []
    for i in range(len(data)):
        fuzzy_arr.append(max(min((data[i] - 8) / 2, 1), 0))
    return fuzzy_arr

#Logical operations##---------------------------------------------------------------------------------------------------

#Conditional AND Function
def intersection(input1, input2):
    return min(input1, input2)


#Conditional OR Function
def union(input1, input2):
    return max(input1, input2)

#Inference System Operations##------------------------------------------------------------------------------------------

#Aggregation Function
def aggregate(arr):
    result = []
    i = 0
    for i in range(len(arr[i])):
        test = []
        for j in range(len(arr)):
            test.append(arr[j][i])
        result.append(max(test))
    return result

#Implication by Lukasiewisc operator
def lukasiewisc_op(input, consequent):
    result = []
    for j in range(len(consequent)):
        result.append(min(1, 1 - input + consequent[j]))
    return result

#Implication by correlation-min operator
def corr_min_op(input, consequent):
    result = []
    for j in range(len(consequent)):
        result.append(min(input, consequent[j]))
    return result

#Implication by correlation-product operator
def corr_product_op(input, consequent):
    result = []
    for j in range(len(consequent)):
        result.append(input * consequent[j])
    return result

#Defuzzification Centroid Function
def find_centroid(fm_arr, data):
    aggregate = 0
    data_sum = 0
    for i in range(len(fm_arr)):
        aggregate += (fm_arr[i] * data[i])
        data_sum += fm_arr[i]
        if data_sum == 0:
            data_sum = 0.1
    centroid = aggregate / data_sum
    return centroid

#conclusion of the inference per the max-min application of the input over the relation
#used for testing purposes
'''def inference(input, relation):
    new_arr = []
    result = []
    for i in range(len(relation)):
        arr = []
        for j in range(len(relation[i])):
            arr.append(min(input[i], relation[i][j]))
        new_arr.append(arr)
    m = 0
    for m in range(len(new_arr[m])):
        arr2 = []
        for n in range(len(new_arr)):
            arr2.append(new_arr[n][m])
        result.append(max(arr2))
    return result'''

def determine_angle(quadrant):
    angles = [0.005, 0.045, 0.09, 0.12, 0.18, 0.225, 0.27, 0.315]
    quadrants = ["east", "northeast","north","northwest","west", "southwest", "south", "southeast"]
    for i in range(len(quadrants)):
        if quadrants[i] == quadrant:
            result = angles[i]
    return result


def rule_execution(input1, input2, consequent, connector, relation_func):
    return relation_func(connector(input1, input2), consequent)

def control_system(power_data, exposure_data, quadrant, connector, relational_func):
    low_power = trapezoidal_power_fuzzifier_low(power_data)
    #print("low power membership: ", low_power)
    moderate_power = trapezoidal_power_fuzzifier_moderate(power_data)
    #print("moderate power membership: ", moderate_power)
    high_power = trapezoidal_power_fuzzifier_high(power_data)
    #print("high power membership: ", high_power)

    small_exposure = trapezoidal_exposure_fuzzifier_small(exposure_data)
    #print("small exposure membership: ", small_exposure)
    regular_exposure = trapezoidal_exposure_fuzzifier_regular(exposure_data)
    #print("regular exposure membership: ", regular_exposure)
    large_exposure = trapezoidal_exposure_fuzzifier_large(exposure_data)
    #print("large exposure membership: ", large_exposure)

    radius_x = [0,1,2,3,4,5,6,7,8,9,10]
    small_radius = trapezoidal_radius_fuzzifier_small(radius_x)
    #print("small radius membership: ", small_radius)
    regular_radius = trapezoidal_radius_fuzzifier_regular(radius_x)
    #print("regular radius membership: ", regular_radius)
    large_radius = trapezoidal_radius_fuzzifier_large(radius_x)
    #print("large radius membership: ", large_radius)

    angle = determine_angle(quadrant)

    result = []
    #if exposure small and power moderate then radius regular
    result.append(rule_execution(small_exposure, moderate_power, regular_radius, connector, relational_func))
    #print("first result: ", result[0])
    #if exposure small and power high then radius regular
    result.append(rule_execution(small_exposure, high_power, regular_radius, union, relational_func))
    #print("second result: ", result[1])
    #if exposure medium and power low then radius small
    result.append(rule_execution(regular_exposure, low_power, small_radius, connector, relational_func))
    #print("third result: ", result[2])
    #if exposure medium and power moderate then radius regular
    result.append(rule_execution(regular_exposure, moderate_power, regular_radius, connector, relational_func))
    #print("fourth result: ", result[3])
    #if exposure medium and power high then radius large
    result.append(rule_execution(regular_exposure, high_power, large_radius, connector, relational_func))
    #if exposure large and power low then radius small
    result.append(rule_execution(large_exposure, low_power, small_radius, union, relational_func))
    #print("sixth result: ", result[5])
    #if exposure large and power moderate then radius regular
    result.append(rule_execution(large_exposure, moderate_power, regular_radius, connector, relational_func))
    #if exposure large and power high then radius large
    result.append(rule_execution(large_exposure, high_power, large_radius, connector, relational_func))
    aggregated_result = aggregate(result)
    #print("final aggregate: ", aggregated_result)
    #final_result = []
    #final_result.append(find_centroid(aggregated_result, radius_x))
    #final_result.append(angle)
    control_result = find_centroid(aggregated_result, radius_x)
    return control_result


if __name__ == '__main__':
    power_readings = [60]
    exposure_readings = [100]

    '''input = [1.0, 0.8, 0.0, 0.0]
    consequent = [0.0, 0.5, 1.0, 0.5, 0.0]

    print("rz = ", lukasiewisc_op(input,consequent))
    print("rcm = ", corr_min_op(input, consequent))
    print("rcp = ", corr_product_op(input, consequent))'''
    control_results = []

    for i in range(0,100,10):
        arr = []
        for j in range(50):
            arr.append(control_system(j, i,"northwest",intersection, corr_product_op))
        control_results.append(arr)
    print(control_results[9])
    plt.plot(control_results[9])
    plt.show()

