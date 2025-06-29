# Input PC Recorder

**Author:** Bocaletto Luca

**Language:** Python

## Overview

Input PC Recorder is a simple Python application for recording audio from your PC's input devices. It provides a user-friendly interface to select input devices, bit depth, and sample rate, and allows you to start and stop audio recordings.

![Screenshot 2023-10-13 064242](https://github.com/elektronoide/Input-PC-Recorder/assets/134635227/98cb4bed-0fd4-4d23-abd9-f50903023535)

## Features

- Select input audio device.
- Choose bit depth (8-bit, 16-bit, 24-bit) and sample rate (44100 Hz, 48000 Hz, 96000 Hz, 192000 Hz).
- Start and stop audio recording.
- Monitor the recording intensity in real-time.
- Save the recorded audio to a WAV file.

## Installation

1. Clone or download this repository to your local machine.
2. Install the required Python packages using pip:

   ```bash
   pip install sounddevice soundfile PyQt5 numpy

# Run the application:

python input_pc_recorder.py

## Usage

1. Launch the application.
2. Select your desired input device from the dropdown menu.
3. Choose the bit depth and sample rate.
4. Click the "Start Recording" button to begin recording audio.
5. Click the "Stop Recording" button to stop the recording and save the audio to a WAV file.
6. The intensity of the recording is displayed in real-time.

## License

This project is licensed under the GPLv3 License. See the LICENSE file for more details.

## Support

For support or inquiries, please visit [elektronoide.it](https://www.elektronoide.it).

## Acknowledgments

This project makes use of the following Python libraries:

- [sounddevice](https://python-sounddevice.readthedocs.io/en/1.0.3/)
- [soundfile](https://pysoundfile.readthedocs.io/en/0.10.3/)
- [PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

Special thanks to the open-source community for their contributions.

---

**Maintainer Update**

All legacy projects from the old `@Elektronoide` GitHub account are now officially maintained by **@bocaletto-luca**. Please direct any issues, pull requests, and stars to **@bocaletto-luca** for all future updates.

---
