import pandas as pd
from print import *
from Information_Gain import *


# Node of a linked list
class Node:
    def __init__(self,data, domains):

        self.cls =""
        self.selected_feature = 0
        self.data = data
    
        self.child = []
        self.leaf = False
        self.height = 0
        
        self.domains = domains
        # self.get_domains(data)
        
        self.gain = 0
        self.p = self.domains[len(self.domains)-1]['Yes'] if "Yes" in self.domains[len(self.domains)-1] else 0
        self.n = self.domains[len(self.domains)-1]['No'] if "No" in self.domains[len(self.domains)-1] else 0

        self.get_class()
    
    def get_class(self):
        self.cls = max(self.domains[len(self.domains)-1], key=self.domains[len(self.domains)-1].get)  # classify

        
    def generate_childs(self, feature, original_domain, attributes): #chk if leaf

        if self.leaf:
            return

        for key in original_domain[feature].keys(): 
            new_data = []
            # print("key is ", key)
            for row in range(len(self.data)):
                colum = []
        
                if self.data[row][feature] == key:   ## group with key = {yes,no}
                    for col in range(len(self.data[0])):
                        if col != feature:    ## skip the feature since its a splitter
                            colum.append(self.data[row][col])

                if len(colum) > 0:
                    new_data.append(colum)
     

            new_domain = get_domains(new_data.copy(), attributes)
            new_node = Node(new_data.copy(), new_domain)
            (self.child).append(new_node)
            # print("((((((((((((((((((((((((((((((((((((((((((  in generate new childs :  new-data is ", new_data)
            new_data.clear()
            
            # print("new domain is ", new_domain)

            new_node.is_leaf()
    
        return
            
    def is_leaf(self):
        if len(self.domains[len(self.domains)-1]) == 1:
            self.leaf = True

    def is_twig(self):

        if self.leaf or self.height <= 1:
            return False
        
        for child in self.child:
            if not child.leaf:
                return False
            
        return True
 
def get_domains(data, attributes):

    # print("len is ",len(data[0]) )
    # print( " in get_domain,    data is : ")
    # for d in data:
    #     print(data)
    #     print("###############################################################################")
    
    domains = dict()
    for col in range(len(data[0])):
        # print( " in get_domain,    col is : ", col)

        refer = attributes[col]

        domains[refer] = dict()

        for row in range(len(data)):

            if data[row][col] in domains[refer].keys():
                domains[refer][data[row][col]]= domains[refer][data[row][col]] + 1
            else:
                domains[refer][data[row][col]] = 1
    # print(domains)

    return domains
       

def learn_decision_tree(cu, height, attributes):

    print("height is ", height)
    # print("selected_featrue", cu.selecteda_feature)

    ######################
    print("Data is : ")
    for d in cu.data:
        print(d)
    ######################

    cu.height = height

    if cu.leaf:  
        return 
    
    if len(attributes) <=0:
        return

    if len(cu.domains) == 1:  # check if attributes is empty
        return
    # print(" err")
    feature = select_importance(cu, attributes, height)  ## feature selection

    # print(" feature is ", feature)
    new_attributes = attributes.copy()
    del new_attributes[feature]
    
    cu.generate_childs(cu.selected_feature, cu.domains, new_attributes)
    count = 0
    for child in cu.child:
        
        # print("new attributes")
        # print(new_attributes)
        print("child count is : ",count)
        
        learn_decision_tree(child, height+1, new_attributes)
        count = count  + 1
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

    
    # data = pd.read_csv('restaurant.csv', header = 0)
    data = load_data('restaurant.csv')
    # print(" after load : ")
    # print(len(data[0])-1)
    attributes = []
    for i in range(len(data[0])):
        attributes.append(i)
    
    # print("attributes")
    # print(attributes)

    domains = get_domains(data, attributes)
    root = Node(data, domains)
 
    print(root.cls)

    learn_decision_tree(root, 0, attributes)
    print_feature_class(root)

    # prune_tree(root)
    # print("after trim")
    # print_feature_class(root)


    # pred_data = pd.read_csv('restaurant_predict.csv', header = 0)
    # test_data = pd.read_csv('restaurant_test.csv',header = None)
    
    # classify_test(root, test_data)


def load_data(filename):
    with open(filename, 'r') as f:
        results = []
        
        for row in f:
                # print(row)
                col = []
                data = row.rstrip('\n').split(',')
                for variable in data:
                    # print(variable)
                     
                    col.append(variable)
                
                results.append(col)

        # print(results)
    return results
     


# Calling main function
if __name__=="__main__":    
	main()
