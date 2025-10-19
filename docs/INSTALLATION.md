# Installation Instructions

## System Requirements
- **Windows:**
  - OS: Windows 10 or later
  - RAM: Minimum 4 GB (8 GB recommended)
  - Disk Space: 500 MB free space

- **macOS:**
  - OS: macOS Mojave (10.14) or later
  - RAM: Minimum 4 GB (8 GB recommended)
  - Disk Space: 500 MB free space

- **Linux:**
  - OS: Ubuntu 18.04 or later, or Fedora 30 or later
  - RAM: Minimum 4 GB (8 GB recommended)
  - Disk Space: 500 MB free space

## Installation Steps

### Windows
1. **Install Python:**
   - Download Python from [python.org](https://www.python.org/downloads/)
   - Run the installer and check "Add Python to PATH".
   - Verify installation by running `python --version` in Command Prompt.

2. **Install MKVToolNix:**
   - Download MKVToolNix from [MKVToolNix official site](https://mkvtoolnix.download/downloads.html).
   - Run the installer and follow the instructions.

### macOS
1. **Install Python:**
   - Open Terminal and run: 
     ```bash
     brew install python
     ```
   - Verify installation by running `python3 --version`.

2. **Install MKVToolNix:**
   - Download MKVToolNix from [MKVToolNix official site](https://mkvtoolnix.download/downloads.html).
   - Open the downloaded `.dmg` file and drag MKVToolNix to Applications.

### Linux
1. **Install Python:**
   - For Ubuntu:
     ```bash
     sudo apt update
     sudo apt install python3
     ```
   - For Fedora:
     ```bash
     sudo dnf install python3
     ```
   - Verify installation by running `python3 --version`.

2. **Install MKVToolNix:**
   - For Ubuntu:
     ```bash
     sudo add-apt-repository ppa:abogdan
     sudo apt update
     sudo apt install mkvtoolnix mkvtoolnix-gui
     ```
   - For Fedora:
     ```bash
     sudo dnf install mkvtoolnix mkvtoolnix-gui
     ```

## Verification Procedures
- For Python, run `python --version` or `python3 --version` in the terminal/command prompt.
- For MKVToolNix, open the application and check the version in the Help menu.

## Troubleshooting
- **Python not recognized:**
  - Ensure Python is added to the PATH during installation.
  
- **MKVToolNix fails to open:**
  - Check if the installation was completed successfully and if your system meets the requirements.

- **Common installation errors:**
  - Refer to the official documentation for Python and MKVToolNix for troubleshooting guides.