verbos = 0
variables = 0

def get_sim_positions(sim_position, n, length):
    pos = []
    for i in range(int(n)):
        position = round( float(sim_position[i])*float(length) )
        pos.append(position)
    return pos

def get_sim_positions_old(alleles, n, length):
    pos = []
    sim_position = alleles.make_bitarray()[1]   # Double check why we would use 'make_bitarray' and not 'make_bitarray_seq'
    for i in range(int(n)):
        position = round(float(sim_position[i])*float(length) )
        pos.append(position)
    return pos




