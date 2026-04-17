# Spotify Ad Auto-Restarter

A Python utility that automatically detects and skips ads in Spotify by restarting the application.

## Overview

This script monitors your Spotify window title in real-time and detects when an ad is playing. When an ad is detected, it automatically:
1. Closes the Spotify process
2. Restarts Spotify
3. Resumes playback

## How It Works

The script uses two detection methods to identify ads:

- **Explicit Ad Detection**: Looks for common ad-related keywords in multiple languages (e.g., "advertisement", "ad", "werbung", "publicidad")
- **Implicit Ad Detection**: Detects songs without the standard artist-track separator (`" - "`) and aren't default Spotify states

A confirmation check is performed after 1 second to prevent false positives during normal song transitions.

## Requirements

- Python 3.6+
- Windows OS (uses Windows-specific APIs)
- Spotify installed on your system
- PowerShell (for retrieving Spotify window title)

## Installation

1. Clone or download this repository
2. Ensure Python is installed and added to your PATH
3. No additional dependencies required (uses only standard library modules)

## Usage

Run the script from the command line:

```bash
python spotify_ad_restarter.py
```

The script will:
- Display a status message
- Begin monitoring Spotify continuously
- Print detected songs/ads with timestamps
- Automatically restart Spotify when ads are detected
- Run until you press `Ctrl+C` to exit

## Configuration

You can adjust the following timings in the code:

- **Line 31**: `time.sleep(5)` - Delay for Spotify to start up (increase if Spotify loads slowly)
- **Line 63**: `time.sleep(1.0)` - Confirmation check delay before restarting
- **Line 72**: `time.sleep(1.5)` - Poll frequency (lower = more CPU usage, higher = slower detection)

## Notes

- This script works with both Spotify Free and Premium accounts
- Requires Spotify to be running before starting the script
- The media play/pause key is used, which may affect other audio applications
- Performance impact is minimal due to low polling frequency

## Troubleshooting

- **Spotify not restarting**: Check that Spotify.exe is in standard installation paths or modify the `spotify_path` variable
- **"Advertisement" not detected**: Ensure your Spotify language is set to one of the supported languages
- **High CPU usage**: Increase the sleep duration in the main loop

## License

This project is provided as-is for personal use.