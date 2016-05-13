Utilisation
===========

Ce module se veut didactique : pour compresser un texte vous allez devoir le faire étape par étape.

Encodage
--------

Vous devez uniquement fournir un texte à compresser::

    >>> text = 'mississippi'

.. note::

    Si le texte contient des caractères non-ASCII ils seront convertis tel que 'à' = u'\xe0' de façon à pouvoir attribuer un ou plusieurs codes ASCII à tous les caractères. Pour cette raison, les caractères non-ascii sont considérés comme plusieurs caractères, ce qui ne gène en rien la compression et la décompression.

Puis il faut calculer la fréquence des caractères du texte en comptant son nombre d'occurences avec occurences()::

    >>> occ = occurences(text)
    >>> print(occ)
    {'i': 4, 'p': 2, 's': 4, 'm': 1}

Il faut désormais construire l'arbre de Huffman grâce à ce dictionnaire::

    >>> tree = make_trie(occ)
    >>> print(tree)
    (11, (4, 's'), (7, (3, (1, 'm'), (2, 'p')), (4, 'i')))

La fonction make_codes() permet d'extraire le code de chaque caractère de l'arbre::

    >>> codes = make_codes(tree)
    >>> print(codes)
    {'i': '11', 'p': '101', 's': '0', 'm': '100'}

.. note::

    Les codes extraient de l'arbre ont tous un préfix unique : aucun code ne peut avoir le même préfix qu'un autre. De ce fait, la compression et la décompression sont des opérations très simples.

.. seealso::

    make_ascii_codes()

Maintenant qu'on connait les codes il ne reste plus qu'à compresser le texte en y remplaçant chaque caractère par son code::

    >>> squeezed = squeeze(text, codes)
    >>> print(''.join(squeezed))
    100110011001110110111

Il est aussi possible de convertir directement les codes en décimal::

    >>> print(squeez_to_decimal(squeezed))
    [153, 157, 23]

La fonction tree_cost() calcule le nombre de bits nécesaire à la représentation du texte compressé. Cela correspond pour un caractère donné à la longueur de son code de Huffman multiplié par son nombre d'occurences::

    >>> print(tree_cost(codes, occ))
    {'i': 8, 'p': 6, 's': 4, 'm': 3}

Décodage
--------

Vous devez fournir la chaine encodée et le dictionnaire charactère / codes qui a permi de l'encoder.

    >>> codes = {'i': '11', 'p': '101', 's': '0', 'm': '100'}

.. seealso::

    save_dict_to_file() and create_dict_from_file()

On créé le dictionnaire inverse avec la fonction suivante::

    >>> codeMap = dict(zip(codes.values(), codes.keys()))
    >>> print(codeMap)
    {'11': 'i', '0': 's', '100': 'm', '101': 'p'}

Étant donné que les codes on tous un préfixe unique il ne reste plus qu'à les remplacer dans la chaine compressée par le caractère qui leur correspond dans le dictionnaire::

    >>> decode = unsqueeze(codeString, codeMap)
    >>> print(''.join(decode))
    mississipi

Module functions
================

Functions list
--------------

| :ref:`occurences-section`
| :ref:`make_trie-section`
| :ref:`make_codes-section`
| :ref:`make_ascii_codes-section`
| :ref:`tree_cost-section`
| :ref:`average_code_length-section`
| :ref:`squeeze-section`
| :ref:`squeeze_to_decimal-section`
| :ref:`unsqueeze-section`
| :ref:`create_dict_from_file-section`
| :ref:`save_dict_to_file-section`

Functions descriptions
----------------------

..  _occurences-section:

occurences(str)
^^^^^^^^^^^^^^^

..  function::  occurences(text)

    Construit un dictionnaire du nombre d'occurences de chaque caractères du 
    texte.
   
    :param text: un texte en langage naturel
    :type text: str
    :return: le dictionnaire d'occurences
    :rtype: dict

    exemple::
    
        occurences('mississipi')
        => {'i': 4, 'p': 1, 's': 4, 'm': 1}

..  _make_trie-section:

make_trie(dict)
^^^^^^^^^^^^^^^

..  function:: make_trie(occ)

    Construit un arbre de huffman à partir d'un dictionnaire d'occurences.
    
    :param occ: un dictionnaire du type charactère: nb_occurences
    :type occ: dict
    :return: l'arbre de huffman sous forme de tuple
    :rtype: tuple
    
    exemple::
    
        make_trie({'i': 4, 'p': 1, 's': 4, 'm': 1})
        => (10, (4, 's'), (6, (2, (1, 'm'), (1, 'p')), (4, 'i')))

..  _make_codes-section:

make_codes(tuple[, dict[, str]])
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..  function:: make_codes(tree[, prefix={}[, code='']])

    Construit le dictionnaire associant un code de huffman à chaque caractère à partir d'un arbre de huffman.
    
    :param tree: un arbre de huffman
    :type tree: tuple
    :param prefix: le dictionnaire qui contiendra les codes
    :type prefix: dict
    :param code: le code actuel
    :type code: str
    :return: le dictionnaire associant un code de huffman à chaque caractère de l'arbre
    :rtype: dict
    
    exemple::
    
        make_code((10, (4, 's'), (6, (2, (1, 'm'), (1, 'p')), (4, 'i'))))
        => {'i': '11', 'p': '101', 's': '0', 'm': '100'}
        
    ..  note::

        Comme la fonction retourne un dictionnaire il n'est pas nécessaire d'utiliser le paramètre prefix, il suffit de stocker le dictionnaire retourné.
        
        Le paramètre code est surtout utilisé par la fonction, il est très peu probable que vous ailelz à le spécifier.

.. _make_ascii_codes-section:

make_ascii_codes(list[, dict])
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..  function:: make_ascii_codes(charList[, prefix={}])

    Contrsuit le dictionnaire associant un code ascii à chaque caractère d'une liste.
    
    :param charList: une liste de caractères
    :type charList: list
    :param prefix: le dictionnaire qui contiendra les codes
    :type prefix: dict
    :return: le dictionnaire associant un code ascii à chaque caractère de la liste
    :rtype: dict

    exemple::
    
        make__ascii_code((10, (4, 's'), (6, (2, (1, 'm'), (1, 'p')), (4, 'i'))))
        => {'i': '01101001', 'p': '01110000', 's': '01110011', 'm': '01101101'}

    ..  note::

        Comme la fonction retourne un dictionnaire il n'est pas nécessaire d'utiliser le paramètre prefix, il suffit de stocker le dictionnaire retourné.

..  _tree_cost-section:

tree_cost(dict, dict)
^^^^^^^^^^^^^^^^^^^^^

..  function:: tree_cost(codesDict, occ)

    Calcule le nombre total de bits codant toutes les occurences de chaque caractère d'un dictionnaire.
    
    :param codesDict: un dictionnaire associant un code à chaque caractère
    :type codesDict: dict
    :param occ: un dictionnaire du type charactère: nb_occurences
    :type occ: dict
    :return: le dictionnaire du nombre de bits total utilisé par chaque caractère
    :rtype: dict
    
    Pour chaque caractère du dictionnaire **occ** cette fonction calcule la taille du code qui le représente et multiplie ce nombre par le nombre d'occurences du caractère.
    
    exemple::
    
        tree_cost({'i': '11', 'p': '101', 's': '0', 'm': '100'}, {'i': 4, 'p': 1, 's': 4, 'm': 1})
        => {'i': 8, 'p': 3, 's': 4, 'm': 3}

..  _average_code_length-section:

average_code_length(list)
^^^^^^^^^^^^^^^^^^^^^^^^^

..  function:: average_code_length(squeezed)

    Calcule la taille moyenne des codes d'une liste de codes.
    
    :param squeezed: une liste de codes (Huffman...)
    :type squeezed: list
    :return: taille moyenne des codes de la liste
    :rtype: float
    
    exemple::
    
        average_code_length(['100', '11', '0', '0', '11', '0', '0', '11', '101', '11'])
        => 1.8
    
    ..  note::
        
        Évidemment cette fonction est inutile pour les liste de codes de taille fixe.

..  _squeeze-section:

squeeze(str, dict)
^^^^^^^^^^^^^^^^^^

..  function:: squeeze(text, codes)

    Construit la liste des codes de Huffman codant un texte.
    
    :param text: un texte à encoder
    :type text: str
    :param codes: un dictionnaire contenant les codes de Huffman
    :type codes: dict
    :return: la liste des codes de Huffman codant le texte
    :rtype: list
    
    exemple::
    
        squeeze('mississipi', {'i': '11', 'p': '101', 's': '0', 'm': '100'})
        => ['100', '11', '0', '0', '11', '0', '0', '11', '101', '11']

..  _squeeze_to_decimal-section:

squeez_to_decimal(list)
^^^^^^^^^^^^^^^^^^^^^^^

..  function:: squeez_to_decimal(binList)

    Convertit une liste de codes binaies en liste de codes décimaux.
    
    :param binList: une liste de codes binaires sous forme de chaine
    :type binList: list
    :return: liste de codes décimaux
    :rtype: list
    
    exemple::
        
        squeeze_to_decimal(['100', '11', '0', '0', '11', '0', '0', '11', '101', '11'])
        => [153, 157, 3]

..  _unsqueeze-section:

unsqueeze(str, dict)
^^^^^^^^^^^^^^^^^^^^

..  function:: unsqueeze(codeString, codeMap)

    Décode un texte encodé à l'aide d'un dictionnaire de codes.
    
    :param codeString: un texte encodé
    :type codeString: str
    :param codeMap: un dictionnaire associant un caractère à chaque code
    :type codemap: dict
    :return: liste des mots du texte décodé
    :rtype: list
    
    exemple::
        
        unsqueeze('100110011001110111', {'11': 'i', '0': 's', '100': 'm', '101': 'p'})
        => mississipi

..  _create_dict_from_file-section:

create_dict_from_file(str)
^^^^^^^^^^^^^^^^^^^^^^^^^^

..  function:: create_dict_from_file(fname)

    Create a dictionnary from a file.
    
    :param fname: the name of the file to read
    :type fname: str
    :return: the dictionnary created from the file
    :rtype: dict
    
    La convention est d'utiliser un fichier .csv contant une liste de paires clé / valeur de la forme `key,value` à raison d'une paire par ligne.
    
    ..  seealso::
    
        :mod:`csv`

..  _save_dict_to_file-section:

save_dict_to_file(str, dict)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..  function:: save_dict_to_file(fname, codes)

    Ŝave a dictionnary in a file.
    
    :param fname: the name of the file to write
    :type fname: str
    :return: the dictionnary to save
    :rtype: dict
    
    La convention est d'utiliser un fichier .csv.
    
    ..  seealso::
    
        :mod:`csv`
