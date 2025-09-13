![icon_trayperf_github](./docs/img/logo.png)

[![Github issues](https://img.shields.io/github/issues/BlackManta64/TrayPerf)](https://github.com/BlackManta64/TrayPerf/issues)
[![Github forks](https://img.shields.io/github/forks/BlackManta64/TrayPerf)](https://github.com/BlackManta64/TrayPerf/network/members)
[![Github stars](https://img.shields.io/github/stars/BlackManta64/TrayPerf)](https://github.com/BlackManta64/TrayPerf/stargazers)
[![Top language](https://img.shields.io/github/languages/top/BlackManta64/TrayPerf)](https://github.com/BlackManta64/TrayPerf/)
[![Release](https://img.shields.io/github/v/release/BlackManta64/TrayPerf)](https://github.com/BlackManta64/TrayPerf/releases)
[![Github license](https://img.shields.io/github/license/BlackManta64/TrayPerf)](https://github.com/BlackManta64/TrayPerf/)

`Python` `sys` `PySide6` `psutil` `GPUtil`

> [!CAUTION]
> This software may be falsely detected as a Trojan (Trojan:Script/Wacatac.B!ml) by some antivirus programs, such as Windows Defender.
> 
> **Why this happens:**  
> TrayPerf reads system information (CPU, RAM, GPU) and is packaged as a self-contained executable (`--onefile`), which can resemble malware behavior to antivirus software. This is a **false positive**, and the software is safe to use.
### ✅ How to Avoid False Detection

1. **Use the recommended build options:**  
```pyinstaller --onedir --noupx main.py```

## 📦 Required Libraries (for Python Scripts)
This app depends on the following Python libraries:

- [psutil](https://pypi.org/project/psutil/) - Get CPU/RAM Usage
- [GPUtil](https://pypi.org/project/GPUtil/) - Get GPU Usage
- [PySide6](https://pypi.org/project/PySide6/) - GUI & System Tray Display

## 💻 Execution Environment
- Python 3.12 (64-bit recommended)
- Windows / Linux
* macOS not tested

## 🎬Run Video
![tray_video](./docs/img/tray_video.gif)
