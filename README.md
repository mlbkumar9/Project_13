# MKV Batch Remuxer (Project 13)

This project provides a tool to batch remux Matroska Video (MKV) files, allowing the user to select specific audio and subtitle tracks to keep while discarding the rest. It comes in two versions: a command-line interface (CLI) and a graphical user interface (GUI).

## Features

- **Batch Processing:** Remux multiple `.mkv` files in a single operation.
- **Language Selection:** Specify which audio and subtitle languages to keep (e.g., `eng`, `jpn`).
- **CLI and GUI:** Choose between a powerful command-line script or an easy-to-use graphical interface.
- **Flexible Options:** Includes options to skip already processed files and perform a "dry run" to see what commands will be executed without modifying any files.
- **Live Progress:** Both versions provide real-time feedback on the remuxing process.

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3:** Make sure Python 3 is installed and accessible from your command line.
2.  **MKVToolNix:** This provides the underlying `mkvmerge` command-line tool that performs the remuxing. You can download it from the [official MKVToolNix website](https://mkvtoolnix.download/). Please ensure the installation directory is added to your system's PATH, or the script will try to find it in the default Windows location.

## Setup

1.  **Clone the repository (or download the files):**
    ```bash
    git clone <repository-url>
    cd Project_13
    ```

2.  **Install the required Python packages:**
    Navigate to the project directory in your terminal and run the following command to install the `rich` library, which is used by the CLI script:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

There are two scripts located in the `REMUX Python Scripts` directory.

### 1. GUI Version (`remux_gui.py`)

This is the recommended version for most users.

1.  **Run the script:**
    ```bash
    python "REMUX Python Scripts/remux_gui.py"
    ```
2.  **Using the application:**
    -   Click **Browse...** to select your **Input** directory (where your MKV files are) and **Output** directory.
    -   In the **Audio Langs** and **Subtitle Langs** fields, enter the 3-letter language codes you wish to keep, separated by commas (e.g., `eng,jpn`).
    -   Select the desired options (`Skip if output exists`, `Dry-run only`).
    -   Click **Start Remux** to begin the process.
    -   Progress will be displayed in the table.

### 2. Command-Line Version (`1_Improved_REMUX_Script.py`)

This version is for users who prefer working in the terminal.

1.  **Run the script:**
    ```bash
    python "REMUX Python Scripts/1_Improved_REMUX_Script.py"
    ```
2.  **Follow the prompts:**
    -   The script will ask you to enter the path to your input directory.
    -   It will then ask for the output directory path (you can leave this blank to create a `remuxed` folder inside the input directory).
    -   You will be prompted to enter the desired audio and subtitle languages (comma-separated).
    -   Finally, you will be asked if you want to skip existing files or perform a dry run.
    -   The script will then display a live progress table in your terminal.
