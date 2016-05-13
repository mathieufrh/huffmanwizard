#!/usr/bin/env python
# coding: utf-8


import csv


def occurences(text):
    """Construit et retourne un dictionnaire du nombre d'occurences de
    chaque caractères du texte <text>.
    exemple: {'a': 54, 'd': 28, 'e': 79}.
    """
    o = {}
    for x in text:
        o[x] = o.get(x, 0) + 1
    return o


def make_trie(occ):
    """Construit et retourne un arbre de huffman à partir du dictionnaire
    d'occurences <occ>.
    exemple: (117, (58, 'e'), (59, (29, 's'), (30, 'a')))."""
    occ = zip(occ.values(), occ.keys())
    while occ[1:]:
        left = min(occ)
        occ.remove(left)
        right = min(occ)
        occ.remove(right)
        occ.append((left[0] + right[0], left, right))
    return occ[0]


def make_codes(tree, prefix={}, code=''):
    """Construit et retourne le dictionnaire associant un code à chaque
    caractère du texte à partir de l'arbre de huffman <tree>.
    exemple: {'a': '0111', 'c': '00110', 'e': '010'}
    """
    if leafp(tree):
        prefix[tree[1]] = code
    else:
        make_codes(tree[1], prefix, code + '0')
        make_codes(tree[2], prefix, code + '1')
    return prefix


def make_ascii_codes(charList, prefix={}):
    for char in charList:
        code = bin(ord(char)).replace('b', '')
        if len(code) == 7:
            code = '0' + code  # ????
        if len(code) == 9:
            code = code[1:]    # ????
        prefix[char] = code
    return prefix


def leafp(x):
    return isinstance(x[1], str)


def tree_cost(codesDict, occ):
    """Construit et retourne le dictionnaire du nombre de bits représentant
    toutes les occurences de chaque caractère du texte en code de huffman.
    exemple: {'a': 120, 'd': 54, 'e': 174}
    """
    costs = {}
    for x in codesDict:
        code = codesDict[x]
        freq = occ[x]
        cost = freq * len(code)
        costs[x] = cost  # freq * len(code)
    return costs


def average_code_length(squeezed):
    """Calcule et retourne la taille moyenne d'un code de huffman dans
    une liste <squeezed>.
    """
    return len(''.join(squeezed)) / float(len(squeezed))


def entropy(Ps):
    Ps = numpy.asarray(Ps)
    Ps /= sum(Ps)
    Ps[numpy.isnan(Ps)] = 0
    return -sum(xlogx(Ps))


def squeeze(text, codes):
    """Construit et retourne la liste des codes de Huffman d'après le
    dictionnaire <codes> codant le texte <text>.
    exemple: ['1011', '111', '00010', '1001', '1001', '010', '01101100']
    """
    squeezed = []
    for z in text:
        squeezed.append(codes[z])
    return squeezed


def squeez_to_decimal(binList):
    """Retourne la liste des codes de Huffman <binList> convertie
    en décimal.
    exemple: [28, 62, 174, 82, 40, 237, 27]
    """
    squeezed = []
    bitString = ''.join(binList)
    for b in range(0, len(bitString), 8):
        squeezed.append(int(bitString[b:b+8], 2))
    return squeezed


def unsqueeze(codeString, codeMap):
    """Construit et retourne la liste des mots d'après le dictionnaire
    <codeMap> décodant le texte <codeString>.
    """
    decode = []
    bit = ''
    while True:
        try:
            codeString[0]
        except:
            break
        bit = bit + codeString[0]
        codeString = codeString[1:]
        if bit in codeMap:
            decode.append(codeMap[bit])
            bit = ''
    return decode


def create_dict_from_file(fname):
    """Utilise le fichier <fname> pour construire un dictionnaire associant
    codes et caractères."""
    if not fname:
        return False
    codes = {}
    with open(fname, 'rb') as f:
        reader = csv.reader(f)
        for key, val in reader:
            codes[key] = val
    codes = codes
    return codes


def save_dict_to_file(fname, codes):
    """Sauvegarde le dictionnaire de codes actuel sous la forme char,code\n."""
    if not fname:
        return False
    with open(fname, 'wb') as f:
        writer = csv.writer(f)
        for key, val in codes.items():
            writer.writerow([key, val])
    return True
