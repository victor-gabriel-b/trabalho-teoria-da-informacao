# LZWOutputWriter objects manage the output to a single file
class LZWOutputWriter:
    def __init__(self, file) -> None:
        # The buffer and its size in bits
        # We need to keep the size so that we don't lose any 0s on the left (if we just keep the number, they'll disappear and we will never know)
        self.buffer = 0
        self.buffer_size = 0


        # The output file name and output stream
        self.file = file
        self.output_stream = open(file, "wb")

    # Reset buffer and get output stream again if it was closed
    def restart(self):
        self.buffer = 0
        if self.output_stream == None:
            self.output_stream = open(self.file, "wb")
        

    # Gets the character that must written as A NUMBER
    # Adds its binary representation to the buffer
    # Calls write_to_output if we have enough bits
    def write(self, number, number_bit_length):
        #print(number, number_bit_length)      
        assert type(number) == int
        assert number.bit_length() <= number_bit_length

        # Add to buffer and get length of the buffer in bits
        self.buffer = self.buffer << number_bit_length
        self.buffer += number
        self.buffer_size += number_bit_length

        # If we have 8 or more bits, it's time to write to the output
        while self.buffer_size >= 8:
            self.write_byte_to_output()


    def write_byte_to_output(self):
        assert self.buffer_size >= 8

        # Mask will get the smaller 8 bits unless we shift it to the left
        shift = self.buffer_size-8  # Use buffer_size to account for the leading 0s
        bitmask = 0b11111111
        bitmask = bitmask << shift
            
        # Get the byte and write it to the file
        output_byte = (bitmask & self.buffer) >> shift
        self.output_stream.write(output_byte.to_bytes(1, byteorder="little"))

        # Remove byte from buffer
        self.buffer -= output_byte << shift
        self.buffer_size -= 8


    # Write the last byte, even if it's not filled and close the output stream 
    def close(self):
        # Shift left so that the right side is filled with 0s until we have 8 bits
        shift = 8 - self.buffer_size
        self.buffer = self.buffer << shift
        self.buffer_size += shift

        # Write the last byte to the output
        self.write_byte_to_output()
        
        

#saida = LZWOutputWriter("h.txt")
#saida.write(64, 7)
#saida.write(0, 10)
#saida.write(106, 10)
#saida.close()
