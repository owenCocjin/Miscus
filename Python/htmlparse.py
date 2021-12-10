##
## Author:  Owen Cocjin
## Version: 0.4.1
## Date:    2021.12.10
## Description:  Functions for HTML parsing
## Notes:
## Updates:
##  - Increased space options for &nbsp in encodeSpecial
##  - Moved dictionaries out of functions

percent_dict={"%26":'&'}
special_dict={'<':"&lt",
'>':"&gt",
'\n':"</br>",
'\t':"&nbsp&nbsp&nbsp&nbsp",
"    ":"&nbsp&nbsp&nbsp&nbsp",
"        ":"&nbsp&nbsp&nbsp&nbsp"}

def decodePercent(data):
	'''Decode percent encoding.
	Assumes all data passed is valid (ie. percent is followed by 2 digits)'''
	for k in percent_dict:
		if data.find(k)!=-1:
			data=data.replace(k, percent_dict[k])
	return data

def encodeSpecial(data):
	'''Encodes special chars within data'''
	for k in special_dict:
		if data.find(k)!=-1:
			data=data.replace(k, special_dict[k])
	return data
