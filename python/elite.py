

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
        return last_numnber

    def word_cases(case, list_with_values):
        if case == 'C':
           del ops[-1]
           del ops[-1]
        if case == 'D':
            last_value = find_first_number_in_list(list_with_values)
            return int(last_value) * 2
        elif case == '+':
                pass

        else:
           if  case.isdigit():
            return case
        #     print(case)
        #     list_with_values.pop()
        #     if(list_with_values[-1].isdigit()):
        #         return  int(list_with_values[-2]) + int(list_with_values[-1])
    
    val=  []
    for value in ops:

        value = word_cases(value, ops)
        print(value)
    print(ops)


calPoints(["5","2",'C', 'D', '+'])

# calPoints(["5","-2","4",'C','D', '9',
#  '+', '+'])
