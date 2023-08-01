import pandas as pd
from print import *
from Information_Gain import *

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
        select.child.clear()

    return

def classify_test(cu, test_data):

    x_data = test_data.iloc[: , :-1]
    y_data = test_data.iloc[: , -1]

    test_cls = [len(x_data)]

    # for 

    return


def main():

    data = pd.read_csv('restaurant.csv', header = 0)
    root = Node(data)

    learn_decision_tree(root, 0)
    print_feature_class(root)

    prune_tree(root)
    print("after trim")
    print_feature_class(root)


    # pred_data = pd.read_csv('restaurant_predict.csv', header = 0)
    test_data = pd.read_csv('restaurant_test.csv',header = None)
    
    classify_test(root, test_data)




# Calling main function
if __name__=="__main__":    
	main()
