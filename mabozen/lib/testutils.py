
"""
test utils
"""

import string

from faker import Factory




def get_word(maxlen=100):       
    """
    varchar()
    """
    fake = Factory.create()
    
    word = fake.word()       

    if len(word)>maxlen:
        
        return word[:maxlen]

    else:
        return word

def get_bpchar(maxlen):        
    """
    char(), ljust to fill space
    """
    fake = Factory.create()
    
    word = fake.word()
    

    if len(word)>maxlen:
        return word[:maxlen]

    else:
        return string.ljust(word, maxlen)
