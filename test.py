
def load_data():
    with open('test.csv', 'r') as f:
        results = []
        
        for row in f:
                # print(row)
                data = row.split(',')
                for variable in data:
                    # print(variable)
                     
                    results.append(variable)

        # print(results)
    return results
     

def main():
     
    print(load_data())

    



if __name__ == "__main__":
    main()