"""
Entry point for PhotoSort CLI.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for PhotoSort CLI."""
    parser = argparse.ArgumentParser(
        prog="photosort",
        description="Organize photos and videos by date and location using metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  photosort scan /path/to/photos          # Scan and generate report
  photosort organize /path/to/photos      # Organize photos (default)
  photosort /path/to/photos               # Organize photos (default)
  photosort organize /path/to/photos --dry-run  # Preview changes
  photosort organize /path/to/photos --output /sorted/photos
        """,
    )

    # First, add the input path as a required positional argument
    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to the input folder containing photos and videos",
    )

    # Add command as an option instead of positional with a default
    parser.add_argument(
        "--command",
        "-c",
        choices=["scan", "organize"],
        default="organize",
        help="Command to execute: 'scan' for report generation, "
        "'organize' for sorting files (default: organize)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output directory for organized files (default: input_path/sorted)",
    )

    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Preview changes without moving files",
    )

    parser.add_argument(
        "--report-file",
        "-r",
        type=Path,
        help="JSON file to save scan report "
        "(default: input_path/photosort_report.json)",
    )

    parser.add_argument(
        "--log-file",
        "-l",
        type=Path,
        help="JSON file to save operation logs "
        "(default: input_path/photosort_log.json)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    # Add a scan subcommand parser for cleaner interface
    parser.add_argument(
        "--scan",
        action="store_const",
        const="scan",
        dest="command",
        help="Generate scan report (shorthand for --command scan)",
    )

    return parser


def validate_arguments(args: argparse.Namespace) -> List[str]:
    """Validate parsed arguments and return list of error messages."""
    errors = []

    # Validate input path
    if not args.input_path.exists():
        errors.append(f"Input path does not exist: {args.input_path}")
    elif not args.input_path.is_dir():
        errors.append(f"Input path is not a directory: {args.input_path}")

    # Validate output path for organize command
    if args.command == "organize" and args.output:
        if args.output.exists() and not args.output.is_dir():
            errors.append(f"Output path exists but is not a directory: {args.output}")

    # Set default values
    if not args.output and args.command == "organize":
        args.output = args.input_path / "sorted"

    if not args.report_file:
        args.report_file = args.input_path / "photosort_report.json"

    if not args.log_file:
        args.log_file = args.input_path / "photosort_log.json"

    return errors


def run_scan_command(args: argparse.Namespace) -> int:
    """Execute the scan command to generate a report."""
    # Placeholder implementation - will connect to scanner module
    print(f"Scanning files in: {args.input_path}")
    print(f"Report will be saved to: {args.report_file}")
    if args.verbose:
        print("Verbose mode enabled")

    # Placeholder implementation
    print("Scan command - Not yet implemented.")
    return 0


def run_organize_command(args: argparse.Namespace) -> int:
    """Execute the organize command to sort files."""
    # Placeholder implementation - will connect to organizer module
    print(f"Organizing files from: {args.input_path}")
    print(f"Output directory: {args.output}")
    if args.dry_run:
        print("DRY RUN MODE - No files will be moved")
    if args.verbose:
        print("Verbose mode enabled")

    # Placeholder implementation
    print("Organize command - Not yet implemented.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point for the PhotoSort command-line interface."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Validate arguments
    errors = validate_arguments(args)
    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        return 1

    # Execute the appropriate command
    try:
        if args.command == "scan":
            return run_scan_command(args)

        return run_organize_command(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
