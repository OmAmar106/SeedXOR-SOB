import hashlib
from mnemonic import Mnemonic

def number_to_mnemonic(number):
    entropy_bits = 128
    entropy_bytes = number.to_bytes(entropy_bits // 8, byteorder='big')
    sha256_hash = hashlib.sha256(entropy_bytes).digest()
    checksum_bits = entropy_bits // 32
    checksum = bin(int.from_bytes(sha256_hash, 'big'))[2:].zfill(256)[:checksum_bits]
    entropy_bin = bin(int.from_bytes(entropy_bytes, 'big'))[2:].zfill(entropy_bits)
    full_bin = entropy_bin + checksum
    words = []
    mnemo = Mnemonic("english")
    for i in range(0, len(full_bin), 11):
        idx = int(full_bin[i:i+11], 2)
        words.append(mnemo.wordlist[idx])
    return ' '.join(words)

def mnemonic_to_number(mnemonic_phrase):
    mnemo = Mnemonic("english")
    words = mnemonic_phrase.strip().split()
    if not mnemo.check(mnemonic_phrase):
        raise ValueError("Invalid mnemonic phrase or checksum")
    indexes = [mnemo.wordlist.index(word) for word in words]
    full_bin = ''.join(bin(index)[2:].zfill(11) for index in indexes)
    total_bits = len(full_bin)
    checksum_bits = total_bits // 33
    entropy_bits = total_bits - checksum_bits
    entropy_bin = full_bin[:entropy_bits]
    entropy_int = int(entropy_bin, 2)
    return entropy_int

# number = 10**36
# mnemonic_phrase = number_to_mnemonic(number)
# print(mnemonic_phrase)
# assert(number==mnemonic_to_number(mnemonic_phrase))
