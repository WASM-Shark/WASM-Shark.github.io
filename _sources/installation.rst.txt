Installation
============

Requirements
------------

- Python 3.8+
- Ubuntu 20.04+ (or any Linux with kernel 5.x+)
- bpftrace (for eBPF runtime monitor)
- Wasabi + Node.js (for dynamic instrumentation)
- Graphviz (for CFG visualization)

Step 1 — Clone and Setup
------------------------

.. code-block:: bash

   git clone https://github.com/WASM-Shark/wasmshark.git
   cd wasmshark

Step 2 — Python Dependencies
-----------------------------

No pip packages required. WASMShark uses only Python standard library.

Optional for YARA integration:

.. code-block:: bash

   pip install yara-python --break-system-packages

Step 3 — eBPF Runtime Monitor
------------------------------

.. code-block:: bash

   sudo apt install bpftrace -y
   sudo bpftrace -e 'BEGIN { print("bpftrace OK\n"); exit(); }'

Step 4 — Wasabi Dynamic Instrumentation
----------------------------------------

.. code-block:: bash

   # Install Rust
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
   source ~/.cargo/env

   # Clone and build Wasabi
   git clone https://github.com/danleh/wasabi.git
   cd wasabi/crates
   cargo install --path ./wasabi
   cd ../..

   # Verify
   wasabi --help

Step 5 — Node.js and long.js
------------------------------

.. code-block:: bash

   sudo apt install nodejs npm -y
   cd ~/wasmshark
   npm install long

Step 6 — wasmtime (for eBPF demos)
------------------------------------

.. code-block:: bash

   curl https://wasmtime.dev/install.sh -sSf | bash
   source ~/.bashrc
   wasmtime --version

Step 7 — Graphviz (for CFG visualization)
------------------------------------------

.. code-block:: bash

   sudo apt install graphviz -y
   dot -V

Step 8 — Generate Test Samples
--------------------------------

.. code-block:: bash

   python3 generate_samples.py

This generates 6 synthetic test WASM binaries:

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - File
     - Size
     - Description
   * - ``sample_cryptominer.wasm``
     - 697 B
     - SHA-256/RandomX/Keccak + .onion C2
   * - ``sample_ransomware.wasm``
     - 1,076 B
     - WASI ransomware + BTC ransom + PowerShell
   * - ``sample_obfuscated_loader.wasm``
     - 2,526 B
     - Indirect calls + encrypted blob + custom sections
   * - ``sample_credential_thief.wasm``
     - 702 B
     - SSH/AWS/shadow + WASI + network exfil
   * - ``sample_browser_cryptojack.wasm``
     - 1,022 B
     - Clipboard + cookie theft + C2
   * - ``sample_clean.wasm``
     - 85 B
     - Fibonacci — clean baseline

Verify Installation
-------------------

.. code-block:: bash

   python3 wasmshark.py sample_cryptominer.wasm -q --rules ./rules/

Expected output::

   MALICIOUS  malice=100.0  obfusc=37.0  confidence=54%
