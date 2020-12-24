## Author:  Owen Cocjin
## Version: 0.1
## Date:    2020.12.24
## Description:  Functions for string manipulation
## Notes:
def ctxt(text, colour=None):
	'''Add/validate colour to a text. Returns original text on fail'''
	try:
		colour=int(colour)
		return f"\033[{colour}m{text}\033[0m"
	except:
		return text
