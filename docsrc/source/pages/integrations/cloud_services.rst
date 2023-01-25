==============
Cloud services
==============

``ydata-profiling`` can be easily used in several hosted computation services.

Lambda GPU Cloud
----------------

.. image:: https://lambdalabs.com/static/images/lambda-logo.png
  :align: right
  :width: 25%

``ydata-profiling`` will be pre-installed on one of the `Lambda GPU Cloud <https://lambdalabs.com/>`_ images. ``pandas-profiling`` itself does not provide GPU acceleration, but does support a workflow in which GPU acceleration is possible, e.g. this is a great setup for profiling your image datasets while developing computer vision applications. Learn how to launch a 4x GPU instance `here <https://www.youtube.com/watch?v=fI3gvaX1crY>`_.

Google Cloud
------------

The Google Cloud Platform documentation features an article that uses ``ydata-profiling``. You can check it here: `Building a propensity model for financial services on Google Cloud <https://github.com/GoogleCloudPlatform/analytics-componentized-patterns/blob/master/retail/propensity-model/bqml/bqml_kfp_retail_propensity_to_purchase.ipynb>`_.

Kaggle
------

``ydata-profiling`` is available in `Kaggle notebooks <https://www.kaggle.com/notebooks>`_ by default, as it is included in the `standard Kaggle image <https://github.com/Kaggle/docker-python/blob/master/Dockerfile>`_.
