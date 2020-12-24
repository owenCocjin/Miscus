## Author:  Owen Cocjin
## Version: 0.1
## Date:    2020.12.24
## Description:  Functions for string manipulation
## Notes:
def ctxt(text, colour=39, bg=49):
	'''Add/validate colour to a text. Returns original text on fail'''
	try:
		colour=int(colour)
		bg=int(bg)
		if (30<=colour<=39 or 90<=colour<=97)\
		and (40<=bg<=49 or 100<=bg<=107):
			return f"\033[{colour}m\033[{bg}m{text}\033[0m"
	except:
		return text
