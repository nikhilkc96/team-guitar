import numpy as np

def string_to_array(s):
  return np.array([1 if x == '1' else 0 for x in s], dtype='i1')

def array_to_string(a):
    return ''.join(['1' if (i) else '0' for i in a])