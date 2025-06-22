def apply_theme(widget):
    is_dark_theme = getattr(widget, 'is_dark_theme', False)
    if is_dark_theme:
        widget.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QComboBox {
                background-color: #3C3C3C;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 4px;
            }
            QTableWidget {
                background-color: #3C3C3C;
                alternate-background-color: #4A4A4A;
                gridline-color: #555555;
                border: 1px solid #555555;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 5px;
                color: #FFFFFF;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #444444;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 2px;
                font-size: 14px;
            }
            QHeaderView::section:hover {
                background-color: #555555;
            }
            QTextEdit {
                background-color: #3C3C3C;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border: 1px solid #777777;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QProgressBar {
                background-color: #4A4A4A;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
            QMenuBar {
                background-color: #2D2D2D;
                color: #FFFFFF;
            }
            QMenuBar::item {
                background-color: #2D2D2D;
                color: #FFFFFF;
            }
            QMenuBar::item:selected {
                background-color: #555555;
            }
        """)
    else:
        widget.setStyleSheet("""
            QWidget {
                background-color: #E6ECEF;
                color: #1A3C63;
            }
            QLabel {
                color: #1A3C63;
            }
            QComboBox {
                background-color: #FFFFFF;
                color: #1A3C63;
                border: 1px solid #4A90E2;
                border-radius: 4px;
            }
            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #D9E4F5;
                gridline-color: #B0C4DE;
                border: 1px solid #B0C4DE;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 5px;
                color: #1A3C63;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #E6ECEF;
                color: #1A3C63;
                border: 1px solid #B0C4DE;
                padding: 2px;
                font-size: 14px;
            }
            QHeaderView::section:hover {
                background-color: #D9E4F5;
            }
            QTextEdit {
                background-color: #FFFFFF;
                color: #1A3C63;
                border: 1px solid #B0C4DE;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #4A90E2;
                color: #FFFFFF;
                border: 1px solid #357ABD;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QProgressBar {
                background-color: #D3DCE6;
                color: #1A3C63;
                border: 1px solid #B0C4DE;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #6BCB77;
                border-radius: 4px;
            }
            QMenuBar {
                background-color: #E6ECEF;
                color: #1A3C63;
            }
            QMenuBar::item {
                background-color: #E6ECEF;
                color: #1A3C63;
            }
            QMenuBar::item:selected {
                background-color: #4A90E2;
                color: #FFFFFF;
            }
        """)