# LZW Decoder
# Name: Aditya Gupta
# ID: 800966229
# ITCS 6114

import sys
from sys import argv
import struct
from struct import *
from lzwinputreader import LZWInputReader


def lzw_decode_file(input_file, output_file, n, dictionary=None, reset_when_full=False):
    # taking the compressed file input and the number of bits from command line
    # defining the maximum table size
    # opening the compressed file
    # defining variables
    maximum_table_size = pow(2,int(n))
    string = ""

    # Building and initializing the dictionary.
    if dictionary == None:
        dictionary_size = 256
        dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])
    else:
        dictionary_size = len(dictionary.keys())
 

    file_input = LZWInputReader(input_file)
    read_value = file_input.read(8)
    counter = 1
    with open(output_file, "wb") as saida:
        while read_value != None:
            if read_value not in dictionary:
                new_string = string + string[0]
            else:
                new_string = dictionary[read_value]

            saida.write(new_string.encode("utf-8"))

            if string != "":
                if(dictionary_size <= maximum_table_size):
                    dictionary[dictionary_size] = string + new_string[0]
                    dictionary_size += 1
                elif reset_when_full:
                    dictionary_size = 257
                    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

            string = new_string
            read_value = file_input.read((dictionary_size).bit_length())
            counter += 1

    return dictionary    
                
#lzw_decode_file("saida.txt", "saida_saida.txt", 16, True)