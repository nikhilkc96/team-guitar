import numpy as np
import task2 as t2
import task3_1 as t3
import task5 as t5
from utils import *
from bitstring import BitArray
from collections import Counter
import matplotlib.pyplot as plt
import math

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

    d=0.0
    while (d<=1):
        n = 10000
        z_pmds = []
        for u in inputs:
            u_integer = BitArray(bin=u).uint
            z_results = []
            for i in range(0,10000):
                x = t2.rand_encoder(u_integer)
                y, z = t5.bsc_channel(string_to_array(x), 0.1, d)
                binary_string = array_to_string(z)
                z_results.append(int(array_to_string(z), 2))

            #Adds 1 value for each word in order to not have problem 
            #while computing the probabilities
            for i in range(0, 128):
                z_results.append(i)
        
            #Sort the dictionary in order to plot it
            z_dict = dict(sorted(Counter(z_results).items()))
            print(z_dict)
            z_pmds.append(z_dict)
      
        matrix = np.empty((0, 128), float)
        #Joint probabilities using P[x, y] = P[y|x]*P[x]
        for i in range(0, len(inputs)):
            single_prob = list(((1/8)*(x-1)) / n for x in z_pmds[i].values())
            prob = [np.array(single_prob)]
            #print(prob)
            matrix = np.append(matrix, prob, axis=0)

        entropy_x_y = 0
        for i in range(0, len(inputs)):
            for j in range(0, 128):
                if(z_pmds[i][j] == 1):
                    continue
                fraction = 1 / ((z_pmds[i][j]-1)/n)
                log = math.log(fraction, 2)
                entropy_x_y += (matrix[i][j]*log)
        
        information_leaked = math.log(128, 2) - entropy_x_y
        plt.scatter(d, information_leaked, c=255)
        d += 0.05
        
    plt.show()