from HuffmanCoding import HuffmanCoding
import os

def main():
	OUTPUT_FREQ_TABLE = True

	gettysburg_txt_path = os.getcwd() + '\\text\\gettysburg.txt' # original text
	gettysburg_bin_path = os.getcwd() + '\\text\\gettysburg.bin' # compressed text

	# create huffman object
	h = HuffmanCoding(gettysburg_txt_path)

	# compress gettysburg text and store the path to the compressed file in output_path
	output_path = h.compress()

	# decompress the compressed gettysburg file
	h.decompress(output_path)

	# print out frquency table and huffman codes for each letter
	if OUTPUT_FREQ_TABLE:
		print('Frequency Table')
		for node in h.og_heap:
			print('%s - %s' % (node.char, node.freq))

	# print out the compression ratio
	og_size = os.stat(gettysburg_txt_path).st_size
	de_size = os.stat(gettysburg_bin_path).st_size
	print('\nCompression Ratio: %.4f' % (og_size/de_size))

if __name__ == '__main__':
	main()
