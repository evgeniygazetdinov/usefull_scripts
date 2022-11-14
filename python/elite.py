

def calPoints(ops):
    def negativeNumber(x):
        neg = x * (-1)
        return neg

    def find_first_number_in_list(list_with_number):
        counter = 1
        isnumber = False
        last_numnber = None
        while not isnumber:
            if (list_with_number[negativeNumber(counter)]).isdigit():
                isnumber =True
                last_numnber = list_with_number[-abs(counter)]
            counter += 1
        return -abs(counter)

    def word_cases(case, list_with_values):
        if case == 'C':
           list_with_values.remove(case)
           case =  None
        if case == 'D':
            last_index = find_first_number_in_list(list_with_values)
            list_with_values.remove(case)
            case = int(list_with_number[last_index]) * 2
        elif case == '+':
            last_index = find_first_number_in_list(list_with_values)
            prev_last_index = last_index -1
            list_with_values.remove(case)
            return int(list_with_values[last_index]) + int(list_with_values[prev_last_index])
        else:
           if  case.isdigit():
            return case
    
    val=  []
    for value in ops:

        value = word_cases(value, ops)
        print(value)
    print(ops)


calPoints(["5","2",'C', 'D', '+'])

# calPoints(["5","-2","4",'C','D', '9',
#  '+', '+'])
