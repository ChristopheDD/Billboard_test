from itertools import product
import pandas as pd
import numpy as np
import sys

### Functions ###

def multi_split(str1,bin_seq):
# Splits the text along white spaces according to a given binary sequence indicating split positions

    x = [pos for pos, char in enumerate(str1) if char == ' '] # Creates a list x with string indices for white spaces

    for i in range(len(bin_seq)):
        x[i] = x[i]*bin_seq[i] # Returns white spaces indices according to the binary sequence
    x = list(filter(lambda a: a != 0, x)) # Filters out zeros

    str1 = list(str1) # Turns string to list for processing
    for i in range(len(str1)):
        if i in x:
            str1[i] = ';' # Replaces relevant spaces in the string by ';'
    str1 = ''.join(str1) # Back from list into string
    
    return str1.split(sep = ';') # Splits the string with ';' and returns the desired list of strings


def width_height_comb(string): 
# Returns lists 'width' and 'height' of all possible configurations of the text (font size =1)

    nwords = len(string.split())
    binseq_list= list(product(range(2), repeat = nwords -1)) # Generates a list of 2^(nwords-1) binary sequences for all string splitting possibilities

    words_seqs = [[]]
    for binary in binseq_list:
        words_seqs.append(multi_split(string, binary)) # Returns all possible splits of string s in words_seqs
    del words_seqs[0]

    width=[]
    height=[]

    for seq in words_seqs: 
        if len(seq) == 1:
            width.append(len(str(seq)))
            height.append(1)
        else:
            width.append(len(max(seq, key =len))) # Calculates the width of the longest line in split 'seq' and adds it to the list
            height.append(len(seq)) # Calculates the height (number of lines) in split 'seq'
    
    return [width,height]


def find_font(Width,Height,String): 
# Calculates maximum font size for each text given Width and Height of the billboard

    max_ratio_list = []
    max_ratio_list = []
    list1 = width_height_comb(String) # List of width and height of the text for each split
    
    for i in range(len(list1[0])):
        ratioW = Width / list1[0][i] # Maximum font size for each split with width constraint only
        ratioH = Height / list1[1][i] # Maximum font size for each split with height constraint only
        max_ratio_list.append(ratioW if ratioW<=ratioH else ratioH) # Maximum font size for each split with both constraints
    
    max_ratio = int(max(max_ratio_list)) # Maximum font size amongst all splits with both constraints, as integer
    return max_ratio



### Main ###

# Opens file into dataframe df
script = sys.argv[0]
filename = sys.argv[1]

df = pd.read_csv(filename)
cases = int(list(df.columns)[0])

# Defines width and height of the billboard plus text
df = df.iloc[:,0].str.split('\s+', n =2, expand = True)
df.columns = ['Width','Height','Text']
n = df.shape[0]
print(df)


out = []
for i in range(cases): # Calls main function 'find_font' for all cases
    font = find_font(float(df.iloc[i,0]),float(df.iloc[i,1]),df.iloc[i,2])
    out.append('Case #' + str(i+1) + ': ' + str(font))

for i in range(cases): print(out[i]) # Returns the results

input("Press enter")





