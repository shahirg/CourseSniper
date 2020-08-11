depts = {}
with open('depts.txt','r') as file:
    file_lines = file.readlines()
    for line in file_lines:
        line = line.rstrip('\n')
        depts.update({line[line.index('(')+1:line.index(')')]: line})
    file.close


