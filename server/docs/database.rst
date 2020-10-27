============
Architecture
============

.. include:: architecture_flow.txt
   :literal:


The flask server can be served by any of the WSGI HTTP server implementations.
We provide default configuration with the `gunicorn` asynchronous WSGI server,
where individual worker processes handle individual requests.

A database is used as a persistence layer for awaited payments as 
well as a synchronization layer between the WSGI backend and 
the incoming payments of the content-provider's Raiden node.

In order to handle payments for paywalled resources, the database has to be synchronized
with incoming payments from a running Raiden node, which is handled by the :meth:`~raiden_paywall.tasks.database_update_payments` task,
that queries the Raiden API payment endpoint and matches payment-id's from unclaimed Payments 
from the database with incoming Raiden payments. If matching Raiden payments are found,
the Database is updated to represent the correct payment status of a payment request.

.. note::

 Task scheduling for Raiden payment synchronization is handled in the config.py
 with a recurring APScheduler task.
 This configutation file is specific for `gunicorn`, so if you want to use another WSGI server,
 make sure that the :meth:`~raiden_paywall.tasks.database_update_payments` task is run regularly,
 in order to make incoming raiden payments available to the database and thus allkow fast paywall unlocking in the HTTP backend.


Payment state
=============

A Payment can have 4 possible states (`AWAITED`, `PAID`, `TIMED_OUT`, `CLAIMED`) that 
are inferred from different conditions and attributes that are set on the Payment.
The WSGI-threads are responsible for creating new and valid Payments in the `AWAITED` state,
as well as setting the `claimed` flag on payments with state `PAID`.
The Raiden facing worker thread is responsible for associating Raiden payment events with
existing Payments that are in it's `AWAITED` state and thus are not timed out yet.

In the database, there must exist only 1 Payment per payment identifier that is not 
in it's `TIMED_OUT` state to any given time.

 - `AWAITED` - Starting state of the Payment. Conditions:
        - payment has no Raiden payment event associated with it
        - payment was not claimed yet
        - payment did not time out yet

 - `PAID` - Conditions:
        - payment has a Raiden payment event associated with it
        - payment was not claimed yet
        - payment did not time out yet

 - `TIMED_OUT` - Conditions:
        - payment did time out
        - payment was not claimed

 - `CLAIMED` - Conditions:
        - payment has a Raiden payment event associated with it
        - payment was claimed
        - payment did not time out before it was claimed

========
Database
========

An SQLite database is used for storage and by default 
a database file is created under `paywall.db` of 
the server's root path. Currently the database path 
can't be set as a configuration parameter.

Models
======

The database uses the following schemas,
as defined by the JSON-Schema syntax:


.. literalinclude:: schema.json
   :language: python


