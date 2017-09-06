import hashlib
import bitarray
import itertools

def bitarray_checksum(a_bitarray):
    assert isinstance(a_bitarray, bitarray.bitarray)
    h = hashlib.md5()
    h.update(a_bitarray.to01())
    return h.hexdigest()

def bitlist_checksum(a_list):
    assert isinstance(a_list, list)
    assert isinstance(a_list[0], tuple)
    h = hashlib.md5()
    h.update(''.join([str(item) for item in itertools.chain.from_iterable(a_list)]))
    return h.hexdigest()
