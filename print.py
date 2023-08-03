 
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
    # print("   |-----"*cu.height, cu.selected_feature, end="")
    print("           |-----"*cu.height,"(" ,cu.decision_branch,"):" ,cu.selected_feature, end="")

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
