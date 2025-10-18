# MKV Batch Remuxer 🎬

## Introduction
MKV Batch Remuxer is a powerful tool designed to streamline the process of remuxing MKV files. It offers both a graphical user interface (GUI) and a command-line interface (CLI) version to cater to different user preferences.

## Features

### REMUX_GUI.py
- **Tkinter-based graphical interface**: A user-friendly 950x700 window.
- **Input/Output directory selection**: Easily browse and select directories.
- **Automatic language detection**: Scans all MKV files to detect available languages.
- **Available languages display**: Shows audio and subtitle languages found.
- **Quick select buttons**: Options to "Select All Audio", "Select All Subtitles", "Clear Audio", and "Clear Subtitles".
- **Language input fields**: Input ISO 639-2 codes (comma-separated).
- **Skip if output exists**: Checkbox to skip processing if output already exists (default: True).
- **Dry-run only**: Checkbox for preview mode without changes.
- **Real-time progress table**: Displays filename, progress bar, percentage, elapsed/remaining time, and status.
- **Multi-threaded processing**: Prevents GUI freezing during long operations.
- **Queue-based progress updates**: Keeps users informed of progress.
- **Completion summary**: Shows counts for OK and Failed operations.
- **Uses mkvmerge from MKVToolNix**: Integrates JSON track identification.
- **Auto-creates output directory**: Creates the output directory automatically if it doesn’t exist.

### REMUX_Script.py
- **Rich library-based CLI**: Offers colorful console output for an engaging experience.
- **Interactive prompts**: Guides users through all settings with prompts.
- **Automatic scanning**: Displays available audio/subtitle languages in files.
- **Smart language selection**: Provides validation warnings for non-existent languages.
- **Select all languages**: Press Enter to select all available languages.
- **Live updating progress table**: Shows SL No., Filename, Progress bar, %, Elapsed, Remaining, Status, Result (✓ or ✗).
- **Batch progress row**: Displays overall completion status.
- **Real-time progress parsing**: Parses progress from mkvmerge output.
- **Fallback to file-size based progress**: Estimates progress based on file size if needed.
- **Detailed logging**: Logs operations in `remux_log.txt` in the output directory.
- **Tab-separated log format**: Provides a full summary in an organized format.
- **Command storage**: Stores executed commands in the log for debugging.
- **Skip existing files**: Prompts for skipping existing files (Y/n).
- **Dry-run mode**: Offers a preview mode (y/N prompt).
- **Cross-platform mkvmerge detection**: Automatically detects mkvmerge across platforms.

### Common Functionality
- **Track identification**: Uses mkvmerge JSON format for track identification.
- **Audio and subtitle filtering**: Filters tracks by language codes.
- **Automatic video track retention**: Keeps video tracks during remuxing.
- **Progress reporting**: Uses --gui-mode for progress reporting.
- **Error handling**: Handles missing mkvmerge, invalid directories, and no MKV files gracefully.
- **Time formatting**: Displays time in MM:SS format.
- **Processing status**: Shows Pending, Processing, OK, Skipped, and Failed statuses.
- **Support for undefined language code**: Handles "und" (undefined) language code appropriately.

## Installation
1. Download and install [MKVToolNix](https://mkvtoolnix.download/).
2. Ensure Python is installed on your system (preferably Python 3.6 or higher).
3. Clone this repository:
   ```bash
   git clone https://github.com/mlbkumar9/Project_13.git
   cd Project_13
   ```

## Usage

### GUI Version
Run the GUI version using the following command:
```bash
python REMUX_GUI.py
```
Follow the on-screen instructions to remux your MKV files.

### CLI Version
Run the CLI version using the following command:
```bash
python REMUX_Script.py
```
Follow the interactive prompts to set up your remuxing preferences.

## Language Code Table
| Language     | ISO 639-2 Code |
|--------------|----------------|
| English      | eng            |
| Spanish      | spa            |
| French       | fra            |
| German       | deu            |
| Undetermined | und            |

## Examples
- **Using the GUI**: Open the application, select the input and output directories, choose your languages, and click "Start!".
- **Using the CLI**: Follow the prompts to enter your desired settings and execute the remuxing process.

## Troubleshooting
- **Error: mkvmerge not found**: Ensure MKVToolNix is installed and in your system PATH.
- **Error: No MKV files found**: Confirm that you have selected a valid directory with MKV files.
- **Output directory issues**: Check permissions for writing to the output directory.

## Conclusion
MKV Batch Remuxer simplifies the remuxing process for MKV files, making it accessible for both GUI and CLI users. For any questions or feedback, feel free to reach out!
