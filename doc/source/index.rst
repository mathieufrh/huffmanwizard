.. hct documentation master file, created by
   sphinx-quickstart on Fri Jul 18 09:06:44 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to hct's documentation!
===============================

Ce module offre un ensemble de fonctions permettant de compresser / décompresser du texte en utilisant l'`algorithme de Huffman <http://en.wikipedia.org/wiki/Huffman_coding>`_. L'algorithme de Huffman permet de générer des codes de longueur variable afin de compresser des données en réduisant le nombre de bits nécessaires à leur codage.
hct possède une interface graphique (hct-gui), sommairement décrite dans la seconde partie de cette documentation.

Key features
------------

* Permet la compression et la décompression
* Possibilité de sauvegarder le dictionnaire de Huffman
* Entièrement implémenté en Python
* Comparaison des encodages de Huffman et ASCII
* Possède une interface graphique didactique

Installation
------------

Ce module requiert Python 2.7 ou supérieur.
Seul le module `csv <https://docs.python.org/2/library/csv.html>`_ est nécessaire à l'import / export du dictionnaire.

L'utilisation de l'interface graphique requiert la biblithèque `PySide <https://pypi.python.org/pypi/PySide>`_.

Avec le gestionnaire de paquet Apt vous pouvez utiliser cette commande pour installer la bibliothèque PySide::

    # apt-get install python-pyside

Contents
--------

.. toctree::
   :maxdepth: 2
   
   hct
   hct-gui

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
