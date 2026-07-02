# Smart Braille Digital Slate

A paperless, low-cost, multi-language tactile ecosystem designed to modernize Braille writing for the visually impaired. 

## The Problem
The traditional Braille slate and stylus system creates a heavy burden in paper management, sharing, and storage. Existing digital Braille displays are highly expensive, often exceeding ₹100,000, putting them out of reach for most users.

## The Solution
This project bridges the gap by proposing a hybrid digital-tactile slate that preserves the natural writing motion of the visually impaired but digitizes the output instantly. By separating the input matrix from the mechanical reading output, we reduce the required mechanical actuators by 95%, bringing the estimated prototype cost down to between ₹15,000 and ₹25,000.

## Key Features
* **Digital Matrix Input:** Writes like a standard slate but registers digital coordinates with zero moving parts in the writing area.
* **Instant Digitization & Erasability:** Mistakes can be toggled off with a double-tap.
* **Multi-Language Translation Engine:** Converts Braille input into standard English, Hindi, or Tamil text instantly.
* **Integrated Text-to-Speech (TTS):** Speaks the translated text aloud for instant auditory feedback.

## Project Structure
* `emulator/`: Contains the Python-based GUI emulator representing a 20-cell Braille slate.
* `firmware/`: Contains the production-ready ESP32 C++ code for matrix scanning and hardware debouncing.

## Quick Start Guide (Software Emulator)

To run the software proof-of-concept on your local machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Smart-Braille-Slate.git](https://github.com/YOUR_USERNAME/Smart-Braille-Slate.git)
   cd Smart-Braille-Slate

2. **Set up the virtual environment:**
python -m venv brail
# Windows activation:
.\brail\Scripts\activate
# Mac/Linux activation:
source brail/bin/activate

3. **Install dependencies:**
pip install -r requirements.txt

4. **Run the Emulator:**
python emulator/slate_emulator.py



## Hardware Architecture

* **Microcontroller:** ESP32 for GPIO multiplexing and local SPIFFS memory management.

* **Input:** Solid-state membrane keypad matrix beneath a standard Braille stencil.

* **Actuation (Future Scope):** 1-cell or 2-cell dynamic Shape Memory Alloy (SMA) Nitinol reader to replace expensive piezoelectric strips.