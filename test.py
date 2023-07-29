import pandas as pd
import math

# Node of a linked list
class Node:
    def __init__(self,data):

        self.data = data
        self.selected_feature = ""
        self.depth = 0
        self.leaf = False
        self.child = []
        self.gain = 0
        self.entropy = 0

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

        print(self.domains)
        

    def generate_childs(self, parent, feature): #generate new data to child nodes
        
        for key in self.domains[feature].keys(): 
            new_data = self.data[self.data[feature] == key].drop(feature, axis=1)  # grouping the new dataset
            new_node = Node(new_data)
            (parent.child).append(new_node)

            print("new_node.data")  
            print(new_data)    
            print("end")   
            new_node.check_if_leaf()
        
        return

    def check_if_leaf(self):
        if len(self.domains['Outputy']) == 1:
            self.leaf = True

def Gain(node, feature):
    # print("gian faeture is ", feature)
    # print(node.p)
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
            if data[feature][vi] == key and data['Outputy'][vi] == 'Yes':
                pk = pk + 1
            elif data[feature][vi] == key and data['Outputy'][vi] == 'No':
                nk = nk + 1

        sum = sum + ((pk+nk)/(p+n) * Entropy(pk/(pk+nk)))

    return sum


# select the importance // feature selection
def select_importance(node):

    x_data = node.data.drop('Outputy', axis=1)
    
    max_gain = 0
    feature = ''
    for col_name in x_data:
        if Gain(node, col_name) > max_gain:
            max_gain = Gain(node, col_name) 
            feature = col_name

    node.gain = max_gain
    node.selected_feature = feature


def learn_decision_tree(cu):

    if cu.leaf:
        print("this is leaf")
        return 
    
    select_importance(cu)
    print("the feature selected: ")
    print(cu.selected_feature)

    return


def main():

    data = pd.read_csv('test.csv', header = 0)

    root = Node(data)
    print(root.data)
    # root.generate_childs(root, 'A2')
    # print(root.child[0].data)

    learn_decision_tree(root)
    # learn_decision_tree(root.child[0])
    # learn_decision_tree(root.child[1])


# Calling main function
if __name__=="__main__":    
	main()
