.. _config:

=====================
Configuration options
=====================


The paywall-raiden server is configured with a configuration file
that complies to the standard Python syntax.
The file has to contain variables on the module level (like global variables)
and has the following options:

.. code-block:: python

        # paywall_config.cfg

        RD_TOKEN_ADDRESS = "0xC563388e2e2fdD422166eD5E76971D11eD37A466"  # Token address of the token to receive paywall payments
        RD_TOKEN_DECIMALS = 18  # Token decimals of the corresponding RD_TOKEN_ADDRESS, used to convert the relative amount to absolute
        RD_DEFAULT_TIMEOUT = "10mins"  # how long the server waits for a payment after a payment request is sent
        RD_DEFAULT_AMOUNT = 0.001  # DEPRECATED - has no effect and will be deprecated
        RD_API_ENDPOINT = 'http://localhost:5002'  # the API endpoint of the Raiden node that receives paywall payments
        RD_NETWORK_ID = 5  # Network id - should correspond to the Network the Raiden node is running on. Currently only 5 (GOERLI) supported


The file has to be provided to the paywall-raiden application by specifying it in
the `RAIDEN_PAYWALL_SETTINGS` environment variable:


.. code-block:: bash

        export RAIDEN_PAYWALL_SETTINGS=paywall_config.cfg


