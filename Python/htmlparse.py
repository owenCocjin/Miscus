##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.01.04
## Description:  Functions for HTML parsing
## Notes:

def decodePercent(data):
	'''Decode percent encoding.
	Assumes all data passed is valid (ie. percent is followed by 2 digits)'''
	percent_dict={"%26":'&'}
	for k in percent_dict:
		data=data.replace(k, percent_dict[k])
	return k
