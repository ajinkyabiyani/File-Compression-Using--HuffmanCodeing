import os
import heapq
import copy

# Huffman Tree Node
class Node:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq

		# children
		self.left = None
		self.right = None

	# compare nodes by frequency
	# min heap requires > operator 
	def __gt__(self, other):
		if other == None or not isinstance(other, Node):
			return -1
		else:
			return self.freq >= other.freq

class HuffmanCoding:
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.encodes = {}
		self.decodes = {}
		self.og_heap = []

	def build_frequency_dict(self, text):
		freq = {}
		for ch in text:
			if not ch in freq:
				freq[ch] = 0
			freq[ch] += 1 
		return freq 

	def build_priority_queue(self, freq):
		for key in freq:
			node = Node(key, freq[key])
			heapq.heappush(self.heap, node)


	def merge_nodes(self):
		while(len(self.heap) > 1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = Node(None, node1.freq + node2.freq)
			merged.left = node1 
			merged.right = node2 

			heapq.heappush(self.heap, merged)

	def recur_make_codes(self, node, currentCode):
		if node == None: return 
		if node.char != None:
			self.encodes[node.char] = currentCode
			self.decodes[currentCode] = node.char
			return
		# going left (0)
		self.recur_make_codes(node.left, currentCode + "0")
		# going right (1)
		self.recur_make_codes(node.right, currentCode + "1")

	def make_codes(self):
		root = heapq.heappop(self.heap)
		currentCode = ""
		self.recur_make_codes(root, currentCode)

	''' COMPRESSION '''

	def get_encoded_text(self, text):
		encoded_text = ""
		for ch in text:
			encoded_text += self.encodes[ch]
		return encoded_text

	def add_padding(self, encodedText):
		''' 
		Adds extra 0's to end of encoded text to ensure 8 bits per byte.
		Padding info put at beginning of encoded text for decompression.
		'''
		padding = 8 - (len(encodedText) % 8)
		for i in range(padding):
			encodedText += "0"

		# convets padding to 8 bit binary
		paddedInfo = "{0:08b}".format(padding)   
		encodedText = paddedInfo + encodedText
		return encodedText


	def get_byte_array(self, paddedText):
		assert len(paddedText) % 8 == 0, "NEED PADDING"

		b = bytearray()
		for i in range(0, len(paddedText), 8):
			byte = paddedText[i:i+8]
			b.append(int(byte, 2))
		return b

	def compress(self):
		file, exten = os.path.splitext(self.path)
		outputPath = file + ".bin"

		with open(self.path, 'r+') as inFile, open(outputPath, 'wb') as outFile:
			# get input text and remove whitespace at beginning/end
			text = inFile.read().rstrip()

			self.freq = self.build_frequency_dict(text)
			self.build_priority_queue(self.freq)

			# Save heap for later output
			self.og_heap = copy.deepcopy(self.heap)

			self.merge_nodes()
			self.make_codes()

			encoded = self.get_encoded_text(text)
			padded = self.add_padding(encoded)

			b = self.get_byte_array(padded)
			outFile.write(bytes(b))

		print("Compressed File")
		return outputPath

	''' DECOMPRESSION '''

	def remove_padding(self, paddedEncodedText):
		# get padding
		paddingInfo = paddedEncodedText[0:8]
		padding = int(paddingInfo, 2)

		# remove padding info
		paddedEncodedText = paddedEncodedText[8:]
		# remove padding
		encodedText = paddedEncodedText[:-1*padding]

		return encodedText

	def decode_text(self, encodedText):
		currentCode = ""
		decodedText = ""

		for bit in encodedText:
			currentCode += bit 
			if currentCode in self.decodes:
				decodedText += self.decodes[currentCode]
				currentCode = ""

		return decodedText

	def decompress(self, path):
		file, ext = os.path.splitext(path)
		outputPath = file + "_decompressed" + ".txt"

		with open(path, 'rb') as inFile, open(outputPath, 'w') as outFile:
			bitString = ""

			byte = inFile.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')

				bitString += bits

				byte = inFile.read(1)

			encodedText = self.remove_padding(bitString)

			decompressedText = self.decode_text(encodedText)

			outFile.write(decompressedText)

		print("DECOMPRESSED FILE")
		return outputPath
