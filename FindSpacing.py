length = int(input("What is the length: " ))

running = True

results = []

while(running):
	width = int(input("What sized width would you like: "))
	if width != ",":
		for x in range(0, length):
			if (length - x) % (x + width) == 0:
				results.append(str(x) + ", " + str(width) + ", " + str((length - x) / (x + width)))
		for result in results:
			print(result)
			results = []
	else:
		running = False

