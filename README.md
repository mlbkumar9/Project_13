# MKV Batch Remuxer

## 📋 Overview

MKV Batch Remuxer is a powerful and user-friendly tool designed to batch process Matroska Video (MKV) files. It enables users to selectively retain specific audio and subtitle tracks based on language preferences while removing unwanted tracks, resulting in smaller file sizes without quality loss. The tool is available in both command-line interface (CLI) and graphical user interface (GUI) versions to accommodate different user preferences.

## ✨ Features

- **Batch Processing**: Process multiple MKV files in a single operation
- **Language Selection**: Specify which audio and subtitle language tracks to keep (e.g., English, Japanese, Spanish)
- **Dual Interface**: Choose between CLI for power users or GUI for ease of use
- **Smart Skipping**: Option to skip files that have already been processed
- **Dry Run Mode**: Preview operations without making any actual changes
- **Real-time Progress**: Live progress tracking with percentage, elapsed time, and estimated time remaining
- **Automatic Language Detection**: Automatically detect available languages in your MKV files
- **Error Handling**: Robust error handling with detailed logging
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🔧 Prerequisites

Before using this tool, ensure you have the following installed:

1. **Python 3.7 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **MKVToolNix**
   - Download from [mkvtoolnix.download](https://mkvtoolnix.download/)
   - The tool uses the `mkvmerge` command-line utility
   - **Windows**: Add MKVToolNix installation directory to system PATH, or install to default location: `C:\Program Files\MKVToolNix\`
   - **macOS**: Install via Homebrew: `brew install mkvtoolnix`
   - **Linux**: Install via package manager: `sudo apt-get install mkvtoolnix` (Ubuntu/Debian) or `sudo yum install mkvtoolnix` (RHEL/CentOS)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mlbkumar9/Project_13.git
   cd Project_13
   ```

2. **Install required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install the `rich` library used for enhanced CLI output.

## 🚀 Usage

### GUI Version (Recommended for Most Users)

The GUI version provides an intuitive interface for batch remuxing MKV files.

#### Running the GUI

```bash
python "REMUX Python Scripts/remux_gui.py"
```

Or on Windows, you can double-click the `remux_gui.py` file.

#### Using the GUI

1. **Input Directory**: Click the **Browse** button next to "Input Directory" to select the folder containing your MKV files
2. **Output Directory**: Click the **Browse** button next to "Output Directory" to choose where remuxed files will be saved
3. **Audio Languages**: Enter 3-letter ISO 639-2 language codes separated by commas (e.g., `eng,jpn,spa`)
4. **Subtitle Languages**: Enter 3-letter language codes for subtitles you want to keep (e.g., `eng,jpn`)
5. **Options**:
   - **Skip if output exists**: Check this to skip files that have already been processed
   - **Dry-run only**: Check this to preview operations without actually processing files
6. **Auto-Detect**: Click to automatically detect available languages in your files
7. **Start Remux**: Click to begin the batch processing

#### GUI Features

- **Progress Table**: Real-time progress display showing:
  - File name
  - Progress bar
  - Percentage complete
  - Elapsed time
  - Estimated remaining time
  - Status
- **Pause/Resume**: Ability to pause and resume operations
- **Cancel**: Stop processing at any time

### CLI Version (For Advanced Users)

The command-line version offers more control and is ideal for automation and scripting.

#### Running the CLI

```bash
python "REMUX Python Scripts/1_Improved_REMUX_Script.py"
```

#### Interactive Prompts

The script will guide you through the following steps:

1. **Input Directory**: Enter the path to the folder containing your MKV files
   ```
   Example: /path/to/your/mkv/files
   ```

2. **Output Directory**: Enter the destination path (leave blank to create a `remuxed` folder in the input directory)
   ```
   Example: /path/to/output (or press Enter for default)
   ```

3. **Audio Languages**: Enter comma-separated language codes
   ```
   Example: eng,jpn
   ```

4. **Subtitle Languages**: Enter comma-separated language codes
   ```
   Example: eng,jpn,spa
   ```

5. **Skip Existing Files**: Choose whether to skip already processed files (y/n)

6. **Dry Run**: Choose whether to perform a dry run without processing (y/n)

#### CLI Features

- **Rich Terminal UI**: Beautiful progress display with colors and formatting
- **Live Progress Table**: Shows real-time status of all files
- **Batch Summary**: Overall progress and statistics
- **Detailed Logging**: Information about tracks being kept and removed

## 📚 Configuration

### Language Codes

Use ISO 639-2 three-letter language codes. Common codes include:

| Language | Code |
|----------|------|
| English | eng |
| Japanese | jpn |
| Spanish | spa |
| French | fre |
| German | ger |
| Italian | ita |
| Portuguese | por |
| Russian | rus |
| Chinese | chi |
| Korean | kor |
| Arabic | ara |
| Hindi | hin |

For a complete list, visit [ISO 639-2 Code List](https://www.loc.gov/standards/iso639-2/php/code_list.php).

### Command-line Arguments (For Advanced CLI Usage)

While the current version uses interactive prompts, you can modify the script to accept command-line arguments for automation purposes.

## 🎯 Examples

### Example 1: Keep Only English Audio and Subtitles

**Input**: Folder with anime episodes containing Japanese, English audio and multiple subtitle tracks

**Settings**:
- Audio Languages: `eng`
- Subtitle Languages: `eng`

**Result**: Files with only English audio and English subtitles

### Example 2: Dual Audio with Multiple Subtitles

**Input**: Movie collection with various audio tracks

**Settings**:
- Audio Languages: `eng,jpn`
- Subtitle Languages: `eng,spa,fre`

**Result**: Files with English and Japanese audio, plus English, Spanish, and French subtitles

### Example 3: Dry Run to Preview Changes

**Settings**:
- Audio Languages: `eng`
- Subtitle Languages: `eng`
- Dry-run: Enabled

**Result**: Console output showing what would be processed without actually modifying any files

## 🐛 Troubleshooting

### MKVMerge Not Found

**Problem**: Error message stating mkvmerge cannot be found

**Solutions**:
- Ensure MKVToolNix is installed
- Add MKVToolNix to your system PATH
- On Windows, install to default location: `C:\Program Files\MKVToolNix\`

### No Files Found

**Problem**: Script reports no MKV files found

**Solutions**:
- Verify the input directory path is correct
- Ensure files have `.mkv` extension (case-sensitive on Linux/macOS)
- Check file permissions

### Process Hangs or Freezes

**Problem**: Processing appears stuck on a file

**Solutions**:
- Check if the file is corrupted (try opening it in a media player)
- Increase timeout value in the script
- Try processing that file separately

### Output File Too Large

**Problem**: Output file is larger than expected

**Solutions**:
- Verify you're not including too many audio/subtitle tracks
- Check that you're not accidentally including all tracks
- Review the language codes you've entered

### Permission Denied Errors

**Problem**: Cannot write to output directory

**Solutions**:
- Ensure you have write permissions for the output directory
- Try running the script with administrator/sudo privileges
- Choose a different output directory

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add some amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 📝 License

This project is open source and available for personal and educational use.

## 🙏 Acknowledgments

- **MKVToolNix** - For providing the excellent mkvmerge tool
- **Rich Library** - For beautiful terminal formatting
- **Python Community** - For continuous support and resources

## 📧 Support

If you encounter any issues or have questions:

1. Check the Troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information:
   - Operating system and version
   - Python version
   - MKVToolNix version
   - Error messages
   - Steps to reproduce

## 🗺️ Roadmap

Future enhancements planned:

- [ ] Add support for selecting specific track indices
- [ ] Implement video codec conversion options
- [ ] Add preset configurations
- [ ] Create standalone executables for Windows/macOS/Linux
- [ ] Add support for other container formats (MP4, AVI)
- [ ] Implement multi-threaded processing
- [ ] Add detailed logging to file
- [ ] Create web-based interface

---

**Made with ❤️ for the multimedia processing community