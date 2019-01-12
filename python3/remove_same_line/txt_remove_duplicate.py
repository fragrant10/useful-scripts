# 打开urls.txt去除重复的行，从新写到文件single_urls.txt


single_lines = []
new_file = open('single_urls.txt', 'w')

with open('urls.txt', 'r') as file:
    for line in file:
        if line not in single_lines:
            single_lines.append(line)
            new_file.write(line)
