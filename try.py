
import sys
from string import ascii_lowercase

# generate average frequency map
freqs = [19,7,1,2,4,10,2,2,5,6,1,1,3,2,6,6,2,1,5,5,7,2,1,2,1,2,1]
freqs = {k:v for k,v in zip(' '+ascii_lowercase,freqs)}

def maybeValid(freqs, ciphertext, candidate):
	for c,f in sorted(freqs.items(), key=lambda x:x[1]):
		c_in_pt = [i for i,j in enumerate(candidate) if j==c] # indices of c in candidate
		mapped_c_in_ct = [ciphertext[i] for i in c_in_pt] # ciphertext characters at those indices
		potential_homophones = set(mapped_c_in_ct)
		if len(potential_homophones) > freqs[c]:
			return False
		c_in_ct = [i for i,j in enumerate(ciphertext[:len(candidate)]) if j in potential_homophones]
		mapped_c_in_pt = [candidate[i] for i in c_in_ct]
		print('mapped_c_in_pt', mapped_c_in_pt)
		if len(set(mapped_c_in_pt)) > 1:
			return False
	return True

def decrypt(ciphertext, freqs, dictionary):
	dfs = [""] # depth first search stack
	while len(dfs):
		cur = dfs.pop()
		# print('cur is :', cur)
		for i in dictionary:
			next_candidate = "{}{} ".format(cur,i)
			# print('next_candidate is', next_candidate)
			# print(dictionary)
			# return 
			# print(freqs, ciphertext, next_candidate[:len(ciphertext)], len(ciphertext) )
			# return
			if maybeValid(freqs, ciphertext, next_candidate[:len(ciphertext)]):
				if len(next_candidate) >= len(ciphertext):
					print('next_candidate is',  next_candidate)
					return next_candidate[:len(ciphertext)]
				else: 
					dfs.append(next_candidate)

if __name__ == "__main__":
	# while True:
	#   ciphertext = input("Enter the ciphertext: ")
	#   if ciphertext == "":
	#     break
	#   print("My plaintext guess is:", decrypt(ciphertext.split(','), freqs, dictionary))
	print(sys.argv)
	if len(sys.argv) < 2:
		print("Usage: python decrypt.py dict_file\n")
		print("\tdictfile: path to text file containing dictionary (one word/plaintext per line)")
	else:
		print('1')
		dict_list = []
		with open(sys.argv[1]) as f:
			for l in f:
				dict_list.append(l.rstrip('\n'))
				print('2')
		print('end 2')
		# for l in sys.stdin:
		ciphertext = "39,42,25,47,21,15,54,15,76,0,19,56,76,0,63,16,51,17,2,91,85,85,61,83,32,9,16,0,32,69,49,79,3,31,61,74,104,51,48,18,79,15,72,36,21,74,98,7,2,54,43,21,26,84,98,53,34,7,54,27,33"
		print('3')
		print(decrypt(ciphertext.split(','), freqs, dict_list))