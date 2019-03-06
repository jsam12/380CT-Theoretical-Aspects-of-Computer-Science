

# -*- coding: utf-8 -*-
import itertools,random, urllib, re
from datetime import datetime
from HTMLParser import HTMLParser
import copy

num_clause = 5
num_var = 5
num_var_in_clause = 3


def literals_list():
    literals_list = []

    item = itertools.product([1,0], repeat=num_var)
    for i in item:
        # Append as Variables increases.
        temp = []
        temp.append(str(i[0]))
        temp.append(str(i[1]))
        temp.append(str(i[2]))
        temp.append(str(i[3]))
        temp.append(str(i[4]))
        literals_list.append(temp)

    # for i in literals_list:
    #     print(i)
    # print(literals_list)
    return(literals_list)

def generate_cnf():
    cnf_list = []
    for i in range(0, num_clause):
        temp = []
        check_if_not_exist_in_clause = random.randint(0, 1)
        if check_if_not_exist_in_clause == 1:
            # Append as num of var in clause increases.
            rand_int = random.randint(0, num_var_in_clause)
            check_not_position = random.randint(0, 2)
            # Change (0,2) if number of variables in clause increases
            if check_not_position == 0:
                temp.append("~")
                temp.append("")
                temp.append("")
            elif check_not_position == 1:
                temp.append("")
                temp.append("~")
                temp.append("")
            elif check_not_position == 2:
                temp.append("")
                temp.append("")
                temp.append("~")
        else:
            temp.append("")
            temp.append("")
            temp.append("")
        cnf_list.append(temp)

    # print(cnf_list)
    return(cnf_list)



def generate_algo(cnf, literal_list):
    cnf_alpha = copy.deepcopy(cnf)
    # for i in literals_list:
    #     print(i , literals_list[i])

    key_list = []
    for key in literal_list:
        key_list.append(key)
    random.shuffle(key_list)

    # lit = random.randint(0,len(key_list)-1)  
    # print(lit)

    for i in range(0, len(cnf)):
        already_selected = []
        for x in range(0, len(cnf[i])):
            while True:
                lit = random.randint(0,len(key_list)-1)   
                if lit not in already_selected:
                    if cnf[i][x] != "":
                        # it's a NOT
                        cnf_alpha[i][x] = str(cnf_alpha[i][x]) + str(key_list[lit])
                        cnf[i][x] = str(cnf[i][x]) + str(literal_list[key_list[lit]])
                    else: 
                        cnf_alpha[i][x] = str(cnf_alpha[i][x]) + str(key_list[lit])
                        cnf[i][x] = str(cnf[i][x]) + str(literal_list[key_list[lit]])
                    already_selected.append(lit)
                    break
                else:
                    continue
    #         # print(already_selected)
    # Increment as number of clause / variables increases
    print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} )".format(cnf_alpha[0][0],cnf_alpha[0][1], cnf_alpha[0][2], cnf_alpha[1][0], cnf_alpha[1][1], cnf_alpha[1][2], cnf_alpha[2][0], cnf_alpha[2][1], cnf_alpha[2][2], cnf_alpha[3][0], cnf_alpha[3][1], cnf_alpha[3][2], cnf_alpha[4][0], cnf_alpha[4][1], cnf_alpha[4][2] ), " <<<< CNF ALPHA generate_algo()" )    
    print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} )".format(cnf[0][0],cnf[0][1], cnf[0][2], cnf[1][0], cnf[1][1], cnf[1][2], cnf[2][0], cnf[2][1], cnf[2][2], cnf[3][0], cnf[3][1], cnf[3][2], cnf[4][0], cnf[4][1], cnf[4][2] ) , " <<<< CNF BOOLEAN generate_algo()" )
    # print(cnf, " <<< CNF ")
    # print(cnf_alpha , " <<< CNF ALPHA")
    return(cnf_alpha)

def sub_int_into_alpha(cnf_alpha, literals_list):

    for i in range(0, len(cnf_alpha)):

        for x in range(0, len(cnf_alpha[i])):
            x_num = re.search(r"x(\d+)", cnf_alpha[i][x])
            # print(cnf_alpha[i][x])
            if x_num is not None: #Increment as variables increases
                if x_num.group(1) == "1":
                    cnf_alpha[i][x] = re.sub(r"x\d+", str(literals_list["x1"]), str(cnf_alpha[i][x]) )
                if x_num.group(1) == "2":
                    cnf_alpha[i][x] = re.sub(r"x\d+", str(literals_list["x2"]), str(cnf_alpha[i][x]) )
                if x_num.group(1) == "3":
                    cnf_alpha[i][x] = re.sub(r"x\d+", str(literals_list["x3"]), str(cnf_alpha[i][x]) )
                if x_num.group(1) == "4":
                    cnf_alpha[i][x] = re.sub(r"x\d+", str(literals_list["x4"]), str(cnf_alpha[i][x]) )
                if x_num.group(1) == "5":
                    cnf_alpha[i][x] = re.sub(r"x\d+", str(literals_list["x5"]), str(cnf_alpha[i][x]) )

            not_exist = re.search(r"~(\d+)", cnf_alpha[i][x])
            if not_exist is not None: #Increment as variables increases
                if not_exist.group(1) == "1":
                    cnf_alpha[i][x] = re.sub(r"~(\d+)", "0", str(cnf_alpha[i][x]) )
                elif not_exist.group(1) == "0":
                    cnf_alpha[i][x] = re.sub(r"~(\d+)", "1", str(cnf_alpha[i][x]) )
               
    # print(cnf_alpha, " <<< CNF ALPHA")
    return cnf_alpha
        

if __name__ == '__main__':
    start_time = datetime.now()

    literal_list = literals_list()
    # print(literal_list)
    cnf = generate_cnf()
    print("************************************")
    literal_dict = {
        "x1":None,
        "x2":None,
        "x3":None,
        "x4":None,
        "x5":None
    }
    key_list = []
    for i in literal_dict:
        key_list.append(i)

    for i in literal_list:
        cnf_alpha = copy.deepcopy(cnf)

        literal_dict[key_list[0]] = i[0]
        literal_dict[key_list[1]] = i[1]
        literal_dict[key_list[2]] = i[2]
        literal_dict[key_list[3]] = i[3]
        literal_dict[key_list[4]] = i[4]
        for x in literal_dict:
            print(str(x) + " : " + str(literal_dict[x]))
    
        generate_cnf = generate_algo(cnf_alpha, literal_dict)
        algo = sub_int_into_alpha(generate_cnf, literal_dict)
        # print(algo)
        verifier_list = []
        for i in algo:
            verifier = int(i[0]) or int(i[1]) or int(i[2])   # Increase when vareiables in clause increases.
            verifier_list.append(verifier)
        # print(verifier_list)


        sat = verifier_list[0] and verifier_list[1] and verifier_list[2] and verifier_list[3] and verifier_list[4] # Increases when clause increases.

        if sat == 1:
            print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) >>> {}".format(algo[0][0],algo[0][1], algo[0][2], algo[1][0], algo[1][1], algo[1][2], algo[2][0], algo[2][1], algo[2][2], algo[3][0], algo[3][1], algo[3][2], algo[4][0], algo[4][1], algo[4][2] , True) )
        else:    
            print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) >>> {}".format(algo[0][0],algo[0][1], algo[0][2], algo[1][0], algo[1][1], algo[1][2], algo[2][0], algo[2][1], algo[2][2], algo[3][0], algo[3][1], algo[3][2], algo[4][0], algo[4][1], algo[4][2] , False) )

        print("*********************************************")

    end_time = datetime.now() #.strftime("%H:%M:%f")
    time_taken = end_time - start_time
    print(time_taken)

    # literals_list = literals_list()
    # random.shuffle(literals_list)
    # print(literals_list)

    # for literal in range(0, len(literals_list)):
    #     print(literals_list[literal]) # << prints out literals used
    #     algo = generate_algo(literals_list, literal)
    #     # print(algo)

    #     verifier_list = []
    #     for i in algo:
    #         verifier = i[0] or i[1] or i[2]
    #         verifier_list.append(verifier)

    #     sat = verifier_list[0] and verifier_list[1] and verifier_list[2]
    #     if sat == 1:
    #         print(True)
    #     else:
    #         print(False)
    #         start_time = datetime.now().strftime("%H:%M:%f")
    #         print("START TIME : " + str(start_time) + " >>> LITERALS : " + str(literals_list[literal]))
    #         while exhaust_search == True:
    #             # Do smtg if false - count time.
    #             # print(literals_list[literal])
    #             algo = generate_algo_new(literals_list[literal])

    #             verifier_list = []
    #             for i in algo:
    #                 verifier = i[0] or i[1] or i[2]
    #                 verifier_list.append(verifier)

    #             sat = verifier_list[0] and verifier_list[1] and verifier_list[2]
    #             if sat == 1:
    #                 exhaust_search == False
    #                 print(True)
    #                 break
    #             else:
    #                 continue
    #                 print(False)
    #         end_time = datetime.now().strftime("%H:%M:%f")
    #         print("END TIME : " + str(end_time) + " >>> LITERALS : " + str(literals_list[literal]))
                
                




# # -*- coding: utf-8 -*-
# import itertools,random, urllib
# from datetime import datetime
# from HTMLParser import HTMLParser

# num_clause = 3
# num_var = 5
# num_var_in_clause = 3


# def literals_list():
#     literals_list = []

#     item = itertools.product([1,0], repeat=num_var)
#     for i in item:
#         # Append as Variables increases.
#         temp = []
#         temp.append(str(i[0]))
#         temp.append(str(i[1]))
#         temp.append(str(i[2]))
#         temp.append(str(i[3]))
#         temp.append(str(i[4]))
#         literals_list.append(temp)

#     # for i in literals_list:
#     #     print(i)
#     # print(literals_list)
#     return(literals_list)

# def generate_cnf():
#     cnf_list = []
#     for i in range(0, num_clause):
#         temp = []
#         check_if_not_exist_in_clause = random.randint(0, 1)
#         if check_if_not_exist_in_clause == 1:
#             # Append as num of var in clause increases.
#             rand_int = random.randint(0, num_var_in_clause)
#             check_not_position = random.randint(0, 2)
#             # Change (0,2) if number of variables in clause increases
#             if check_not_position == 0:
#                 temp.append("~")
#                 temp.append("")
#                 temp.append("")
#             elif check_not_position == 1:
#                 temp.append("")
#                 temp.append("~")
#                 temp.append("")
#             elif check_not_position ==2:
#                 temp.append("")
#                 temp.append("")
#                 temp.append("~")
#         else:
#             temp.append("")
#             temp.append("")
#             temp.append("")
#         cnf_list.append(temp)

#     print(cnf_list , " <<< generate_cnf() ")
#     return(cnf_list)

# def generate_algo(cnf, literal):
#     # print(literal , " Hello")
#     random.shuffle(literal)
#     # print(literal , " Hello")
#     # print(cnf, " Hello")
    
#     for i in range(0, len(cnf)):
#         already_selected = []
#         for x in range(0, len(cnf[i])):

#             while True:
#                 lit = random.randint(0,len(literal)-1)   
#                 if lit not in already_selected:
#                     if cnf[i][x] != "":
#                         # it's a NOT
#                         cnf[i][x] = str(cnf[i][x]) + str(literal[lit])
#                     else: 
#                         cnf[i][x] = str(cnf[i][x]) + str(literal[lit])
#                     already_selected.append(lit)
#                     break
#                 else:
#                     continue
#             # print(already_selected)
                
#     # print(cnf, " <<< generate_algo() ")
#     return cnf
        
        


# if __name__ == '__main__':
#     # literals_list = {
#     #     "x1":1,
#     #     "x2":1,
#     #     "x3":0,
#     #     "x4":0,
#     #     "x5":0
#     # }

#     literals_list = literals_list()

#     cnf = generate_cnf()
#     print("************************************")
#     for i in literals_list:
#         algo = generate_algo(cnf, i)
#         print(algo)
#         verifier_list = []
#         for i in algo:
#             verifier = i[0] or i[1] or i[2]
#             verifier_list.append(verifier)

#         sat = verifier_list[0] and verifier_list[1] and verifier_list[2]
#         if sat == 1:
#             print(True)
#         else:
#             print(False)




# import itertools, random

# clauses = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
# random_var = []

# item = itertools.product([1,0], repeat=3)

# for i in random.sample(list(item), 3):
#   x1 = i[0]
#   x2 = i[1]
#   x3 = i[2]
#   temp_list = [x1,x2,x3]
#   random_var.append(temp_list)

# print(random_var)
# verifier_list = []
# for i in random_var:
#   verifier = i[0] or i[1] or i[2]
#   verifier_list.append(verifier)

# sat = verifier_list[0] and verifier_list[1] and verifier_list[2]
# if sat == 1:
#   print(True)
# else:
#   print(False)









# import itertools
# n = 4 
# formula = [[1, -2, 3], [-1, 3], [-3], [2, 3]]

# allorderings = itertools.product ([False, True], repeat = n)

# for potential in allorderings:
#     print ("Initial values:", potential)
#     allclauses = []
#     for clause in formula:
#         curclause = []
#         for item in clause:
#             x = potential[abs (item) - 1]
#             curclause.append (x if item > 0 else not x)
#         cal = any (curclause)
#         allclauses.append (cal)
#     print ("Clauses:", allclauses)
#     formcheck = all (allclauses)
#     print ("This combination works:", formcheck)