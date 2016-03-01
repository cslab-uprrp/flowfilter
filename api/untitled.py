d = [[1, 2], [3, 4], 5]

num = 5

for item in d:
	if len(item > 1):
		if num in item:
			print 'yes in'
	else:
		if item == num:
			print 'yes eq'
