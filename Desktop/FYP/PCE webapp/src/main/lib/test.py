# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process

# print(fuzz.token_set_ratio('Samsung Galaxy Note 5 Duos', 'Samsung Galaxy Note5 Duos Smart Mobile Phone 4GB 16MP 32GB'))

a = []

def aa():
	# for i in range(3):
	global a
	a = [1, 2]

def pa():
	print(bool(a))

pa()
aa()
pa()
aa()
pa()
