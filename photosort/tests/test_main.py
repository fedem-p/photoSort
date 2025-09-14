"""Test module for main CLI functionality."""

import argparse
import tempfile
from pathlib import Path
from unittest.mock import patch

from photosort.main import create_parser, main, validate_arguments


class TestCreateParser:
    """Test cases for create_parser function."""

    def test_parser_creation(self):
        """Test that parser is created successfully."""
        parser = create_parser()
        assert isinstance(parser, argparse.ArgumentParser)
        assert parser.prog == "photosort"

    def test_default_command(self):
        """Test default command is organize."""
        parser = create_parser()
        args = parser.parse_args(["/test/path"])
        assert args.command == "organize"
        assert args.input_path == Path("/test/path")

    def test_scan_command(self):
        """Test scan command parsing."""
        parser = create_parser()
        args = parser.parse_args(["/test/path", "--command", "scan"])
        assert args.command == "scan"
        assert args.input_path == Path("/test/path")

        # Test shorthand --scan
        args = parser.parse_args(["/test/path", "--scan"])
        assert args.command == "scan"
        assert args.input_path == Path("/test/path")

    def test_organize_command_explicit(self):
        """Test explicit organize command parsing."""
        parser = create_parser()
        args = parser.parse_args(["/test/path", "--command", "organize"])
        assert args.command == "organize"
        assert args.input_path == Path("/test/path")

    def test_dry_run_flag(self):
        """Test dry-run flag parsing."""
        parser = create_parser()
        args = parser.parse_args(["--dry-run", "/test/path"])
        assert args.dry_run is True

        args = parser.parse_args(["-n", "/test/path"])
        assert args.dry_run is True

    def test_output_option(self):
        """Test output option parsing."""
        parser = create_parser()
        args = parser.parse_args(["--output", "/output/path", "/test/path"])
        assert args.output == Path("/output/path")

        args = parser.parse_args(["-o", "/output/path", "/test/path"])
        assert args.output == Path("/output/path")

    def test_verbose_flag(self):
        """Test verbose flag parsing."""
        parser = create_parser()
        args = parser.parse_args(["--verbose", "/test/path"])
        assert args.verbose is True

        args = parser.parse_args(["-v", "/test/path"])
        assert args.verbose is True

    def test_report_file_option(self):
        """Test report file option parsing."""
        parser = create_parser()
        args = parser.parse_args(["--report-file", "/report.json", "/test/path"])
        assert args.report_file == Path("/report.json")

        args = parser.parse_args(["-r", "/report.json", "/test/path"])
        assert args.report_file == Path("/report.json")

    def test_log_file_option(self):
        """Test log file option parsing."""
        parser = create_parser()
        args = parser.parse_args(["--log-file", "/log.json", "/test/path"])
        assert args.log_file == Path("/log.json")

        args = parser.parse_args(["-l", "/log.json", "/test/path"])
        assert args.log_file == Path("/log.json")


class TestValidateArguments:
    """Test cases for validate_arguments function."""

    def test_validate_nonexistent_input_path(self):
        """Test validation fails for nonexistent input path."""
        args = argparse.Namespace(
            command="scan",
            input_path=Path("/nonexistent/path"),
            output=None,
            report_file=None,
            log_file=None,
        )
        errors = validate_arguments(args)
        assert len(errors) == 1
        assert "Input path does not exist" in errors[0]

    def test_validate_input_path_not_directory(self):
        """Test validation fails when input path is not a directory."""
        with tempfile.NamedTemporaryFile() as tmp_file:
            args = argparse.Namespace(
                command="scan",
                input_path=Path(tmp_file.name),
                output=None,
                report_file=None,
                log_file=None,
            )
            errors = validate_arguments(args)
            assert len(errors) == 1
            assert "Input path is not a directory" in errors[0]

    def test_validate_valid_input_path(self):
        """Test validation passes for valid input path."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = argparse.Namespace(
                command="scan",
                input_path=Path(tmp_dir),
                output=None,
                report_file=None,
                log_file=None,
            )
            errors = validate_arguments(args)
            assert len(errors) == 0

    def test_validate_sets_default_output_for_organize(self):
        """Test validation sets default output path for organize command."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = argparse.Namespace(
                command="organize",
                input_path=Path(tmp_dir),
                output=None,
                report_file=None,
                log_file=None,
            )
            errors = validate_arguments(args)
            assert len(errors) == 0
            assert args.output == Path(tmp_dir) / "sorted"

    def test_validate_sets_default_report_file(self):
        """Test validation sets default report file path."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = argparse.Namespace(
                command="scan",
                input_path=Path(tmp_dir),
                output=None,
                report_file=None,
                log_file=None,
            )
            errors = validate_arguments(args)
            assert len(errors) == 0
            assert args.report_file == Path(tmp_dir) / "photosort_report.json"

    def test_validate_sets_default_log_file(self):
        """Test validation sets default log file path."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = argparse.Namespace(
                command="scan",
                input_path=Path(tmp_dir),
                output=None,
                report_file=None,
                log_file=None,
            )
            errors = validate_arguments(args)
            assert len(errors) == 0
            assert args.log_file == Path(tmp_dir) / "photosort_log.json"

    def test_validate_output_path_exists_but_not_directory(self):
        """Test validation fails when output path exists but is not a directory."""
        with tempfile.TemporaryDirectory() as tmp_dir, tempfile.NamedTemporaryFile() as tmp_file:
            args = argparse.Namespace(
                command="organize",
                input_path=Path(tmp_dir),
                output=Path(tmp_file.name),
                report_file=None,
                log_file=None,
            )
            errors = validate_arguments(args)
            assert len(errors) == 1
            assert "Output path exists but is not a directory" in errors[0]


class TestMainFunction:
    """Test cases for main function."""

    def test_main_with_invalid_input_path(self, capsys):
        """Test main function with invalid input path."""
        result = main(["/nonexistent/path", "--scan"])
        assert result == 1
        captured = capsys.readouterr()
        assert "Error: Input path does not exist" in captured.err

    def test_main_scan_command(self, capsys):
        """Test main function with scan command."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = main([tmp_dir, "--command", "scan"])
            assert result == 0
            captured = capsys.readouterr()
            assert f"Scanning files in: {tmp_dir}" in captured.out
            assert "Scan command - Not yet implemented." in captured.out

    def test_main_organize_command(self, capsys):
        """Test main function with organize command."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = main([tmp_dir, "--command", "organize"])
            assert result == 0
            captured = capsys.readouterr()
            assert f"Organizing files from: {tmp_dir}" in captured.out
            assert "Organize command - Not yet implemented." in captured.out

    def test_main_organize_command_dry_run(self, capsys):
        """Test main function with organize command and dry-run."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = main([tmp_dir, "--command", "organize", "--dry-run"])
            assert result == 0
            captured = capsys.readouterr()
            assert "DRY RUN MODE - No files will be moved" in captured.out

    def test_main_with_verbose_flag(self, capsys):
        """Test main function with verbose flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = main([tmp_dir, "--scan", "--verbose"])
            assert result == 0
            captured = capsys.readouterr()
            assert "Verbose mode enabled" in captured.out

    def test_main_default_command(self, capsys):
        """Test main function with default command (organize)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = main([tmp_dir])
            assert result == 0
            captured = capsys.readouterr()
            assert f"Organizing files from: {tmp_dir}" in captured.out

    def test_main_keyboard_interrupt(self, capsys):
        """Test main function handling keyboard interrupt."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch(
                "photosort.main.run_scan_command", side_effect=KeyboardInterrupt
            ):
                result = main([tmp_dir, "--scan"])
                assert result == 130
                captured = capsys.readouterr()
                assert "Operation cancelled by user." in captured.err

    def test_main_unexpected_exception(self, capsys):
        """Test main function handling unexpected exception."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch(
                "photosort.main.run_scan_command",
                side_effect=RuntimeError("Test error"),
            ):
                result = main([tmp_dir, "--scan"])
                assert result == 1
                captured = capsys.readouterr()
                assert "Unexpected error: Test error" in captured.err

    def test_main_with_custom_output_path(self, capsys):
        """Test main function with custom output path."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            custom_output = Path(tmp_dir) / "custom_output"
            result = main(
                [tmp_dir, "--command", "organize", "--output", str(custom_output)]
            )
            assert result == 0
            captured = capsys.readouterr()
            assert f"Output directory: {custom_output}" in captured.out

    def test_main_with_custom_report_file(self, capsys):
        """Test main function with custom report file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            custom_report = Path(tmp_dir) / "custom_report.json"
            result = main([tmp_dir, "--scan", "--report-file", str(custom_report)])
            assert result == 0
            captured = capsys.readouterr()
            assert f"Report will be saved to: {custom_report}" in captured.out
