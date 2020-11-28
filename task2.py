import random as r
from bitstring import BitArray

'''
#possible inputs
inputs = ["000", "001", "010", "100",
          "011", "101", "110",
          "111"]
'''

#codewords
X = ["0000000", "1000110", "0100101", "0010011", "0001111", "1100011", "1010101", "1001001",
"0110110", "0101010", "0011100", "1110000", "1101100", "1011010", "0111001", "1111111"]

def rand_encoder(d):
    # checks if the input is valid
    if 0 <= d < 8:
        # codeword
        u1 = ""
        # complement
        u2 = ""
        # The prefix of the codeword
        prefix = "0" + bin(d)[2:].zfill(3)
        #print("Message: ", prefix[1:])
        # checks which codeword starts with the prefix and gets it
        for x in X:
            if x.startswith(prefix):
                u1 = x
                break
        # Calculates the complment of the binary given as input
        for i in u1:
            if i == "1":
                u2 += "0"
            else:
                u2 += "1"
        print("Possible choices: {", u1, ", ", u2, "}")
        # the codeword x is chosen randomly and uniformly within the bin associated to the message u
        rand = r.randint(0, 1)
        if rand == 0:
            print("codeword: ", u1)
            u = u1
        else:
            u = u2
            print("codeword: ", u2)
        # to optimize the code we could compute the complement if, and only if, the rand == 1
        # in this case i preferred to show the two choices and how the randomness choice it
    else:
        u = "Input not valid"
        #print("input not valid!")
    return u

if __name__ == "__main__":
    #input
    d = 0b111
    x = rand_encoder(d)
    print(x)
