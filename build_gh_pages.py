#!/usr/bin/env python3
"""
build_gh_pages.py
Builds a self-contained index.html using Stlite (@stlite/browser) to run
CarScope entirely in the browser via WebAssembly on GitHub Pages.
"""

import json
from pathlib import Path

FILES_TO_BUNDLE = [
    "app.py",
    "src/__init__.py",
    "src/ui.py",
    "src/data_loader.py",
    "src/column_mapping.py",
    "src/cleaning.py",
    "src/analytics.py",
    "src/charts.py",
    "src/filters.py",
    "data/sample_cars.csv",
    ".streamlit/config.toml",
]

def main():
    root_dir = Path(__file__).resolve().parent
    bundled = {}
    for rel_path in FILES_TO_BUNDLE:
        full_path = root_dir / rel_path
        if full_path.exists():
            bundled[rel_path] = full_path.read_text(encoding="utf-8")
        else:
            print(f"Warning: {rel_path} not found")

    files_json = json.dumps(bundled)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <title>CarScope 🚘 — Interactive Vehicle Data Analytics</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@stlite/browser@1.10.0/build/stlite.css"
    />
    <style>
      body, html {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        background-color: #0B1220;
      }}
      #root {{
        width: 100%;
        height: 100%;
      }}
      .loading-splash {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #E2E8F0;
        background: #0B1220;
      }}
      .spinner {{
        width: 44px;
        height: 44px;
        border: 4px solid #1E293B;
        border-top: 4px solid #0284C7;
        border-radius: 50%;
        animation: spin 0.9s linear infinite;
        margin-bottom: 20px;
      }}
      @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}
      .title {{
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        margin-bottom: 8px;
      }}
      .subtitle {{
        font-size: 14px;
        color: #94A3B8;
      }}
    </style>
  </head>
  <body>
    <div id="root">
      <div class="loading-splash">
        <div class="spinner"></div>
        <div class="title">CarScope 🚘</div>
        <div class="subtitle">Booting Pyodide & Streamlit WebAssembly engine...</div>
      </div>
    </div>
    <script type="module">
      import {{ mount }} from "https://cdn.jsdelivr.net/npm/@stlite/browser@1.10.0/build/stlite.js";

      const files = {files_json};

      mount(
        {{
          entrypoint: "app.py",
          files: files,
          requirements: ["pandas", "seaborn", "matplotlib"],
          streamlitConfig: {{
            "theme.primaryColor": "#0284C7",
            "theme.backgroundColor": "#F8FAFC",
            "theme.secondaryBackgroundColor": "#F1F5F9",
            "theme.textColor": "#0F172A",
            "server.headless": true
          }}
        }},
        document.getElementById("root")
      );
    </script>
  </body>
</html>
"""

    # Write root index.html
    (root_dir / "index.html").write_text(html_content, encoding="utf-8")
    
    # Also write to docs/ directory
    docs_dir = root_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    (docs_dir / "index.html").write_text(html_content, encoding="utf-8")
    (docs_dir / ".nojekyll").write_text("# Bypass Jekyll\n", encoding="utf-8")
    (root_dir / ".nojekyll").write_text("# Bypass Jekyll\n", encoding="utf-8")

    print(f"Successfully generated self-contained index.html and docs/index.html ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
