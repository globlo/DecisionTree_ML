import math

def Gain(node, feature):

    q = node.p/(node.p+node.n)
    return Entropy(q) - reminder(node, feature)

def Entropy(q):

    if q == 0 or q == 1: return 0

    return -1 * (q*math.log2(q) + (1-q)*math.log2(1-q))

def reminder(node, feature):  

    data = node.data
    domains = node.domains

    # print(' data is ')
    # for row in data:
    #     print(row)

    # print(' domain is ')
    # print(domains)
    # print(" feature is ", feature)

    p = node.p
    n = node.n
    sum = 0

    for key in domains[feature].keys():  # iterate through every element in domain
        # print(key)
        pk = nk = 0
        
        for vi in range(len(data[feature])):  # iterate through every rows of current col

            # print("vi: ",vi, " feature: ",feature)
            # print(" data: ",data[vi][feature])

            if data[vi][feature] == key and data[vi][len(domains)-1] == 'Yes':
                pk = pk + 1
            elif data[vi][feature] == key and data[vi][len(domains)-1]  == 'No':
                nk = nk + 1

        sum = sum + ((pk+nk)/(p+n) * Entropy(pk/(pk+nk)))

    return sum

# select the importance // feature selection
def select_importance(node, attributes, height):

    print("_--------    IN SELECT IMPORTANT  ----    attributes is ", attributes)
    print(" height is : " , height)

    # print("node selected feature ", node.selected_feature) ## initialy 0

    # x_data = node.data.drop('Outputy', axis=1) # drop last column
    # x_data = node.data[: , :-1]
    x_data = []
    for row in range(len(node.data)):
        colum = []
        for col in range(len(node.data[0])  - 1):
            colum.append(node.data[row][col])

        x_data.append(colum)
    # print("x - data : ")
    # for dt in x_data:
    #     print(dt)
    # print("domain : ")
    # for key, val in node.domains.items():
    #     print(key,": ", val)

    max_gain = 0
    feature = 0
    for col in range(len(x_data[0])):
        # print("col_ is ", col)
        if Gain(node, col) > max_gain:
            max_gain = Gain(node, col) 
            feature = col
    # print("selected feature is Index: ", feature)
    # print("selected feature is ", attributes[feature])
    node.gain = max_gain
    node.selected_feature = attributes[feature]
    # print('selected fearure')
    # print(node.selected_feature)

    # print("eeeeeeee")

    return feature

