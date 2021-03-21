import numpy as np
import time

ch = np.array([0, 0, 0.4, 0.5, 0.08, 0.02])
pityBorder = 50

def printPityAndUnits(units, pity):
	for i in range(0, 9):
		# pity[1-11, 11-21, etc]
		print("Pity:", pity[i*10+1:(i+1)*10+1])

	print("-------------------------------------------------------------------")

	sum = np.sum(units) / 100.0
	per = np.fromiter(((unit / sum) for unit in units), dtype=np.double, count=units.size)

	print("Units: {}\n%%%%%: {}\n1 and 2 stars exluded\n".format(units[2:], per[2:]))

def calc(units, n, pity):
	if n <= 0:
		return
	
	for i in range(1, n+1):
		# generating units
		for j in range(1, pityBorder + 1):
			if pity[j] >= 1.0E-5:
				for u in range(2, 6):
					units[u] += pity[j] * ch[u]
					
		for j in range(pityBorder + 1, pity.size):
			if pity[j] >= 1.0E-5:
				addedSixStarChance = (j - pityBorder) * 0.02
				
				chance = (ch[5] + addedSixStarChance) * pity[j]
				units[5] += chance
				
				help = (1 - (addedSixStarChance / (1 - ch[5]))) * pity[j]
				
				for u in range(2, 5):
					units[u] += ch[u] * help 
					
		# setting pity
		pnext = 0
	
		for j in range(0, pity.size - 1):
			pj = pnext
			pnext = pity[j+1]
			
			extraPity = 0
				
			if j > pityBorder:
				extraPity = (j - pityBorder) * 0.02
					
			pity[1] += pj * (ch[5] + extraPity)
			pity[j+1]  = pj * (ch[2] + ch[3] + ch[4] - extraPity)	
		
		if pnext != 0:
			print(i, ":", pnext)
		pity[1] += pnext

e = "n"
while e == "n" or e == "N":
	units = np.zeros_like(ch)
	pity = np.zeros([101], dtype=np.double)
	pity[1] = 1 
	
	np.set_printoptions(precision=5)
	np.set_printoptions(suppress=True)
	np.set_printoptions(linewidth=120)

	print("CH: ", ch)
	print("UN: ", units)

	print("\n-----------------------------\n")
	n = int(input("Number of rolls: ")) # num of rolls

	print("N:", n)
	print("Pity:", pity[1:21])
	print("-------------------------------------------------------------------")

	start = time.time()
	calc(units, n, pity)
	end = time.time()
	printPityAndUnits(units, pity)

	print("Time: {} | Lmao, doing it w/o the profiler using time lib, what a loser.".format(end-start))

	e = input("Enter n or N to do another sim: ")

'''
def calc(units, n, pity):
	if n <= 0:
		return
	
	for i in range(1, n+1):
		# generating units
		for j in range(1, pityBorder + 1):
			if pity[j] >= 1.0E-5:
				for u in range(2, 6):
					units[u] += pity[j] * ch[u]
					
		for j in range(pityBorder + 1, pity.size):
			if pity[j] >= 1.0E-5:
				chance = (ch[5] + 0.02 * (j - pityBorder)) * pity[j]
				units[5] += chance
				
				help = (1 - ch[5] - (j - pityBorder) * 0.02) / (1 - ch[5])
				
				for u in range(2, 5):
					chance = ch[u] * help * pity[j]
					units[u] += chance
					
		# setting pity
		pnext = 0

		for j in range(0, pity.size - 1):
			pj = pnext
			pnext = pity[j+1]
				
			if j <= pityBorder:
				pity[j+1] = pj
			else:
				extraPity = (j - pityBorder) * 0.02
					
				pity[1] += pj * (ch[5] + extraPity)
				pity[j+1]  = pj * (ch[2] + ch[3] + ch[4] - extraPity)
		
		if pnext != 0:
			print(i, ":", pnext)
		pity[1] += pnext
		'''

'''After pity comes into play, how much does that decrease the chances of other rarities? Is it proportional? 
Eg. We get to 4% chance of a 6\*. What is now the chance of a 5\*?
Is it 8% / 98 * 96 ? Did the devs disclose this somewhere?'''