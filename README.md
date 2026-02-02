# SignalTrust AI Scanner

An AI-powered content scanning and analysis tool designed to detect security issues, analyze text, and provide intelligent insights.

## Features

- **File Scanning**: Analyze files for security vulnerabilities and content issues
- **Text Analysis**: Scan text content for sensitive information
- **Security Alerts**: Detect potential sensitive data patterns (passwords, API keys, tokens, etc.)
- **Multiple Output Formats**: Export results in JSON or text format
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Requirements

- Python 3.7 or higher
- No additional dependencies required for basic functionality

## Installation

1. Clone the repository:
```bash
git clone https://github.com/signaltrustai/SignalTrust-AI-Scanner.git
cd SignalTrust-AI-Scanner
```

2. (Optional) Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

The easiest way to start the scanner is using the provided startup scripts:

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

**Cross-Platform (Python):**
```bash
python3 start.py
```

### Command Line Usage

You can also run the scanner directly:

```bash
# Interactive mode (displays help)
python3 scanner.py

# Scan a file
python3 scanner.py /path/to/file.txt

# Scan text directly
python3 scanner.py "Your text content here"

# Scan with verbose output
python3 scanner.py -v /path/to/file.txt

# Save results to a file
python3 scanner.py -o results.json /path/to/file.txt

# Save results in text format
python3 scanner.py -o results.txt -f text /path/to/file.txt
```

### Using Startup Scripts with Arguments

You can pass arguments to the startup scripts:

**Linux/Mac:**
```bash
./start.sh -v myfile.txt
./start.sh -o results.json "text to scan"
```

**Windows:**
```cmd
start.bat -v myfile.txt
start.bat -o results.json "text to scan"
```

**Python:**
```bash
python3 start.py -v myfile.txt
python3 start.py -o results.json "text to scan"
```

## Configuration

You can customize the scanner behavior by editing `config.json`:

```json
{
  "scanner": {
    "version": "1.0.0",
    "name": "SignalTrust AI Scanner"
  },
  "settings": {
    "verbose": false,
    "output_format": "json",
    "max_file_size": 10485760
  },
  "security": {
    "enable_security_checks": true,
    "sensitive_patterns": [
      "password",
      "api_key",
      "secret"
    ]
  }
}
```

## Examples

### Example 1: Scan a Text File

```bash
python3 scanner.py -v example.txt
```

Output:
```
============================================================
SignalTrust AI Scanner v1.0.0
============================================================

Scanning target: example.txt

Scan completed for: example.txt
Status: completed
Scan type: file
Findings: 2

Detailed findings:

1. file_analysis: File scanned: example.txt
   - size: 1234
   - lines: 50
   - encoding: utf-8

2. text_analysis: Text content analyzed
   - word_count: 200
   - character_count: 1234
```

### Example 2: Scan and Export Results

```bash
python3 scanner.py -o scan_results.json myfile.py
```

This will scan `myfile.py` and save the results to `scan_results.json`.

### Example 3: Detect Sensitive Information

```bash
python3 scanner.py "My password is secret123"
```

The scanner will detect the word "password" and flag it as a potential security issue.

## Output Format

### JSON Output

```json
[
  {
    "target": "example.txt",
    "status": "completed",
    "findings": [
      {
        "type": "file_analysis",
        "description": "File scanned: example.txt",
        "details": {
          "size": 1234,
          "lines": 50,
          "encoding": "utf-8"
        }
      }
    ],
    "metadata": {
      "scanner_version": "1.0.0",
      "scan_type": "file"
    }
  }
]
```

## Development

### Project Structure

```
SignalTrust-AI-Scanner/
├── scanner.py          # Main scanner module
├── start.py           # Python startup script
├── start.sh           # Linux/Mac startup script
├── start.bat          # Windows startup script
├── config.json        # Configuration file
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Copyright © 2026 SignalTrust AI

## Support

For issues, questions, or contributions, please visit:
https://github.com/signaltrustai/SignalTrust-AI-Scanner

## Version History

### v1.0.0 (2026-02-02)
- Initial release
- File and text scanning capabilities
- Security pattern detection
- Cross-platform startup scripts
- JSON and text output formats

