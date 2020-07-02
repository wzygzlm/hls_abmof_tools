import sys
import os
import ctypes

# This python script convert events along with OF_GT to non-standard AEDAT file.
# The purpose of the result .bin file is used as testbench file on Vivado HLS.
# Every event in the standard AEDAT file consists of two 32bits data, but in this
# format, one event has 3 32bits data. The first and the second 4Byte data is the
# same and the third 4Byte data is the GT data.
POLARITY_SHIFT = 11
POLARITY_MASK = (1 << POLARITY_SHIFT)
POLARITY_Y_ADDR_SHIFT = 22
POLARITY_Y_ADDR_MASK = (511 << POLARITY_Y_ADDR_SHIFT)
POLARITY_X_ADDR_SHIFT = 12
POLARITY_X_ADDR_MASK = (1023 << POLARITY_X_ADDR_SHIFT)

def main():
   filepath = sys.argv[1]

   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

   bag_of_words = {}
   with open(filepath) as fp:
       cnt = 0
       f = open(os.path.splitext(filepath)[0] + '_GT.bin', 'w+b')

       for line in fp:
           print("processing line {}".format(cnt))
           if cnt <= 2:
               print("line {} contents {}".format(cnt, line))
           else:
               lineList = list(map(int, line.split()))
               ts = lineList[0]
               x = lineList[1]
               y = lineList[2]
               pol = lineList[3]
               OFRetValid = lineList[6]
               OF_x = ((lineList[4]))
               OF_x = OF_x + 127   # Make sure it is positive so we can remove sign bit
               OF_y = ((lineList[5]))
               OF_y = OF_y + 127    # Make sure it is positive so we can remove sign bit
               rotateFlg = lineList[7]
               SFASTCorner = lineList[8]
               GT = (SFASTCorner << 24) + (rotateFlg << 23) + (OFRetValid << 16) + ( (OF_y & 0xff) << 8 ) + (OF_x & 0xff)

               address = ((y << POLARITY_Y_ADDR_SHIFT) + (x << POLARITY_X_ADDR_SHIFT)+ (pol << POLARITY_SHIFT))
               addr_arr = address.to_bytes(4, 'big', signed=False)
               addr_bin = bytearray(addr_arr)
               ts_arr = ts.to_bytes(4, 'big')
               ts_bin = bytearray(ts_arr)
               GT_arr = GT.to_bytes(4, 'big')
               GT_bin = bytearray(GT_arr)
               f.write(addr_bin)
               f.write(ts_bin)
               f.write(GT_bin)
               # print("line {} ts {:02x} address {:02x} OF_x {} OF_y {}".format(cnt, ts, address, OF_x, OF_y))
               # print(byte_arr)
           cnt += 1
   f.close()
   print("Convert finished.")

def order_bag_of_words(bag_of_words, desc=False):
   words = [(word, cnt) for word, cnt in bag_of_words.items()]
   return sorted(words, key=lambda x: x[1], reverse=desc)

def record_word_cnt(words, bag_of_words):
    for word in words:
        if word != '':
            if word.lower() in bag_of_words:
                bag_of_words[word.lower()] += 1
            else:
                bag_of_words[word.lower()] = 1

if __name__ == '__main__':
    main()
