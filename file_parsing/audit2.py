# audit2.py - stub script for output file audits on ADP PSS files. Determine what you'd like to test for and follow the examples
# below to extract specific data points. Ask your ADP rep for the 200-byte layout guide for the locations of additional data 
# elements.

import re
import sys
import struct

payments = {}
current_worker = ''
worker_name = ''
total_pay = 0.0

for line in open(sys.argv[1], 'r'):
	# If we reach a P00000 record we're starting a new worker. print totals and clear counters
	if re.match('^P00000', line):
		if current_worker != '':
			print "Employee ID: %s Name: %s" %(current_worker, worker_name)
			
		current_worker = ''
		
	# Retrieve employee ID from position 45-53 of P00010
	if re.match('^P00010', line):
		fmt = '44x9s' # skip 44 characters, and read the next 9
		fieldstruct = struct.Struct(fmt)
		result = fieldstruct.unpack_from # unpack field
		fields = result(line)
		current_worker = fields[0]
		
	# Retrieve employee name from position 7-47 of P00025
	if re.match('^P00025', line):
		fmt = '6x40s' # skip 6 characters, read the next 40
		fieldstruct = struct.Struct(fmt)
		result = fieldstruct.unpack_from
		fields = result(line)
		worker_name = fields[0]
		
	if re.match('^P01000', line):
		fmt = '109x14s' # skip 109 characters, read the next 14
		fieldstruct = struct.Struct(fmt)
		result = fieldstruct.unpack_from
		fields = result(line)
		total_pay += (long(fields[0]) / 100.0) # add implied decimal place in payment amount
		
# print last employee's name		
print "Employee ID: %s Name: %s" %(current_worker, worker_name)

#print file total_pay
print "Payment total for file: %s"  %total_pay