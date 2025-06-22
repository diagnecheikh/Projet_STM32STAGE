from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QTableWidget, QProgressBar, QAction, QMenuBar
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from styles import apply_theme
from utils import lister_ports, envoyer_commande, add_to_table, export_results, clear_results

class STM32Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface STM32 - Banc de Test")
        self.setFixedSize(900, 800)
        self.is_dark_theme = False
        self.is_fullscreen = False
        self.tests = {
            "Tous les tests": b't',
            "Test LED": b'b',
            "Test Bouton": b'c',
            "Test UART": b'd',
            "Test ADC": b'e',
            "Test SPI": b'f',
            "Test I2C": b'g',
            "Test TIMER": b'h',
        }
        self.init_ui()

    def init_ui(self):
        # Création des menus
        menubar = QMenuBar(self)
        theme_menu = menubar.addMenu("Thème")
        toggle_theme_action = QAction("Basculer vers thème sombre", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        theme_menu.addAction(toggle_theme_action)

        display_menu = menubar.addMenu("Affichage")
        toggle_fullscreen_action = QAction("Basculer en plein écran", self)
        toggle_fullscreen_action.triggered.connect(self.toggle_fullscreen)
        display_menu.addAction(toggle_fullscreen_action)

        # Layout principal avec marges
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        main_layout.addWidget(menubar)
        main_layout.addSpacing(10)

        # Ajout du logo
        logo_label = QLabel(self)
        try:
            pixmap = QPixmap("./image_ubs1.png")
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                logo_label.setText("Logo non trouvé")
        except Exception:
            logo_label.setText("Erreur de chargement du logo")
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)
        main_layout.addSpacing(10)

        # Titre
        title_label = QLabel("Banc de Test STM32F411RE")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(10)

        # Sélection du port COM
        port_label = QLabel("Choisir le port COM :")
        port_label.setFont(QFont("Arial", 11))
        main_layout.addWidget(port_label)
        main_layout.addSpacing(5)

        self.port_combo = QComboBox()
        self.port_combo.addItems(lister_ports())
        main_layout.addWidget(self.port_combo)
        main_layout.addSpacing(10)

        # Sélection du test
        test_label = QLabel("Choisir un test à lancer :")
        test_label.setFont(QFont("Arial", 11))
        main_layout.addWidget(test_label)
        main_layout.addSpacing(5)

        self.test_combo = QComboBox()
        self.test_combo.addItems(self.tests.keys())
        main_layout.addWidget(self.test_combo)
        main_layout.addSpacing(10)

        # Bouton pour lancer le test
        self.button = QPushButton("Démarrer le test")
        self.button.clicked.connect(lambda: envoyer_commande(self))
        main_layout.addWidget(self.button)
        main_layout.addSpacing(10)

        # Tableau pour afficher les résultats
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Test", "Statut", "Détails"])
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 450)
        main_layout.addWidget(self.table)
        main_layout.addSpacing(10)

        # Zone de texte pour messages bruts
        self.reponse_text = QTextEdit()
        self.reponse_text.setReadOnly(True)
        self.reponse_text.setFixedHeight(150)
        main_layout.addWidget(self.reponse_text)
        main_layout.addSpacing(10)

        # Boutons "Exporter" et "Effacer"
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.export_button = QPushButton("Exporter en CSV")
        self.export_button.clicked.connect(lambda: export_results(self))
        button_layout.addWidget(self.export_button)

        self.clear_button = QPushButton("Effacer les résultats")
        self.clear_button.clicked.connect(lambda: clear_results(self))
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)
        main_layout.addSpacing(10)

        # Barre de progression
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

        main_layout.addStretch()

        self.setLayout(main_layout)

        apply_theme(self)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        apply_theme(self)
        menubar = self.findChild(QMenuBar)
        theme_menu = menubar.actions()[0].menu()
        theme_menu.actions()[0].setText("Basculer vers thème " + ("clair" if self.is_dark_theme else "sombre"))

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen()
            menubar = self.findChild(QMenuBar)
            display_menu = menubar.actions()[1].menu()
            display_menu.actions()[0].setText("Quitter le plein écran")
        else:
            self.showNormal()
            self.setFixedSize(900, 800)
            menubar = self.findChild(QMenuBar)
            display_menu = menubar.actions()[1].menu()
            display_menu.actions()[0].setText("Basculer en plein écran")