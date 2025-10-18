<div align="center">
  <!-- 
    NOTE: This is a placeholder banner. You can create your own banner image 
    (e.g., 1200x400 pixels) and replace the URL below. 
  -->
  <img src="https://via.placeholder.com/800x300.png?text=MKV+Batch+Remuxer" alt="Project Banner">
  <h1>MKV Batch Remuxer</h1>
  <p>
    A powerful and versatile tool for batch remuxing MKV files with both a GUI and a CLI.
  </p>

  <!-- Badges -->
  <p>
    <a href="https://github.com/mlbkumar9/Project_13/blob/main/LICENSE"><img src="https://img.shields.io/github/license/mlbkumar9/Project_13?style=for-the-badge" alt="License"></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python" alt="Python Version"></a>
    <a href="https://mkvtoolnix.download/"><img src="https://img.shields.io/badge/MKVToolNix-Required-green?style=for-the-badge" alt="MKVToolNix"></a>
  </p>
</div>

---

## 📖 Overview

MKV Batch Remuxer is a robust, cross-platform tool designed to streamline the process of remuxing Matroska (MKV) files. Whether you prefer a graphical interface or a command-line workflow, this tool provides a comprehensive solution for efficiently processing large batches of video files. It's built with Python and leverages the power of `mkvmerge` to provide accurate and fast remuxing capabilities.

---

## ✨ Key Features

This tool is packed with features to make your media management tasks as simple and efficient as possible.

### 🖥️ Graphical User Interface (`REMUX_GUI.py`)

*   **Intuitive Design:** A clean and user-friendly interface built with Tkinter, perfect for visual users.
*   **Effortless File Handling:** Easily select input and output directories using the file browser.
*   **Automatic Language Detection:** Intelligently scans all MKV files to find available audio and subtitle tracks.
*   **Flexible Language Selection:** Use quick-select buttons or manually input a comma-separated list of ISO 639-2 language codes.
*   **Safety First:** Includes options for a "dry run" to preview changes and to skip files that already exist in the output directory.
*   **Real-Time Progress:** A detailed table provides live feedback on the status of each file, including progress bars and time estimates.
*   **Non-Blocking Operation:** The GUI remains responsive thanks to multi-threaded processing, even during intensive operations.
*   **Clear Summaries:** A post-processing summary details the number of successful and failed operations.

### ⌨️ Command-Line Interface (`REMUX_Script.py`)

*   **Rich & Interactive:** A modern and colorful CLI powered by the `rich` library for an enhanced user experience.
*   **Guided Workflow:** Interactive prompts walk you through every step of the configuration process.
*   **Smart Scanning:** Automatically detects and displays available audio and subtitle languages from your files.
*   **Live Progress Tracking:** A beautifully formatted, real-time table shows the progress of individual files and the overall batch.
*   **Comprehensive Logging:** All actions, including the exact `mkvmerge` commands executed, are logged to `remux_log.txt` for easy debugging and review.
*   **Cross-Platform:** Automatically detects the `mkvmerge` executable on Windows, macOS, and Linux.

---

## 🚀 Getting Started

Follow these steps to get the MKV Batch Remuxer up and running on your system.

### Prerequisites

*   **Python 3.7+**
*   **MKVToolNix:** The `mkvmerge` command-line tool must be installed and accessible in your system's PATH. You can download it from the [official website](https://mkvtoolnix.download/).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mlbkumar9/Project_13.git
    cd Project_13
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚙️ Usage Guide

This guide provides detailed instructions for both the GUI and CLI modes.

### GUI Mode (`REMUX_GUI.py`)

The GUI provides a visual way to interact with the tool.

**1. Launch the Application:**
   Run the script from your terminal:
   ```bash
   python "Project_13/REMUX_GUI.py"
   ```

**2. Select Directories:**
   *   Click the **"Browse"** button next to "Input Directory" to choose the folder containing your MKV files.
   *   Click the **"Browse"** button next to "Output Directory" to choose where the new files will be saved. The tool will create this directory if it doesn't exist.

**3. Scan for Languages:**
   *   Once you select an input directory, the tool automatically scans the files and populates the "Available Audio Languages" and "Available Subtitle Languages" lists. This shows you all the language tracks present in your media collection.

**4. Choose Languages:**
   *   **Manual Entry:** Type the desired ISO 639-2 language codes (e.g., `eng,spa,jpn`) into the "Audio Languages" and "Subtitle Languages" fields.
   *   **Quick Select:** Use the **"Select All Audio"** or **"Select All Subtitles"** buttons to automatically populate the fields with all available languages. Use the **"Clear"** buttons to reset the fields.

**5. Configure Options:**
   *   **Skip if output exists:** Keep this checked (default) to avoid re-processing files that are already in the output directory.
   *   **Dry-run only:** Check this box if you want the tool to perform a test run. It will generate logs and show what it *would* do without creating any new video files.

**6. Start Remuxing:**
   *   Click the **"Start!"** button.
   *   The progress table will update in real-time, showing the status of each file. You can monitor the progress bar, elapsed/remaining time, and status (e.g., `Processing`, `OK`, `Skipped`, `Failed`).

**7. Review Summary:**
   *   After the process is complete, a message box will appear summarizing the results (e.g., "Processed 10 files: 8 OK, 2 Skipped, 0 Failed").

### CLI Mode (`REMUX_Script.py`)

The CLI is perfect for automation, scripting, or for users who prefer the terminal.

**1. Launch the Application:**
   Run the script from your terminal:
   ```bash
   python "Project_13/REMUX_Script.py"
   ```

**2. Follow Interactive Prompts:**
   The script will guide you with a series of questions:
   *   **Input Directory:** Enter the full path to the folder containing your MKV files.
   *   **Output Directory:** Enter the path for the processed files.
   *   **Available Languages:** The script will scan your files and show you the available audio and subtitle languages.
   *   **Select Audio/Subtitle Languages:** Enter the language codes you want to keep, separated by commas. You can press **Enter** to select all available languages. The script will warn you if you enter a language code that wasn't found.
   *   **Skip Existing Files:** You'll be asked if you want to skip files that already exist in the output directory (default is Yes).
   *   **Dry-Run Mode:** You'll be asked if you want to run in preview mode (default is No).

**3. Monitor Progress:**
   *   Once configured, the script will display a live progress table powered by `rich`. It shows the status of each file and a summary row for the overall batch progress.

**4. Check the Logs:**
   *   After completion, you can find a detailed `remux_log.txt` file in your output directory. This log contains a summary of all operations, the exact `mkvmerge` commands that were executed, and any errors that occurred. This is extremely useful for troubleshooting.

---

## 📁 Project Structure

```
Project_13/
├── .github/                # GitHub-specific files
├── docs/                   # Project documentation
├── Project_13/             # Core source code
│   ├── REMUX_GUI.py        # The GUI application script
│   └── REMUX_Script.py     # The CLI application script
├── REMUX Python Scripts/   # Additional Python scripts
├── .gitignore              # Files to be ignored by Git
├── CHANGELOG.md            # A log of changes to the project
├── CODE_OF_CONDUCT.md      # Guidelines for community interaction
├── CONTRIBUTING.md         # Guidelines for contributing to the project
├── LICENSE                 # The project's open-source license
├── README.md               # This file
└── requirements.txt        # A list of Python dependencies
```

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) file for details on our code of conduct and the process for submitting pull requests.

---

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

---

## 🙏 Acknowledgments

*   [MKVToolNix](https://mkvtoolnix.download/)
*   [Rich](https://github.com/Textualize/rich)
*   [Tkinter](https://docs.python.org/3/library/tkinter.html)

