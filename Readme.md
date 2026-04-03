# Grok Task Downloader & PDF Compiler

A complete two-part toolkit to extract your conversation tasks from Grok and compile them into a beautifully styled, single PDF document with a 19th-century academic aesthetic. 

The project consists of a **Browser Userscript** to download the chats as Markdown (`.md`) files, and a **Python script** to chronologically merge and style them.

## Features

- **Automated Chat Extraction:** A Tampermonkey/Violentmonkey userscript that seamlessly downloads your Grok tasks directly into Markdown format.
- **Smart Date Extraction:** Intelligently extracts dates written within the actual Markdown text to chronologically sort reports.
- **Fail-safe Filename Parsing:** Automatically falls back to parsing dates directly from filenames (e.g., `Grok_Task_YYYY-MM-DDTHH-MM-SS.md`).
- **19th-Century Academic Aesthetic:** Utilizes the `xhtml2pdf` library to apply a vintage parchment background color, deep sepia typefaces, and classic layouts directly to the output PDF.
- **Auto-Dependency Setup:** The Python script automatically checks for and installs any missing required packages (`markdown` and `xhtml2pdf`).

## Step 1: Downloading Tasks (Userscript)

To extract your tasks from the web interface, use the included browser userscript:

1. Install a userscript manager extension in your browser (e.g., **Tampermonkey**, **Violentmonkey**, or **Greasemonkey**).
2. Add the contents of `Downloadeing Script.js` (or import the file) into your userscript manager to create a new script.
3. Keep the script enabled, navigate to the Grok web interface, and use the script's injected functionality to batch-download your tasks. 
4. Move all the downloaded `.md` files into a folder (by default, name it `md files/` in this project directory).

## Step 2: Compiling the PDF (Python)

Once you have your downloaded `.md` files, use the Python command-line tool to compile them. Ensure you have Python 3.x installed.

### Basic Run
By default, the script reads all markdown files from the `md files/` directory and outputs a final file named `compiled_tasks.pdf` in the current folder.

```bash
python "pdf make.py"
```

### Custom Input and Output
You can define specific folders to fetch markdown files from and set a custom output name using the `-i` (input) and `-o` (output) flags.

```bash
python "pdf make.py" -i "path/to/your/markdown_folder" -o "custom_tech_report.pdf"
```

### Get Help
To see a full list of commands and default values, view the help menu:

```bash
python "pdf make.py" --help
```
