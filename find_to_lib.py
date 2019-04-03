posib = list(filter((lambda x:'{}'.format(name) in x ), dir(module))
print(posib if posib != [] else "module not exist")
