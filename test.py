import pandas as pd
import math

# Node of a linked list
class Node:
    def __init__(self,data):

        self.cls =""
        self.selected_feature = ""
        self.data = data
    
        self.child = []
        self.leaf = False
        self.height = 0
        
        self.domains = dict()
        self.get_domains(data)
        
        self.gain = 0
        self.p = self.domains['Outputy']['Yes'] if "Yes" in self.domains['Outputy'] else 0
        self.n = self.domains['Outputy']['No'] if "No" in self.domains['Outputy'] else 0

        self.get_class()
    
    def get_class(self):
        self.cls = max(self.domains['Outputy'], key=self.domains['Outputy'].get)  # classify

        
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

    def is_twig(self):

        if self.leaf or self.height <= 1:
            return False
        
        for child in self.child:
            if not child.leaf:
                return False
            
        return True
    
def print_feature_class(cu):

    if cu.leaf: 
        print("    |-----|"*cu.height, cu.cls)
        return

    print("    |-----|"*cu.height, cu.selected_feature, end="")
    print("( Gain:","{:.2f}".format(cu.gain),")")

    for child in cu.child:
        print_feature_class(child)
        
    
    return




def print_class(cu):  

    # print("height is ", count)
    print("    |-----"*cu.height, cu.cls)

    if cu.leaf: 
        return

    for child in cu.child:
        print_class(child)
        
    
    return

def print_feature(cu):  

    # print("height is ", count)
    print("    |-----"*cu.height, cu.selected_feature, end="")

    if cu.is_twig():
        print("(twig)", end="")
      

    if cu.selected_feature == "": print("LEAF")
    else: print('')

    if cu.leaf: return

    for child in cu.child:
        print_feature(child)
        
    
    return

def print_datas(cu):  # take variable that wants to print

    print("Selected Feature: ", cu.selected_feature, end="")
    if cu.selected_feature == "": print("[LEAF]"," - Height:(",cu.height,")" )
    else: print(" - Height:(",cu.height,")" )

    print(cu.data, end="\n\n\n")

    if cu.leaf: return

    for child in cu.child:
        print_datas(child)   
    
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


def learn_decision_tree(cu, height):

    cu.height = height

    if cu.leaf:  
        return 

    if len(cu.domains) == 1:  # check if attributes is empty
        return
        
    select_importance(cu)  ## feature selection

    cu.generate_childs(cu.selected_feature)
    for child in cu.child:
        learn_decision_tree(child, height+1)

    return

def prune_tree(cu):

    if cu.leaf:  
        # print( "reach to the leaf")
        return 
    
    select = None
    least_gain = 1.1  # since Gain range: 0-1
    for child in cu.child:
        if child.is_twig() and child.gain < least_gain:
            select = child
            least_gain = child.gain
            
        prune_tree(child)

    if select != None:  ## trim the twig
        # print("the selected : ")
        # print(select.selected_feature)
        select.leaf = True
        select.selected_feature = ""

    return


def main():

    data = pd.read_csv('restaurant.csv', header = 0)
    root = Node(data)
    # print(root.data)

    learn_decision_tree(root, 0)
    print_feature(root)
    # print_class(root)
    # print_datas(root)
    prune_tree(root)

    print("after trim")
    print_feature(root)
    # print_class(root)

    print_feature_class(root)


    # p_data = pd.read_csv('restaurant_predict.csv', header = 0)



# Calling main function
if __name__=="__main__":    
	main()
