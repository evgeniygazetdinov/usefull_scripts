s = {}
result = []
with open('russian.txt','r') as file1:
    with open('english.txt','r') as file2:
        transleted_lines = [d.split(", ") for d in file1.readlines()]
        not_transleted_lines = [x.split(", ") for x in file2.readlines()]
        s = dict(zip(transleted_lines[0], not_transleted_lines[0]))
print(s)
for key, value in s.items():
    result.append("{" + '"' + value + '"' +':' + '"' +key + '"' +'},')
with open("res.json", "w+") as text_file:
    text_file.write('[')
    for res in result:
        text_file.write('\n')
        text_file.write(res)
        text_file.write('\n')
    text_file.write(']')
