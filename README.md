<div align="center">
  <img src="https://via.placeholder.com/600x200.png?text=MKV+Batch+Remuxer" alt="Project Banner">
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

## ⚙️ Usage

You can run the tool in either GUI or CLI mode.

### GUI Mode

Launch the graphical interface with the following command:

```bash
python "Project_13/REMUX_GUI.py"
```

### CLI Mode

Launch the interactive command-line interface with this command:

```bash
python "Project_13/REMUX_Script.py"
```

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