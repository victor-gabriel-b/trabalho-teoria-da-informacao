# LZWOutputWriter objects manage the output to a single file
class LZWInputReader:
    def __init__(self, file) -> None:
        # The buffer and its size in bits
        # We need to keep the size so that we don't lose any 0s on the left (if we just keep the number, they'll disappear and we will never know)
        self.buffer = 0
        self.buffer_size = 0

        # The output file name and output stream
        self.file = file
        self.input_stream = open(file, "rb")

    # Reset buffer and get output stream again if it was closed
    def restart(self):
        self.buffer = 0
        if self.input_stream == None:
            self.input_stream = open(self.file, "rb")
        
    def read(self, desired_bit_length):
        # Read one byte until we get the desired amount of bits or the file ends
        eof = False
        while self.buffer_size < desired_bit_length and not eof:
            eof = self.read_byte_from_input()

        if eof:
            if self.buffer_size != 0 and self.buffer != 0:
                assert self.buffer_size < desired_bit_length

                bits_needed = desired_bit_length - self.buffer_size
                self.buffer = self.buffer << bits_needed
                self.buffer_size += bits_needed
            else:
                return None

   
        # Get bitmask of size 'desired_bit_length' and shift it to the start
        bitmask = (2**desired_bit_length) - 1 
        shift = self.buffer_size - desired_bit_length
        bitmask = bitmask << shift

        # Apply mask
        input_number = (bitmask & self.buffer)

        # Remove read bits from buffer
        self.buffer -= input_number
        self.buffer_size -= desired_bit_length

        # Shift the number back so it doesn't have extra zeroes on the end
        input_number = input_number >> shift

        #print(input_number, desired_bit_length)
        return input_number


    def read_byte_from_input(self):
        input_byte = self.input_stream.read(1)
        eof = len(input_byte) == 0
        if eof: 
            return True

        # Shift buffer and add byte to the end
        self.buffer = self.buffer << 8
        self.buffer += int.from_bytes(input_byte, "little")
        self.buffer_size += 8

        return False  # If it wasn't EOF, it was a sucessful read


    # Write the last byte, even if it's not filled and close the output stream 
    def close(self):
        self.buffer = 0
        self.buffer_size = 0
        self.input_stream.close()

#saida = LZWInputReader("h.txt")
#print(saida.read(7))
#print(saida.read(10))
#print(saida.read(10))
#print()