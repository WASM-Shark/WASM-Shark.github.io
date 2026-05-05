CLI Reference
=============

.. code-block:: text

   python3 wasmshark.py [OPTIONS] [FILE]

Arguments
---------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Argument
     - Description
   * - ``file``
     - WASM binary to analyze (positional)

Output Options
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``-v``, ``--verbose``
     - Show full analysis report
   * - ``-q``, ``--quiet``
     - Show verdict line only
   * - ``--html``
     - Write HTML report
   * - ``--json``
     - Write JSON report
   * - ``--sarif``
     - Write SARIF report (for IDE/CI integration)
   * - ``--output-html FILE``
     - Custom HTML output path
   * - ``--output-json FILE``
     - Custom JSON output path
   * - ``--cfg-dir DIR``
     - Export CFG DOT files to directory

Analysis Options
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``--rules-dir DIR``
     - Load ``.wsr`` rule files from directory
   * - ``--plugins-dir DIR``
     - Load plugins from directory
   * - ``--wasabi``
     - Run Wasabi dynamic instrumentation
   * - ``--cfg-anomaly``
     - Run CFG anomaly detection on all functions
   * - ``--cfg-overview DIR``
     - Export module-level CFG overview to directory
   * - ``--disasm``
     - Show disassembly of top suspicious functions

Batch Operations
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``-d``, ``--scan-dir DIR``
     - Scan directory for all ``.wasm`` files
   * - ``--csv OUT.CSV``
     - Write batch scan results to CSV (use with ``-d``)
   * - ``--diff FILE_B``
     - Compare FILE against FILE_B

Examples
--------

.. code-block:: bash

   # Basic scan
   python3 wasmshark.py sample.wasm

   # Full analysis
   python3 wasmshark.py sample.wasm -v \
     --rules ./rules/ --plugins ./plugins/ \
     --html --json --sarif

   # Quiet mode with rules
   python3 wasmshark.py sample.wasm -q --rules ./rules/

   # Directory scan + CSV
   python3 wasmshark.py -d ./samples/ \
     --rules ./rules/ --csv results.csv

   # Diff two binaries
   python3 wasmshark.py a.wasm --diff b.wasm --rules ./rules/

   # Static + Wasabi dynamic
   python3 wasmshark.py sample.wasm --rules ./rules/ --wasabi

   # CFG anomaly export
   python3 wasmshark.py sample.wasm \
     --plugins ./plugins/ \
     --cfg-anomaly --cfg-overview ./cfgs/

Watch Mode
----------

.. code-block:: text

   python3 wasmshark_watch.py [PATHS...] [OPTIONS]

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``--rules-dir DIR``
     - Rules directory for rescans
   * - ``--plugins-dir DIR``
     - Plugins directory for rescans
   * - ``-i``, ``--interval SECS``
     - Poll interval in seconds (default: 1.0)
   * - ``--on-malicious CMD``
     - Shell command to run on MALICIOUS verdict. Use ``{file}``

eBPF Monitor
------------

.. code-block:: text

   python3 wasmshark_ebpf.py [OPTIONS]

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``--pid PID``
     - PID to monitor (required)
   * - ``--bpf``
     - Enable bpftrace eBPF probes
   * - ``--no-bpf``
     - Use /proc polling only
   * - ``--timeout SECS``
     - Duration in seconds
   * - ``--output FILE``
     - Write JSON report to FILE
