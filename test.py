import pandas as pd
import math

# Node of a linked list
class Node:
    def __init__(self,data):

        self.selected_feature = ""
        self.data = data
    
        self.child = []
        self.leaf = False
        self.gain = 0

        self.domains = dict()
        self.get_domains(data)
        
        self.p = self.domains['Outputy']['Yes'] if "Yes" in self.domains['Outputy'] else 0
        self.n = self.domains['Outputy']['No'] if "No" in self.domains['Outputy'] else 0

        
    def get_domains(self,data):

        for col_name in data:
            self.domains[col_name] = dict()
            for dt in data[col_name]:

                if dt in self.domains[col_name]:
                    self.domains[col_name][dt] = self.domains[col_name][dt] + 1
                else:
                    self.domains[col_name][dt] = 1

        # print(self.domains)
        

    def generate_childs(self, feature): #chk if leaf
        
        for key in self.domains[feature].keys(): 

            new_data = self.data[self.data[feature] == key].drop(feature, axis=1)  # grouping the new dataset
            new_data.reset_index(inplace=True, drop=True) 

            new_node = Node(new_data)
            (self.child).append(new_node)


            new_node.is_leaf()
        
        return
            
    def is_leaf(self):
        if len(self.domains['Outputy']) == 1:
            self.leaf = True


def print_tree(cu, count):  # take variable that wants to print

    # print("height is ", count)
    print("    |-----"*count, cu.selected_feature, end="")

    if cu.selected_feature == "": print("LEAF")
    else: print('')

    if cu.leaf: return

    for child in cu.child:
        print_tree(child, count + 1)
        
    
    return

def print_datas(cu, count):  # take variable that wants to print

    print("Selected Feature: ", cu.selected_feature, end="")
    if cu.selected_feature == "": print("[LEAF]"," - Height:(",count,")" )
    else: print(" - Height:(",count,")" )

    print(cu.data, end="\n\n\n")

    if cu.leaf: return

    for child in cu.child:
        print_datas(child, count + 1)
        
    
    return

def Gain(node, feature):

    q = node.p/(node.p+node.n)
    return Entropy(q) - reminder(node, feature)

def Entropy(q):

    # print("entropy")
    # print("q is ", q)

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

    x_data = node.data.drop('Outputy', axis=1) # drop last column
    
    max_gain = 0
    feature = ''
    for col_name in x_data:
        if Gain(node, col_name) > max_gain:
            max_gain = Gain(node, col_name) 
            feature = col_name

    node.gain = max_gain
    node.selected_feature = feature


def learn_decision_tree(cu):

    if cu.leaf: return

    if len(cu.domains) == 1:  # check if attributes is empty
        return
        
    select_importance(cu)  ## feature selection

    cu.generate_childs(cu.selected_feature)
    for child in cu.child:
        learn_decision_tree(child)

    return


# def classify(cu, data):

#     if cu.leaf:
#         return cu.domains

#     return

def main():

    data = pd.read_csv('restaurant.csv', header = 0)
    root = Node(data)
    # print(root.data)

    learn_decision_tree(root)
    print_tree(root, 0)
    # print_datas(root, 0)
    print("after pruning")
    # print_tree(root,0)

    p_data = pd.read_csv('restaurant_predict.csv', header = 0)



# Calling main function
if __name__=="__main__":    
	main()
