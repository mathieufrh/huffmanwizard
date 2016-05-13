#!/usr/bin/env python
# coding: utf-8


from PySide import QtCore, QtGui
from huff import *


class EncodeWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(EncodeWizard, self).__init__(parent)
        self.parent = parent
        self.addPage(EncodeIntroPage(self))
        self.addPage(StepOnePage(self))
        self.addPage(StepTwoPage(self))
        self.addPage(StepThreePage(self))
        self.addPage(StepFourPage(self))
        self.addPage(StepFivePage(self))
        self.addPage(StepSixPage(self))
        self.setButtonText(QtGui.QWizard.BackButton, u"Précédent")
        self.setButtonText(QtGui.QWizard.NextButton, "Suivant")
        self.setButtonText(QtGui.QWizard.FinishButton, "Fin")
        self.setButtonText(QtGui.QWizard.CancelButton, "Annuler")


class EncodeIntroPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(EncodeIntroPage, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"Encodage du texte.")
        label = QtGui.QLabel(
            u"<font>    Vous êtes ici dans l'assistant d'encodage du texte.\nLe but est de compresser le <font color=#008000>Texte original</font> en utilisant un codage de taille variable : l'encodage de Huffman.\nJe vais vous guider au fil des étapes de l'encodage en expliquant le fonctionnement de la compression à l'aide de l'algorithme de Huffman et en comparant cet encodage de taille variable à l'encodage ASCII de taille fixe.\nC'est parti ?</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_encode_init()


class StepOnePage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(StepOnePage, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 1: Calcul du nombre d'occurrences des caractères")
        label = QtGui.QLabel(
            u"<font>    Je compte le nombre d'occurrences de chaque caractère du texte.\nLes caractères sont reportés dans la  colonne <font color=#008000>Char</font> du tableau ci-dessous, les nombres d'occurences des caractères sont inscrits dans la  colonne <font color=#008000>Freq</font>.\nLa fréquence relative des caractères est très importante pour l'étape suivante.</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_occ()


class StepTwoPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(StepTwoPage, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 2: Construction de l'arbre de Huffman")
        label = QtGui.QLabel(
            u"<font>    L'arbre de Huffman est un arbre binaire. Un tel arbre permet d'attribuer un code unique à chaque caractère qui y est stocké. Ce code est constitué de 0 et de 1 selon que l'on emprunte les branches gauche ou droite pour atteindre le caractère dans l'arbre. Si je dois emprunter cinq branches pour arriver au caractère, son code sera composé de cinq 0/1.\nJe construit l'arbre de Huffman en plaçant les caractères les plus fréquents au plus proche de la racine, ainsi ils auront un code court.\nCela est important pour compresser le texte : plus le caractère est fréquent dans le texte plus il a un code court et plus la compression sera importante.</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_tree()


class StepThreePage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(StepThreePage, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 3: Génération des codes de Huffman")
        label = QtGui.QLabel(
            u"<font>    Je lis l'arbre de Huffman créé à l'étape précédente afin de récupérer le code de tous les caractères. Pour trouver le code attribué à un caractère je pars de la racine de l'arbre puis je remonte ses branches en direction du caractère. Si j'emprunte une branche gauche j'ajoute un 0 au code, si j'emprunte une branche droite j'y ajoute un 1. Une fois que je suis arrivé au caractère je connais son code et je l'ajoute dans la colonne <font color=#008000>Huff</font> du tableau ci-dessous.\nAfin de comparer la taille des codes de Huffman à celle des codes ASCII je reporte également le code ASCII du caractère dans la colonne <font color=#008000>ASCII</font> du tableau.</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_codes()


class StepFourPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(StepFourPage, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 4: Calcul du coût mémoire total")
        label = QtGui.QLabel(
            u"<font>    Cette étape est facultative mais permet de mieux illustrer l'utilité de la compression des caractères.\nIci, je calcule le nombre total de bits nécessaire à la représentation de toutes les occurrences de chaque caractère du texte.\nPour cela je fais une simple multiplication : nombre d'occurences x longueur du code.\nJe calcule de cette façon le coût mémoire totale de chaque caractère en utilisant son code de Huffman, reporté dans la colonne <font color=#008000>Ĉ Huff</font> et son code ASCII, reporté dans la colonne <font color=#008000>Ĉ ASCII</font>.</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_cost()


class StepFivePage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(StepFivePage, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 5: Encodage du texte original")
        label = QtGui.QLabel(
            u"<font>    Maintenant que je possède les codes de Huffman et ASCII des caractères du texte je peux encoder le texte original en utilisant l'encodage de taille variable de Huffman (cf. <font color=#008000>Text compressé</font>) et l'encodage ASCII de taille fixe (cf. <font color=#808000>Text ASCII</font>).</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_encoded_text()


class StepSixPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(StepSixPage, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 6: Comparaison des encodages")
        label = QtGui.QLabel(
            u"<font>    Enfin, je peux rendre compte de l'espace économisé en utilisant l'encodage de Huffman plutôt que l'encodage ASCII en calculant la nombre de bits nécessaires à l'encodage du texte en Huffman et en ASCII et la taille moyenne du code d'un caractère.\nCes variables sont regroupées dans un tableau, cliquez sur 'Terminer' pour l'afficher.</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_comp()


###############################################################################
class DecodeWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(DecodeWizard, self).__init__(parent)
        self.parent = parent
        self.addPage(DecodeIntroPage(self))
        self.addPage(MakeCodeMap(self))
        self.addPage(MakeDecodedText(self))
        self.addPage(MakeAsciiComp(self))
        self.addPage(MakeComp(self))


class DecodeIntroPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(DecodeIntroPage, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"Décodage du texte.")
        label = QtGui.QLabel(
            u"<font>Afin de décoder un <font color=#008000>Texte compressé</font> avec l'algorithme de Huffman il est nécessaire de disposer d'un dictionnaire de Huffman associant codes et caractères.\nComme le dictionnaire est déjà fourni il n'y a pas besoin de le recréer. De ce fait, la décompression est plus rapide que la compression. On y va ?</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_decode_init()


class MakeCodeMap(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(MakeCodeMap, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 1: Construction du dictionnaire de décodage")
        label = QtGui.QLabel(
            u"<font>    Pour obtenir le dictionnaire de décodage il suffit d'inverser les clés (caractères) et les valeurs (codes de Huffman) du dictionnaire original. On obtient ainsi un dictionnaire associant un caractère à chaque code de Huffman.</font")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_code_map()


class MakeDecodedText(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(MakeDecodedText, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 2: Décodage du texte encodé")
        label = QtGui.QLabel(
            u"<font>    Maintenant je n'ai plus qu'à lire le texte compressé en y remplaçant chaque code de Huffman par le caractère correspondant dans le dictionnaire de décodage. Vous pouvez voir le résultat dans l'encadré du <font color=#008000>Texte original</font></font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_decoded_text()


class MakeAsciiComp(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(MakeAsciiComp, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 3: Équivalent ASCII")
        label = QtGui.QLabel(
            u"<font>    Le texte à été décodé, je pourrais m'arrêter là mais je vais tout de même compléter le tableau ci-dessous  en comptant le nombre d'occurences de chaque caractère du texte et en encodant ce texte en ASCII afin de comparer le nombre de bits utilisé par l'encodage fixe ASCII et l'encodage de taille variable de Huffman.\nJ'ai ainsi rempli les colonnes <font color=#008000>Freq</font>, <font color=#008000>ASCII</font>, <font color=#008000>Ĉ ASCII</font>, <font color=#008000>Ĉ Huff</font> et l'encadré du <font color=#008000>Texte ASCII</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_ascii_decode()


class MakeComp(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(MakeComp, self).__init__(parent)
        self.gparent = parent.parent
        self.setTitle(u"STEP 6: Comparaison des encodages")
        label = QtGui.QLabel(
            u"<font>    Enfin, je peux rendre compte de l'espace économisé en utilisant l'encodage de Huffman plutôt que l'encodage ASCII en calculant la nombre de bits nécessaires à l'encodage du texte en Huffman et en ASCII et la taille moyenne du code d'un caractère.\nCes variables sont regroupées dans un tableau, cliquez sur 'Terminer' pour l'afficher.</font>")
        label.setWordWrap(True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def initializePage(self):
        self.gparent.make_comp()
