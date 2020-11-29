import numpy as np
import task2 as t2
import task1 as t1
from collections import Counter
from bitstring import BitArray
import matplotlib.pyplot as plt
import math

#all of possible inputs
inputs = ["000", "001", "010", "100",
          "011", "101", "110",
          "111"]

if __name__ == "__main__":
    n = 10000
    z_pmds = []
    for u in inputs:
        u_integer = BitArray(bin=u).uint
        z_results = []
        for i in range(0, n):
            intermediate_u = t2.rand_encoder(u_integer)
            z = bin(t1.eve_channel(intermediate_u))[2:].zfill(7)
            #Save the integer number in order to be more readable in
            #the plot/tabulate
            z_results.append(int(z, 2))

        #Sort the dictionary in order to plot it
        z_dict = dict(sorted(Counter(z_results).items()))
        z_pmds.append(z_dict)

    #Plot the PMDs
    # for i in range(0, len(inputs)):
    #     plt.plot(list(z_pmds[i].keys()), list(x / n for x in z_pmds[i].values()))
    # plt.xlabel('Number')
    # plt.ylabel('Probability')
    # plt.suptitle('Simulation of Eavesdropper channel')
    # plt.show()
    fig, axs = plt.subplots(math.ceil(len(inputs)/4), 4)
    for i in range(0, len(inputs)):
        axs[i//4, i%4].plot(list(z_pmds[i].keys()), list(x / n for x in z_pmds[i].values()))
        axs[i//4, i%4].set(xlabel='Number')
        axs[i//4, i%4].set_title('Input ' + str(inputs[i]))
        if (i%4 == 0):
            axs[i//4, i%4].set(ylabel='Probability') # only for first column or it overlaps
    fig.suptitle('Simulation of Eavesdropper channel')
    plt.show()

    matrix = np.empty((0, 128), float)
    #Joint probabilities using P[x, y] = P[y|x]*P[x]
    for i in range(0, len(inputs)):
        single_prob = list(((1/8)*x) / n for x in z_pmds[i].values())
        prob = [np.array(single_prob)]
        matrix = np.append(matrix, prob, axis=0)

    #Marginal distribution by sum the rows and the cols
    marginal_distribution_c = matrix.sum(axis=0)
    marginal_distribution_d = matrix.sum(axis=1)
    print("Marginal distribution p(c): ", marginal_distribution_c, "\n")
    print("Marginal distribution p(d): ", marginal_distribution_d, "\n")
    

    
    #Compute the mutual information using the formula in the PDF
    mutual_information = 0
    for i in range(0, len(inputs)):
        for j in range(0, 128):
            joint_distribution = matrix[i][j]
            fraction = joint_distribution/(marginal_distribution_c[j]*marginal_distribution_d[i])
            log = math.log(fraction, 2)
            mutual_information += (joint_distribution*log)
    
    print("Mutual information: ", mutual_information, "\n")
