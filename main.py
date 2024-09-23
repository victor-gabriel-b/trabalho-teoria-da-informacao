import ppmcompress, ppmdecompress
from lzwencoder import lzw_encode_file
from lzwdecoder import lzw_decode_file
import time
import pickle





start_time = time.time()
#model = ppmcompress.compress_file("./inputs/dickens", "./outputs/dickens.compress")
#ppmcompress.compress_file("./inputs/curto.txt", "./outputs/curto2.compress", model)
model = lzw_encode_file("./inputs/silesia/dickens", "./outputs/dickens.compress", 21, None)
#print("Trocando arquivo")
#lzw_encode_file("./inputs/silesiafull", "./outputs/silesiafull.compress", 21, None, True)
#print("Trocando arquivo")

# Save model
with open('model.pkl', 'wb') as outp:
    pickle.dump(model, outp, pickle.HIGHEST_PROTOCOL)

# Retrieve model
with open('model.pkl', 'rb') as inp:
    model = pickle.load(inp)

print("--- %s seconds ---" % (time.time() - start_time))

print("DESCOMPRIMINDO")

start_time = time.time()
#model = lzw_decode_file("./outputs/silesiafull.compress", "./outputs/silesiafull.decompressed", 12, None)
#print("Trocando arquivo")
#model = lzw_decode_file("./outputs/mozilla.compress", "./outputs/mozilla.decompressed", 16, model)
#print("Trocando arquivo")

#model = lzw_decode_file( "./outputs/dickens.compress", "./outputs/dickens", 12, None, True)
#print("Trocando arquivo")
#lzw_decode_file( "./outputs/silesiafull.compress", "./outputs/silesiafull.decompressed", 21, None, True)
#model = ppmdecompress.decompress_file("./outputs/dickens.compress", "./outputs/dickens.decompressed")
#ppmdecompress.decompress_file("./outputs/curto2.compress", "./outputs/curto2.txt", model)
print("--- %s seconds ---" % (time.time() - start_time))


