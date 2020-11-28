import numpy as np
import task2 as t2
import task1 as t1
from bitstring import BitArray

#all of possible inputs
inputs = ["000", "001", "010", "100",
          "011", "101", "110",
          "111"]

#codewords
X = ["0000000", "1000110", "0100101", "0010011", "0001111", "1100011", "1010101", "1001001",
"0110110", "0101010", "0011100", "1110000", "1101100", "1011010", "0111001", "1111111"]


def rand_decoder(y_string):
    u_hat=""

    #Check for the hamming distance for each codeword in X' and
    #sets x_hat as the codeword with the minimum hamming distance
    index = -1
    minHammingDistance = 8
    for i in range(0, len(X)):
        localHammingDistance = 0
        for ch1, ch2 in zip(X[i], y_string):
            if(ch1 != ch2 ):
                localHammingDistance += 1
        if(localHammingDistance < minHammingDistance):
            minHammingDistance = localHammingDistance
            index = i

    x_hat = X[index]

    #Retrieve the u_hat from the codeword and change the bits
    #if the first one is 1
    if(x_hat[0] == "0"):
        u_hat = x_hat[1:4]
    else:
        for ch in x_hat[1:4]:
            if(ch == "0"):
                u_hat += "1"
            else:
                u_hat += "0"

    return u_hat

if __name__ == "__main__":
    errors1 = 0
    errors2 = 0
    #I try my decoder for very possible input encoded by my encoder (case no error from channel)
    for u in inputs:
        # transform inp to Integer and call the encoder
        u_integer = BitArray(bin=u).uint
        #encode input string
        x = t2.rand_encoder(u_integer)

        u_hat = rand_decoder(x)

        if u != u_hat:
            errors1 += 1

        #compare my decode with input
        print("A : ", u, " B : ", u_hat)

    print("-----LEGITTIMATE CHANNEL-----")
    for u in inputs:
        # transform inp to Integer and call the encoder
        u_integer = BitArray(bin=u).uint
        #encode input string
        x = t2.rand_encoder(u_integer)

        #send message thorught the legittimate channel
        y = bin(t1.legittimate_channel(x))[2:].zfill(7)
        print(y)

        u_hat = rand_decoder(y)

        if u != u_hat:
            errors2 += 1

        #compare my decode with input
        print("A : ", u, " B : ", u_hat)

    print("Error1 ", errors1, "Errors2", errors2)