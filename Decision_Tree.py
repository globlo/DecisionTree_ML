
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
        self.p = self.domains[str(len(self.data[0])-1)]['Yes'] if "Yes" in self.domains[str(len(self.data[0])-1)].keys() else 0
        self.n = self.domains[str(len(self.data[0])-1)]['No'] if "No" in self.domains[str(len(self.data[0])-1)].keys() else 0

        self.get_class()
    
    def get_class(self):
        self.cls = max(self.domains[str(len(self.data[0])-1)], key=self.domains[str(len(self.data[0])-1)].get)  # classify

        
    def get_domains(self,data):

        self.domains = dict()
        for col in range(len(data[0])):

            col_name = data[0][col]
            self.domains[col_name] = dict()
            
            for row in range(1,len(data)):

                if data[row][col] in self.domains[col_name].keys():
                    self.domains[col_name][data[row][col]]= self.domains[col_name][data[row][col]] + 1
                else:
                    self.domains[col_name][data[row][col]] = 1
        # print(domains)
        

    def generate_childs(self, feature): #chk if leaf

    
        for key in self.domains[feature].keys(): 

            new_data = self.filter_data(key, feature)
            new_node = Node(new_data)
            (self.child).append(new_node)

            new_node.is_leaf()
        
        return
    
    def filter_data(self, key, feature):

        new_data = []
        new_data.append(self.data[0])  # add the attributes

        for row in range(1, len(self.data)):  # grouping by rows 
            if self.data[row][int(feature)] == key:
                new_data.append(self.data[row])


        return new_data
            
    def is_leaf(self):
        if len(self.domains[str(len(self.data[0])-1)]) == 1:
            self.leaf = True

    def is_twig(self):

        if self.leaf or self.height <= 1:
            return False
        
        for child in self.child:
            if not child.leaf:
                return False
            
        return True
 


def learn_decision_tree(cu, height, attributes):

    cu.height = height

    if cu.leaf or len(attributes) <= 0:  
        return 

        
    feature = select_importance(cu, attributes)  ## feature selection
    attributes.remove(feature) # update attributes
        
    cu.generate_childs(cu.selected_feature)

    for child in cu.child:
        learn_decision_tree(child, height+1, attributes)

    return

def prune_tree(cu):

    if cu.leaf:  return 
    
    select = None
    least_gain = 1.1  # since Gain range: 0-1
    for child in cu.child:
        if child.is_twig() and child.gain < least_gain:
            select = child
            least_gain = child.gain
            
        prune_tree(child)

    if select != None:  ## trim the twig

        select.leaf = True
        select.selected_feature = ""
        select.child.clear()

    return

# def classify_test(cu, test_data):

#     x_data = test_data.iloc[: , :-1]
#     y_data = test_data.iloc[: , -1]

#     test_cls = [len(x_data)]

#     # for 

#     return


def main():


    # data = pd.read_csv('restaurant.csv', header = 0)
    data = load_data('restaurant.csv')
    attributes = []
    for i in range(len(data[0]) -1): attributes.append(str(i))  # store attributes 


    root = Node(data)

    learn_decision_tree(root, 0, attributes)
    print_class(root)
    prune_tree(root)
    print_class(root)
    


    
def load_data(filename):
    with open(filename, 'r') as f:
        results = []
        for fr in f:  ## add name in the datas
            data = fr.rstrip('\n').split(',')
        
        cl =[]
        for i in range(len(data)):
            cl.append(str(i))
        results.append(cl)

        f.seek(0)
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