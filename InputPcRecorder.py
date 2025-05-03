# Software Name: Input PC Recorder
# Author: Luca Bocaletto
# License: GPLv3
import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QTimer

# Main app class definition
class AudioRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window settings
        self.setWindowTitle("Audio Recorder")  # Set the main window title
        self.setGeometry(100, 100, 400, 200)  # Set the position and dimensions of the window

        # Create the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the main layout
        self.layout = QVBoxLayout()

        # Create user interface widgets
        self.device_combo = QComboBox()  # Dropdown menu for device selection
        self.layout.addWidget(self.device_combo)

        self.bit_depth_combo = QComboBox()  # Dropdown menu for bit depth
        self.bit_depth_combo.addItems(["8 bit", "16 bit", "24 bit"])
        self.layout.addWidget(self.bit_depth_combo)

        self.sample_rate_combo = QComboBox()  # Dropdown menu for sample rate
        self.sample_rate_combo.addItems(["44100 Hz", "48000 Hz", "96000 Hz", "192000 Hz"])
        self.layout.addWidget(self.sample_rate_combo)

        self.start_button = QPushButton("Start Recording")  # Button to start recording
        self.stop_button = QPushButton("Stop Recording")  # Button to stop recording
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)

        self.intensity_label = QLabel("Intensity: 0")  # Label to display intensity
        self.layout.addWidget(self.intensity_label)

        self.central_widget.setLayout(self.layout)

        # Audio state and data variables
        self.is_recording = False
        self.selected_device_index = None
        self.audio_data = []

        # Connect buttons to slots
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        # Set a timer for intensity updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_intensity)
        self.timer.start(1000)

        # Get the list of audio devices
        self.device_info = sd.query_devices()
        self.device_names = []  # List to store device names without duplicates

        for i, info in enumerate(self.device_info):
            if info["max_input_channels"] > 0:
                device_name = f"{info['name']} ({info['max_input_channels']} channels)"
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
            QMessageBox.critical(self, "Error", "Select a valid input device.")
            return

        bit_depth_text = self.bit_depth_combo.currentText()
        sample_rate_text = self.sample_rate_combo.currentText()

        self.sample_rate = int(sample_rate_text.split()[0])
        self.bit_depth = int(bit_depth_text.split()[0])

        try:
            if self.device_info[self.selected_device_index]["max_input_channels"] < 1:
                QMessageBox.critical(self, "Error", "The selected device does not support audio input.")
                return

            self.is_recording = True
            self.audio_data = []

            self.p = sd.InputStream(device=self.selected_device_index, channels=1, samplerate=self.sample_rate, callback=self.audio_callback)
            self.p.start()
            QMessageBox.information(self, "Recording Started", "Recording has started.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error while starting the recording: {str(e)}")

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
                    QMessageBox.information(self, "Recording Stopped", "Recording has been stopped, and the audio file has been saved.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error while saving the audio file: {str(e)}")

    def audio_callback(self, in_data, frames, time, status):
        if self.is_recording:
            audio_chunk = np.frombuffer(in_data, dtype=np.int16)
            self.audio_data.extend(audio_chunk)

    def update_intensity(self):
        if self.is_recording:
            if len(self.audio_data) > 0:
                intensity = int(np.abs(np.mean(self.audio_data)))
                self.intensity_label.setText(f"Intensity: {intensity}")

    def save_audio_file(self):
        try:
            filename = f"audio_recording_{self.device_info[self.selected_device_index]['name']}.wav"
            sf.write(filename, self.audio_data, self.sample_rate, subtype=f'PCM_{self.bit_depth}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error while saving the audio file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioRecorderApp()
    window.show()
    sys.exit(app.exec_())
