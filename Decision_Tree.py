
from print import *
from Information_Gain import *

# Node of a linked list
class Node:
    def __init__(self,data):

        self.cls =""
        self.selected_feature = ""
        self.decision_branch = ""
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

            new_data = self.group_data(key, feature)
            new_node = Node(new_data)
            new_node.decision_branch = key

            (self.child).append(new_node)

            new_node.is_leaf()
        
        return
    
    def group_data(self, key, feature):  # allows to grouping the data by rows according to the key in domains

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

def get_class(cu, test_row ): # allows to predict the class by reach out to leaf

    if cu.leaf: 
        return cu.cls
    
    # get the cu.selected_feature and chk that feature in the row
    feature = cu.selected_feature  ## str 
    value = test_row[int(feature)]

    cls = ""
    for child_node in cu.child:
        
        if child_node.decision_branch == value:
        #    print("value is ", value)
           cls =  get_class(child_node, test_row)

    return cls

def predict_class(root, test_data):

    predicttion = []

    for row in range(1,len(test_data)):  # iterate through all the rows except the name row

        pred = get_class(root, test_data[row]) 
        # print("================  predicted velue for [",row,"] : ",pred)
        predicttion.append(pred)

    return predicttion

def accuracy(predction, outputy):

    print("prediction: ",predction)
    print("outputy: ",outputy)

    correct = 0
    for i in range(len(outputy)):
        if predction[i] == outputy[i]:
            correct = correct + 1
    return correct/len(outputy)

def main():


    ###########################     restaurant.csv     ##############################
    data, y_data, attributes = load_data('restaurant.csv')
    root = Node(data)

    learn_decision_tree(root, 0, attributes)

    prune_tree(root)
    print_feature(root)
    print_feature_class(root)


    ###########################     restaurant_test.csv      ##############################
    data_test, y_test, test_attributes = load_data('restaurant_test.csv')
    pred__cls_test = predict_class(root, data_test)

    print("Accuracy for : restaurant_test.csv")
    print(accuracy(pred__cls_test, y_test))

    ###########################     restaurant_predict.csv     #############################
    data_pred, y_pred, test_attributes = load_data('restaurant_predict.csv')
    pred__cls_pred = predict_class(root, data_pred)
    print("Predictions for : restaurant_test.csv")
    print(pred__cls_pred)
 






def load_data(filename):
    with open(filename, 'r') as f:
        results = []
        for fr in f:  ## add attribute names in the datas
            data = fr.rstrip('\n').replace(" ", "").split(',')
        
        cl =[]
        for i in range(len(data)):
            cl.append(str(i))
        results.append(cl)

        f.seek(0)
        for row in f:
                # print(row)
                col = []
                data = row.rstrip('\n').replace(" ", "").split(',')
                for variable in data:
                    # print(variable)
                     
                    col.append(variable)
                
                results.append(col)

    y_data = []
    res = [ele[-1:] for ele in results]
    for i in range(1, len(res)):
        y_data.append(res[i][0])

    attributes =[]
    for atbt in range(len(results[0]) -1): attributes.append(str(atbt))  # store attributes for reference

    return results, y_data, attributes
     


# Calling main function
if __name__=="__main__":    
	main()