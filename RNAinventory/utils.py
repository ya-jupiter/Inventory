# Calculate extinction coefficiency
def CalcExCoef(sequence):
    length = len(sequence)
    ep1 = 0
    ep2 = 0

    ep1_dict = {
        "AA": 13.7, "AC": 10.5, "AG": 12.5, "AU": 12.0,
        "CA": 10.5, "CC": 7.1, "CG": 8.9, "CU": 8.1,
        "GA": 12.6, "GC": 8.7, "GG": 10.8, "GU": 10.6,
        "UA": 12.3, "UC": 8.6, "UG": 10.0, "UU": 9.8
    }

    ep2_dict = {
        "A": 15.4, "C": 7.2, "G": 11.5, "U": 9.9
    }

    for i in range(1, length):
        xy = sequence[i-1:i+1]
        y = sequence[i]

        ep1 += ep1_dict[xy]

        if i < length - 1:
            ep2 += ep2_dict[y]

    # for debug
    # print(sequence)
    # print(2 * ep1 - ep2)

    return round(2 * ep1 - ep2, 1)

# Input register
def RegistrationInfo(name, sequence, note, a260, volume):
    # return error flag if input data is not suitable
    if not all(base in 'AUGC' for base in sequence):
        return [False, 'Sequence contains strings except "A", "U", "G", "C"']
    
    if not isinstance(a260, (int, float, complex)):
        return [False, 'A260 value is not numeric']
    
    if not isinstance(volume, (int, float, complex)):
        return [False, 'volume value is not numeric']
    
    length = len(sequence)
    excoef = CalcExCoef(sequence)
    conc = round(a260 * 1000 / excoef, 1)
    mol = round(conc * volume /1000, 2)
    
    register_info = [name, sequence, note, length, excoef, a260, conc, volume, mol]
    print(register_info)
    return register_info