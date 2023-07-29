
class Node:
	def __init__(self, data = None):
		self.key = data
		self.child = []


def importdata():
	balance_data = pd.read_csv('restaurant.csv', header = 0)
	
	# Printing the dataswet shape
	print ("Dataset Length: ", len(balance_data))
	print ("Dataset Shape: ", balance_data.shape)
	
	# Printing the dataset obseravtions
	print ("Dataset: ",balance_data.head())
	return balance_data

# Function to split the dataset
def splitdataset(balance_data):

	# Separating the target variable
	X = balance_data.values[:, 1:5]
	Y = balance_data.values[:, 0]

	# Splitting the dataset into train and test
	X_train, X_test, y_train, y_test = train_test_split(
	X, Y, test_size = 0.3, random_state = 100)
	
	return X, Y, X_train, X_test, y_train, y_test
	
	
# Function to perform training with entropy.
def tarin_using_entropy(X_train, X_test, y_train):

	# # Decision tree with entropy
	# clf_entropy = DecisionTreeClassifier(
	# 		criterion = "entropy", random_state = 100,
	# 		max_depth = 3, min_samples_leaf = 5)

	# # Performing training
	# clf_entropy.fit(X_train, y_train)
	# return clf_entropy
    return 

range_count = dict()
def get_domain_size(data):
	
    for col_name in data:
        range_count[col_name] = dict()
        for dt in data[col_name]:
            # print(dt,end=' ')
            
            if dt in range_count[col_name]:
                range_count[col_name][dt] = range_count[col_name][dt] + 1
            else:
                range_count[col_name][dt] = 1
    
    print(range_count)



def main():
	
	# Building Phase
	data = importdata()
	X, Y, X_train, X_test, y_train, y_test = splitdataset(data)
	clf_entropy = tarin_using_entropy(X_train, X_test, y_train)
	get_domain_size(data)
	
	# print("Results Using Entropy:")
	# # Prediction using entropy
	# y_pred_entropy = prediction(X_test, clf_entropy)
	# cal_accuracy(y_test, y_pred_entropy)
	
	
        
if __name__ == "__main__":
    main()