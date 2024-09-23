# LZW Encoder
# Name: Aditya Gupta
# ID: 800966229
# ITCS 6114

import sys
from sys import argv
from struct import *
from lzwoutputwriter import LZWOutputWriter
import os


def lzw_encode_file(input_file, output_file, n, dictionary=None, reset_when_full=False):
    # defining the maximum table size           
    maximum_table_size = pow(2,int(n))      

    # Building and initializing the dictionary.

    if dictionary == None:
        dictionary_size = 256
        dictionary = {chr(i): i for i in range(dictionary_size)}
    else:
        dictionary_size = len(dictionary.keys())
    full = False
    string = ""             # The word we are currently trying to write
    output = LZWOutputWriter(output_file)
    log = open("lzm_compression.txt", "w")

    with open(input_file, "rb") as file:
        # iterating through the input symbols.
        # LZW Compression algorithm
        read_byte = file.read(1)
        symbol = chr(int.from_bytes(read_byte))
        counter = 0
        while read_byte:  # Until we reach EOF  
            counter += 1        
            string_plus_symbol = string + symbol # get input symbol.
            if string_plus_symbol in dictionary: 
                string = string_plus_symbol
            else:
                output.write(dictionary[string], (dictionary_size-1).bit_length())
                if(dictionary_size <= maximum_table_size):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                elif reset_when_full:
                    dictionary_size = 256
                    dictionary = {chr(i): i for i in range(dictionary_size)} 
                string = symbol

            if counter%100 == 0:
                pass
                log.write(f"{counter},{os.stat(output_file).st_size}\n")
                                   
            read_byte = file.read(1)
            symbol = chr(int.from_bytes(read_byte))
            
        if string in dictionary:
            output.write(dictionary[string], (dictionary_size-1).bit_length())

    log.close()
    output.close()

    print(list(dictionary.keys())[-1])
    return dictionary

#lzw_encode_file("./inputs/dickens", "saida.txt", 16, True)