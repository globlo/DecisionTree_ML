import pandas as pd
import math



# Node of a linked list
class Node:
	def __init__(self, data = None):
		self.key = data
		self.child = []


def importdata():
	balance_data = pd.read_csv('test.csv', header = 0)
        
    
	
	# # Printing the dataswet shape
	# print ("Dataset Length: ", len(balance_data))
	# print ("Dataset Shape: ", balance_data.shape)
	
	# # Printing the dataset obseravtions
	# print ("Dataset: ",balance_data.head())
	return balance_data

range_count = dict()
def get_domain_size(data):
	
    for col_name in data:
        range_count[col_name] = dict()
        for dt in data[col_name]:

            if dt in range_count[col_name]:
                range_count[col_name][dt] = range_count[col_name][dt] + 1
            else:
                range_count[col_name][dt] = 1

    print(range_count)
    global p, n 
    p = range_count['Outputy']['Yes']
    n = range_count['Outputy']['No']

def Gain(Entropy,reminder):
    return Entropy - reminder

def Entropy():

    q = p/(p+n)

    if q == 0: return 0

    return -1 * (q*math.log2(q) + (1-q)*math.log2(1-q))

def reminder(feature_name, data):  
    # p = range_count['Outputy']['Yes']
    # n = range_count['Outputy']['No']

    sum = 0

    for key in range_count[feature_name].keys():  # iterate through every count in domain
        print(key)
        pk = nk = 0

        for vi in range(len(data[feature_name])):  # iterate through every rows of current col
            if data[feature_name][vi] == key and data['Outputy'][vi] == 'Yes':
                pk = pk + 1
            elif data[feature_name][vi] == key and data['Outputy'][vi] == 'No':
                nk = nk + 1

        # print("pk is ",pk)      
        # print("nk is ",nk)    
        sum = sum + ((pk+nk)/(p+n) * Entropy(pk/(pk+nk)))

    return sum

def selected_feature():
    
    for col_name in range_count.keys():
        
        print(col_name)


def main():

    data = importdata()
    get_domain_size(data)

    print("Entropy : ", Entropy())
    

    print("Reminder(A1) : ", reminder('A1',data))
    print("Reminder(A2) : ", reminder('A2',data))
    print("Reminder(A3) : ", reminder('A3',data))
    


	
	
# Calling main function
if __name__=="__main__":    
	main()
