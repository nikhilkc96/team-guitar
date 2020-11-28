import numpy as np
import task2 as t2
import task3 as t3
from bitstring import BitArray
from utils import *
import math
import matplotlib.pyplot as plt
from statistics import mean
import matplotlib.pyplot as plt2

def main():
  rng = np.random.default_rng()
  # random input with equal number of 0 and 1
  input = rng.choice([0,1], 10000, p=[0.5, 0.5])
  epsilon = 0.2
  delta = 0.3
  output_y, output_z = bsc_channel(input, epsilon, delta)
  # check number of flipped bits
  error_y = sum(abs(input - output_y))/np.size(input)
  error_z = sum(abs(input - output_z))/np.size(input)
  print("Provided values are: epsilon = " + str(epsilon) + " delta = " + str(delta))
  print("Computed values after test are: epsilon = " + str(error_y) + " delta = " + str(error_z))

  # test with task 2/3 encoder decoder
  print("TESTING WITH ENCODER/DECODER")

  deltas = np.arange(0, 1.1, 0.1)
  epsilon = 0.1
  wrong_eves = [] # number of wrong codewords decoded by eve in percentage
  wrong_bobs = [] # number of wrong codewords decoded by bob in percentage
  codeword_error_eve = [] # % of wrong bits in the codeword received by eve

  for delta in deltas:
    # compute channel capacity
    if abs(epsilon - 0.5) > abs(delta - 0.5):
      log_epsilon = epsilon*math.log(epsilon, 1./2.) + (1-epsilon)*math.log(1-epsilon, 1./2.) if epsilon != 0 and epsilon != 1 else 0
      log_delta = delta*math.log(delta, 1./2.) + (1-delta)*math.log(1-delta, 1./2.) if delta != 0 and delta != 1 else 0
      capacity = log_delta - log_epsilon
    else:
      capacity = 0

    print("With epsilon = ", str(epsilon), " and delta = ", str(delta), " the channel capacity is ", str(capacity))

    # count of how many pairs of codewords have more than 1 bit different, or in other words, how many wrong codewords are decoded
    multi_error_codeword_count = 0 
    error_bob_count = 0 # this is the same as multi_error_codeword_count, kept for redundancy
    error_eve_count = 0 # wrong codewords decoded by eve 
    codeword_error_eve_cycle = []
    
    repeat = 100 # how many times to repeat input sequences
  
    # repeat multiple times for better estimates
    for u in np.repeat(t3.inputs, repeat):
      # transform inp to Integer and call the encoder
      u_integer = BitArray(bin=u).uint
      # encode input string
      x = t2.rand_encoder(u_integer)

      y, z = bsc_channel(string_to_array(x), epsilon, delta)

      if sum(abs(y - string_to_array(x))) > 1:
        multi_error_codeword_count += 1
      
      y = array_to_string(y)
      u_hat = t3.rand_decoder(y)

      codeword_error_eve_cycle.append(sum(abs(z - string_to_array(x)))/np.size(z))
      
      z = array_to_string(z)
      z_h = t3.rand_decoder(z)

      if u != u_hat:
        error_bob_count += 1
      
      if z_h != u:
        error_eve_count += 1

      # compare decode with input
      print("Original : ", u, " Bob : ", u_hat, " Eve : ", z_h)
      print("-------")
      
    wrong_bob = error_bob_count/len(t3.inputs)/repeat
    wrong_bobs.append(wrong_bob)
    print("Codewords wrongly decoded by bob: ", str(wrong_bob), "%")
    
    if multi_error_codeword_count > 0:
      print("Perfect reliability is violated!")

    codeword_error_eve.append(mean(codeword_error_eve_cycle))
    
    wrong_eve = error_eve_count/len(t3.inputs)/repeat
    wrong_eves.append(wrong_eve)
    print("Codewords wrongly decoded by eve: ", str(wrong_eve), "%")
    print("#"*20)
  
  # plot message error
  plt.plot(deltas, wrong_eves, color="red")
  plt.xlabel('Delta')
  plt.ylabel('Error')
  plt.suptitle('Error probability of eve decode')
  plt.show()

  plt2.plot(deltas, codeword_error_eve, color="blue")
  plt2.xlabel('Delta')
  plt2.ylabel('Error')
  plt2.suptitle('Error probability of eve codeword')
  plt2.show()
  

def bsc_channel(input, e, d):
  """
  Args:
    input : np.array input array 
    e : error probability in bob channel
    d : error probability in eve channel

  Returns:
    output_y : np.array output string in bob channel
    output_z : np.array output string in eve channel

  """
  input_size = np.size(input)
  rng = np.random.default_rng()
  # generate random 01 array, where 1 means an error occurred in the channel
  mask_y = rng.choice([0,1], input_size, p=[1-e, e]) 
  # 1 => flip
  output_y = np.logical_xor(input, mask_y) 
  mask_z = rng.choice([0,1], input_size, p=[1-d, d])
  output_z = np.logical_xor(input, mask_z)
  return output_y, output_z

if __name__ == "__main__": 
  main()