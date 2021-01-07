##
## Author:  Owen Cocjin
## Version: 0.2
## Date:    2021.01.04
## Description:  Functions for HTML parsing
## Notes:
## Updates:
##    - Added encodeSpecials
##    - Added an if check which should make encode/decoders more efficient(?)

def decodePercent(data):
	'''Decode percent encoding.
	Assumes all data passed is valid (ie. percent is followed by 2 digits)'''
	percent_dict={"%26":'&'}
	for k in percent_dict:
		if data.find(k)!=-1:
			data=data.replace(k, percent_dict[k])
	return data

def encodeSpecials(data):
	'''Encodes special chars within data'''
	special_dict={'<':"&lt",
	'>':"&gt",
	'\n':"</br>"}
	for k in special_dict:
		if data.find(k)!=-1:
			data=data.replace(k, special_dict[k])
	return data
