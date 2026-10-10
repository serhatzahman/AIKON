# AIKON for Nokia N9 (MeeGo 1.2 Harmattan)

[![Platform: MeeGo 1.2 Harmattan](https://img.shields.io/badge/platform-MeeGo%201.2%20Harmattan-blue.svg)](https://en.wikipedia.org/wiki/MeeGo)
[![Device: Nokia N9](https://img.shields.io/badge/device-Nokia%20N9%20(RM--696)-lightgrey.svg)](https://en.wikipedia.org/wiki/Nokia_N9)
[![UI: Sailfish OS Silica Ambiance](https://img.shields.io/badge/UI-Sailfish%20OS%20Silica-cyan.svg)](https://sailfishos.org/)
[![Protocol: S40/1 Gateway](https://img.shields.io/badge/protocol-S40%2F1%20Gateway-green.svg)](https://github.com/emir/AIKON)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Language: Turkish](https://img.shields.io/badge/lang-T%C3%BCrk%C3%A7e-red.svg)](README_TR.md)

> **English** | [Türkçe](README_TR.md)

A native modern AI chat client designed for the legendary **Nokia N9** running **MeeGo 1.2 Harmattan**. Powered by Python 2.7, PySide, and Qt Quick 1.1, featuring a gorgeous **Sailfish OS (Silica)** translucent glass ambiance, full-screen AMOLED dark aesthetic, and a lightweight local PC bridge communicating over the **S40/1 gateway protocol**.

---

## 📸 Screenshots

Captured live on Nokia N9 hardware (480×854 AMOLED):

| Chat Experience & Literary Analysis | Live Weather & Dynamic Conversation |
| :---: | :---: |
| <img src="screenshots/screenshot1.png" width="340" alt="Nokia N9 AIKON Chat 1" /> | <img src="screenshots/screenshot2.png" width="340" alt="Nokia N9 AIKON Chat 2" /> |
| *Crisp 22px Nokia Pure typography with wide frosted glass bubbles* | *Real-time conversational responses running on MeeGo 1.2 Harmattan* |

---

## ✨ Features

- **Sailfish OS Silica Ambiance**: Designed from the ground up with deep oceanic gradients (`#081018` to `#000000`), frosted glass translucent bubbles, glowing cyan accents (`#00D2FF`), and the iconic top Pulley Menu.
- **AMOLED-Optimized Typography**: Enhanced 22px body font and 20px input text using the native *Nokia Pure Text* font engine for readability on the 3.9" 251 ppi screen.
- **Hardware Ergonomics**: Seamless virtual keyboard integration with instant send-on-Enter (`onAccepted`), full-screen portrait orientation lock, and 10px bezel-safe bottom margin.
- **S40/1 Gateway Protocol**: Bypasses legacy TLS/OpenSSL handshake limitations on vintage mobile operating systems by bridging requests over Wi-Fi through a lightweight PC companion server.
- **Multi-Provider AI Bridge**:
  - **Free Live AI Engine** (Built-in, zero configuration, no API key needed).
  - **Anthropic Claude** (Claude 3.5 Sonnet / Haiku).
  - **OpenAI** (GPT-4o / GPT-4o-mini).
  - **Google Gemini** (Gemini 1.5 Flash).
  - **Groq** (LLaMA 3.3 70B Versatile).
  - **Local Ollama** (Self-hosted offline LLMs).
- **OTA Asset Sync**: Built-in HTTP server capability in `server.py` allowing instant Over-The-Air QML/Python updates to the N9 via local Wi-Fi.

---

## 🏗️ Architecture

```
 ┌──────────────────────┐             HTTP (Wi-Fi)            ┌────────────────────────┐             HTTPS             ┌─────────────────────────┐
 │       Nokia N9       │   S40/1 Wire Protocol (Plaintext)   │    AIKON PC Bridge     │   Modern TLS 1.3 / REST API   │     Cloud AI Models     │
 │ (MeeGo 1.2 Harmattan)│ ──────────────────────────────────> │      (server.py)       │ ────────────────────────────> │  • Claude 3.5 Sonnet    │
 │                      │                                     │  • Windows / Mac / Lin │                               │  • OpenAI GPT-4o mini   │
 │ • PySide / QtQuick   │ <────────────────────────────────── │  • Port 5000           │ <──────────────────────────── │  • Google Gemini Flash  │
 │ • Nokia Pure 22px    │          S40/1 Response             │  • Built-in Free AI    │           JSON Response       │  • Groq LLaMA 3.3       │
 └──────────────────────┘                                     └────────────────────────┘                               └─────────────────────────┘
```

---

## 🚀 Getting Started

### 1. Requirements

- **Nokia N9** (RM-696) with Developer Mode enabled.
- Python 2.7 & PySide installed on N9 (`apt-get install python python-pyside`).
- Any PC (Windows / Linux / macOS) connected to the same Wi-Fi network as the N9.
- Python 3.x installed on the PC.

### 2. PC Bridge Setup

1. Clone or download this repository on your PC:
   ```bash
   git clone https://github.com/your-username/aikon-n9.git
   cd aikon-n9
   ```

2. (Optional) Set your API key if you wish to use your own cloud account:
   ```powershell
   # Windows PowerShell:
   $env:ANTHROPIC_API_KEY = "sk-ant-..."
   # or $env:OPENAI_API_KEY = "sk-..."
   # or $env:GROQ_API_KEY = "gsk_..."
   ```
   *Note: If no API key is specified, the server automatically defaults to the built-in free live AI engine.*

3. Start the bridge server on your PC:
   ```bash
   python server.py
   ```
   You will see:
   ```
   ============================================================
     AIKON Nokia N9 Bridge Server - Port 5000
     Active AI Engine: Built-in Free Live AI (No key required!)
     Target Address: http://<YOUR_PC_IP>:5000
   ============================================================
   ```

### 3. Nokia N9 Client Installation

1. Copy the project folder to your Nokia N9 over SCP:
   ```powershell
   scp -O -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa -r aikon-n9 user@192.168.8.144:/home/user/
   ```
   *(Default password for Nokia N9 developer mode is `rootme`)*

2. SSH into your Nokia N9:
   ```bash
   ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa user@192.168.8.144
   ```

3. Configure your PC's IP address (default is set to `http://192.168.8.137:5000`):
   ```bash
   # In aikon-n9/backend/chat_manager.py or in the in-app Settings dialog
   ```

4. Run the application:
   ```bash
   cd /home/user/aikon-n9
   python main.py
   ```

---

## 📂 Repository Structure

```
aikon-n9/
├── aikon-n9.desktop          # MeeGo Harmattan application launcher
├── main.py                   # PySide entry point with portrait lock
├── server.py                 # PC Bridge server (multi-provider AI & OTA updater)
├── requirements.txt          # Optional dependencies for PC bridge
├── LICENSE                   # MIT License
├── README.md                 # English documentation
├── README_TR.md              # Türkçe dokümantasyon
├── assets/
│   └── aikon-80.png          # High-resolution Harmattan 80x80 app icon
├── backend/
│   ├── __init__.py
│   ├── aikon_client.py       # S40/1 wire protocol network client
│   └── chat_manager.py       # Qt QObject bridge & SQLite history cache
├── debian/
│   └── control               # Harmattan packaging manifest
├── qml/
│   ├── ChatBubble.qml        # Frosted glass message bubbles (22px Nokia Pure)
│   ├── ChatPage.qml          # Main chat interface with input dock & status
│   ├── ConversationsPage.qml # Conversation history drawer
│   ├── CoverView.qml         # Nokia N9 multitasking live cover
│   ├── ModelSelectorDialog.qml # Model switcher dialog
│   ├── PulleyMenu.qml        # Sailfish OS flickable pulley menu
│   ├── SettingsDialog.qml    # Server IP & token configuration dialog
│   ├── SilicaTheme.qml       # Sailfish OS Silica ambiance design tokens
│   └── main.qml              # MeeGo PageStackWindow root
└── screenshots/
    ├── screenshot1.png       # Live N9 screenshot: literary analysis
    └── screenshot2.png       # Live N9 screenshot: weather conversation
```

---

## 🙏 Credits & Acknowledgments

This project is inspired by and builds upon the gateway architecture pioneered by:

- **[emir/AIKON](https://github.com/emir/AIKON)** — *AI Client for Nokia S40 / J2ME phones.*
  Special thanks to **Emir** ([@emir](https://github.com/emir)) for designing the elegant and lightweight **S40/1 wire protocol**, which makes connecting vintage mobile hardware to modern Large Language Models possible.

- **Nokia & MeeGo Community**: For creating one of the most visionary mobile user experiences in history with the Nokia N9.
- **Sailfish OS (Jolla)**: For the enduring inspiration of the Silica ambiance and pulley navigation design language.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
