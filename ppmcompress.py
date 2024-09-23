# 
# Compression application using prediction by partial matching (PPM) with arithmetic coding
# 
# Usage: python ppm-compress.py InputFile OutputFile
# Then use the corresponding ppm-decompress.py application to recreate the original input file.
# Note that both the compressor and decompressor need to use the same PPM context modeling logic.
# The PPM algorithm can be thought of as a powerful generalization of adaptive arithmetic coding.
# 
# Copyright (c) Project Nayuki
# MIT License. See readme file.
# https://www.nayuki.io/page/reference-arithmetic-coding
# 

import contextlib, sys
import arithmeticcoding, ppmmodel
import os


# Must be at least -1 and match ppm-decompress.py. Warning: Exponential memory usage at O(257^n).
MODEL_ORDER = 4


def compress_file(inputfile, outputfile, model=None):
	# Perform file compression
	with open(inputfile, "rb") as inp, \
			contextlib.closing(arithmeticcoding.BitOutputStream(open(outputfile, "wb"))) as bitout:
		return compress(inp, bitout, outputfile, model)


def compress(inp, bitout, outputfile, model=None):
	# Set up encoder and model. In this PPM model, symbol 256 represents EOF;
	# its frequency is 1 in the order -1 context but its frequency
	# is 0 in all other contexts (which have non-negative order).
	enc = arithmeticcoding.ArithmeticEncoder(32, bitout)
	# If no model was provided, create a new one
	if model == None: 
		model = ppmmodel.PpmModel(MODEL_ORDER, 257, 256)
	history = []
	
	n = 0
	with open("ppm_compression.txt", "a") as log:
		while True:
			n += 1
			# Read and encode one byte
			symbol = inp.read(1)
			if len(symbol) == 0:
				break
			symbol = symbol[0]
			encode_symbol(model, history, symbol, enc)
			model.increment_contexts(history, symbol)
			
			if model.model_order >= 1:
				# Prepend current symbol, dropping oldest symbol if necessary
				if len(history) == model.model_order:
					history.pop()
				history.insert(0, symbol)

			
			if n%100 == 0:
				log.write(f"{n},{os.stat(outputfile).st_size}\n")
	
		encode_symbol(model, history, 256, enc)  # EOF
		enc.finish()  # Flush remaining code bits
	

	return model


def encode_symbol(model, history, symbol, enc):
	# Try to use highest order context that exists based on the history suffix, such
	# that the next symbol has non-zero frequency. When symbol 256 is produced at a context
	# at any non-negative order, it means "escape to the next lower order with non-empty
	# context". When symbol 256 is produced at the order -1 context, it means "EOF".
	exclude = []
	for order in reversed(range(len(history) + 1)):
		ctx = model.root_context
		for sym in history[ : order]:
			assert ctx.subcontexts is not None
			ctx = ctx.subcontexts[sym]
			if ctx is None:
				break
		else:  # ctx is not None
			if symbol != 256 and ctx.frequencies.get(symbol) > 0:
				enc.write(ctx.frequencies, symbol, exclude)
				return
			# Else write context escape symbol and continue decrementing the order
			enc.write(ctx.frequencies, 256, exclude)


			# Add symbols to impossible symbols list
			non_zero = ctx.frequencies.list_non_zero()
			for exclude_symbol in range(len(non_zero)-1):
				if exclude_symbol not in exclude and non_zero[exclude_symbol]:
					exclude.append(exclude_symbol)

	# Logic for order = -1
	enc.write(model.order_minus1_freqs, symbol, exclude)



# Main launcher
if __name__ == "__main__":
	main(sys.argv[1 : ])
