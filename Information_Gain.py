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

    p = node.p
    n = node.n
    sum = 0

    for key in domains[feature].keys():  # iterate through every element in domain
        # print(key)
        pk = nk = 0
        
        for vi in range(len(data[feature])):  # iterate through every rows of current col

            if data.loc[vi, feature] == key and data.loc[vi, 'Outputy'] == 'Yes':
                pk = pk + 1
            elif data.loc[vi, feature] == key and data.loc[vi, 'Outputy'] == 'No':
                nk = nk + 1

        sum = sum + ((pk+nk)/(p+n) * Entropy(pk/(pk+nk)))

    return sum

# select the importance // feature selection
def select_importance(node):

    # x_data = node.data.drop('Outputy', axis=1) # drop last column
    x_data = node.data.iloc[: , :-1]
    
    max_gain = 0
    feature = ''
    for col_name in x_data:
        if Gain(node, col_name) > max_gain:
            max_gain = Gain(node, col_name) 
            feature = col_name

    node.gain = max_gain
    node.selected_feature = feature

