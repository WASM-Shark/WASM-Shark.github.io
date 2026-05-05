Plugins
=======

WASMShark has an extensible plugin architecture. Plugins receive the
complete analysis report and return additional findings.

Built-in Plugins
----------------

plugin_call_graph
^^^^^^^^^^^^^^^^^

Builds a function call graph and identifies suspicious call paths.

.. code-block:: text

   [call_graph]
   total_functions: 1
   suspicious_paths: [{'from_func': 5, 'reaches': 'env.sha256_block'}]
   summary: 1 suspicious call paths found

Outputs a Graphviz DOT call graph with suspicious paths highlighted in red.

plugin_cfg_anomaly
^^^^^^^^^^^^^^^^^^

Detects structural anomalies in function CFGs:

- Unreachable basic blocks
- High cyclomatic complexity
- Dispatcher blocks (control flow flattening)
- Monolithic single-block functions (possible packing)

plugin_cfg_advanced
^^^^^^^^^^^^^^^^^^^

Advanced CFG analysis using compiler algorithms:

- Dominance tree (Lengauer-Tarjan)
- Strongly connected components (Tarjan)
- Natural loop detection
- Irreducible CFG detection
- Path count estimation
- CFG fingerprinting

plugin_complexity_analyzer
^^^^^^^^^^^^^^^^^^^^^^^^^^

Computes software complexity metrics per function:

- Halstead volume and effort
- Fan-in / fan-out
- Opcode entropy
- Cyclomatic complexity

.. code-block:: text

   [complexity_analyzer]
   top_complex_functions:
     func[5]: halstead_volume=599.7  effort=1199.4  cyclomatic=1

plugin_memory_safety
^^^^^^^^^^^^^^^^^^^^

Detects suspicious memory access patterns:

- Excessive ``memory.grow`` calls (heap spray indicator)
- Sequential bulk memory writes (encryption/wipe pattern)
- Unchecked loop memory access (buffer overread indicator)

plugin_memory_behavior
^^^^^^^^^^^^^^^^^^^^^^

Behavioral memory analysis:

- Load/store ratio anomalies
- Write-only functions (data staging)
- Read-only functions (data scanning)
- Cross-region memory movement

plugin_opcode_anomaly
^^^^^^^^^^^^^^^^^^^^^

Statistical anomaly detection on opcode frequency distributions using
KL-divergence. Functions whose opcode distribution deviates significantly
from the module baseline are flagged.

plugin_string_deobfuscator
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Attempts to decode obfuscated strings using:

- Base64 decoding
- Hex decoding
- ROT13
- Single-byte XOR brute force
- URL decoding

Running Plugins
---------------

.. code-block:: bash

   # Run all plugins
   python3 wasmshark.py sample.wasm \
     --plugins ./plugins/ --rules ./rules/

   # Run specific plugins (drop unwanted .py files from plugins/)
   python3 wasmshark.py sample.wasm \
     --plugins ./plugins/

Writing Custom Plugins
----------------------

Create a Python file in ``plugins/`` with a ``WASMPlugin`` class:

.. code-block:: python

   from wasmshark_core import AnalysisReport

   class WASMPlugin:
       name        = "my_plugin"
       description = "My custom analysis plugin"
       version     = "1.0"

       def analyze(self, report: AnalysisReport) -> dict:
           # Access report fields
           functions = report.functions
           imports   = report.imports
           findings  = report.findings

           # Return results dict
           return {
               "my_metric": 42,
               "summary":   "Plugin analysis complete"
           }

Available report fields:

.. code-block:: python

   report.filename          # str
   report.file_size         # int
   report.sha256            # str
   report.functions         # List[FunctionAnalysis]
   report.imports           # List[ImportEntry]
   report.exports           # List[ExportEntry]
   report.strings           # List[str]
   report.iocs              # List[Tuple[str,str]]
   report.crypto_hits       # List[Dict]
   report.findings          # List[Finding]
   report.matched_rules     # List[Dict]
   report.malice_score      # float
   report.obfuscation_score # float
   report.verdict           # str
   report.imphash           # str
   report.dead_functions    # List[int]
