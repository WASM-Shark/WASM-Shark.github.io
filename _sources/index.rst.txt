.. WASMShark documentation master file

WASMShark — WebAssembly Malware Analyzer
===============================================

.. image:: https://img.shields.io/badge/version-1.0-blue
.. image:: https://img.shields.io/badge/python-3.8%2B-brightgreen


**WASMShark** is a university project. It's a WebAssembly malware analyzer combining
static analysis, dynamic instrumentation, and eBPF kernel-level runtime
monitoring — the first tool of its kind for WASM binary analysis.

.. code-block:: text

    ██╗    ██╗ █████╗ ███████╗███╗   ███╗███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗
    ██║    ██║██╔══██╗██╔════╝████╗ ████║██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝
    ██║ █╗ ██║███████║███████╗██╔████╔██║███████╗███████║███████║██████╔╝█████╔╝
    ██║███╗██║██╔══██║╚════██║██║╚██╔╝██║╚════██║██╔══██║██╔══██║██╔══██╗██╔═██╗
    ╚███╔███╔╝██║  ██║███████║██║ ╚═╝ ██║███████║██║  ██║██║  ██║██║  ██║██║  ██╗
     ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    WebAssembly Malware Analyzer

.. admonition:: Key Capabilities

   - **Static Analysis** — Full WASM binary parser, disassembler, CFG, taint analysis
   - **Dynamic Analysis** — Wasabi instruction-level instrumentation, state machine extraction
   - **Runtime Monitoring** — eBPF/bpftrace kernel tracepoints, W+X memory detection
   - **170+ Detection Rules** — Cryptominer, ransomware, C2, dropper, credential theft
   - **CFG Analysis** — Dominance trees, SCC, natural loops, irreducibility detection

----

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Analysis Modules

   static_analysis
   dynamic_analysis
   ebpf_monitor
   cfg_analysis

.. toctree::
   :maxdepth: 2
   :caption: Detection

   rules
   plugins

.. toctree::
   :maxdepth: 2
   :caption: Reference

   cli_reference
   output_formats
   architecture

----

Detection Results
-----------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Sample
     - Verdict
     - Rules Matched
   * - ``sample_cryptominer.wasm``
     - MALICIOUS 100/100
     - CRYPTOMINER_WASM, TOR_C2_BEACON, RANDOMX_MONERO_MINER
   * - ``sample_ransomware.wasm``
     - MALICIOUS 100/100
     - WASI_RANSOM_TRIAD, RANSOMWARE_KW, WASI_DROPPER
   * - ``sample_obfuscated_loader.wasm``
     - MALICIOUS 100/100
     - BALANCED_MALICE_OBFUSC, XOR_DECRYPTOR, INDIRECT_DISPATCHER
   * - ``sample_credential_thief.wasm``
     - MALICIOUS 100/100
     - WASI_DROPPER, CREDENTIAL_EXFIL
   * - ``sample_browser_cryptojack.wasm``
     - MALICIOUS 100/100
     - CRYPTOMINER_WASM, BROWSER_STORAGE_EXFIL
   * - ``sample_clean.wasm``
     - CLEAN 0/100
     - —
