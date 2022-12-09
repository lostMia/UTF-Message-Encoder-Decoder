# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
# Encoding - UTF-8 (Text) => UTF-16 (Unreadable Garbage)                      #
# Example: "bored"                                                            #
#                                                                             #
# Bytes: |  1  |  2  |  3  |  4  |  5  |  6  | NOTE: We add a Space, if the   #
#        |-----|-----|-----|-----|-----|-----| string has an odd number of    #
# UTF8   |  b  |  o  |  r  |  e  |  d  |     | characters.                    #
# Int    | 98  | 111 | 114 | 101 | 100 | 32  | ord()                          #
# Hex    | 62  | 6f  | 72  | 65  | 64  | 20  | hex()                          #
# Str    |0x62 |0x6f |0x72 |0x65 |0x64 |0x20 |                                #
#           |_   _|     |_   _|     |_   _|                                   #
#             | |         | |         | |                                     #
# Str    |  0x626f   |  0x7265   |  0x6420   | int()                          #
# Int    |   25199   |   29285   |   25632   | chr()                          #
# UTF16  |    扯     |     牥     |     搠    |                                #
#                                                                             #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
#                                                                             #
# Decoding - UTF-16 (Unreadable Garbage) => UTF-8 (Text)                      #
# Example: "桥汬漠"(hello)                                                     #
#                                                                             #
# Bytes  |  1  |  2  |  3  |  4  |  5  |  6  |                                #
#        |-----|-----|-----|-----|-----|-----|                                #
# UTF16  |    桥     |     汬     |    漠     | ord()                          #
# Int    |   26725   |   27756   |   28448   | hex()                          #
# Str    |  0x6865   |  0x6c6c   |  0x6f20   |                                #
#            _| |_       _| |_       _| |_                                    #
#           |     |     |     |     |     |                                   #
# Hex    | 68  | 65  | 6c  | 6c  | 6f  | 20  |                                #
# Str    |0x68 |0x65 |0x6c |0x6c |0x6f |0x20 | int()                          #
# Int    | 104 | 101 | 108 | 108 | 111 | 32  | chr()                          #
# UTF8   |  h  |  e  |  l  |  l  |  o  |     | NOTE: The last Byte returns    #
#                                              a space, if the input          #
#                                              string has an odd number of    #
#                                              characters.                    #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #


import argparse


def main():
	args = parser()

	if (args.string != None):
		raw = args.string
	elif (args.file != None):
		file = open(args.file, 'r', encoding="utf8")
		raw = file.read()
		file.close()
	else:
		print("No input was detected. Please specify some source using the -s or -f options")
		return

	if (args.decode):
		output = decode(raw)
	else:
		output = encode(raw)

	if (args.output):
		file = open(args.output, 'w', encoding="utf8")
		file.write(output)
		file.close()
	else:
		print(output)


def parser():
	parser = argparse.ArgumentParser()

	textInput = parser.add_mutually_exclusive_group(required=True)
	textInput.add_argument('-s', '--string', type=str, required=False, help="the input in string format") # Input string
	textInput.add_argument('-f', '--file', type=str, required=False, help="the location of a input file") # Input file

	parser.add_argument('-o', '--output', type=str, required=False, help="the location of the output file (Defaults to printing in the console if the option is not present)")
	parser.add_argument('-d', '--decode', action='store_true', required=False, help="decodes the input (Defaults to encoding if the option is not present)")

	args = parser.parse_args()

	return args


def encode(string):
	hexcodes = list()
	output = ""

	for char in string:
		if (char == "\n"):
			hexcodes.append("0a")
		else:
			hexcodes.append(hex(ord(char))[2:4])

	# So input strings with an odd number of chr's dont fry the system
	# Essentially just changes the last Byte to be a space, so as to not compromise the input string
	hexcodes.append("20") 

	for i in range(0, len(hexcodes) - 1, 2):
		output += chr(int(f"0x{hexcodes[i]}{hexcodes[i+1]}", 0))

	return output


def decode(string):
	hexcodes = list()
	output = ""

	for char in string:
		longhex = hex(ord(char))
		length = len(longhex)

		if (length != 5 and length != 6): # If the input char is UTF-8 Encoded simply add it to the output
			hexcodes.append(longhex)
			continue

		if (length == 5): # If the hex() function cut of the leading 0; Example: 0x0aff -> 0xaff
			longhex = longhex[:2] + '0' + longhex[2:] # return the leading 0
		
		hexcodes.append(longhex[:4])
		hexcodes.append("0x" + longhex[4:6])

	for i in range(0, len(hexcodes)):
		output += chr(int(hexcodes[i], 0))

	return output


if __name__ == '__main__':
	main()