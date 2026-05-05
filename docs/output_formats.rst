Output Formats
==============

WASMShark produces four output formats from a single analysis run.

HTML Report
-----------

A self-contained HTML report with dark theme, score bars, and full findings.

.. code-block:: bash

   python3 wasmshark.py sample.wasm --html
   xdg-open sample_wasmshark.html

Sections in the HTML report:

- File metadata (SHA-256, size, entropy, imphash)
- Verdict and score bars (malice, obfuscation, complexity, confidence)
- Matched rules with descriptions
- MITRE ATT&CK tags
- Section layout with per-section entropy
- Import and export tables
- Crypto constants detected
- IoC strings
- Function analysis table
- Extracted strings
- Findings grouped by severity
- Plugin results
- WASI capability analysis
- Loop analysis
- Obfuscation detail
- API abuse score
- Section anomalies
- Entropy timeline (SVG chart)
- Suspicious string scores

JSON Report
-----------

Machine-readable report for integration with other tools.

.. code-block:: bash

   python3 wasmshark.py sample.wasm --json
   cat sample_wasmshark.json | python3 -m json.tool

Key JSON fields:

.. code-block:: json

   {
     "filename":         "sample_cryptominer.wasm",
     "sha256":           "b669127d...",
     "verdict":          "MALICIOUS",
     "scores": {
       "malice":         100.0,
       "obfuscation":    37.0,
       "complexity":     0.0,
       "confidence":     54.0
     },
     "matched_rules":    [...],
     "findings":         [...],
     "iocs":             [...],
     "imports":          [...],
     "functions":        [...],
     "imphash":          "93673bcb...",
     "dead_functions":   [],
     "dynamic_analysis": {...},
     "dynamic_cfg":      {...}
   }

SARIF Report
------------

Static Analysis Results Interchange Format — for integration with GitHub
Code Scanning, VS Code, and other IDE/CI tools.

.. code-block:: bash

   python3 wasmshark.py sample.wasm --sarif
   # Produces: sample_wasmshark.sarif

Upload to GitHub Code Scanning:

.. code-block:: yaml

   # .github/workflows/wasmshark.yml
   - name: Upload SARIF
     uses: github/codeql-action/upload-sarif@v2
     with:
       sarif_file: sample_wasmshark.sarif

CSV Report
----------

Batch scan summary for spreadsheet analysis.

.. code-block:: bash

   python3 wasmshark.py -d ./samples/ \
     --rules ./rules/ --csv results.csv

CSV columns:

.. code-block:: text

   filename, path, verdict, malice_score, obfuscation_score,
   complexity_score, confidence, file_size, entropy, sha256, md5,
   imphash, imports, exports, functions, dead_functions, iocs,
   crypto_hits, rules_matched, rule_names, findings,
   has_start_func, data_segments, mitre_tags

Dynamic CFG DOT
---------------

Graphviz DOT file for dynamic CFG visualization (generated with ``--wasabi``).

.. code-block:: bash

   python3 wasmshark.py sample.wasm --wasabi -q

   # Convert to image
   dot -Tpng sample_dynamic_cfg.dot -o sample_dynamic_cfg.png
   dot -Tsvg sample_dynamic_cfg.dot -o sample_dynamic_cfg.svg

   # View online
   # Paste .dot contents at: https://dreampuf.github.io/GraphvizOnline/
