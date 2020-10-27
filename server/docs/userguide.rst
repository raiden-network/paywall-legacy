==========
User Guide
==========


For configuration of the `raiden-paywall`, see :ref:`config`.
The `raiden-paywall` is provided as a Flask-extension, that is initialized
by providing it with the Flask application:

.. code-block:: python

        from flask import Flask
        from flask_raiden import RaidenPaywall
        
        app = Flask(__name__)
        paywall = RaidenPaywall(app)
        

The Paywall API provides a very simple interface, that is complying with flask's *per-request*
architecture. Inside of a view function, the amount of token to be paid for this request 
can be modified dynamically by modifying the :attr:`~raiden_paywall.flask_raiden.RaidenPaywall.amount` attribute.


At what time the database is queried for valid Payment associated with the current request can be controlled by calling :meth:`~raiden_paywall.flask_raiden.RaidenPaywall.check_payment`.
That way, the payment can be checked before heavy computation is done during the request lifecycle. 

An optional, additional preview can be provided to the payment request by wrapping the preview in a call to :meth:`~raiden_paywall.flask_raiden.RaidenPaywall.preview` just before returning the view function.

.. code-block:: python

  @app.route('/compute/<computations>')
  def get_expensive_stuff(computations):
      # here we could observe the request and calculate the amount to pay based on request data
      computations = int(computations)
      # this is the base amount!
      paywall.amount += 0.0001
  
      # now we also add dynamic pricing based on the request param!
      paywall.amount += 0.000001 * computations
  
      # Now it is checked, wether a payment identifier was provided in the request,
      # and wether that identifier corresponds to a paid, unclaimed payment in Raiden:
      if not paywall.check_payment():
          # if this is not the case, attach a preview to the response, which will also contain
          # the payment request
          return paywall.preview(f'If you pay, this would compute {computations} rounds of computations!')

      # If the payment was valid, it is considered as claimed at this point;
      # now we can do heavy computation
      for _ in range(computations):
          pr = 213123
          pr * pr
          pr = pr + 1
      # and return the result:
      return f"Thank you for paying! Here is the result of your computation: {pr}"

If  there is a payment amount set on the app context before the request returns,
the resource will automatically be converted to a response requesting the payment,
if no valid payment was associated with the request:


.. code-block:: python

  @app.route('/simple')
  def simple_endpoint():
      paywall.amount = 0.1
      return f"Simple resource text."


While non-paywalled resources are achieved by not setting a payment amount 
on the app context:

.. code-block:: python

  @app.route('/unpaywalled')
  def unpaywalled_endpoint():
      return f"This one is for free!"

There is no persisting association between an initial request and subsequent
request tries: the initial request is **not** cached and executed after successful payment!
The initial request is rather a means for the caller to observe that the endpoint **is** paywalled in the first place,
and it will inform the caller what payment is expected for the combination of requested enpoint and parameters.

This means, that since there is no "session persitence", the requested Payment should always be deterministic
for a specific combination of endpoint and request parameters!

For example, this would be a non-deterministic endpoint pricing, which should 
be avoided by all means:

.. code-block:: python

        import datetime
        
        @app.route('/paytime')
        def get_expensive_stuff():
            current_time = datetime.datetime.utcnow()
            paywall.amount = current_time.timestamp() * 0.00001
            if not paywall.check_payment():
            	return paywall.preview(f'You know what time it is?')
            return currrent_time


Here, between the first request and a second request some time will pass, which will lead to increasing the amount
to be paid for this endpoint. Even if the requester successfully sends a transfer with the amount as specified in the payment requesst that is contained in the first response, 
they will be unable to claim the payment and pass the paywall, since the call to :meth:`~raiden_paywall.flask_raiden.RaidenPaywall.check_payment` will assume a slightly higher transfer-amount, letting the check fail.
