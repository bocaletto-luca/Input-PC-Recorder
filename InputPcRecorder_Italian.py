# Software Name: Input PC Recorder
# Author: Bocaletto Luca
# Site Web: https://www.elektronoide.it
# License: GPLv3
import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QTimer

# Definizione della classe principale dell'app
class AudioRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Impostazioni della finestra principale
        self.setWindowTitle("Audio Recorder")  # Imposta il titolo della finestra principale
        self.setGeometry(100, 100, 400, 200)  # Imposta posizione e dimensioni della finestra

        # Creazione del widget centrale
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Creazione del layout principale
        self.layout = QVBoxLayout()

        # Creazione dei widget dell'interfaccia utente
        self.device_combo = QComboBox()  # Menù a discesa per la selezione del dispositivo
        self.layout.addWidget(self.device_combo)

        self.bit_depth_combo = QComboBox()  # Menù a discesa per la profondità in bit
        self.bit_depth_combo.addItems(["8 bit", "16 bit", "24 bit"])
        self.layout.addWidget(self.bit_depth_combo)

        self.sample_rate_combo = QComboBox()  # Menù a discesa per la frequenza di campionamento
        self.sample_rate_combo.addItems(["44100 Hz", "48000 Hz", "96000 Hz", "192000 Hz"])
        self.layout.addWidget(self.sample_rate_combo)

        self.start_button = QPushButton("Avvia Registrazione")  # Pulsante per avviare la registrazione
        self.stop_button = QPushButton("Interrompi Registrazione")  # Pulsante per interrompere la registrazione
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)

        self.intensity_label = QLabel("Intensità: 0")  # Etichetta per mostrare l'intensità
        self.layout.addWidget(self.intensity_label)

        self.central_widget.setLayout(self.layout)

        # Variabili di stato e dati dell'audio
        self.is_recording = False
        self.selected_device_index = None
        self.audio_data = []

        # Connetti i pulsanti agli slot
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        # Imposta un timer per l'aggiornamento dell'intensità
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_intensity)
        self.timer.start(1000)

        # Ottieni la lista dei dispositivi audio
        self.device_info = sd.query_devices()
        self.device_names = []  # Lista per memorizzare i nomi dei dispositivi senza duplicati

        for i, info in enumerate(self.device_info):
            if info["max_input_channels"] > 0:
                device_name = f"{info['name']} ({info['max_input_channels']} canali)"
                if device_name not in self.device_names:
                    self.device_names.append(device_name)
                    self.device_combo.addItem(device_name)

        self.p = None
        self.sample_rate = 44100
        self.bit_depth = 16

    def start_recording(self):
        if self.is_recording:
            return

        self.selected_device_index = self.device_combo.currentIndex()
        if self.selected_device_index < 0:
            QMessageBox.critical(self, "Errore", "Seleziona un dispositivo di input valido.")
            return

        bit_depth_text = self.bit_depth_combo.currentText()
        sample_rate_text = self.sample_rate_combo.currentText()

        self.sample_rate = int(sample_rate_text.split()[0])
        self.bit_depth = int(bit_depth_text.split()[0])

        try:
            if self.device_info[self.selected_device_index]["max_input_channels"] < 1:
                QMessageBox.critical(self, "Errore", "Il dispositivo selezionato non supporta l'input audio.")
                return

            self.is_recording = True
            self.audio_data = []

            self.p = sd.InputStream(device=self.selected_device_index, channels=1, samplerate=self.sample_rate, callback=self.audio_callback)
            self.p.start()
            QMessageBox.information(self, "Registrazione Avviata", "La registrazione è iniziata.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante l'avvio della registrazione: {str(e)}")

    def stop_recording(self):
        if not self.is_recording:
            return

        self.is_recording = False
        if self.p:
            self.p.stop()
            self.p.close()

            if self.audio_data:
                try:
                    self.save_audio_file()
                    QMessageBox.information(self, "Registrazione Interrotta", "La registrazione è stata interrotta e il file audio è stato salvato.")
                except Exception as e:
                    QMessageBox.critical(self, "Errore", f"Errore durante il salvataggio del file audio: {str(e)}")

    def audio_callback(self, in_data, frames, time, status):
        if self.is_recording:
            audio_chunk = np.frombuffer(in_data, dtype=np.int16)
            self.audio_data.extend(audio_chunk)

    def update_intensity(self):
        if self.is_recording:
            if len(self.audio_data) > 0:
                intensity = int(np.abs(np.mean(self.audio_data)))
                self.intensity_label.setText(f"Intensità: {intensity}")

    def save_audio_file(self):
        try:
            filename = f"registrazione_audio_{self.device_info[self.selected_device_index]['name']}.wav"
            sf.write(filename, self.audio_data, self.sample_rate, subtype=f'PCM_{self.bit_depth}')
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante il salvataggio del file audio: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioRecorderApp()
    window.show()
    sys.exit(app.exec_())
