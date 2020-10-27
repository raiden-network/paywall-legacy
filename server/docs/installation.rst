=====================
Installation & Usage
=====================

.. note::

        Please install the raiden-paywall inside 
        of a virtual environment!



1) Install Raiden
=================

Please consult the `official Raiden documentation <https://docs.raiden.network/installation/starting-raiden-manually#downloading-raiden>`_ on how to get a stable version of the Python Raiden node running.
The `raiden-paywall` currently supports Raiden version `1.1.1`, but should be compatible 
with all future versions.


2) Install the `raiden-paywall` server:
========================================

.. code-block:: shell

        cd paywall/server
        make install-dev

3) Start the Raiden node
==============================

.. code-block:: shell

        raiden \
        --address <node-hex-address> \
        --keystore-path <path-to-keystore> \
        --password-file <path-to-password-file> \
        --config-file config-dev.toml


4) Start the WSGI server:
===============================

.. code-block:: shell

        make start-server


For configuration of the `raiden-paywall`, see :ref:`config`.
It is assumed, that the Raiden node is connected to the Goerli testnet and has a connection to
the paying nodes on the Token-Network that is specified in the config file.


