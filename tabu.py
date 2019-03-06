# -*- coding: utf-8 -*-
import itertools,random, urllib, re
from datetime import datetime
from HTMLParser import HTMLParser
import copy 

num_clause = 24
num_var = 5
num_var_in_clause = 3


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
            elif check_not_position ==2:
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
    print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} )".format(cnf[0][0],cnf[0][1], cnf[0][2], cnf[1][0], cnf[1][1], cnf[1][2], cnf[2][0], cnf[2][1], cnf[2][2], cnf[3][0], cnf[3][1], cnf[3][2], cnf[4][0], cnf[4][1], cnf[4][2] ) )
    print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} )".format(cnf_alpha[0][0],cnf_alpha[0][1], cnf_alpha[0][2], cnf_alpha[1][0], cnf_alpha[1][1], cnf_alpha[1][2], cnf_alpha[2][0], cnf_alpha[2][1], cnf_alpha[2][2], cnf_alpha[3][0], cnf_alpha[3][1], cnf_alpha[3][2], cnf_alpha[4][0], cnf_alpha[4][1], cnf_alpha[4][2] ) )      


    
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

    tabu_search = True
    literals_list = {
        "x1":1,
        "x2":1,
        "x3":0,
        "x4":0,
        "x5":0
    }

    key_list = []
    for x in literals_list:
        key_list.append(x)

    cnf = generate_cnf()
    generated_alpha = generate_algo(cnf, literals_list)
    already_changed_variable=[]

    while tabu_search == True:
        generate_cnf = copy.deepcopy(generated_alpha)
        # print(generate_cnf, " <<< GENERATED CNF")
        for y in literals_list:
            print(str(y) + " : " + str(literals_list[y]))
        algo = sub_int_into_alpha(generate_cnf, literals_list)
        # print(algo)
        print("*************************************************")

        verifier_list = []
        for i in algo:
            verifier = int(i[0]) or int(i[1]) or int(i[2]) # Increase when vareiables in clause increases.
            verifier_list.append(verifier)
        # print(verifier_list)


        sat = verifier_list[0] and verifier_list[1] and verifier_list[2] and verifier_list[3] and verifier_list[4] and verifier_list[5] and verifier_list[6] and verifier_list[7] and verifier_list[8] and verifier_list[9] and verifier_list[10] and verifier_list[11] and verifier_list[12] and verifier_list[13] and verifier_list[14] and verifier_list[15] and verifier_list[16] and verifier_list[17] and verifier_list[18] and verifier_list[19] and verifier_list[20] and verifier_list[21] and verifier_list[22] and verifier_list[23] # Increases as clause increases
        if sat == 1:
            print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) >>> {}".format(algo[0][0],algo[0][1], algo[0][2], algo[1][0], algo[1][1], algo[1][2], algo[2][0], algo[2][1], algo[2][2] , algo[3][0] , algo[3][1] , algo[3][2] , algo[4][0] , algo[4][1] , algo[4][2] , True) )
            tabu_search = False

        else:    
            print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) >>> {}".format(algo[0][0],algo[0][1], algo[0][2], algo[1][0], algo[1][1], algo[1][2], algo[2][0], algo[2][1], algo[2][2], algo[3][0], algo[3][1], algo[3][2], algo[4][0], algo[4][1], algo[4][2] , False) )
            tabu_search = True

            for x in key_list:
                if x not in already_changed_variable:
                    if literals_list[x] == 1:
                        literals_list[x] = 0
                    else:
                        literals_list[x] = 1
                    already_changed_variable.append(x)
                    break
                else:
                    if literals_list[x] == 1:
                        literals_list[x] = 0
                    else:
                        literals_list[x] = 1
                    continue
            # print(literals_list)
        print("*************************************************")

    end_time = datetime.now()
    time_taken = end_time - start_time
    # time_taken = time_taken.strftime("%H:%M:%f")
    print(time_taken)




    # print(literal_list_alphabet)
    # cnf = generate_cnf()
    # print("************************************")
    # # for i in literals_list:
    # algo = generate_algo(cnf, literal_list_alphabet, literal_list_boolean)
    # print("************************************")


    # while tabu_search == True:
       
    #     for literal in range(0, len(literal_list_boolean)):

    #         if literal_list_boolean[literal] == 0:
    #             literal_list_boolean[literal] == 1
    #         else:
    #             literal_list_boolean[literal] == 0

    #         clause_list = []
    #         for i in range(0, len(algo)):
    #             temp = []
    #             for x in range(0, len(algo[i])):
    #                 if re.search("~", algo[i][x]):
    #                     algo[i][x] = re.search(r"(\d+)", algo[i][x]).group(1).strip()
    #                     if algo[i][x] == "0":
    #                         algo[i][x] = 1
    #                     elif algo[i][x] == "1":
    #                         algo[i][x] = 0
    #                 else:
    #                     algo[i][x]  = re.search(r"(\d+)", algo[i][x]).group(1).strip()
                    
    #                 temp.append(int(algo[i][x]))
    #             clause_list.append(temp)

    #         #Increment as variable increases
    #         print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} )".format(clause_list[0][0],clause_list[0][1], clause_list[0][2], clause_list[1][0], clause_list[1][1], clause_list[1][2], clause_list[2][0], clause_list[2][1], clause_list[2][2] ) )

    #         verifier_list = []
    #         for i in clause_list:
    #             verifier = i[0] or i[1] or i[2] # Increase when vareiables in clause increases.
    #             verifier_list.append(verifier)

    #         print(verifier_list)

    #         print(algo)

    #         sat = verifier_list[0] and verifier_list[1] and verifier_list[2]
    #         if sat == 1:
    #             print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) >>> {}".format(clause_list[0][0],clause_list[0][1], clause_list[0][2], clause_list[1][0], clause_list[1][1], clause_list[1][2], clause_list[2][0], clause_list[2][1], clause_list[2][2] , True) )
    #             tabu_search = False
    #             break
    #         else:    
    #             print("CNF : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) >>> {}".format(clause_list[0][0],clause_list[0][1], clause_list[0][2], clause_list[1][0], clause_list[1][1], clause_list[1][2], clause_list[2][0], clause_list[2][1], clause_list[2][2] , False) )
    #             tabu_search = True

    #             if literal_list_boolean[literal] == 0:
    #                 literal_list_boolean[literal] == 1
    #             else:
    #                 literal_list_boolean[literal] == 0
    #             continue










# # -*- coding: utf-8 -*-
# import itertools,random, urllib, re
# from datetime import datetime
# from HTMLParser import HTMLParser
# import copy


# num_clause = 3
# num_var = 5
# num_var_in_clause = 3

# def generate_cnf():
#     cnf_list = []
#     for i in range(0, num_clause):
#         temp = []
#         check_if_not_exist_in_clause = random.randint(0, 1)
#         if check_if_not_exist_in_clause == 1:
#             check_not_position = random.randint(0, 2)
#             # Change (0,2) if number of variables in clause increases
#             # Increase temp append as variables in clauses increases.
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

#     return(cnf_list)

# def generate_algo_alpha(cnf, literal_alpha):
#     cnf_algo_alpha = cnf
#     # print(literal_alpha , " Hello")
#     random.shuffle(literal_alpha)
#     # print(literal_alpha , " Hello")
#     # print(cnf_algo_alpha, " Hello")
    
#     for i in range(0, len(cnf_algo_alpha)):
#         already_selected = []
#         for x in range(0, len(cnf_algo_alpha[i])):
#             while True:
#                 lit = random.randint(0,len(literal_alpha)-1)   
#                 if lit not in already_selected:
#                     if cnf_algo_alpha[i][x] != "":
#                         # it's a NOT
#                         cnf_algo_alpha[i][x] = str(cnf_algo_alpha[i][x]) + str(literal_alpha[lit])
#                     else: 
#                         cnf_algo_alpha[i][x] = str(cnf_algo_alpha[i][x]) + str(literal_alpha[lit])
#                     already_selected.append(lit)
#                     break
#                 else:
#                     continue
#     already_selected = []
#             # print(already_selected)
#     # Increment as number of clause / variables increases
#     print("CNF VARIABLE : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} )".format(cnf_algo_alpha[0][0],cnf_algo_alpha[0][1], cnf_algo_alpha[0][2], cnf_algo_alpha[1][0], cnf_algo_alpha[1][1], cnf_algo_alpha[1][2], cnf_algo_alpha[2][0], cnf_algo_alpha[2][1], cnf_algo_alpha[2][2] ) )        
#     # print(cnf_algo_alpha)
#     return(cnf_algo_alpha)

# def generate_algo_boolean(cnf, literal_boolean):
#     cnf_algo_boolean = cnf
#     for i in range(0, len(cnf_algo_boolean)):

#         for x in range(0, len(cnf_algo_boolean[i])):
#             x_num = re.search(r"x(\d+)", cnf_algo_boolean[i][x])
#             if x_num is not None: #Increment as variables increases
#                 if x_num.group(1) == "1":
#                     cnf_algo_boolean[i][x] = re.sub(r"x\d+", str(literal_boolean[0]), str(cnf_algo_boolean[i][x]) )
#                 if x_num.group(1) == "2":
#                     cnf_algo_boolean[i][x] = re.sub(r"x\d+", str(literal_boolean[1]), str(cnf_algo_boolean[i][x]) )
#                 if x_num.group(1) == "3":
#                     cnf_algo_boolean[i][x] = re.sub(r"x\d+", str(literal_boolean[2]), str(cnf_algo_boolean[i][x]) )
#                 if x_num.group(1) == "4":
#                     cnf_algo_boolean[i][x] = re.sub(r"x\d+", str(literal_boolean[3]), str(cnf_algo_boolean[i][x]) )
#                 if x_num.group(1) == "5":
#                     cnf_algo_boolean[i][x] = re.sub(r"x\d+", str(literal_boolean[4]), str(cnf_algo_boolean[i][x]) )
                                
#     # print(cnf_algo_boolean)
#     return(cnf_algo_boolean)

# def generate_tabu(algo_alpha_tabu, key, value) :
#     algo_alpha_tabu = algo_alpha_tabu
#     key = key
#     value = value

#     cnf_tabu = []
#     for i in range(0, len(algo_alpha_tabu)):
#         temp = []
#         for x in range(0, len(algo_alpha_tabu)):
#             algo_alpha_tabu[i][x] = re.sub(str(key), str(value), algo_alpha_tabu[i][x])


#     print(algo_alpha_tabu)
#     return(algo_alpha_tabu)


# if __name__ == '__main__':
#     x1 = 0
#     x2 = 1
#     x3 = 1
#     x4 = 0
#     x5 = 0

#     literal_list_boolean = [x1,x2,x3,x4,x5] # Increment as Variables increases
#     literal_list_alphabet = ['x1','x2','x3','x4','x5'] # Increment as Variables increases
#     for i in range(0, len(literal_list_alphabet)):
#         print(str(literal_list_alphabet[i]) + " : " + str(literal_list_boolean[i]))

#     cnf = generate_cnf()

#     cnf_tabu = copy.deepcopy(cnf)

#     # print(cnf)
#     # print(cnf_tabu)
    
#     algo_alpha = generate_algo_alpha(cnf, literal_list_alphabet)
#     print(algo_alpha, " <<< Algo Alpha ") # for display nia
#     algo_alpha_tabu = copy.deepcopy(algo_alpha)
#     print("************************************")
#     algo_boolean = generate_algo_boolean(cnf, literal_list_boolean)
#     print(algo_boolean, " <<< Algo Boolean ") # for display nia
#     algo_boolean_tabu = copy.deepcopy(algo_boolean)
#     print("************************************")

#     clause_list = []
#     for i in range(0, len(algo_alpha)):
#         temp = []
#         for x in range(0, len(algo_alpha[i])):
#             if re.search("~", algo_alpha[i][x]):
#                 algo_alpha[i][x] = re.search(r"(\d+)", algo_alpha[i][x]).group(1).strip()
#                 if algo_alpha[i][x] == "0":
#                     algo_alpha[i][x] = 1
#                 elif algo_alpha[i][x] == "1":
#                     algo_alpha[i][x] = 0
#             else:
#                 algo_alpha[i][x]  = re.search(r"(\d+)", algo_alpha[i][x]).group(1).strip()
            
#             temp.append(int(algo_alpha[i][x]))
#         clause_list.append(temp)

#     #Increment as variable increases
#     print("CNF BOOLEAN : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} )".format(clause_list[0][0],clause_list[0][1], clause_list[0][2], clause_list[1][0], clause_list[1][1], clause_list[1][2], clause_list[2][0], clause_list[2][1], clause_list[2][2] ) )

#     verifier_list = []
#     for i in clause_list:
#         verifier = i[0] or i[1] or i[2] # Increase when vareiables in clause increases.
#         verifier_list.append(verifier)

#     print(verifier_list)



#     # print(algo_alpha)
#     sat = verifier_list[0] and verifier_list[1] and verifier_list[2]
#     if sat == 1:
#         print("CNF BOOLEAN : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) >>> {}".format(clause_list[0][0],clause_list[0][1], clause_list[0][2], clause_list[1][0], clause_list[1][1], clause_list[1][2], clause_list[2][0], clause_list[2][1], clause_list[2][2] , True) )
#         print("************************************")
#     else:
#         print("CNF BOOLEAN : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} ) >>> {}".format(clause_list[0][0],clause_list[0][1], clause_list[0][2], clause_list[1][0], clause_list[1][1], clause_list[1][2], clause_list[2][0], clause_list[2][1], clause_list[2][2] , False) )
#         print("************************************")

#         taboo_search = True

#         reset_literal_list_alphabet = ['x1','x2','x3','x4','x5'] # Increment as Variables increases
#         print(cnf_tabu)
#         print(literal_list_boolean)
#         print(reset_literal_list_alphabet)
#         print(algo_alpha_tabu, "<<< Algo Alpha")
#         print(algo_boolean_tabu,  "<<< Algo Bool")
#         for i in range(0, len(reset_literal_list_alphabet)):
#             print(str(reset_literal_list_alphabet[i]) + " : " + str(literal_list_boolean[i]))

#         # tabu_dict =  {
#         #   "x1": 0,
#         #   "x2": 1,
#         #   "x3": 1,
#         #   "x4" : 0,
#         #   "x5" : 0
#         # }
#         # for i in tabu_dict:

#         #     if tabu_dict[i] == 0:
#         #         changed_tabu = 1
#         #     else:
#         #         changed_tabu = 0

#         clause_list = []
#         for i in range(0, len(algo_alpha_tabu)):
#             temp = []
#             for x in range(0, len(algo_alpha_tabu[i])):
#                 if re.search("~", algo_alpha_tabu[i][x]):
#                     algo_alpha_tabu[i][x] = re.search(r"(\d+)", algo_alpha_tabu[i][x]).group(1).strip()
#                     if algo_alpha_tabu[i][x] == "1":
#                         algo_alpha_tabu[i][x] = x1
#                     elif algo_alpha_tabu[i][x] == "2":
#                         algo_alpha_tabu[i][x] = x2
#                     elif algo_alpha_tabu[i][x] == "3":
#                         algo_alpha_tabu[i][x] = x3
#                     elif algo_alpha_tabu[i][x] == "4":
#                         algo_alpha_tabu[i][x] = x4
#                     elif algo_alpha_tabu[i][x] == "5":
#                         algo_alpha_tabu[i][x] = x5
#                 else:
#                     algo_alpha_tabu[i][x]  = re.search(r"(\d+)", algo_alpha_tabu[i][x]).group(1).strip()
#                     if algo_alpha_tabu[i][x] == "1":
#                         algo_alpha_tabu[i][x] = x1
#                     elif algo_alpha_tabu[i][x] == "2":
#                         algo_alpha_tabu[i][x] = x2
#                     elif algo_alpha_tabu[i][x] == "3":
#                         algo_alpha_tabu[i][x] = x3
#                     elif algo_alpha_tabu[i][x] == "4":
#                         algo_alpha_tabu[i][x] = x4
#                     elif algo_alpha_tabu[i][x] == "5":
#                         algo_alpha_tabu[i][x] = x5
                
#                 temp.append(int(algo_alpha_tabu[i][x]))
#             clause_list.append(temp)

#         print(algo_alpha_tabu)
#         #Increment as variable increases
#         print("CNF BOOLEAN : ( {} or {} or {} ) and ( {} or {} or {} ) and ( {} or {} or {} )".format(clause_list[0][0],clause_list[0][1], clause_list[0][2], clause_list[1][0], clause_list[1][1], clause_list[1][2], clause_list[2][0], clause_list[2][1], clause_list[2][2] ) )

#         verifier_list = []
#         for i in clause_list:
#             verifier = i[0] or i[1] or i[2] # Increase when vareiables in clause increases.
#             verifier_list.append(verifier)

#         print(verifier_list)




#             # if tabu_dict[i] == 0:
#             #     changed_tabu = 1
#             # else:
#             #     changed_tabu = 0

#             # print(algo_alpha_tabu)

            




        
