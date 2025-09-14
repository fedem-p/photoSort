# PhotoSort Program Specification

## Overview
PhotoSort is a command-line tool to organize large collections of photos and videos by date and location, using metadata. It also provides an initial scan report of your files.

## Features

### 1. Input & File Types
- Supported file types: `.jpg`, `.png`, `.mp4`, `.mov`, `.heic`, `.avi`, `.gif`
- Scans all subfolders recursively.

### 2. Metadata Extraction
- Uses EXIF data for images and video metadata for videos.
- If a file lacks date info: moved to an `unsorted` folder.
- If a file lacks GPS info: no location tag is added; folder is just date-based.
- If GPS is available: uses city/country for location tag in folder name.

### 3. Folder Naming & Structure
- Structure:
  ```
  YYYY/
    YYYY-MM/
      YYYY-MM-DD[-location]/
        files...
  ```
  - If location is available: `YYYY-MM-DD-location/`
  - If not: `YYYY-MM-DD/`
- Files are only moved, not renamed.
- Images and videos are mixed in the same folders.

### 4. Handling Duplicates & Conflicts
- If a file with the same name already exists in the target folder: keep both by appending a counter (e.g., `IMG_001.jpg`, `IMG_001_1.jpg`).
- No content-based duplicate checking.

### 5. Logging & Reporting
- All actions (moved, skipped, errors) are logged in JSON format.
- All errors are written to a log file in JSON format.
- Supports a "dry run" mode to preview changes without moving files.

### 6. Performance & Usability
- Command-line interface only.
- Supports batch processing of large numbers of files, with progress bar and resume capability.

### 7. Extensibility
- No requirements for tagging, face recognition, or cloud sync.

### 8. Error Handling
- On error: do nothing, but log all errors for later review.

## Initial Scan Functionality
- Scans all files and collects:
  - Supported vs unsupported extensions (lists all extensions found)
  - Count of pictures and videos
  - Count of files with/without date info
  - Count of files with/without GPS info
  - Largest/smallest file size
  - Oldest/newest date found
  - Most common locations (if GPS available)
  - List of files with unreadable metadata
- Initial scan output is printed and saved in a JSON file.

## Preferences
- Filename conflicts: append a counter
- Images and videos: mixed in folders
- Log format: JSON
- Initial scan output: printed and saved in JSON
