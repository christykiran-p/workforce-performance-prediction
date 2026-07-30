"""
Workforce Performance Intelligence Platform - PDF / HTML Generator Script
Exports the comprehensive tutorial document into a print-optimized PDF-ready HTML page.
"""

import re
from pathlib import Path

INPUT_MD = Path("Workforce_Performance_Prediction_Tutorial.md")
OUTPUT_HTML = Path("Workforce_Performance_Prediction_Tutorial.html")

def convert_md_to_printable_html():
    if not INPUT_MD.exists():
        print(f"Error: {INPUT_MD} not found.")
        return

    content = INPUT_MD.read_text(encoding="utf-8")

    # Simple HTML conversion for headings, code blocks, tables, and lists
    html_lines = []
    in_code_block = False
    code_lang = ""

    html_lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Workforce Performance Intelligence - Comprehensive Tutorial</title>
<style>
    @page {
        size: A4;
        margin: 20mm;
    }
    body {
        font-family: 'Segoe UI', Arial, sans-serif;
        line-height: 1.6;
        color: #1e293b;
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
        background: #ffffff;
    }
    h1 { font-size: 26px; color: #0f172a; border-bottom: 3px solid #2563eb; padding-bottom: 8px; margin-top: 30px; }
    h2 { font-size: 20px; color: #1e40af; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; margin-top: 25px; }
    h3 { font-size: 16px; color: #334155; margin-top: 20px; }
    code { font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 13px; }
    pre { background: #0f172a; color: #f8fafc; padding: 15px; border-radius: 8px; overflow-x: auto; font-size: 12px; line-height: 1.45; }
    pre code { background: none; color: inherit; padding: 0; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
    th, td { border: 1px solid #cbd5e1; padding: 10px 12px; text-align: left; }
    th { background: #f8fafc; font-weight: 600; color: #0f172a; }
    tr:nth-child(even) { background: #f8fafc; }
    blockquote { border-left: 4px solid #2563eb; background: #eff6ff; margin: 15px 0; padding: 10px 15px; color: #1e3a8a; }
    @media print {
        body { max-width: 100%; padding: 0; }
        pre { page-break-inside: avoid; }
        h1, h2, h3 { page-break-after: avoid; }
    }
</style>
</head>
<body>
""")

    for line in content.splitlines():
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lang = line.strip("`").strip()
                html_lines.append(f'<pre><code class="{code_lang}">')
            else:
                in_code_block = False
                html_lines.append('</code></pre>')
            continue

        if in_code_block:
            escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_lines.append(escaped_line)
            continue

        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"### {line[4:]}")
        elif line.startswith("#### "):
            html_lines.append(f"<h4>{line[5:]}</h4>")
        elif line.startswith("---"):
            html_lines.append("<hr/>")
        elif line.strip() == "":
            html_lines.append("<br/>")
        else:
            # Simple inline bold/code replacement
            formatted = line
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
            formatted = re.sub(r'`(.*?)`', r'<code>\1</code>', formatted)
            html_lines.append(f"<p>{formatted}</p>")

    html_lines.append("</body></html>")

    OUTPUT_HTML.write_text("\n".join(html_lines), encoding="utf-8")
    print(f"Printable Tutorial HTML successfully generated -> {OUTPUT_HTML.resolve()}")

if __name__ == "__main__":
    convert_md_to_printable_html()
