from datetime import datetime

example = '2023-07-17'

test = datetime.strptime(example, '%Y-%m-%d')

print(test)
print(type(test))