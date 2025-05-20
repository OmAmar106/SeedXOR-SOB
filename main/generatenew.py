import phrase
import random

def create_new_phrase(phras):
    k = phrase.mnemonic_to_number(phras)
    l = random.randint(1,10**36)
    t = l^k
    return (phrase.number_to_mnemonic(t),phrase.number_to_mnemonic(l))

def reconstruct_num(phrases):
    ans = 0
    for i in phrases:
        ans ^= phrase.mnemonic_to_number(i)
    return ans