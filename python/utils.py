import serial
import serial.tools.list_ports
import time
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QColor

def lister_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def envoyer_commande(widget):
    port = widget.port_combo.currentText()
    test_nom = widget.test_combo.currentText()
    commande = widget.tests[test_nom]

    widget.button.setEnabled(False)
    widget.progress.setVisible(True)
    widget.progress.setValue(0)

    anim = widget.anim = widget.findChild(type(None), "progressAnimation") or QPropertyAnimation(widget.progress, b"value")
    anim.setDuration(5000)
    anim.setStartValue(0)
    anim.setEndValue(100)
    anim.start()

    try:
        ser = serial.Serial(port, baudrate=115200, timeout=0.1)
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(commande)
        lines = []
        start_time = time.time()
        while time.time() - start_time < 5:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                lines.append(line)
                progress = min(100, int((len(lines) / max(1, 10)) * 100))
                widget.progress.setValue(progress)
            time.sleep(0.05)
        ser.close()
        heure = datetime.now().strftime("[%H:%M:%S]")
        for i, line in enumerate(lines):
            widget.reponse_text.append(f"{heure} Réponse : {line}")
            add_to_table(widget, line, test_nom)
    except Exception as e:
        QMessageBox.critical(widget, "Erreur", f"Erreur de communication avec {port}.\n{e}")
    finally:
        widget.progress.setValue(100)
        anim.stop()
        time.sleep(0.2)
        widget.progress.setVisible(False)
        widget.button.setEnabled(True)

def add_to_table(widget, line, test_nom):
    row = widget.table.rowCount()
    widget.table.insertRow(row)
    status = "Info"
    details = line
    test_name = test_nom
    if test_nom == "Tous les tests":
        if "START" in line or "END" in line:
            test_name = "Système"
        elif "SYSTEM OK" in line or "SYSTEM ERROR" in line:
            test_name = "Système"
        elif "LED" in line:
            test_name = "LED"
        elif "BUTTON" in line:
            test_name = "Bouton"
        elif "UART" in line:
            test_name = "UART"
        elif "ADC" in line:
            test_name = "ADC"
        elif "SPI" in line:
            test_name = "SPI"
        elif "I2C" in line or "MPU" in line:
            test_name = "I2C"
        elif "PWM" in line:
            test_name = "Timer"
    else:
        test_name = test_nom
    if "OK" in line:
        status = "Succès"
    elif "FAIL" in line or "ERROR" in line:
        status = "Échec"
    status_icon = "ℹ️"
    if status == "Succès":
        status_icon = "✅"
    elif status == "Échec":
        status_icon = "❌"
    status_text = f"{status_icon} {status}"
    test_item = QTableWidgetItem(test_name)
    status_item = QTableWidgetItem(status_text)
    details_item = QTableWidgetItem(details)
    status_item.setTextAlignment(Qt.AlignCenter)
    if status == "Succès":
        status_item.setBackground(QColor(200, 255, 200))
    elif status == "Échec":
        status_item.setBackground(QColor(255, 200, 200))
    elif status == "Info":
        status_item.setBackground(QColor(200, 200, 255))
    widget.table.setItem(row, 0, test_item)
    widget.table.setItem(row, 1, status_item)
    widget.table.setItem(row, 2, details_item)

def export_results(widget):
    import csv
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.csv"
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Test", "Statut", "Détails"])
            for row in range(widget.table.rowCount()):
                test = widget.table.item(row, 0).text() if widget.table.item(row, 0) else ""
                status = widget.table.item(row, 1).text()[2:].strip() if widget.table.item(row, 1) else ""
                details = widget.table.item(row, 2).text() if widget.table.item(row, 2) else ""
                writer.writerow([test, status, details])
        QMessageBox.information(widget, "Succès", f"Résultats exportés dans {filename}")
    except Exception as e:
        QMessageBox.critical(widget, "Erreur", f"Erreur lors de l'exportation : {e}")

def clear_results(widget):
    widget.table.setRowCount(0)
    widget.reponse_text.clear()
    widget.progress.setValue(0)