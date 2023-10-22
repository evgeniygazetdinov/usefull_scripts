s = {}
result = []
with open('city_russian_translated.txt','r') as file1:
    with open('city_russian_not_translated','r') as file2:
        transleted_lines = [d.strip() for d in file1.readlines()]
        not_transleted_lines = [x.strip() for x in file2.readlines()]
        s = dict(zip(transleted_lines, not_transleted_lines))
for key, value in s.items():
    result.append(f'''msgid "{value}"\nmsgstr "{key}"''')
with open("Output.txt", "a+") as text_file:
    for res in result:
        text_file.write('\n')
        text_file.write(res)
        text_file.write('\n')
