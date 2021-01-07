##
## Author:  Owen Cocjin
## Version: 0.3
## Date:    2021.01.04
## Description:  Functions for HTML parsing
## Notes:
## Updates:
##    - Added &nbsp to encodeSpecial

def decodePercent(data):
	'''Decode percent encoding.
	Assumes all data passed is valid (ie. percent is followed by 2 digits)'''
	percent_dict={"%26":'&'}
	for k in percent_dict:
		if data.find(k)!=-1:
			data=data.replace(k, percent_dict[k])
	return data

def encodeSpecial(data):
	'''Encodes special chars within data'''
	special_dict={'<':"&lt",
	'>':"&gt",
	'\n':"</br>",
	'\t':"&nbsp&nbsp&nbsp&nbsp"}
	for k in special_dict:
		if data.find(k)!=-1:
			data=data.replace(k, special_dict[k])
	return data
