import sys
import tempfile
from settings import *
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QVBoxLayout, QStatusBar, QToolBar, QLabel, QLineEdit, QPushButton, QSpinBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        ### initialisation des variables

        # détection des changements
        self.changedFile = False
        self.changedInfo = False

        # limites du nombre de colonnes et de diagrames
        self.max_cols = 5
        self.max_diags = 15

        # chargement des paramètres
        settingFile = getSettingsFile()
        self.appSettings = getSettings(settingFile)
        self.userInput = initializeUserInput()
        self.imagesDict = initializeImagesDict()
        self.activeEditor = int()

        # création du fichier temporaire d'image plateau
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_board_file:
            self.temp_board_path = temp_board_file.name

        # localisation du dossier actif suivant le mode d'exécution
        if getattr(sys, 'frozen', False):
            self.base_dir = sys._MEIPASS
        else:
            self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            
        self.resources_dir = os.path.join(self.base_dir, "resources")

        # mise en place du titre de la fenêtre
        self.currentFileName = "Nouveau document"
        self.newFileName = ""
        self.setWindowTitle(self.currentFileName + " | EZDraw Diagramm Generator")
        self.setWindowIcon(QIcon(os.path.join(self.resources_dir, "chess.png")))
        
        ### Définition des widgets et layouts
        self.mainWidget = QWidget()

        self.setCentralWidget(self.mainWidget)

        self.layMain = QVBoxLayout()
        self.layTitle = QGridLayout()
        self.layNum = QGridLayout()
        self.layForm = QGridLayout()

        self.layMain.addLayout(self.layTitle)
        self.layMain.addLayout(self.layForm)
        self.layMain.addLayout(self.layNum)
        self.mainWidget.setLayout(self.layMain)

        
        # Définition des actions
        self.act_New = QAction(QIcon(os.path.join(self.resources_dir, "add-document.png")), "Nouveau document", self)
        self.act_Open = QAction(QIcon(os.path.join(self.resources_dir, "folder-open.png")), "Ouvrir un formulaire", self)
        self.act_Save = QAction(QIcon(os.path.join(self.resources_dir, "save.png")), "Enregistrer le formulaire", self)
        self.act_Save_as = QAction(QIcon(os.path.join(self.resources_dir, "save-as.png")), "Enregistrer le formulaire sous", self)
        self.act_PGN = QAction(QIcon(os.path.join(self.resources_dir, "overview.png")), "Ouvrir un fichier pgn", self)
        self.act_Img = QAction(QIcon(os.path.join(self.resources_dir, "search.png")), "Aperçu de la page", self)
        self.act_Save_img = QAction(QIcon(os.path.join(self.resources_dir, "image.png")), "Enregistrer la page", self)
        self.act_Save_diags = QAction(QIcon(os.path.join(self.resources_dir, "images.png")), "Enregistrer les diagrammes", self)
        self.act_Settings = QAction(QIcon(os.path.join(self.resources_dir, "settings.png")), "Paramètres", self)
        self.act_Help = QAction(QIcon(os.path.join(self.resources_dir, "help.png")), "Aide", self)
        self.act_About = QAction(QIcon(os.path.join(self.resources_dir, "info.png")), "À propos", self)
        self.act_Exit = QAction(QIcon(os.path.join(self.resources_dir, "power.png")), "Quitter", self)

        self.act_New.setStatusTip("Nouveau document")
        self.act_New.setShortcut(QKeySequence("Ctrl+n"))
        # self.act_New.triggered.connect(self.newDoc)

        self.act_Open.setStatusTip("Ouvrir un formulaire")
        self.act_Open.setShortcut(QKeySequence("Ctrl+o"))
        # self.act_Open.triggered.connect(self.openDoc)

        self.act_Save.setStatusTip("Enregistrer le formulaire")
        self.act_Save.setShortcut(QKeySequence("Ctrl+s"))
        # self.act_Save.triggered.connect(self.saveForm)

        self.act_Save_as.setStatusTip("Enregistrer sous")
        self.act_Save_as.setShortcut(QKeySequence("Ctrl+Shift+s"))
        # self.act_Save_as.triggered.connect(self.saveAs)

        self.act_PGN.setStatusTip("Ouvrir un fichier pgn")
        self.act_PGN.setShortcut(QKeySequence("Ctrl+t"))
        # self.act_PGN.triggered.connect(self.openPgn)

        self.act_Img.setStatusTip("Aperçu de la page de diagrammes")
        self.act_Img.setShortcut(QKeySequence("Ctrl+Shift+o"))
        # self.act_Img.triggered.connect(self.preview)

        self.act_Save_img.setStatusTip("Enregistrer l'image de la page")
        self.act_Save_img.setShortcut(QKeySequence("Ctrl+i"))
        # self.act_Save_img.triggered.connect(self.saveImg)

        self.act_Save_diags.setStatusTip("Enregistrer une image par diagramme")
        self.act_Save_diags.setShortcut(QKeySequence("Ctrl+Shift+i"))
        # self.act_Save_diags.triggered.connect(self.saveDiags)

        self.act_Settings.setStatusTip("Paramètres")
        self.act_Settings.setShortcut(QKeySequence("Ctrl+Shift+p"))
        # self.act_Settings.triggered.connect(self.openProp)

#       self.act_PGN = QAction(QIcon.fromTheme("document-print"), "Imprimer", self)
#       self.act_PGN.setStatusTip("Imprimer")
#       self.act_PGN.setShortcut(QKeySequence("Ctrl+p"))
#       self.act_PGN.triggered.connect(self.print)

        self.act_Help.setStatusTip("Aide")
        self.act_Help.setShortcut(QKeySequence("Ctrl+h"))
        # self.act_Help.triggered.connect(self.openHelp)

        self.act_About.setStatusTip("À propos")
        # self.act_About.triggered.connect(self.openAbout)

        self.act_Exit.setStatusTip("Quitter")
        self.act_Exit.setShortcut(QKeySequence("Ctrl+q"))
        # self.act_Exit.triggered.connect(self.quit)

        # Définition de la barre d'outils
        self.toolbar = QToolBar("Main toolbar")
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.act_New)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Open)
        self.toolbar.addAction(self.act_PGN)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Save)
        self.toolbar.addAction(self.act_Save_as)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Img)
        self.toolbar.addAction(self.act_Save_img)
        self.toolbar.addAction(self.act_Save_diags)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Settings)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_Help)
        self.toolbar.addAction(self.act_About)

        # Définition de la barre de menu
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("&Fichier")

        self.fileMenu.addAction(self.act_New)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Open)
        self.fileMenu.addAction(self.act_PGN)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Save)
        self.fileMenu.addAction(self.act_Save_as)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Img)
        self.fileMenu.addAction(self.act_Save_img)
        self.fileMenu.addAction(self.act_Save_diags)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Settings)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.act_Exit)


        self.fileHelp = self.menu.addMenu("&Aide")
        self.fileHelp.addAction(self.act_Help)
        self.fileHelp.addAction(self.act_About)

        # Définition de la barre de status
        self.setStatusBar(QStatusBar(self))
        # self.load_widgets()

        i = 0
        while i < self.max_diags:
            self.userInput["fens"].append("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
            self.userInput["legends"].append("Position de départ")
            self.userInput["symbols"].append("0000000000000000000000000000000000000000000000000000000000000000")
            self.userInput["arrows"].append([])
            i += 1
        i = 0

        self.load_widgets()

    def load_widgets(self):
        i = 1
        # Section de titre
        if self.appSettings["title_state"] == True:
            self.layTitle.addWidget(QLabel("Titre : "), 0, 0)
            self.title_text = QLineEdit("")
            self.title_text.setText(self.userInput["title_text"])
            # self.title_text.textChanged.connect(self.change_title_text)
            self.layTitle.addWidget(self.title_text, 0, 1)

        # Section de formulaire
        self.layForm.addWidget(QLabel("            Saisir un FEN ou un identifiant de problème Lichess            "), 0, 1)

        if self.appSettings["legend_state"]:
            self.layForm.addWidget(QLabel("       Saisir une légende       "), 0, 3)

        self.fens = list()
        self.legends = list()
        self.edits = list()

        while i <= int(self.appSettings["diags_value"]):

            self.layForm.addWidget(QLabel("Fig." + str(i)), i, 0)

            self.fens.append(QLineEdit(self.userInput["fens"][i-1]))
            self.fens[i-1].id = i-1
            # self.fens[i-1].textChanged.connect(self.change_fens)
            self.layForm.addWidget(self.fens[i-1], i, 1)

            if self.appSettings["legend_state"] == True:
                self.legends.append(QLineEdit(self.userInput["legends"][i-1]))
                self.legends[i-1].id = i-1
                # self.legends[i-1].textChanged.connect(self.change_legends)
                self.layForm.addWidget(self.legends[i-1], i, 3)

            self.edits.append(QPushButton("Éditeur graphique"))
            self.edits[i-1].id = i-1
            # self.edits[i-1].clicked.connect(self.openEdit)
            self.layForm.addWidget(self.edits[i-1], i, 4)
            i += 1

        # Section de numérotation
        if self.appSettings["numPage_state"] == True:
            self.layNum.addWidget(QLabel("Numéro de page"), 0, 0)
            self.numPage_value = QSpinBox()
            self.numPage_value.setValue(self.userInput["numPage_value"]) 
            # self.numPage_value.valueChanged.connect(self.change_numPage_value)
            self.layNum.addWidget(self.numPage_value, 0, 1)
        if self.appSettings["numDiag_state"] == True:
            self.layNum.addWidget(QLabel("Numéro du premier diagramme"), 1, 0)
            self.numDiag_value = QSpinBox()
            self.numDiag_value.setValue(self.userInput["numDiag_value"]) 
            # self.numDiag_value.valueChanged.connect(self.change_numDiag_value)
            self.layNum.addWidget(self.numDiag_value, 1, 1)

