def NextFit(blockSize, m, processSize, n):
	allocation = [-1] * n
	j = 0
	t = m-1

	for i in range(n):
		while j < m:
			if blockSize[j] >= processSize[i]:
				allocation[i] = j
				blockSize[j] -= processSize[i]
				t = (j - 1) % m
				break

			if t == j:
				t = (j - 1) % m
				break
			
			j = (j + 1) % m
			
	print("Process No. \t Process Size \t Block no.")
	
	for i in range(n):
		print(" ", i + 1, "\t\t", processSize[i], "\t\t", end = "\t")
  
		if allocation[i] != -1:
			print(allocation[i] + 1)
		else:
			print("Not Allocated.")

if __name__ == '__main__':
	blockSize = [5, 10, 20]
	processSize = [10, 20, 5]
	m = len(blockSize)
	n = len(processSize)

	NextFit(blockSize, m, processSize, n)
