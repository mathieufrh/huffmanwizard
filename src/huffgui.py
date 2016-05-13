#!/usr/bin/env python
# coding: utf-8


import csv
import operator
from PySide.QtCore import QAbstractTableModel, QModelIndex, QMetaObject, QSize, Qt

from PySide.QtGui import (
    QAbstractItemView, QApplication, QColor, QDesktopWidget, QFileDialog,
    QFont, QGridLayout, QGroupBox, QKeySequence, QLabel, QMainWindow, QMenu,
    QMenuBar, QPalette, QPushButton, QSizePolicy, QStatusBar, QTableView,
    QTableWidget, QTableWidgetItem, QTextBrowser, QTextEdit, QWidget)

from huff import *
from wizard import *


#========================= CLASS FOR THE MAIN WINDOW =========================#
class Ui_MainWindow(QMainWindow):
    """Cette classe contient tous les widgets de notre application."""
    
    defaultPalette = QPalette()
    defaultPalette.setColor(QPalette.Base, QColor("#151515"))
    defaultPalette.setColor(QPalette.Text, Qt.white)

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        # initialise la GUI avec un exemple
        self.text = "Ceci est un petit texte d'exemple."
        # les variables sont en place, initialise la GUI
        self.initUI()
        # exécute l'exemple
        self.orgText.setText(self.text)
        self.encode_text(False)
        self.logLab.setText(
            u"Saisir du texte ou importer un fichier, puis pousser \n"
            u"le bouton correspondant à l'opération souhaitée.")

    def initUI(self):
        """Met en place les éléments de l'interface."""
        # -+++++++------------------- main window -------------------+++++++- #
        self.setWindowTitle(u"Encodage / Décodage de Huffman")
        self.centerAndResize()
        centralwidget = QWidget(self)
        mainGrid = QGridLayout(centralwidget)
        mainGrid.setColumnMinimumWidth(0, 450)
        # -+++++++------------------ groupe analyse -----------------+++++++- #
        analysGroup = QGroupBox(u"Analyse", centralwidget)
        self.analysGrid = QGridLayout(analysGroup)
        #         ----------- groupe de la table des codes ----------         #
        codeTableGroup = QGroupBox(u"Table des codes", analysGroup)
        codeTableGrid = QGridLayout(codeTableGroup)
        # un tableau pour les codes
        self.codesTableModel = MyTableModel()
        self.codesTable = QTableView(codeTableGroup)
        self.codesTable.setModel(self.codesTableModel)
        self.codesTable.setFont(QFont("Mono", 8))
        self.codesTable.resizeColumnsToContents()
        self.codesTable.setSortingEnabled(True)
        codeTableGrid.addWidget(self.codesTable, 0, 0, 1, 1)
        self.analysGrid.addWidget(codeTableGroup, 1, 0, 1, 1)
        #        ----------- label du ratio de compression ----------         #
        self.ratioLab = QLabel(u"Ratio de compression: ", analysGroup)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.ratioLab.setFont(font)
        self.analysGrid.addWidget(self.ratioLab, 2, 0, 1, 1)
        # -+++++++-------- groupe de la table de comparaison --------+++++++- #
        self.compGroup = QGroupBox(analysGroup)
        self.compGroup.setTitle(u"Comparaisons")
        compGrid = QGridLayout(self.compGroup)
        # un tableau pour le ratio
        self.compTable = QTableWidget(self.compGroup)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.compTable.sizePolicy().hasHeightForWidth())
        self.compTable.setSizePolicy(sizePolicy)
        self.compTable.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setWeight(50)
        self.compTable.setFont(font)
        self.compTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.compTable.setShowGrid(True)
        self.compTable.setGridStyle(Qt.SolidLine)
        # lignes / colonnes
        self.compTable.setColumnCount(2)
        self.compTable.setRowCount(3)
        self.compTable.setVerticalHeaderItem(0, QTableWidgetItem("Taille (bits)"))
        self.compTable.setVerticalHeaderItem(1, QTableWidgetItem("Entropie"))
        self.compTable.setVerticalHeaderItem(2, QTableWidgetItem("Taille moy. (bits)"))
        for i in range(2):
            self.compTable.verticalHeaderItem(i).setTextAlignment(
                Qt.AlignRight)
        self.compTable.setHorizontalHeaderItem(0, QTableWidgetItem("ASCII"))
        self.compTable.setHorizontalHeaderItem(1, QTableWidgetItem("Huffman"))
        
        # nom des items
        self.compTabASCIIMem = QTableWidgetItem()
        self.compTable.setItem(0, 0, self.compTabASCIIMem)
        self.compTabASCIIEnt = QTableWidgetItem()
        self.compTable.setItem(1, 0, self.compTabASCIIEnt)
        self.compTabASCIIAvg = QTableWidgetItem()
        self.compTable.setItem(2, 0, self.compTabASCIIAvg)
        self.compTabHuffMem = QTableWidgetItem()
        self.compTable.setItem(0, 1, self.compTabHuffMem)
        self.compTabHuffEnt = QTableWidgetItem()
        self.compTable.setItem(1, 1, self.compTabHuffEnt)
        self.compTabHuffAvg = QTableWidgetItem()
        self.compTable.setItem(2, 1, self.compTabHuffAvg)
        # parem du tableau
        self.compTable.horizontalHeader().setCascadingSectionResizes(False)
        self.compTable.verticalHeader().setVisible(True)
        font = QFont("Mono", 8)
        self.compTable.setFont(font)
        compGrid.addWidget(self.compTable, 1, 0, 1, 1)
        self.analysGrid.addWidget(self.compGroup, 0, 0, 1, 1)
        mainGrid.addWidget(analysGroup, 0, 1, 1, 1)
        # -+++++++----------------- groupe du texte -----------------+++++++- #
        groupBox = QGroupBox(u"Texte", centralwidget)
        textGrid = QGridLayout(groupBox)
        # -+++++++------------- groupe du texte original ------------+++++++- #
        orgTextGroup = QGroupBox(u"Texte original (Ctrl+T)", groupBox)
        orgTextGrid = QGridLayout(orgTextGroup)
        self.orgText = QTextEdit(orgTextGroup)
        self.orgText.setPalette(self.defaultPalette)
        orgTextGrid.addWidget(self.orgText, 0, 0, 1, 1)
        textGrid.addWidget(orgTextGroup, 0, 0, 1, 2)
        # -+++++++------------ groupe du texte compressé ------------+++++++- #
        compressedTextGroup = QGroupBox(u"Texte compressé (Ctrl+H)", groupBox)
        compressedTextGrid = QGridLayout(compressedTextGroup)
        self.compressedText = QTextEdit(compressedTextGroup)
        self.compressedText.setPalette(self.defaultPalette)
        compressedTextGrid.addWidget(self.compressedText, 0, 0, 1, 1)
        textGrid.addWidget(compressedTextGroup, 1, 0, 1, 2)
        # -+++++++------------ groupe pour le texte ascii -----------+++++++- #
        asciiTextGroup = QGroupBox(u"Texte ASCII", groupBox)
        asciiTextGrid = QGridLayout(asciiTextGroup)
        self.asciiText = QTextBrowser(asciiTextGroup)
        self.asciiText.setPalette(self.defaultPalette)
        asciiTextGrid.addWidget(self.asciiText, 0, 0, 1, 1)
        textGrid.addWidget(asciiTextGroup, 2, 0, 1, 2)
        # -+++++++-------------------- label de log -----------------+++++++- #
        self.logLab = QLabel(analysGroup)
        textGrid.addWidget(self.logLab, 3, 0, 1, 2)
        # -+++++++----------- bouton pour encoder le texte ----------+++++++- #
        self.encodeBut = QPushButton(groupBox)
        self.encodeBut.setStatusTip(
            u"Cliquez sur ce bouton pour encoder le texte original.")
        self.encodeBut.setText(u"ENCODER")
        self.encodeBut.clicked.connect(self.encode_text)
        textGrid.addWidget(self.encodeBut, 4, 0, 1, 1)
        # -+++++++----------- bouton pour décoder le texte ----------+++++++- #
        self.decodeBut = QPushButton(groupBox)
        self.decodeBut.setStatusTip(
            u"Cliquez sur ce bouton pour décoder le texte compressé.")
        self.decodeBut.setText(u"DÉCODER")
        self.decodeBut.clicked.connect(self.decode_text)
        textGrid.addWidget(self.decodeBut, 4, 1, 1, 1)
        mainGrid.addWidget(groupBox, 0, 0, 1, 1)
        self.setCentralWidget(centralwidget)
        # -+++++++--------------- une barre de statut ---------------+++++++- #
        self.setStatusBar(QStatusBar(self))
        # -+++++++--------------------- le menu ---------------------+++++++- #
        self.fileMenu = QMenu(u"Fichier")
        self.fileMenu.addAction(u"Importer un texte...", self.open_text)
        self.fileMenu.addAction(
            u"Importer un texte encodé...", lambda: self.open_text(True))
        self.fileMenu.addAction(u"Importer un dictionnaire...", self.open_dict)
        self.fileMenu.addAction(u"Enregistrer le dictionnaire...", self.save_dict)
        self.fileMenu.addAction(u"Quitter", self.close)
        self.menuBar().addMenu(self.fileMenu)
        QMetaObject.connectSlotsByName(self)

    def open_text(self, compressed=False):
        """Ouvrir un fichier contenant un texte compressé ou non."""
        fname, _ = QFileDialog.getOpenFileName(self, u'Ouvrir')
        f = open(fname, 'r')
        with f:
            data = f.read()
            if compressed:
                self.compressedText.setText(data)
            else:
                self.orgText.setText(data)

    def open_dict(self):
        """Ouvrir un dictionnaire de codes Huffman."""
        fname, _ = QFileDialog.getOpenFileName(self, u'Ouvrir')
        self.occ = {}
        self.hCodes = {}
        self.aCodes = {}
        self.hCost = {}
        self.aCost = {}
        self.hCodes = create_dict_from_file(fname)
        self.update_codes_table()
        self.logLab.setText(u"Dictionnaire de Huffman importé.")
        return self.hCodes

    def save_dict(self):
        """Enregistrer le dictionnaire de codes Huffman."""
        fname, _ = QFileDialog.getSaveFileName(self, "Enregistrer sous")
        save_dict_to_file(fname, self.hCodes)

    def make_tab_rows(self):
        """Génère le remplissage des lignes du tableau des codes."""
        dictList = [self.occ, self.aCodes, self.hCodes, self.aCost, self.hCost]
        tabList = []
        charList = self.hCodes.keys() if self.hCodes else self.occ.keys()
        for char in charList:
            l = ["'" + char + "'"]
            for dic in dictList:
                try:
                    l.append(dic[char])
                except KeyError:
                    l.append('')
            tabList.append(l)
        return tabList

    def encode_text(self, wizard=True):
        """Encode le texte original."""
        self.text = self.orgText.toPlainText().encode('utf-8')
        if not self.text:
            self.compressedText.setText(u"")
            self.asciiText.setText(u"")
            self.logLab.setText(
                u"<font color=#A52A2A>Rien à compresser.</font>")
            return
        self.occ = {}
        self.tree = ()
        self.hCodes = {}
        self.aCodes = {}
        self.hCost = {}
        self.aCost = {}
        self.hSqueezed = []
        self.aSqueezed = []
        self.stringHSqueezed = ''
        self.stringASqueezed = ''
        if wizard:
            self.launch_wizard(
                EncodeWizard(self),
                u"<font color=#008000>Compression achevée.</font>")
        else:
            self.make_occ()
            self.make_tree()
            self.make_codes()
            self.make_cost()
            self.make_encoded_text()
            self.make_comp()

    def decode_text(self, wizard=True):
        """Décode le texte compressé."""
        self.codeString = str(
            self.compressedText.toPlainText().replace(' ', ''))
        if not self.codeString or not self.hCodes:
            self.orgText.setText(u"")
            self.asciiText.setText(u"")
            if not self.codeString:
                self.logLab.setText(
                    u"<font color=#A52A2A>Rien à décompresser.</font>")
            if not self.hCodes:
                self.logLab.setText(
                    u"<font color=#A52A2A>Dictionnaire indisponible pour la décompression.</font>")
            return
        self.text = ''
        self.stringASqueezed = ''
        if wizard:
            self.launch_wizard(
                DecodeWizard(self),
                u"<font color=#008000>Texte décompressé.</font>")
        else:
            self.make_code_map()
            self.make_decoded_text()

    def launch_wizard(self, wizard, finishString):
        """Lance l'assistant d'en/décodage pour guider l'utilisateur.
        Cache les options inaccessibles pendant l'assistant.
        """
        self.logLab.setText(
            u"<font color=#9E6A00>Opération en cours. "
            u"Suivre les indications.</font>")
        disItems = [self.orgText, self.compressedText, self.encodeBut,
                    self.decodeBut, self.fileMenu.actions()[1],
                    self.fileMenu.actions()[2], self.fileMenu.actions()[3]]
        for item in disItems:
            item.setEnabled(False)
        self.compGroup.setVisible(False)
        self.analysGrid.addWidget(wizard, 0, 0, 1, 1)
        res = wizard.exec_()
        if res:
            self.logLab.setText(finishString)
        else:
            self.logLab.setText(
                u"<font color=#A52A2A>Opération interrompue.</font>")
        for item in disItems:
            item.setEnabled(True)
        self.compGroup.setVisible(True)

    def update_ratio_lab(self):
        """Replace la valeur du label du ratio de compression."""
        if not self.stringASqueezed:
            val = '/'
        else:
            val = (len(self.stringHSqueezed.replace(' ', '')) /
                   float(len(self.stringASqueezed.replace(' ', ''))))
        self.ratioLab.setText(unicode('Taux de compression:  ' + str(val)))

    def update_comp_table(self):
        """Met à jour le tableau de comparaison ASCII VS Huffman."""
        self.compTabASCIIMem.setText(unicode(len(''.join(self.aSqueezed))))
        self.compTabHuffMem.setText(unicode(len(''.join(self.hSqueezed))))
        # entropie ?
        self.compTabASCIIEnt.setText('0')
        self.compTabHuffEnt.setText('0')
        self.compTabASCIIAvg.setText(unicode(8))
        self.compTabHuffAvg.setText(unicode(
            average_code_length(self.hSqueezed)))
        self.compTable.resizeColumnsToContents()

    def update_codes_table(self, hlRow=[]):
        """Met à jour le tableau des codes et surligne les lignes de hlRow."""
        self.codesTableModel.hlRow = hlRow
        self.codesTableModel.emptyTable()
        self.codesTableModel.fillTable(self.make_tab_rows())
        self.codesTable.resizeColumnsToContents()

    def centerAndResize(self):
        """Centre et redimmensionne le widget.""" 
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 1.6, screen.height() / 1.4)
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2)

    #===================== METHODS FOR EN/DECODE WIZARDS =====================#
    def make_encode_init(self):
        self.compressedText.setText(unicode(self.stringHSqueezed))
        self.asciiText.setText(unicode(self.stringASqueezed))
        self.orgText.setTextColor(QColor(Qt.darkGreen))
        self.orgText.setText(unicode(self.text.decode('utf-8')))
        self.update_codes_table()

    def make_occ(self):
        self.orgText.setTextColor(QColor(Qt.white))
        self.orgText.setText(unicode(self.text.decode('utf-8')))
        self.occ = occurences(self.text)
        self.update_codes_table([0, 1])

    def make_tree(self):
        self.tree = make_trie(self.occ)
        self.update_codes_table()

    def make_codes(self):
        self.hCodes = make_codes(self.tree, {})
        self.aCodes = make_ascii_codes(self.occ.keys(), {})
        self.update_codes_table([2, 3])

    def make_cost(self):
        self.hCost = tree_cost(self.hCodes, self.occ)
        self.aCost = tree_cost(self.aCodes, self.occ)
        self.update_codes_table([4, 5])

    def make_encoded_text(self):
        self.hSqueezed = squeeze(self.text, self.hCodes)
        self.aSqueezed = squeeze(self.text, self.aCodes)
        self.stringHSqueezed = ' '.join(self.hSqueezed)
        self.stringASqueezed = ' '.join(self.aSqueezed)
        self.compressedText.setTextColor(QColor(Qt.darkGreen))
        self.asciiText.setTextColor(QColor(Qt.darkYellow))
        self.compressedText.setText(unicode(self.stringHSqueezed))
        self.asciiText.setText(unicode(self.stringASqueezed))
        self.update_codes_table()

    def make_comp(self):
        self.compressedText.setTextColor(QColor(Qt.white))
        self.asciiText.setTextColor(QColor(Qt.white))
        self.compressedText.setText(unicode(self.stringHSqueezed))
        self.asciiText.setText(unicode(self.stringASqueezed))
        self.update_codes_table()
        self.update_comp_table()
        self.update_ratio_lab()

    def make_decode_init(self):
        self.orgText.setText(unicode(self.text))
        self.asciiText.setText(unicode(self.stringASqueezed))
        self.compressedText.setTextColor(QColor(Qt.darkGreen))
        self.compressedText.setText(self.compressedText.toPlainText())

    def make_code_map(self):
        self.compressedText.setTextColor(QColor(Qt.white))
        self.compressedText.setText(self.compressedText.toPlainText())
        self.orgText.setText(unicode(self.text))
        self.asciiText.setText(unicode(self.stringASqueezed))
        self.codeMap = dict(zip(self.hCodes.values(), self.hCodes.keys()))
        self.update_codes_table([0, 3])

    def make_decoded_text(self):
        self.unSqueezed = unsqueeze(self.codeString, self.codeMap)
        self.text = ''.join(self.unSqueezed)
        self.orgText.setTextColor(QColor(Qt.darkGreen))
        self.orgText.setText(unicode(self.text.decode('utf-8')))
        self.asciiText.setText(unicode(self.stringASqueezed))
        self.update_codes_table()

    def make_ascii_decode(self):
        self.orgText.setTextColor(QColor(Qt.white))
        self.orgText.setText(unicode(self.text.decode('utf-8')))
        self.aCodes = make_ascii_codes(self.codeMap.values(), {})
        self.aSqueezed = squeeze(self.text, self.aCodes)
        self.stringASqueezed = ' '.join(self.aSqueezed)
        self.occ = occurences(self.text)
        self.hCost = tree_cost(self.hCodes, self.occ)
        self.aCost = tree_cost(self.aCodes, self.occ)
        self.asciiText.setTextColor(QColor(Qt.darkGreen))
        self.asciiText.setText(unicode(self.stringASqueezed))
        self.update_codes_table([1, 2, 4, 5])


#============================ CLASS FOR THE TABLE ============================#
class MyTableModel(QAbstractTableModel):
    """Contient les données récoltées par le programme lors
    de l'encodage de Huffman d'un texte.
    """
    def __init__(self, tabList=None, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__headers = [
            'Char', 'Freq', 'ASCII', 'Huff', u'Ĉ ASCII', u'Ĉ Huff']
        if tabList is None:
            tabList = [['' for x in range(len(self.__headers))]]
        for x in range(len(tabList)):
            missingCols = len(self.__headers) - len(tabList[x])
            for x in range(missingCols):
                tabList[x].append('/')
        self.__tabList = tabList
        self.hlRow = []

    def rowCount(self, parent=None):
        return len(self.__tabList)

    def columnCount(self, parent=None):
        if len(self.__tabList) is 0:
            return 0
        return len(self.__tabList[0])

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        if role == Qt.ForegroundRole and index.column() in self.hlRow:
                return QColor(Qt.darkGreen)
        if role == Qt.EditRole:
            return self.__tabList[index.row()][index.column()]
        if role == Qt.ToolTipRole:
            return str(self.__tabList[index.row()][index.column()])
        if role == Qt.DecorationRole:
            return None
        if role == Qt.DisplayRole:
            return self.__tabList[index.row()][index.column()]

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.__tabList[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "N/A"

    def sort(self, col, order):
        """Trie la table selon une colonne."""
        self.layoutAboutToBeChanged.emit()
        self.__tabList = sorted(self.__tabList, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.__tabList.reverse()
        self.layoutChanged.emit()

    def emptyTable(self):
        self.removeRows(0, self.rowCount())
        return True

    def fillTable(self, tabList):
        self.beginInsertRows(QModelIndex(), 0, len(tabList))
        for x in tabList:
            self.__tabList.insert(self.rowCount(), x)
        self.endInsertRows()
        
    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in reversed(range(rows)):
            self.__tabList.pop(i)
        self.endRemoveRows()
        return True

#================================== PROGRAMM =================================#
if __name__ == '__main__':
    app = QApplication([])  # la gui globale
    win = Ui_MainWindow()
    win.show()
    app.exec_()
