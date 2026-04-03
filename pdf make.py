import sys
import subprocess

def install_and_import(package_name, module_name=None):
    if module_name is None:
        module_name = package_name
    try:
        __import__(module_name)
    except ImportError:
        print(f"Module '{module_name}' is missing. Installing '{package_name}'...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
            print(f"Successfully installed {package_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_name}. Error: {e}")
            sys.exit(1)

# Check dependencies before running the rest of the script
install_and_import("markdown")
install_and_import("xhtml2pdf")

import os
import glob
import re
import argparse
from datetime import datetime
import markdown
from xhtml2pdf import pisa

def parse_date_from_text(text, filename):
    """
    Extracts dates like 'April 1–2, 2026' or 'March 14, 2026' from the text content.
    Returns a datetime object for sorting, and the extracted string for labeling.
    """
    months = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
    pattern = re.compile(rf"({months})\s+(\d{{1,2}})(?:\s*(?:[-–—]|to|â€“)\s*\d{{1,2}})?,\s*(\d{{4}})", re.IGNORECASE)
    
    match = pattern.search(text)
    if match:
        month_str, day_str, year_str = match.groups()
        try:
            clean_date_str = f"{month_str} {day_str}, {year_str}"
            return datetime.strptime(clean_date_str, "%B %d, %Y"), match.group(0)
        except ValueError:
            pass
            
    # Fallback to filename if no date found in the text
    try:
        date_str = os.path.basename(filename).replace('Grok_Task_', '').replace('.md', '')
        return datetime.strptime(date_str, '%Y-%m-%dT%H-%M-%S'), "Date from filename"
    except ValueError:
        return datetime.min, "Unknown Date"

def main():
    parser = argparse.ArgumentParser(description="Compile downloaded Markdown tasks into a styled PDF.")
    parser.add_argument("-i", "--input", default="md files", help='Directory containing the markdown files (default: "md files").')
    parser.add_argument("-o", "--output", default="compiled_tasks.pdf", help='Output PDF filename or path (default: "compiled_tasks.pdf").')
    args = parser.parse_args()

    md_dir = args.input
    output_pdf = args.output

    # Resolve paths relative to the current script directory if not absolute
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_dir_path = os.path.abspath(md_dir) if os.path.isabs(md_dir) else os.path.join(script_dir, md_dir)
    output_pdf_path = os.path.abspath(output_pdf) if os.path.isabs(output_pdf) else os.path.join(script_dir, output_pdf)

    # Note: glob will find files if they exist in the md_dir
    md_files = glob.glob(os.path.join(md_dir_path, '*.md'))
    
    if not md_files:
        print(f"No '.md' files found in '{md_dir_path}'.")
        return
        
    print(f"Found {len(md_files)} markdown file(s). Processing...")

    file_data = []
    for file in md_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        date_obj, extracted_str = parse_date_from_text(content, file)
        file_data.append({
            'date': date_obj,
            'date_label': extracted_str,
            'filepath': file,
            'content': content
        })

    # Sort files chronologically based on the extracted text dates
    file_data.sort(key=lambda x: x['date'])

    # --- 19TH CENTURY ACADEMIC CSS & HTML STRUCTURE ---
    combined_html = """
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {
                margin: 2.5cm;
                background-color: #f0e6d2; 
            }
            body { 
                background-color: #f0e6d2;
                font-family: 'Book Antiqua', Palatino, 'Palatino Linotype', Georgia, serif; 
                font-size: 14pt; 
                line-height: 1.6; 
                color: #2c1e16; 
                margin: 0;
                padding: 0;
            }
            h1 { 
                color: #1a110b; 
                text-align: center; 
                text-transform: uppercase; 
                letter-spacing: 3px; 
                border-bottom: 3px double #5c3a21; 
                padding-bottom: 15px;
                font-weight: normal; 
                font-size: 26pt;
                margin-bottom: 40px;
            }
            h2 { 
                color: #3d2616; 
                border-bottom: 1px solid #8c6d53; 
                padding-bottom: 5px; 
                margin-top: 40px; 
                font-size: 18pt;
                font-style: italic; 
            }
            h3 {
                color: #4a3b32;
                font-size: 15pt;
                font-weight: bold;
            }
            .meta-info { 
                color: #5c534d; 
                font-size: 11pt; 
                margin-bottom: 25px; 
                font-style: italic; 
                text-align: left;
                padding: 8px 12px;
                background-color: #e6d8c3; 
                border-left: 4px solid #8b7355;
            }
            a {
                color: #5c3a21;
                text-decoration: none;
                border-bottom: 1px dashed #5c3a21;
            }
            code { 
                font-family: 'Courier New', Courier, monospace;
                background-color: #e6d8c3; 
                color: #4a2e1b; 
                padding: 2px 6px; 
                border: 1px solid #d1bfae;
                font-size: 12pt;
            }
            pre { 
                background-color: #2b2622; 
                color: #dcd3c6; 
                padding: 15px; 
                border-left: 5px solid #8b7355;
                font-size: 12pt;
            }
            pre code {
                background-color: transparent;
                color: inherit;
                border: none;
                padding: 0;
            }
            blockquote { 
                border-left: 4px solid #8b7355; 
                margin: 20px 0; 
                padding: 10px 20px; 
                background-color: #e6d8c3; 
                color: #4a3b32; 
                font-style: italic; 
            }
            ul, ol {
                padding-left: 30px;
            }
            li {
                margin-bottom: 10px;
            }
            hr.divider {
                border: 0;
                border-top: 2px dashed #8c6d53;
                margin: 50px 0;
            }
        </style>
    </head>
    <body>
        <h1>Compiled Technical Summaries</h1>
    """

    for data in file_data:
        html_content = markdown.markdown(data['content'], extensions=['tables', 'fenced_code'])
        
        formatted_date = data['date'].strftime('%B %d, %Y')
        extracted_context = data['date_label']
        
        combined_html += f"<h2>Report: {formatted_date}</h2>\n"
        combined_html += f"<div class='meta-info'><strong>Extracted Context:</strong> {extracted_context} <br> <strong>Source Archive:</strong> {os.path.basename(data['filepath'])}</div>\n"
        combined_html += html_content + "\n<hr class='divider'>\n"

    combined_html += """
    </body>
    </html>
    """

    print(f"Generating PDF: {output_pdf_path}...")

    try:
        with open(output_pdf_path, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                combined_html,
                dest=result_file,
                encoding='utf-8'
            )

        if pisa_status.err:
            print(f"Error generating PDF: {pisa_status.err}")
        else:
            print("PDF generation complete!")
            
    except Exception as e:
        print(f"Exception encountered: {e}")

if __name__ == "__main__":
    main()
