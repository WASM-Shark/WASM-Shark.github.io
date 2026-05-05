Architecture
============

WASMShark is composed of three independent analysis layers that each
produce a verdict, which are then correlated for high-confidence detection.

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────┐
   │                        WASMShark                            │
   │                                                             │
   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
   │  │   STATIC    │  │   DYNAMIC   │  │   eBPF RUNTIME      │  │
   │  │  ANALYSIS   │  │  (Wasabi)   │  │    MONITOR          │  │
   │  │             │  │             │  │                     │  │
   │  │ • Parser    │  │ • Instr     │  │ • execve()          │  │
   │  │ • CFG       │  │   counting  │  │ • mmap W+X          │  │
   │  │ • Taint     │  │ • Call graph│  │ • mprotect EXEC     │  │
   │  │ • Entropy   │  │ • State     │  │ • connect()         │  │
   │  │ • Rules     │  │   machine   │  │ • /proc monitor     │  │
   │  │ • Plugins   │  │ • Dyn CFG   │  │                     │  │
   │  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
   │         │                │                    │             │
   │         └────────────────┴────────────────────┘             │
   │                          │                                  │
   │                ┌─────────┴──────────┐                       │
   │                │     CORRELATOR     │                       │
   │                │                    │                       │
   │                │ CONFIRMED_AUTORUN  │                       │
   │                │   CONFIRMED_XOR    │                       │
   │                └─────────┬──────────┘                       │
   │                          │                                  │
   │                   ┌──────┴──────┐                           │
   │                   │   VERDICT   │                           │
   │                   │ MALICIOUS   │                           │
   │                   │ 100.0/100   │                           │
   │                   └─────────────┘                           │
   └─────────────────────────────────────────────────────────────┘

Module Map
----------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Module
     - Responsibility
   * - ``wasmshark.py``
     - CLI entry point, orchestrates all modules
   * - ``wasmshark_core.py``
     - Parser, disassembler, CFG builder, taint analysis, rule engine, scoring, HTML/JSON/SARIF generation
   * - ``wasmshark_advanced.py``
     - WASI capability analyzer, loop characterizer, obfuscation classifier, section anomaly detector, scan history
   * - ``wasmshark_cfg_analysis.py``
     - Dominance tree, SCC, natural loops, irreducibility, path counting, CFG fingerprinting
   * - ``wasmshark_dynamic.py``
     - State machine extraction, dynamic CFG reconstruction, static/dynamic divergence analysis
   * - ``wasmshark_wasabi.py``
     - Wasabi instrumentation runner, Node.js integration, analysis JS, result parser
   * - ``wasmshark_ebpf.py``
     - bpftrace eBPF monitor, /proc polling, alert generation, runtime report
   * - ``wasmshark_watch.py``
     - File system watcher, CI/CD integration
   * - ``wasmshark_yara.py``
     - YARA rule integration (optional)

Data Flow
---------

.. code-block:: text

   WASM binary
       │
       ▼
   WASMParser.parse()
       │ AnalysisReport
       ▼
   ScoringEngine.score()
       │
       ├──► RuleEngine.evaluate()
       │        │ matched_rules, findings
       │
       ├──► PluginManager.run()
       │        │ plugin_results
       │
       ├──► WasabiRunner.run()          (--wasabi)
       │        │ WasabiResult
       │        ▼
       │    extract_state_machine()
       │    reconstruct_dynamic_cfg()
       │    analyze_divergence()
       │
       ├──► generate_html_report()      (--html)
       ├──► to_json_report()            (--json)
       └──► to_sarif()                  (--sarif)

Plugin Interface
----------------

.. code-block:: python

   class WASMPlugin:
       name:        str   # Plugin identifier
       description: str   # Human-readable description
       version:     str   # Version string

       def analyze(self, report: AnalysisReport) -> dict:
           """
           Receive the complete analysis report.
           Return a dict of plugin results.
           Keys should be snake_case strings.
           Must include a 'summary' key.
           """
           ...

Rule Engine
-----------

Rules are parsed from ``.wsr`` files using a simple block format.
The rule engine evaluates conditions against the ``AnalysisReport``
object and creates ``Finding`` objects for each match.

Condition evaluation supports:

- String matching against report fields
- Numeric comparisons (``>``, ``<``, ``>=``, ``<=``)
- Boolean flags (``has_start_func``, ``is_wasi``, etc.)
- Crypto constant presence checks
- Score threshold checks
