
import random

def randN():
	N = 9
	min = pow(10, N-1)
	max = pow(10, N) - 1
	return random.randint(min, max)