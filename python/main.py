import sys
from ui import STM32Interface
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = STM32Interface()
    fenetre.show()
    anim = QPropertyAnimation(fenetre, b"windowOpacity")
    anim.setDuration(500)
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.setEasingCurve(QEasingCurve.InOutQuad)
    anim.start()
    sys.exit(app.exec_())