import numpy as np
import task2 as t2
import task3_1 as t3
import task5 as t5
from utils import *
from bitstring import BitArray

#All of possible inputs
inputs = ["000", "001", "010", "100",
          "011", "101", "110",
          "111"]

if __name__ == "__main__":
    values_e = [0.1, 0.2, 0.3]
    values_d = [0.3, 0.35, 0.45]
    #Repeating task 3 and computing realiabilty of Bob

    
    for e, d in zip(values_e, values_d):
        errors = 0
        errors2 = 0
        for u in inputs:
            #Transform inp to Integer and call the encoder
            u_integer = BitArray(bin=u).uint
            #Encode input string
            x = t2.rand_encoder(u_integer)

            y, z = t5.bsc_channel(string_to_array(x), e, d)

            u_hat = t3.rand_decoder(array_to_string(y))

            if(u_hat != u):
                errors += 1

        print("Errors rate (e,d)=(",e, ",",d, "): ", errors/len(inputs))