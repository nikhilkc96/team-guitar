import numpy as np
import task2 as t2
import task1 as t1
from bitstring import BitArray


#4 linear indipendent codewords (as columns)
#first 4 rows form the identity matrix 4x4
G = np.array([[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1],
              [1, 1, 0, 1],
              [1, 0, 1, 1],
              [0, 1, 1, 1]])

# H is the parity check matrix
# built starting from G:
#     • last 3 rows of G + Identity 3x3
H = np.array([[1, 1, 0, 1, 1, 0, 0],
              [1, 0, 1, 1, 0, 1, 0],
              [0, 1, 1, 1, 0, 0, 1]])

# look-up table for choosing the coset leader of the syndrome
# computed in a paper using H and all of possible choices of 3 bits [x x x]
coset_leader = np.array([[0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 1],
                         [0, 0, 0, 0, 0, 1, 0],
                         [0, 0, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0],
                         [1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0]])

#all of possible inputs
inputs = ["000", "001", "010", "100",
          "011", "101", "110",
          "111"]

def rand_decoder(y_string):
    #transform the input string to an array
    y = np.array([1 if x == '1' else 0 for x in y_string], dtype='i1')

    print("y: ", y)
    # compute the syndrome of the input (received word)
    syn = np.dot(H, y) % 2
    print("syn: ", syn)

    # convert the syndrome in dec in order to see which coset leader has to be taken
    syn_dec = syn[0] * 4 + syn[1] * 2 + syn[2]
    print("syndec: ", syn_dec)

    # compute the codeword as follow...
    cd = (y + coset_leader[syn_dec]) % 2
    print("codeword: ",cd)

    # if the first bit of codeword is 0 no need to take the complement
    if cd[0] == 0:
        u_hat = cd[1:4]
    else:
        # compute the complement of the bits in positions 2-3-4
        u_hat = ([1, 1, 1] + cd[1:4]) % 2

    # convert array to string and return it
    u_str = ''
    for bit in u_hat:
        u_str += str(bit)

    return u_str

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