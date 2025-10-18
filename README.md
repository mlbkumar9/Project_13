# MKV Batch Remuxer 🎬

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Project Objectives](#-project-objectives)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Folder Structure](#-folder-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [ISO 639-2 Language Codes Reference](#-iso-639-2-language-codes-reference)
- [Workflow and Data Flow](#-workflow-and-data-flow)
- [Practical Usage Examples](#-practical-usage-examples)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

## 📖 Project Overview

**MKV Batch Remuxer** is a professional, feature-rich tool designed to streamline and automate the process of remuxing MKV (Matroska Video) files. The application provides both a modern graphical user interface (GUI) and a powerful command-line interface (CLI), making it accessible to users of all technical levels—from beginners who prefer visual tools to advanced users who need scriptable automation.

### What is Remuxing?

Remuxing is the process of changing the container format of a video file without re-encoding the actual video or audio streams. This means:
- **No quality loss**: The video and audio remain identical to the source
- **Fast processing**: Only metadata is processed, not the media streams
- **Selective track inclusion**: Choose which audio and subtitle tracks to keep
- **Reduced file size**: Remove unnecessary language tracks to save space

### Key Benefits

- **Dual Interface**: Choose between intuitive GUI or efficient CLI based on your needs
- **Batch Processing**: Process multiple files simultaneously with multi-threaded support
- **Language Filtering**: Automatically detect and select desired audio/subtitle languages
- **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux
- **Real-time Progress**: Live progress tracking with time estimates for all operations
- **Production Ready**: Error handling, logging, and validation for reliable operations

## 🎯 Project Objectives

1. **Simplify MKV File Management**: Provide an easy-to-use solution for managing multi-language MKV files
2. **Reduce Storage Requirements**: Enable users to remove unwanted language tracks to save disk space
3. **Maintain Quality**: Ensure lossless remuxing without re-encoding video or audio streams
4. **Enhance User Experience**: Offer both GUI and CLI interfaces to cater to different user preferences
5. **Automate Workflow**: Support batch processing to handle large video libraries efficiently
6. **Ensure Reliability**: Implement robust error handling and comprehensive logging
7. **Cross-Platform Support**: Provide consistent functionality across major operating systems
8. **Transparency**: Offer dry-run mode and detailed progress reporting for user confidence

## ✨ Features

### 🖥️ GUI Version (REMUX_GUI.py)

#### Interface & Usability
- **Modern Tkinter-Based Interface**: Clean, professional 950x700 pixel window optimized for readability
- **Intuitive Directory Selection**: Browse buttons for easy input/output folder selection with visual feedback
- **Responsive Design**: Multi-threaded architecture prevents UI freezing during long operations
- **Queue-Based Updates**: Smooth, non-blocking progress updates using thread-safe queue communication

#### Language Detection & Selection
- **Automatic Language Scanning**: Intelligent detection of all available audio and subtitle languages across your MKV collection
- **Visual Language Display**: Real-time display of detected languages in dedicated panels with color-coded status
- **Quick Selection Tools**: 
  - "Select All Audio" - Instantly select all detected audio languages
  - "Select All Subtitles" - Instantly select all detected subtitle languages
  - "Clear Audio" - Quick reset of audio language selection
  - "Clear Subtitles" - Quick reset of subtitle language selection
- **Manual Language Input**: Direct input fields for ISO 639-2 language codes (comma-separated)
- **Language Validation**: Warns users if selected languages aren't found in the source files

#### Processing Options
- **Skip Existing Files**: Smart checkbox to bypass files that already exist in the output directory (enabled by default)
- **Dry-Run Mode**: Preview what would happen without actually processing files - perfect for testing
- **Batch Processing**: Handle multiple files simultaneously with configurable threading
- **Auto-Directory Creation**: Automatically creates output directories if they don't exist

#### Progress Monitoring
- **Real-Time Progress Table**: Comprehensive view showing:
  - Filename with smart truncation for readability
  - Visual progress bar for each file
  - Percentage completion (0-100%)
  - Elapsed time in MM:SS format
  - Remaining time estimation
  - Current status (Pending, Processing, OK, Skipped, Failed)
- **Completion Summary**: Final statistics showing total files processed, successful operations, and failures
- **Color-Coded Status**: Visual indicators for quick status identification

#### Technical Features
- **MKVToolNix Integration**: Uses industry-standard `mkvmerge` tool with JSON track identification
- **Error Recovery**: Graceful handling of corrupted files, missing dependencies, or permission issues
- **Resource Efficient**: Optimized memory usage even with large file collections

### 💻 CLI Version (REMUX_Script.py)

#### User Interface
- **Rich Library Integration**: Beautiful, colorful console output with professional formatting
- **Interactive Prompts**: Step-by-step guided setup process for all configuration options
- **Terminal Compatibility**: Works with standard terminals on all platforms (Windows CMD/PowerShell, macOS/Linux Terminal)
- **Clear Visual Hierarchy**: Organized sections with headers, dividers, and color-coded messages

#### Language Management
- **Automatic File Scanning**: Pre-scan all MKV files to detect available audio and subtitle languages
- **Intelligent Language Display**: Shows all detected languages before prompting for selection
- **Smart Selection System**:
  - Enter specific languages (e.g., "eng,jpn,kor") for precise control
  - Press Enter without input to select ALL detected languages
  - Comma-separated input with automatic trimming and validation
- **Validation Warnings**: Real-time feedback if you select languages not present in your files

#### Processing Features
- **Live Progress Table**: Dynamic, updating table showing:
  - Serial number for each file
  - Shortened filename (40 characters max)
  - Animated progress bar
  - Percentage completion
  - Elapsed processing time
  - Remaining time estimate
  - Current status
  - Result indicator (✓ for success, ✗ for failure)
- **Batch Progress Row**: Separate row showing overall batch completion with gap separator
- **Real-Time Updates**: Progress parsed directly from mkvmerge's output stream
- **Fallback Progress Calculation**: Uses file size comparison if direct progress parsing fails

#### Logging & Debugging
- **Comprehensive Logging**: Creates `remux_log.txt` in the output directory with:
  - Timestamp for each operation
  - Source and destination file paths
  - Selected language tracks
  - Processing status and results
  - Error messages and stack traces
- **Tab-Separated Format**: Structured log format for easy parsing and analysis
- **Command Storage**: Logs the exact mkvmerge commands executed for reproducibility and debugging
- **Session Summary**: Final statistics including success/failure counts

#### Operation Modes
- **Skip Existing Files**: Configurable prompt (Y/n) to skip files that already exist in output
- **Dry-Run Mode**: Preview mode (y/N) that shows what would happen without making changes
- **Interactive Confirmation**: Prompts before starting batch operations for safety

#### Platform Support
- **Cross-Platform Detection**: Automatically finds mkvmerge on:
  - Windows (checks PATH and default installation locations)
  - macOS (checks PATH and common installation directories)
  - Linux (uses system PATH)
- **Path Handling**: Robust path resolution for all operating systems

### 🔧 Common Functionality (Both Versions)

#### Track Processing
- **JSON-Based Track Identification**: Uses mkvmerge's JSON output format for accurate track detection
- **Language Code Filtering**: Filters audio and subtitle tracks by ISO 639-2 language codes
- **Automatic Video Retention**: Always preserves all video tracks during remuxing
- **Selective Track Inclusion**: Include only desired audio and subtitle languages
- **Multiple Track Support**: Handles files with multiple tracks of the same type

#### Progress & Reporting
- **GUI Mode Integration**: Uses mkvmerge's `--gui-mode` for standardized progress reporting
- **Real-Time Progress Parsing**: Extracts progress percentage from mkvmerge output
- **Time Estimation**: Calculates elapsed and remaining time based on current progress
- **MM:SS Time Format**: Human-readable time display (e.g., "05:23" for 5 minutes 23 seconds)

#### Error Handling & Validation
- **Missing mkvmerge Detection**: Clear error message if MKVToolNix is not installed
- **Invalid Directory Handling**: Validates input/output directories before processing
- **Empty Directory Check**: Warns if no MKV files are found in the input directory
- **File Access Validation**: Checks read permissions for input files and write permissions for output
- **Corrupted File Handling**: Gracefully handles files that mkvmerge cannot process

#### Status Management
- **Comprehensive Status Codes**:
  - **Pending**: File queued for processing
  - **Processing**: Currently being remuxed
  - **OK**: Successfully completed
  - **Skipped**: File skipped (already exists or user choice)
  - **Failed**: Processing failed (with error details)
- **Undefined Language Support**: Properly handles "und" (undefined) language code
- **Exit Code Checking**: Validates mkvmerge's return code for success/failure detection

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
├──────────────────────────────┬──────────────────────────────────┤
│      GUI (Tkinter)           │      CLI (Rich Console)          │
│   - Event-driven UI          │   - Interactive prompts          │
│   - Multi-threaded           │   - Live table display           │
│   - Queue-based updates      │   - Progress tracking            │
└──────────────────┬───────────┴─────────────┬────────────────────┘
                   │                         │
                   └────────┬────────────────┘
                            │
┌───────────────────────────▼────────────────────────────────────┐
│                  Core Processing Layer                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Language Detection Engine                                │  │
│  │  - Scan MKV files                                         │  │
│  │  - Extract track metadata (JSON)                          │  │
│  │  - Build language inventory                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Remuxing Engine                                          │  │
│  │  - Build mkvmerge commands                                │  │
│  │  - Execute subprocess                                     │  │
│  │  - Parse progress output                                  │  │
│  │  - Handle errors                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Progress Tracking System                                 │  │
│  │  - Real-time percentage calculation                       │  │
│  │  - Time estimation (elapsed/remaining)                    │  │
│  │  - Status management                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬───────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────┐
│                  External Dependencies Layer                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  MKVToolNix (mkvmerge)                                    │  │
│  │  - Track identification (--identify --json)               │  │
│  │  - File remuxing (--audio-tracks --subtitle-tracks)       │  │
│  │  - Progress reporting (--gui-mode)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Python Standard Library                                  │  │
│  │  - tkinter (GUI)                                          │  │
│  │  - subprocess (process management)                        │  │
│  │  - threading (concurrency)                                │  │
│  │  - queue (thread communication)                           │  │
│  │  - pathlib (file system operations)                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Third-Party Libraries                                    │  │
│  │  - rich (CLI formatting and live display)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
[User Input] → [UI Layer] → [Language Detection] → [Track Filtering]
      ↓              ↓              ↓                      ↓
[Settings] → [Validation] → [Command Building] → [mkvmerge Execution]
      ↓              ↓              ↓                      ↓
[Progress] ← [Status Update] ← [Output Parsing] ← [Process Output]
      ↓              ↓              ↓                      ↓
[UI Display] ← [Queue/Thread] ← [Result Handling] ← [File Validation]
```

### Threading Model (GUI)

```
Main Thread                    Worker Threads
     │                              │
     ├─ UI Rendering                │
     ├─ Event Handling              │
     ├─ Queue Processing ←──────────┤
     │                              │
     │                         ┌────┴────┐
     │                         │ Thread 1 │ → File 1 → mkvmerge
     │                         ├─────────┤
     │                         │ Thread 2 │ → File 2 → mkvmerge
     │                         ├─────────┤
     │                         │ Thread N │ → File N → mkvmerge
     │                         └────┬────┘
     │                              │
     └──────── Updates ─────────────┘
          (via Queue)
```

## 📁 Folder Structure

```
Project_13/
│
├── REMUX Python Scripts/          # Main application directory
│   ├── REMUX_GUI.py               # GUI application (Tkinter-based)
│   │                              # - 435 lines of code
│   │                              # - Provides graphical interface
│   │                              # - Multi-threaded processing
│   │                              # - Real-time progress display
│   │
│   └── REMUX_Script.py            # CLI application (Rich-based)
│                                  # - 566 lines of code
│                                  # - Interactive command-line interface
│                                  # - Live table updates
│                                  # - Comprehensive logging
│
├── docs/                          # Documentation files
│   ├── FAQ.md                     # Frequently asked questions
│   ├── INSTALLATION.md            # Detailed installation guide
│   └── USAGE.md                   # Usage guide and examples
│
├── .github/                       # GitHub-specific files
│   └── workflows/                 # CI/CD workflows (if any)
│
├── README.md                      # Main project documentation (this file)
├── LICENSE                        # MIT License
├── CHANGELOG.md                   # Version history and changes
├── CODE_OF_CONDUCT.md             # Community guidelines
├── CONTRIBUTING.md                # Contribution guidelines
├── SECURITY.md                    # Security policy and reporting
├── requirements.txt               # Python dependencies (rich)
└── .gitignore                     # Git ignore rules

Generated Files (Not in Repository):
────────────────────────────────────
output_directory/
├── remuxed_file1.mkv              # Processed MKV files
├── remuxed_file2.mkv
├── ...
└── remux_log.txt                  # CLI processing log (CLI only)
                                   # - Tab-separated format
                                   # - Timestamps, paths, status
                                   # - Command history
```

### File Descriptions

#### Core Application Files

**REMUX_GUI.py**
- Tkinter-based graphical user interface
- Multi-threaded file processing
- Queue-based progress communication
- Visual progress tracking with table display
- Automatic language detection and display
- Quick selection buttons for convenience

**REMUX_Script.py**
- Rich library-powered CLI with beautiful formatting
- Interactive prompts for all settings
- Live updating progress table
- Comprehensive logging to file
- Tab-separated log format for easy parsing
- Batch progress tracking with summaries

#### Documentation Files

**README.md**
- Comprehensive project documentation
- Installation and usage instructions
- Feature descriptions and examples
- Troubleshooting guide

**docs/FAQ.md**
- Common questions and answers
- Quick reference for common issues

**docs/INSTALLATION.md**
- Platform-specific installation steps
- System requirements
- Verification procedures

**docs/USAGE.md**
- Detailed usage examples
- Language code reference
- Advanced scenarios

#### Configuration Files

**requirements.txt**
- Python package dependencies
- Currently only requires: `rich`

**.gitignore**
- Excludes Python cache files (`__pycache__`)
- Excludes compiled bytecode (`.pyc`, `.pyo`)
- Excludes IDE-specific files

#### Community Files

**LICENSE**
- MIT License - permissive open-source license
- Allows commercial and private use

**CONTRIBUTING.md**
- Guidelines for contributing to the project
- Code style and pull request process

**CODE_OF_CONDUCT.md**
- Community standards and expectations
- Reporting guidelines

**SECURITY.md**
- Security policy
- How to report vulnerabilities

**CHANGELOG.md**
- Version history
- Feature additions and bug fixes

## 🔧 Prerequisites

### System Requirements

#### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 4 GB (8 GB recommended for large files)
- **Disk Space**: 500 MB for software + space for remuxed files
- **Processor**: Any modern CPU (multi-core recommended for batch processing)

#### Software Dependencies

1. **Python 3.6 or Higher**
   - Required for running the scripts
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version` or `python3 --version`

2. **MKVToolNix (mkvmerge)**
   - Core dependency for MKV file processing
   - Download from [mkvtoolnix.download](https://mkvtoolnix.download/)
   - Version 40.0.0 or higher recommended
   - Must be accessible via system PATH or default installation location

3. **Python Packages**
   - **rich**: For CLI version only (installed via pip)
   - **tkinter**: For GUI version (usually included with Python)

### Checking Prerequisites

```bash
# Check Python version
python --version
# or
python3 --version

# Check if mkvmerge is installed
mkvmerge --version

# Check if tkinter is available (for GUI)
python -m tkinter
# A small window should appear if tkinter is installed

# Check if rich is installed (for CLI)
python -c "import rich; print(rich.__version__)"
```

## 📥 Installation

### Step-by-Step Installation Guide

#### For Windows

**1. Install Python**
```powershell
# Download Python from https://www.python.org/downloads/
# During installation:
# ✓ Check "Add Python to PATH"
# ✓ Check "Install pip"

# Verify installation
python --version
pip --version
```

**2. Install MKVToolNix**
```powershell
# Download from https://mkvtoolnix.download/downloads.html#windows
# Run the installer (mkvtoolnix-64-bit-XX.X.X-setup.exe)
# Follow the installation wizard
# Default location: C:\Program Files\MKVToolNix\

# Verify installation
mkvmerge --version

# If not found, add to PATH:
# 1. Open System Properties > Environment Variables
# 2. Edit "Path" under System Variables
# 3. Add: C:\Program Files\MKVToolNix\
# 4. Restart Command Prompt
```

**3. Clone the Repository**
```powershell
# Install Git if not already installed
# Download from: https://git-scm.com/download/win

# Clone the repository
git clone https://github.com/mlbkumar9/Project_13.git
cd Project_13
```

**4. Install Python Dependencies**
```powershell
# For CLI version (required)
pip install -r requirements.txt

# For GUI version (tkinter usually comes with Python)
# If tkinter is missing, reinstall Python with tcl/tk support
```

**5. Verify Installation**
```powershell
# Test CLI version
cd "REMUX Python Scripts"
python REMUX_Script.py --help

# Test GUI version
python REMUX_GUI.py
```

#### For macOS

**1. Install Python**
```bash
# Option 1: Using Homebrew (recommended)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3

# Option 2: Download from python.org
# Visit https://www.python.org/downloads/macos/

# Verify installation
python3 --version
pip3 --version
```

**2. Install MKVToolNix**
```bash
# Option 1: Using Homebrew (recommended)
brew install mkvtoolnix

# Option 2: Download DMG from https://mkvtoolnix.download/downloads.html#macos
# Open the .dmg file
# Drag MKVToolNix to Applications folder
# Add to PATH in ~/.zshrc or ~/.bash_profile:
# export PATH="/Applications/MKVToolNix.app/Contents/MacOS:$PATH"

# Verify installation
mkvmerge --version
```

**3. Clone the Repository**
```bash
# Install Git (if not already installed)
brew install git

# Clone the repository
git clone https://github.com/mlbkumar9/Project_13.git
cd Project_13
```

**4. Install Python Dependencies**
```bash
# For CLI version
pip3 install -r requirements.txt

# tkinter should be included with Python
# If missing: brew install python-tk@3.x
```

**5. Verify Installation**
```bash
# Test CLI version
cd "REMUX Python Scripts"
python3 REMUX_Script.py

# Test GUI version
python3 REMUX_GUI.py
```

#### For Linux (Ubuntu/Debian)

**1. Install Python**
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-tk

# Verify installation
python3 --version
pip3 --version
```

**2. Install MKVToolNix**
```bash
# Add MKVToolNix repository (for latest version)
sudo add-apt-repository ppa:ubuntuhandbook1/apps
sudo apt update

# Install MKVToolNix
sudo apt install mkvtoolnix mkvtoolnix-gui

# Verify installation
mkvmerge --version
```

**3. Clone the Repository**
```bash
# Install Git (if not already installed)
sudo apt install git

# Clone the repository
git clone https://github.com/mlbkumar9/Project_13.git
cd Project_13
```

**4. Install Python Dependencies**
```bash
# For CLI version
pip3 install -r requirements.txt

# Or system-wide
sudo pip3 install -r requirements.txt
```

**5. Verify Installation**
```bash
# Test CLI version
cd "REMUX Python Scripts"
python3 REMUX_Script.py

# Test GUI version
python3 REMUX_GUI.py
```

#### For Linux (Fedora/RHEL)

**1. Install Python**
```bash
# Install Python and pip
sudo dnf install python3 python3-pip python3-tkinter

# Verify installation
python3 --version
pip3 --version
```

**2. Install MKVToolNix**
```bash
# Install MKVToolNix
sudo dnf install mkvtoolnix mkvtoolnix-gui

# Verify installation
mkvmerge --version
```

**3. Clone and Setup**
```bash
# Install Git
sudo dnf install git

# Clone the repository
git clone https://github.com/mlbkumar9/Project_13.git
cd Project_13

# Install Python dependencies
pip3 install --user -r requirements.txt

# Verify installation
cd "REMUX Python Scripts"
python3 REMUX_Script.py
python3 REMUX_GUI.py
```

### Post-Installation Verification

Run these commands to ensure everything is working:

```bash
# Check all dependencies
python3 --version              # Should show Python 3.6+
mkvmerge --version             # Should show MKVToolNix version
python3 -c "import rich"       # Should complete without errors
python3 -m tkinter             # Should open a test window

# Quick test (CLI)
cd "REMUX Python Scripts"
python3 REMUX_Script.py

# Quick test (GUI)
python3 REMUX_GUI.py
```

### Installation Troubleshooting

**Python not found:**
- Ensure Python is added to system PATH
- On Windows, reinstall Python with "Add to PATH" checked
- On macOS/Linux, use `python3` instead of `python`

**mkvmerge not found:**
- Check if MKVToolNix is installed: find installation directory
- Add installation directory to system PATH
- On Windows: Usually `C:\Program Files\MKVToolNix\`
- On macOS: `/Applications/MKVToolNix.app/Contents/MacOS/`
- On Linux: Should be in `/usr/bin/` after installation

**tkinter not available:**
- Windows: Reinstall Python with tcl/tk support
- macOS: `brew install python-tk`
- Ubuntu/Debian: `sudo apt install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`

**Permission denied errors:**
- Use `sudo` for system-wide installations (Linux/macOS)
- Or use `pip3 install --user` for user-only installation
- On Windows, run Command Prompt as Administrator

## 📖 Usage

### GUI Version (REMUX_GUI.py)

#### Launching the Application

**Windows:**
```powershell
cd "REMUX Python Scripts"
python REMUX_GUI.py
```

**macOS/Linux:**
```bash
cd "REMUX Python Scripts"
python3 REMUX_GUI.py
```

#### Step-by-Step GUI Walkthrough

**Step 1: Select Directories**
```
┌─────────────────────────────────────────────────────┐
│ Input Directory:  [C:\Videos\Source]    [Browse...] │
│ Output Directory: [C:\Videos\Remuxed]   [Browse...] │
└─────────────────────────────────────────────────────┘
```
- Click **Browse** next to "Input" to select the folder containing your MKV files
- Click **Browse** next to "Output" to select where remuxed files will be saved
- Output directory will be created automatically if it doesn't exist

**Step 2: Review Available Languages**
```
┌──────────────────────────────────────────────────────┐
│ Available Languages in MKV Files:                    │
│ Audio:     eng, jpn, spa, fra                        │
│ Subtitles: eng, jpn, spa, fra, ger                   │
└──────────────────────────────────────────────────────┘
```
- After selecting input directory, available languages are automatically detected
- This shows all audio and subtitle languages found across ALL files

**Step 3: Select Languages**
```
┌──────────────────────────────────────────────────────┐
│ Audio Languages:    [eng,jpn]  [Select All] [Clear] │
│ Subtitle Languages: [eng,jpn]  [Select All] [Clear] │
└──────────────────────────────────────────────────────┘
```
- Enter ISO 639-2 codes (comma-separated) for languages you want to keep
- Use **Select All** buttons to include all detected languages
- Use **Clear** buttons to reset the selection

**Step 4: Configure Options**
```
┌──────────────────────────────────────────────────────┐
│ ☑ Skip if output exists (recommended)                │
│ ☐ Dry-run only (preview without processing)          │
└──────────────────────────────────────────────────────┘
```
- **Skip if output exists**: Prevents re-processing already remuxed files
- **Dry-run**: Shows what would happen without actually processing files

**Step 5: Start Processing**
- Click the **Start!** button to begin processing
- Progress table will show real-time updates for each file
- You can monitor:
  - Filename
  - Progress bar
  - Percentage (0-100%)
  - Elapsed time
  - Estimated remaining time
  - Status (Pending → Processing → OK/Failed/Skipped)

**Step 6: Review Results**
```
Processing complete!
Files processed: 10
Successful: 9
Failed: 1
```

#### GUI Tips & Best Practices

1. **Test with Dry-Run**: Always test with dry-run mode first on a few files
2. **Use Skip Option**: Enable "Skip if output exists" for resumable batch processing
3. **Monitor Progress**: Watch the progress table for any failed files
4. **Language Validation**: Only include languages that appear in "Available Languages"
5. **Free Space**: Ensure output directory has enough free disk space

### CLI Version (REMUX_Script.py)

#### Launching the Application

**Windows:**
```powershell
cd "REMUX Python Scripts"
python REMUX_Script.py
```

**macOS/Linux:**
```bash
cd "REMUX Python Scripts"
python3 REMUX_Script.py
```

#### Interactive Prompts Guide

**Prompt 1: Input Directory**
```
Enter input directory (containing MKV files): /home/user/Videos/Source
```
- Enter the full path to the folder containing your MKV files
- Use absolute paths for reliability
- Windows example: `C:\Videos\Source`
- Linux/macOS example: `/home/user/Videos/Source`

**Prompt 2: Output Directory**
```
Enter output directory (for remuxed files): /home/user/Videos/Remuxed
```
- Enter the full path where remuxed files should be saved
- Directory will be created if it doesn't exist
- Can be the same as input directory (files will have same names)

**Prompt 3: Language Scanning**
```
Scanning files for available languages...

Available Audio Languages: eng, jpn, spa
Available Subtitle Languages: eng, jpn, spa, fra, ger
```
- Automatic scanning shows all detected languages
- This helps you know which languages are available

**Prompt 4: Audio Language Selection**
```
Enter audio languages to keep (comma-separated, e.g., 'eng,jpn') or press Enter for all: eng,jpn
```
- Enter desired language codes separated by commas
- Press **Enter** without input to keep ALL detected languages
- Example: `eng,jpn,kor`
- Invalid languages trigger a warning but are still accepted

**Prompt 5: Subtitle Language Selection**
```
Enter subtitle languages to keep (comma-separated, e.g., 'eng,jpn') or press Enter for all: eng
```
- Same as audio selection
- Press **Enter** for all languages
- Example: `eng,spa`

**Prompt 6: Skip Existing Files**
```
Skip files that already exist in output directory? (Y/n): Y
```
- **Y** or **Enter**: Skip existing files (default, recommended)
- **n**: Re-process all files even if they exist

**Prompt 7: Dry-Run Mode**
```
Dry-run only? (preview without processing) (y/N): N
```
- **y**: Preview mode - shows what would happen without processing
- **N** or **Enter**: Normal mode - actually process files (default)

**Prompt 8: Processing Begins**
```
┌────┬──────────────────────────┬─────────────┬──────┬─────────┬───────────┬────────────┬────────┐
│ SL │ Filename                 │ Progress    │   %  │ Elapsed │ Remaining │ Status     │ Result │
├────┼──────────────────────────┼─────────────┼──────┼─────────┼───────────┼────────────┼────────┤
│  1 │ movie1.mkv               │ ████████░░  │  75% │ 00:45   │ 00:15     │ Processing │        │
│  2 │ movie2.mkv               │             │   0% │ 00:00   │ --:--     │ Pending    │        │
│  3 │ movie3.mkv               │ ██████████  │ 100% │ 01:23   │ 00:00     │ OK         │   ✓    │
├────┼──────────────────────────┼─────────────┼──────┼─────────┼───────────┼────────────┼────────┤
│    │ Batch Progress           │ ████░░░░░░  │  40% │ 02:08   │ 03:12     │            │        │
└────┴──────────────────────────┴─────────────┴──────┴─────────┴───────────┴────────────┴────────┘
```
- Live updating table shows progress for all files
- Batch progress row at bottom shows overall completion
- ✓ indicates successful completion, ✗ indicates failure

**Processing Complete**
```
Summary:
Files processed: 10
Successful: 9
Failed: 1

Log file created: /home/user/Videos/Remuxed/remux_log.txt
```

#### CLI Tips & Best Practices

1. **Use Full Paths**: Avoid relative paths to prevent confusion
2. **Test First**: Use dry-run mode (`y`) on first run to verify settings
3. **Check Log**: Review `remux_log.txt` in output directory for detailed information
4. **Resume Processing**: Use skip existing files to resume interrupted batches
5. **Language Codes**: Refer to ISO 639-2 language codes table below

### Common Usage Patterns

#### Keep Only English Audio and Subtitles
```
Audio languages: eng
Subtitle languages: eng
```

#### Keep Multiple Languages
```
Audio languages: eng,jpn,kor
Subtitle languages: eng,jpn,kor
```

#### Keep All Available Languages
```
Audio languages: [Press Enter]
Subtitle languages: [Press Enter]
```

#### Preview Before Processing
```
Dry-run only? (y/N): y
```

#### Process New Files Only
```
Skip files that already exist? (Y/n): Y
```

## 🌍 ISO 639-2 Language Codes Reference

Complete reference table for common languages. Use these three-letter codes when selecting languages.

| Language | ISO 639-2 Code | Language | ISO 639-2 Code |
|----------|----------------|----------|----------------|
| **English** | **eng** | **Japanese** | **jpn** |
| **Spanish** | **spa** | **Korean** | **kor** |
| **French** | **fra** | **Chinese** | **chi/zho** |
| **German** | **deu/ger** | **Portuguese** | **por** |
| **Italian** | **ita** | **Russian** | **rus** |
| **Dutch** | **dut/nld** | **Arabic** | **ara** |
| **Polish** | **pol** | **Turkish** | **tur** |
| **Swedish** | **swe** | **Hindi** | **hin** |
| **Norwegian** | **nor** | **Thai** | **tha** |
| **Danish** | **dan** | **Vietnamese** | **vie** |
| **Finnish** | **fin** | **Hebrew** | **heb** |
| **Czech** | **cze/ces** | **Indonesian** | **ind** |
| **Greek** | **gre/ell** | **Malay** | **may/msa** |
| **Hungarian** | **hun** | **Tamil** | **tam** |
| **Romanian** | **rum/ron** | **Telugu** | **tel** |
| **Ukrainian** | **ukr** | **Bengali** | **ben** |
| **Croatian** | **hrv** | **Marathi** | **mar** |
| **Slovak** | **slo/slk** | **Gujarati** | **guj** |
| **Bulgarian** | **bul** | **Kannada** | **kan** |
| **Serbian** | **srp** | **Malayalam** | **mal** |
| **Catalan** | **cat** | **Punjabi** | **pan** |
| **Lithuanian** | **lit** | **Urdu** | **urd** |
| **Slovenian** | **slv** | **Persian/Farsi** | **per/fas** |
| **Latvian** | **lav** | **Swahili** | **swa** |
| **Estonian** | **est** | **Filipino/Tagalog** | **fil/tgl** |
| **Icelandic** | **ice/isl** | **Burmese** | **bur/mya** |
| **Irish** | **gle** | **Khmer** | **khm** |
| **Albanian** | **alb/sqi** | **Lao** | **lao** |
| **Macedonian** | **mac/mkd** | **Nepali** | **nep** |
| **Bosnian** | **bos** | **Sinhala** | **sin** |
| **Basque** | **baq/eus** | **Mongolian** | **mon** |
| **Galician** | **glg** | **Kazakh** | **kaz** |
| **Welsh** | **wel/cym** | **Uzbek** | **uzb** |
| **Afrikaans** | **afr** | **Azerbaijani** | **aze** |
| **Belarusian** | **bel** | **Georgian** | **geo/kat** |
| **Armenian** | **arm/hya** | **Amharic** | **amh** |
| **Maltese** | **mlt** | **Pashto** | **pus** |
| **Yiddish** | **yid** | **Kurdish** | **kur** |
| **Esperanto** | **epo** | **Hausa** | **hau** |
| **Latin** | **lat** | **Somali** | **som** |
| **Undetermined** | **und** | **Multiple Languages** | **mul** |

### Notes on Language Codes

1. **Alternative Codes**: Some languages have two valid ISO 639-2 codes:
   - **German**: `deu` (bibliographic) or `ger` (terminologic) - both are valid
   - **French**: `fra` is standard
   - **Chinese**: `chi` (bibliographic) or `zho` (terminologic)
   - Use whichever code appears in your files (check "Available Languages")

2. **Special Codes**:
   - **und**: Undetermined/undefined language (commonly found in MKV files)
   - **mul**: Multiple languages in one track
   - **zxx**: No linguistic content (e.g., music, sound effects)

3. **Case Sensitivity**: Codes are case-insensitive
   - `ENG`, `eng`, and `Eng` are all equivalent
   - The application automatically converts to lowercase

4. **Finding Language Codes**:
   - Run the application and check "Available Languages" to see codes in your files
   - Official ISO 639-2 list: [Library of Congress](https://www.loc.gov/standards/iso639-2/php/code_list.php)

### Examples of Language Selection

**Keep English and Japanese only:**
```
Audio: eng,jpn
Subtitles: eng,jpn
```

**Keep multiple European languages:**
```
Audio: eng,fra,deu,spa,ita
Subtitles: eng,fra,deu,spa,ita
```

**Keep Asian languages:**
```
Audio: jpn,kor,chi
Subtitles: jpn,kor,chi,eng
```

**Include undefined language tracks:**
```
Audio: eng,und
Subtitles: eng,und
```

## 🔄 Workflow and Data Flow

### Overall Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        START: User Launch Application                   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Interface Selection    │
                    │  GUI or CLI?            │
                    └─────┬──────────────┬────┘
                          │              │
                ┌─────────▼─────┐   ┌────▼────────┐
                │   GUI Mode    │   │  CLI Mode   │
                │  (Tkinter)    │   │   (Rich)    │
                └─────┬─────────┘   └────┬────────┘
                      │                  │
                      └────────┬─────────┘
                               │
                    ┌──────────▼───────────┐
                    │  Get User Settings   │
                    │  - Input directory   │
                    │  - Output directory  │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼────────────┐
                    │  Validate Directories │
                    │  - Check existence    │
                    │  - Check permissions  │
                    └──────────┬────────────┘
                               │
                    ┌──────────▼────────────┐
                    │   Find MKV Files      │
                    │   in Input Directory  │
                    └──────────┬────────────┘
                               │
                    ┌──────────▼────────────┐
                    │  Scan All Files for   │
                    │  Available Languages  │
                    │  (Audio & Subtitles)  │
                    └──────────┬────────────┘
                               │
                    ┌──────────▼────────────┐
                    │  Display Available    │
                    │  Languages to User    │
                    └──────────┬────────────┘
                               │
                    ┌──────────▼────────────┐
                    │  User Selects         │
                    │  Desired Languages    │
                    └──────────┬────────────┘
                               │
                    ┌──────────▼────────────┐
                    │  User Sets Options    │
                    │  - Skip existing?     │
                    │  - Dry-run mode?      │
                    └──────────┬────────────┘
                               │
                    ┌──────────▼────────────┐
                    │  Start Processing     │
                    │  (Loop through files) │
                    └──────────┬────────────┘
                               │
                ┌──────────────┴──────────────┐
                │  FOR EACH MKV FILE:         │
                └──────────────┬──────────────┘
                               │
                    ┌──────────▼────────────┐
                    │  Check if Output      │
                    │  Already Exists       │
                    └──────┬───────────┬────┘
                           │           │
                      [Exists &    [Doesn't exist
                       Skip=Yes]    or Skip=No]
                           │           │
                    ┌──────▼───┐       │
                    │  SKIP    │       │
                    │  FILE    │       │
                    └──────┬───┘       │
                           │           │
                           │    ┌──────▼────────────┐
                           │    │  Identify Tracks  │
                           │    │  using mkvmerge   │
                           │    │  (JSON format)    │
                           │    └──────┬────────────┘
                           │           │
                           │    ┌──────▼────────────┐
                           │    │  Filter Tracks by │
                           │    │  Selected Langs   │
                           │    └──────┬────────────┘
                           │           │
                           │    ┌──────▼────────────┐
                           │    │  Build mkvmerge   │
                           │    │  Command          │
                           │    └──────┬────────────┘
                           │           │
                           │    ┌──────▼────────────┐
                           │    │  Execute Command  │
                           │    │  [Dry-run?]       │
                           │    └──────┬────────────┘
                           │           │
                           │    ┌──────▼────────────┐
                           │    │  Parse Progress   │
                           │    │  Update UI        │
                           │    └──────┬────────────┘
                           │           │
                           │    ┌──────▼────────────┐
                           │    │  Check Exit Code  │
                           │    │  Validate Output  │
                           │    └──────┬────────────┘
                           │           │
                           └───────────┴─────┐
                                             │
                                    ┌────────▼────────┐
                                    │  Update Status  │
                                    │  (OK/Failed)    │
                                    └────────┬────────┘
                                             │
                ┌────────────────────────────┴─────────────────────┐
                │  END OF LOOP - All files processed               │
                └────────────────────────────┬─────────────────────┘
                                             │
                                    ┌────────▼────────┐
                                    │  Show Summary   │
                                    │  - Total files  │
                                    │  - Successful   │
                                    │  - Failed       │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │  Create Log     │
                                    │  (CLI only)     │
                                    └────────┬────────┘
                                             │
┌────────────────────────────────────────────▼────────────────────────────┐
│                        END: Processing Complete                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
┌──────────────┐
│  User Input  │
│  - Dirs      │
│  - Languages │
│  - Options   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│          Application Layer                   │
│  ┌────────────────────────────────────────┐  │
│  │  Input Validation                      │  │
│  │  - Directory exists?                   │  │
│  │  - Permissions OK?                     │  │
│  │  - MKV files present?                  │  │
│  └────────────┬───────────────────────────┘  │
│               ▼                               │
│  ┌────────────────────────────────────────┐  │
│  │  Language Detection                    │  │
│  │  Input: List of MKV files              │  │
│  │  Process: mkvmerge --identify (JSON)   │  │
│  │  Output: Available audio/sub languages │  │
│  └────────────┬───────────────────────────┘  │
│               ▼                               │
│  ┌────────────────────────────────────────┐  │
│  │  User Language Selection               │  │
│  │  Input: Available languages            │  │
│  │  Process: User chooses languages       │  │
│  │  Output: Selected language list        │  │
│  └────────────┬───────────────────────────┘  │
│               ▼                               │
│  ┌────────────────────────────────────────┐  │
│  │  File Processing Loop                  │  │
│  │  For each MKV file:                    │  │
│  │    1. Read track info (JSON)           │  │
│  │    2. Filter by selected languages     │  │
│  │    3. Build command                    │  │
│  │    4. Execute mkvmerge                 │  │
│  │    5. Monitor progress                 │  │
│  └────────────┬───────────────────────────┘  │
└───────────────┼───────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────┐
│           MKVToolNix Layer                    │
│  ┌────────────────────────────────────────┐   │
│  │  mkvmerge Process                      │   │
│  │  Input: Source MKV + Command           │   │
│  │  Process:                              │   │
│  │    - Read source file                  │   │
│  │    - Extract video tracks (all)        │   │
│  │    - Extract selected audio tracks     │   │
│  │    - Extract selected subtitle tracks  │   │
│  │    - Mux into new container            │   │
│  │  Output: Remuxed MKV file              │   │
│  └────────────┬───────────────────────────┘   │
└───────────────┼───────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────┐
│         Progress & Status Flow                │
│  ┌────────────────────────────────────────┐   │
│  │  Progress Data                         │   │
│  │  - Percentage (0-100%)                 │   │
│  │  - Elapsed time                        │   │
│  │  - Estimated remaining time            │   │
│  │  - Current status                      │   │
│  └────────────┬───────────────────────────┘   │
│               │                               │
│       ┌───────┴────────┐                      │
│       ▼                ▼                      │
│  ┌─────────┐     ┌──────────┐                │
│  │   GUI   │     │   CLI    │                │
│  │  Queue  │     │  Table   │                │
│  │ Updates │     │ Updates  │                │
│  └─────────┘     └──────────┘                │
└───────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────┐
│              Output Files                     │
│  ┌────────────────────────────────────────┐   │
│  │  Remuxed MKV Files                     │   │
│  │  - Same video quality                  │   │
│  │  - Selected audio languages            │   │
│  │  - Selected subtitle languages         │   │
│  │  - Reduced file size (usually)         │   │
│  └────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────┐   │
│  │  Log File (CLI only)                   │   │
│  │  - Processing timestamp                │   │
│  │  - Source/destination paths            │   │
│  │  - Languages selected                  │   │
│  │  - Commands executed                   │   │
│  │  - Success/failure status              │   │
│  └────────────────────────────────────────┘   │
└───────────────────────────────────────────────┘
```

### Track Selection Logic

```
Input MKV File
├── Video Tracks
│   ├── Track 0: H.264 video ──────────────┐
│   └── Track 1: H.264 video (commentary) ──┤
│                                           │
├── Audio Tracks                            │  ALL video tracks
│   ├── Track 2: Japanese (jpn) ────┐      │  always included
│   ├── Track 3: English (eng) ─────┤      │          │
│   ├── Track 4: Spanish (spa)      │      │          │
│   └── Track 5: French (fra)       │      │          │
│                                    │      │          │
└── Subtitle Tracks             Selected   │          │
    ├── Track 6: English (eng) ────┐ based │          │
    ├── Track 7: Spanish (spa)     │  on   │          │
    ├── Track 8: French (fra) ─────┤ user  │          │
    └── Track 9: Japanese (jpn)    │ input │          │
                                    │       │          │
                                    ▼       ▼          ▼
                            ┌────────────────────────────┐
                            │     mkvmerge Command       │
                            │  --audio-tracks 2,3        │
                            │  --subtitle-tracks 6,8     │
                            └────────────┬───────────────┘
                                         │
                                         ▼
                                Output MKV File
                                ├── Video Track 0
                                ├── Video Track 1
                                ├── Audio Track 2 (jpn)
                                ├── Audio Track 3 (eng)
                                ├── Subtitle Track 6 (eng)
                                └── Subtitle Track 8 (fra)
```

## 💡 Practical Usage Examples

### Example 1: Anime Collection - Keep Japanese Audio and English Subtitles

**Scenario**: You have a large anime collection with multiple audio and subtitle tracks. You want to keep Japanese audio and English subtitles only to save space.

**Setup**:
- Input: `/home/user/Anime/Raw/` (100 GB of anime with multiple languages)
- Output: `/home/user/Anime/Cleaned/`
- Goal: Reduce file size by ~30-40% while keeping essential tracks

**GUI Steps**:
1. Launch `REMUX_GUI.py`
2. Set Input: `/home/user/Anime/Raw/`
3. Set Output: `/home/user/Anime/Cleaned/`
4. Wait for language detection
5. Audio Languages: `jpn`
6. Subtitle Languages: `eng`
7. ✓ Skip if output exists
8. ☐ Dry-run (uncheck for actual processing)
9. Click **Start!**

**CLI Steps**:
```bash
python3 REMUX_Script.py

Enter input directory: /home/user/Anime/Raw/
Enter output directory: /home/user/Anime/Cleaned/
# (automatic scanning)
Audio languages: jpn
Subtitle languages: eng
Skip existing? Y
Dry-run? N
```

**Expected Result**:
- Original: 50 files × 2 GB = 100 GB
- Cleaned: 50 files × 1.3 GB = 65 GB
- Space saved: 35 GB
- Processing time: ~20-30 minutes (depending on CPU)

---

### Example 2: International Movie Library - Multiple Languages

**Scenario**: You maintain a movie library for a multilingual family. You need English, Spanish, and French audio and subtitles, removing all others.

**Setup**:
- Input: `C:\Movies\Downloads\`
- Output: `C:\Movies\Library\`
- Languages needed: English, Spanish, French
- Files: Mixed content with 8-10 language tracks each

**GUI Steps**:
1. Launch `REMUX_GUI.py`
2. Set Input: `C:\Movies\Downloads\`
3. Set Output: `C:\Movies\Library\`
4. Review detected languages (might show: eng, spa, fra, deu, ita, jpn, por, rus)
5. Audio Languages: `eng,spa,fra`
6. Subtitle Languages: `eng,spa,fra`
7. ✓ Skip if output exists
8. Click **Start!**

**Expected Result**:
- Each file reduced from 8-10 tracks to 3-4 tracks
- File size reduction: 20-35% per file
- Library remains fully functional for target languages

---

### Example 3: Video Archive - Testing Before Batch Processing

**Scenario**: You have 500+ video files and want to ensure settings are correct before processing them all.

**Setup**:
- Create a test subset first
- Use dry-run mode to verify
- Process test batch
- Review results before full batch

**Steps**:
```bash
# Step 1: Create test directory with 5 sample files
mkdir /tmp/test_input
cp /path/to/archive/sample*.mkv /tmp/test_input/

# Step 2: Dry-run test
python3 REMUX_Script.py
Input: /tmp/test_input
Output: /tmp/test_output
Audio: eng,jpn
Subtitles: eng
Skip existing? Y
Dry-run? y    # <-- DRY RUN MODE

# Step 3: Review dry-run output
# Verify which tracks would be selected
# Check for any errors or warnings

# Step 4: Actual test run on 5 files
# Repeat with Dry-run? N

# Step 5: Verify output files
ffprobe /tmp/test_output/sample1.mkv  # Check tracks
vlc /tmp/test_output/sample1.mkv      # Test playback

# Step 6: Full batch processing (if test successful)
python3 REMUX_Script.py
Input: /path/to/archive/
Output: /path/to/archive_cleaned/
# ... same settings as test
```

**Best Practice**: Always test on a small subset before processing large batches!

---

### Example 4: Resumable Large Batch - Handling Interruptions

**Scenario**: You're processing 1000 files, but your computer crashes or you need to stop midway. You want to resume without reprocessing completed files.

**Setup**:
- Large batch processing (overnight job)
- Potential interruptions (power, system updates, etc.)
- Need resumable processing

**CLI Steps**:
```bash
# Initial run
python3 REMUX_Script.py
Input: /media/external/Videos/
Output: /media/external/Videos_Processed/
Audio: eng
Subtitles: eng,spa
Skip existing? Y    # <-- CRITICAL for resumable processing
Dry-run? N

# ... processes 347/1000 files before interruption ...

# Resume after interruption (next day)
python3 REMUX_Script.py
# Use EXACT same settings
Input: /media/external/Videos/
Output: /media/external/Videos_Processed/  # Same output!
Audio: eng
Subtitles: eng,spa
Skip existing? Y    # <-- Will skip the 347 already processed

# Result: Only remaining 653 files are processed
```

**Key Points**:
- "Skip existing" must be enabled
- Use same output directory
- Previously completed files are automatically skipped
- Check log file to see which files were skipped vs. newly processed

---

### Example 5: Corporate Training Videos - Standardization

**Scenario**: Company has training videos in various formats and languages. HR wants to standardize them: English audio only, English and Spanish subtitles.

**Setup**:
- Input: Mixed video files from various departments
- Output: Standardized corporate library
- Requirement: English audio + English & Spanish subtitles only
- Compliance: Keep log for audit trail

**Workflow**:

**Phase 1: Assessment**
```bash
# Step 1: Scan files to see what languages exist
python3 REMUX_Script.py
Input: /company/training/raw/
# Check "Available Languages" output
# Document findings for stakeholders
```

**Phase 2: Test Run**
```bash
# Step 2: Test with dry-run
Output: /company/training/test/
Audio: eng
Subtitles: eng,spa
Dry-run? y
# Review dry-run results
```

**Phase 3: Production Run**
```bash
# Step 3: Actual processing
Output: /company/training/standardized/
Audio: eng
Subtitles: eng,spa
Skip existing? Y
Dry-run? N
```

**Phase 4: Documentation**
```bash
# Step 4: Archive the log for compliance
cp /company/training/standardized/remux_log.txt \
   /company/training/audit_logs/remux_$(date +%Y%m%d).txt

# Step 5: Generate summary report
awk -F'\t' '{print $NF}' /company/training/standardized/remux_log.txt | \
sort | uniq -c
# Shows count of OK, Failed, Skipped files
```

**Deliverables**:
- Standardized video library
- Audit log showing all transformations
- Summary report for management
- Reduced storage costs (typically 30-50% reduction)

---

### Common Patterns Across Examples

**Space Savings**:
- Removing 5-6 language tracks: 40-50% size reduction
- Removing 2-3 language tracks: 20-30% size reduction
- Keeping only 1 audio + 1 subtitle: Maximum reduction

**Processing Speed** (rough estimates):
- 1 GB file: 30-60 seconds
- 10 GB file: 5-10 minutes
- 100 GB batch: 1-2 hours
- 1 TB batch: 10-20 hours

**Recommended Workflow**:
1. Always test with dry-run first
2. Process a small test batch (3-5 files)
3. Verify output quality and completeness
4. Process full batch with "skip existing" enabled
5. Keep logs for future reference

## 🔧 Troubleshooting

Comprehensive guide to resolving common issues with MKV Batch Remuxer.

### 1. mkvmerge Not Found

**Symptoms**:
```
Error: mkvmerge not found
Please install MKVToolNix
```

**Causes**:
- MKVToolNix not installed
- MKVToolNix not in system PATH
- Incorrect installation

**Solutions**:

**Windows**:
```powershell
# Check if installed
where mkvmerge

# If not found, add to PATH manually:
# 1. Find installation directory (usually C:\Program Files\MKVToolNix\)
# 2. Add to System PATH:
#    - Right-click "This PC" → Properties
#    - Advanced system settings → Environment Variables
#    - Edit "Path" under System variables
#    - Add: C:\Program Files\MKVToolNix\
#    - Click OK and restart Command Prompt

# Alternative: Reinstall MKVToolNix
# Download from https://mkvtoolnix.download/downloads.html
```

**macOS**:
```bash
# Check if installed
which mkvmerge

# Install via Homebrew (recommended)
brew install mkvtoolnix

# Or add to PATH if installed via DMG
echo 'export PATH="/Applications/MKVToolNix.app/Contents/MacOS:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Linux**:
```bash
# Check if installed
which mkvmerge

# Ubuntu/Debian
sudo apt update
sudo apt install mkvtoolnix

# Fedora/RHEL
sudo dnf install mkvtoolnix
```

---

### 2. Python Not Recognized

**Symptoms**:
```
'python' is not recognized as an internal or external command
python: command not found
```

**Solutions**:

**Windows**:
```powershell
# Check Python installation
python --version
# or
py --version

# If not found, reinstall Python
# Download from https://www.python.org/downloads/
# During installation: ✓ Check "Add Python to PATH"
```

**macOS/Linux**:
```bash
# Use python3 instead of python
python3 --version

# Or create alias
echo 'alias python=python3' >> ~/.bashrc  # Linux
echo 'alias python=python3' >> ~/.zshrc  # macOS
source ~/.bashrc  # or ~/.zshrc
```

---

### 3. No MKV Files Found

**Symptoms**:
```
Error: No MKV files found in input directory
```

**Causes**:
- Wrong directory selected
- Files have different extension (.mkv vs .MKV)
- Files in subdirectories (not searched recursively)

**Solutions**:
```bash
# Verify files exist
ls -la /path/to/directory/*.mkv

# Check for uppercase extensions
ls -la /path/to/directory/*.MKV

# If files are in subdirectories, move them to main folder
find /path/to/directory -name "*.mkv" -exec mv {} /path/to/directory/ \;

# Or copy instead of move
find /path/to/directory -name "*.mkv" -exec cp {} /path/to/directory/ \;
```

---

### 4. Permission Denied Errors

**Symptoms**:
```
PermissionError: [Errno 13] Permission denied
Cannot write to output directory
```

**Solutions**:

**Windows**:
```powershell
# Run as Administrator
# Right-click Command Prompt → "Run as administrator"

# Or change folder permissions
# Right-click output folder → Properties → Security
# Give your user account "Full control"
```

**macOS/Linux**:
```bash
# Check permissions
ls -ld /path/to/output

# Fix permissions
chmod 755 /path/to/output

# Or use sudo (not recommended for normal operation)
sudo python3 REMUX_Script.py

# Better: Change ownership to your user
sudo chown -R $USER:$USER /path/to/output
```

---

### 5. GUI Window Not Appearing

**Symptoms**:
- GUI script runs but no window appears
- Error: `ModuleNotFoundError: No module named 'tkinter'`

**Solutions**:

**Windows**:
```powershell
# Reinstall Python with tcl/tk support
# Download and run Python installer
# Choose "Modify" and ensure tcl/tk is selected
```

**macOS**:
```bash
# Install tkinter
brew install python-tk@3.11  # Replace 3.11 with your Python version
```

**Linux**:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Test installation
python3 -m tkinter
# A small test window should appear
```

---

### 6. "Rich" Module Not Found (CLI)

**Symptoms**:
```
ModuleNotFoundError: No module named 'rich'
```

**Solutions**:
```bash
# Install rich library
pip install rich
# or
pip3 install rich

# If permission denied
pip3 install --user rich

# Verify installation
python3 -c "import rich; print(rich.__version__)"
```

---

### 7. Processing Extremely Slow

**Symptoms**:
- Files taking much longer than expected
- System becomes unresponsive
- High CPU/memory usage

**Solutions**:

**Check System Resources**:
```bash
# Linux/macOS
top
htop  # if installed

# Windows
# Open Task Manager (Ctrl+Shift+Esc)
```

**Optimize Processing**:
- Close other applications
- Process files in smaller batches
- Ensure sufficient free disk space (2x largest file size)
- Check if antivirus is scanning processed files (exclude output folder)
- Use SSD for output directory if possible

**For GUI**: Processing happens in parallel by default, which might overload older systems.

---

### 8. Output File Smaller Than Expected

**Symptoms**:
- Output file significantly smaller than input
- Missing video or audio content

**Solutions**:

**Check if tracks were removed**:
```bash
# Compare input and output tracks
mkvmerge -i input.mkv
mkvmerge -i output.mkv

# Or use mediainfo
mediainfo input.mkv > input_info.txt
mediainfo output.mkv > output_info.txt
diff input_info.txt output_info.txt
```

**Common causes**:
- Removed more language tracks than intended
- Check selected language codes match your needs
- Verify "Available Languages" before processing

---

### 9. "No Desired Audio" or Track Errors

**Symptoms**:
```
Status: No desired audio
Status: ID Failed
```

**Causes**:
- Selected language not present in file
- Typo in language code
- File corruption

**Solutions**:

**Verify language codes**:
```bash
# Check what languages are actually in the file
mkvmerge -i problematic_file.mkv

# Look for "language:" field in output
```

**Fix approach**:
1. Use "Available Languages" display to see what's actually present
2. Only select languages that appear in "Available Languages"
3. Check for typos: `eng` not `en`, `jpn` not `jp`
4. Try including `und` (undefined) if tracks have no language tag

---

### 10. Files Skipped Unexpectedly

**Symptoms**:
- All files show "Skipped (exists)" status
- Files not processing even though they should

**Causes**:
- "Skip if output exists" is enabled
- Previous partial run created output files

**Solutions**:

**GUI**:
- Uncheck "Skip if output exists" option
- Or manually delete existing output files

**CLI**:
- Answer "n" to "Skip files that already exist?"
- Or delete output directory contents:
```bash
rm -rf /path/to/output/*  # Linux/macOS
del /Q /path/to/output\*  # Windows
```

---

### 11. Dry-Run Mode Confusion

**Symptoms**:
- No files being created
- Everything shows as "Dry-run (skipped)"

**Cause**:
- Dry-run mode is enabled (preview only)

**Solutions**:

**GUI**: Uncheck "Dry-run only" checkbox

**CLI**: Answer "N" to "Dry-run only?" prompt

---

### 12. GUI Freezing or Not Responding

**Symptoms**:
- GUI becomes unresponsive during processing
- Window shows "(Not Responding)"

**Causes**:
- Threading issue
- Very large files
- System resource exhaustion

**Solutions**:
```bash
# Close and restart the application
# Process fewer files at once
# Monitor system resources
# Ensure adequate free RAM (2-4 GB minimum)
```

If persistent, use CLI version instead:
```bash
python3 REMUX_Script.py
```

---

### 13. Output File Won't Play

**Symptoms**:
- Remuxed file won't play in media player
- Corrupted video/audio

**Causes**:
- Processing interrupted
- Source file corrupted
- Insufficient disk space during processing

**Solutions**:

**Verify output file**:
```bash
# Check if file is complete
ls -lh output.mkv

# Verify with mkvmerge
mkvmerge -i output.mkv

# Try playing with VLC (more forgiving)
vlc output.mkv

# Check mkvmerge error output
ffprobe output.mkv
```

**Recovery**:
1. Delete corrupted output file
2. Re-process source file
3. Ensure sufficient free disk space (2x source file size)
4. Check source file plays correctly before remuxing

---

### 14. Wrong Language Tracks in Output

**Symptoms**:
- Output has different languages than selected
- Unexpected tracks included

**Causes**:
- Files have incorrect language tags
- Misunderstanding of ISO 639-2 codes

**Solutions**:

**Verify source file language tags**:
```bash
mkvmerge -i source.mkv
# Check "language:" field for each track
```

**Common issues**:
- Track tagged as "und" (undefined) when it's actually English
- Track tagged incorrectly by original encoder
- Using wrong ISO code (eng vs en)

**Fix**:
- Include "und" in your language selection if needed
- Use MKVToolNix GUI to manually check and retag source files
- Or accept the language tags as-is and select accordingly

---

### 15. Log File Not Created (CLI)

**Symptoms**:
- No `remux_log.txt` in output directory
- Can't find processing log

**Causes**:
- Permission issues
- Script error before log creation
- Output directory doesn't exist

**Solutions**:
```bash
# Check output directory exists and is writable
ls -ld /path/to/output
touch /path/to/output/test.txt
rm /path/to/output/test.txt

# Check script errors
python3 REMUX_Script.py 2>&1 | tee error_log.txt

# Ensure output directory is created before processing starts
mkdir -p /path/to/output
```

---

### 16. Subtitle Synchronization Issues

**Symptoms**:
- Subtitles out of sync in remuxed file
- Subtitle timing different from original

**Cause**:
- This shouldn't happen with remuxing (no re-encoding)
- If it does, source file may have issues

**Solutions**:
```bash
# Verify source file subtitles
vlc source.mkv  # Check if subs are in sync

# If source is fine but output is not:
# This indicates a bug - report it!

# Workaround: Use MKVToolNix GUI manually
# Or extract subs and re-mux separately
```

---

### 17. Unsupported File Format

**Symptoms**:
```
Error: Not a valid MKV file
File format not supported
```

**Solutions**:
```bash
# Verify file is actually MKV
file suspicious_file.mkv

# Check file isn't corrupted
mkvmerge -i suspicious_file.mkv

# Convert to MKV if different format
ffmpeg -i input.mp4 -c copy output.mkv
```

---

### 18. Batch Progress Not Updating (CLI)

**Symptoms**:
- Progress table not refreshing
- Terminal appears frozen but process is running

**Causes**:
- Terminal doesn't support live updates
- Rich library compatibility issue

**Solutions**:
```bash
# Try different terminal
# Windows: Use Windows Terminal instead of CMD
# macOS: Use iTerm2 or default Terminal
# Linux: Use gnome-terminal or konsole

# Check Rich version
pip show rich

# Update Rich
pip install --upgrade rich
```

---

### Getting Additional Help

If you encounter issues not covered here:

1. **Check the logs**:
   - CLI: Review `remux_log.txt` in output directory
   - Look for error messages and stack traces

2. **Enable verbose output**:
   ```bash
   python3 REMUX_Script.py 2>&1 | tee debug.txt
   ```

3. **Test with single file**:
   - Isolate the problem file
   - Process it individually
   - Share error output when reporting issues

4. **Gather information**:
   ```bash
   python3 --version
   mkvmerge --version
   uname -a  # Linux/macOS
   systeminfo  # Windows
   ```

5. **Report issues**:
   - Create an issue on GitHub
   - Include: OS, Python version, mkvmerge version, error message
   - Provide steps to reproduce

## ❓ FAQ

### General Questions

**Q: What is the difference between remuxing and re-encoding?**

A: Remuxing changes the container format without touching the actual video/audio streams, so there's no quality loss and it's very fast. Re-encoding converts the video/audio streams themselves, which takes much longer and can reduce quality.

**Q: Will remuxing reduce video quality?**

A: No! Remuxing does not re-encode the video or audio streams. The quality remains exactly the same as the source. Only the container and track selection change.

**Q: How much space can I save?**

A: It depends on how many tracks you remove:
- Removing 5-6 language tracks: 40-50% reduction
- Removing 2-3 language tracks: 20-30% reduction
- Removing 1 language track: 5-15% reduction

**Q: Can I undo a remux operation?**

A: No, removed tracks cannot be recovered. Always keep your original files until you've verified the remuxed versions are correct. Use dry-run mode to preview changes first.

**Q: Does this work with other video formats besides MKV?**

A: No, this tool is specifically designed for MKV (Matroska) files. For other formats, consider converting to MKV first using tools like FFmpeg or HandBrake.

---

### Technical Questions

**Q: Why do I need MKVToolNix? Can't the script handle everything?**

A: MKVToolNix's `mkvmerge` is an industry-standard tool specifically designed for MKV manipulation. It's more reliable and efficient than trying to manually parse and rebuild MKV files. This script is a user-friendly wrapper around mkvmerge.

**Q: Can I run multiple instances simultaneously?**

A: Yes, but be aware of system resources. Each instance will consume CPU and disk I/O. For best performance, process different directories or use different output locations.

**Q: What's the difference between GUI and CLI versions?**

A: 
- **GUI**: Graphical interface, better for occasional use, visual progress tracking
- **CLI**: Command-line interface, better for automation, remote servers, scripting, and detailed logging

Both have the same core functionality and use the same remuxing engine.

**Q: Does it support HDR, Dolby Vision, or other advanced formats?**

A: Yes! Since remuxing doesn't re-encode, all original formats are preserved including HDR10, HDR10+, Dolby Vision, Atmos, DTS:X, etc. The streams are copied as-is.

**Q: Can this tool merge multiple MKV files into one?**

A: No, this tool is designed for track selection/removal, not file merging. Use MKVToolNix GUI or `mkvmerge` directly for merging files.

---

### Usage Questions

**Q: How do I keep all languages except one?**

A: Currently, you must specify which languages to keep. There's no "exclude" mode. Check "Available Languages" and list all languages except the one you want to remove.

**Q: What does "und" mean in language codes?**

A: "und" stands for "undefined" - it means the track has no language tag. This is common in MKV files. Include "und" in your selection if you want to keep these tracks.

**Q: Can I process files from a network drive?**

A: Yes, but performance will be slower due to network I/O. For best results, copy files locally, process them, then copy back to the network drive.

**Q: Why is my processing so slow?**

A: Processing speed depends on:
- File size (larger = slower)
- Disk speed (SSD >> HDD)
- CPU speed
- Number of simultaneous operations
- Whether you're reading/writing to the same disk

Typical speed: 1-2 minutes per GB on modern hardware.

**Q: Can I schedule automated batch processing?**

A: Yes! The CLI version is perfect for automation:

**Windows Task Scheduler**:
```powershell
# Create a batch file (remux_batch.bat):
cd "C:\Project_13\REMUX Python Scripts"
python REMUX_Script.py
# Configure answers in script or use process automation
```

**Linux/macOS Cron**:
```bash
# Add to crontab
0 2 * * * cd /path/to/scripts && python3 REMUX_Script.py < config.txt
```

---

### Error Questions

**Q: Why do some files fail while others succeed?**

A: Common reasons:
- File corruption in source
- Selected language not present in that file
- Insufficient disk space
- File locked by another process
- Permission issues

Check the error message and `remux_log.txt` for specific details.

**Q: The script says "No desired audio" - what does this mean?**

A: None of your selected audio languages were found in that file. Either:
- The file has different language tracks than you selected
- Language tags are incorrect in the source file
- Typo in your language code selection

Use "Available Languages" display to see what's actually in your files.

**Q: Why is the output file larger than the input?**

A: This should rarely happen, but can occur if:
- Original file was already heavily compressed/optimized
- You're keeping more tracks than the original had
- Original file had corrupt/incomplete tracks

Usually output is same size or smaller.

---

### Performance Questions

**Q: How many files can I process at once?**

A: There's no hard limit, but consider:
- **GUI**: Processes multiple files in parallel (uses threading)
- **CLI**: Processes files sequentially
- System resources (RAM, disk I/O) are the limiting factors

Recommended: Start with small batches (10-20 files) and scale up based on performance.

**Q: Will this damage my hard drive with heavy use?**

A: No more than any other file operations. Modern SSDs and HDDs are designed for this. However:
- Ensure adequate cooling
- Don't fill disk to 100% capacity
- Consider using a separate drive for output

**Q: Can I use this on a Raspberry Pi or low-power device?**

A: Yes! Both versions will work, but processing will be slower. The CLI version is recommended for resource-constrained devices as it has less overhead.

---

### Safety Questions

**Q: Is it safe to delete original files after remuxing?**

A: Only after:
1. Verifying all files processed successfully
2. Playing back several remuxed files to confirm quality
3. Checking file sizes are reasonable
4. Reviewing the log for any errors

Best practice: Keep originals until you're 100% confident, or backup to external storage.

**Q: What happens if processing is interrupted (power loss, crash)?**

A: 
- Incomplete files will be left in the output directory
- Enable "Skip if output exists" to resume processing
- Delete incomplete output files before resuming
- No damage to source files (they're never modified)

**Q: Can this tool introduce viruses or malware?**

A: No. The tool:
- Only manipulates MKV containers
- Doesn't execute code from video files
- Doesn't download anything
- Is open source (you can review the code)

However, always download from official sources (GitHub) and verify dependencies.

---

## 🤝 Contributing

We welcome contributions to MKV Batch Remuxer! Here's how you can help:

### Ways to Contribute

1. **Report Bugs**: Open an issue on GitHub with details about the problem
2. **Suggest Features**: Share ideas for improvements
3. **Submit Pull Requests**: Fix bugs or add features
4. **Improve Documentation**: Help make docs clearer and more comprehensive
5. **Share Use Cases**: Tell us how you're using the tool

### Contribution Guidelines

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Code style and standards
- Pull request process
- Testing requirements
- Documentation standards

### Development Setup

```bash
# Clone the repository
git clone https://github.com/mlbkumar9/Project_13.git
cd Project_13

# Install dependencies
pip install -r requirements.txt

# Make your changes
# Test thoroughly

# Submit pull request
```

### Code of Conduct

We follow a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming environment for all contributors.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

✅ **Permissions**:
- Commercial use
- Modification
- Distribution
- Private use

❌ **Limitations**:
- Liability
- Warranty

📋 **Conditions**:
- License and copyright notice must be included

---

## 📞 Support

### Getting Help

1. **Documentation**: Read this README and docs/ folder thoroughly
2. **FAQ**: Check the FAQ section above
3. **Troubleshooting**: Review the troubleshooting guide
4. **Search Issues**: Look for similar issues on GitHub
5. **Ask Questions**: Open a new issue with the "question" label

### Reporting Issues

When reporting bugs, please include:
- Operating system and version
- Python version (`python --version`)
- MKVToolNix version (`mkvmerge --version`)
- Complete error message
- Steps to reproduce
- Sample file info (if applicable)

### Feature Requests

We're always looking to improve! For feature requests:
- Check existing issues first to avoid duplicates
- Clearly describe the use case
- Explain why this would be valuable
- Consider contributing the feature yourself!

### Contact

- **GitHub Issues**: [https://github.com/mlbkumar9/Project_13/issues](https://github.com/mlbkumar9/Project_13/issues)
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Security Issues**: See [SECURITY.md](SECURITY.md) for reporting security vulnerabilities

---

## 🙏 Acknowledgments

- **MKVToolNix Team**: For creating the excellent mkvmerge tool
- **Rich Library**: For beautiful terminal formatting ([https://github.com/Textualize/rich](https://github.com/Textualize/rich))
- **Python Community**: For the robust standard library and ecosystem
- **Contributors**: Everyone who has contributed to this project

---

## 📚 Additional Resources

### Related Tools

- **MKVToolNix**: [https://mkvtoolnix.download/](https://mkvtoolnix.download/)
- **FFmpeg**: [https://ffmpeg.org/](https://ffmpeg.org/)
- **HandBrake**: [https://handbrake.fr/](https://handbrake.fr/)
- **MediaInfo**: [https://mediaarea.net/en/MediaInfo](https://mediaarea.net/en/MediaInfo)

### Learning Resources

- **ISO 639-2 Standard**: [https://www.loc.gov/standards/iso639-2/](https://www.loc.gov/standards/iso639-2/)
- **Matroska Specification**: [https://www.matroska.org/technical/specs/index.html](https://www.matroska.org/technical/specs/index.html)
- **Python Documentation**: [https://docs.python.org/3/](https://docs.python.org/3/)

### Project Links

- **Repository**: [https://github.com/mlbkumar9/Project_13](https://github.com/mlbkumar9/Project_13)
- **Issues**: [https://github.com/mlbkumar9/Project_13/issues](https://github.com/mlbkumar9/Project_13/issues)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Security Policy**: [SECURITY.md](SECURITY.md)

---

## 🎬 Conclusion

MKV Batch Remuxer is designed to make video file management easier, whether you're managing a personal media library or processing professional content. With both GUI and CLI interfaces, comprehensive language support, and robust error handling, it provides a reliable solution for MKV file remuxing.

**Key Takeaways**:
- ✅ Lossless quality preservation
- ✅ Easy language track selection
- ✅ Batch processing capability
- ✅ Cross-platform compatibility
- ✅ User-friendly interfaces
- ✅ Comprehensive logging and error handling

**Getting Started**:
1. Install MKVToolNix and Python
2. Clone the repository
3. Install dependencies (`pip install -r requirements.txt`)
4. Run GUI (`python REMUX_GUI.py`) or CLI (`python REMUX_Script.py`)
5. Start processing your MKV files!

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/mlbkumar9/Project_13).

Happy remuxing! 🎬

---

*Last updated: 2025-10-18*
*Version: 1.0*

