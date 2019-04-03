
def test_simple_numbers(number):
    exceptions = [3,13,29]
    n = list()
    if number >= 2 :
        for y in range(2,number):
            if not ( number % y ):
                return "{} this not simple digit".format(number)
        if number in exceptions :
            print("exception")
            for exception in exceptions:
                 n.append(number)
                 return n
        else:
            return "{} this simple number".format(number)


if __name__ == "__main__":
    for i in range(50):
        print(test_simple_numbers(i))
