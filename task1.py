import random as r
from bitstring import BitArray
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3

def legittimate_channel(x):
    # Legitimate
    # random integer for choosing which is the error
    index = r.randint(0, 6)
    # XOR error with the input
    return BitArray(bin=x).uint ^ BitArray(bin=errors[index]).uint # BitArray(bin=errors[index]).uint transforms binary string to integer

def eve_channel(x):
    index = r.randint(0, len(errors) - 1)
    return BitArray(bin=x).uint ^ BitArray(bin=errors[index]).uint

errors = [
'0000000','0000001', '0000010', '0000100', '0001000', '0010000', '0100000', '1000000',
'0000011', '0000101', '0000110', '0001001', '0001010', '0001100', '0010001', '0010010', '0010100', '0011000', '0100001', '0100010', '0100100', '0101000', '0110000', '1000001', '1000010', '1000100', '1001000', '1010000', '1100000',
'0000111', '0001011', '0001101', '0001110', '0010011', '0010101', '0010110', '0011001', '0011010', '0011100', '0100011', '0100101', '0100110', '0101001', '0101010', '0101100', '0110001', '0110010', '0110100', '0111000', '1000011', '1000101', '1000110', '1001001', '1001010', '1001100', '1010001', '1010010', '1010100', '1011000', '1100001', '1100010', '1100100', '1101000', '1110000'
      ]

def main():
  x = "01001000"
  y = []
  z = []
  contyz = 0
  conty = 0
  contz = 0
  n = 25000
  for _ in range(0, n):

      word_y = legittimate_channel(x)
      # adds new word to a list
      y.append(word_y)

      # Same for Eve
      word_z = eve_channel(x)
      z.append(word_z)


      #Verify the conditional independence and uniformity
      if word_y == 64:
          conty += 1
          if word_z == 4:
              contyz += 1
              contz += 1
      else:
          if word_z == 4:
              contz += 1

  print('number of y:', conty, 'number of z:', contz, 'number of pairs yz:', contyz)
  print('P(y=64,z=4|x=72) =', contyz/n)
  print('P(y|x)*P(z|x) =', (conty/n) * (contz/n))
  print('P(y,z|x) - P(y|x)*P(z|x) =', (contyz/n) - ((conty/n) * (contz/n)))

  y_dict = Counter(y)
  z_dict = Counter(z)

  print("Words obtained by Legittimate receiver: ", y)
  print("Occurences for each word: ", y_dict)

  print("Words obtained by Eve receiver: ", z)
  print("Occurences for each word: ",z_dict)

  #print("word_y = ", conty, "word_z = ", contz, "coppia: ", contyz)

  #plot the graphic for Legitimate channel
  plt.bar(y_dict.keys(), y_dict.values(), color="purple")
  plt.xlabel('Number')
  plt.ylabel('Times')
  plt.suptitle('Simulation of Legitimate channel')
  plt.show()

  # plot the graphic for Eavesdropper channel
  plt2.bar(z_dict.keys(), z_dict.values(), color="red")
  plt2.xlabel('Evea Receiver')
  plt2.ylabel('Times')
  plt2.suptitle('Simulation of Eavesdropper channel')
  plt2.show()

  plt3.scatter(list(sorted(z_dict.keys())), list(x / n for x in z_dict.values()), color="black")
  plt3.xlabel('Numbers received by Eavesdropper')
  plt3.ylabel('p_(z|x)(·|1001000)')
  plt3.suptitle('plot of the conditional pmd p_(z|x)(·|1001000) for Eavesdropper channel')
  plt3.axis([0. ,128., 0., 0.2])
  plt3.show()

if __name__ == "__main__":
  main()
