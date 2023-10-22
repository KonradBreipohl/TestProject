.. _ac-tools:

Algorithm configuration tools
==============================

Irace
-----

Irace (Iterated Race) is an autoconfiguration tool that focuses on tuning the parameters of optimization algorithms.
It employs a racing mechanism to iteratively select the best configurations among a set of candidate configurations based on their performance on a set of problem instances.


.. automodule:: up_ac.Irace_configurator
    :members:

.. automodule:: up_ac.Irace_interface
    :members:


OAT
---

The Optano algorithm tuner (OAT) executes tuning on optimization functions using different algorithms like GGA, GGA++, JADE, and active CMA-ES.
While it is able to run on a single computing node it also supports multiple workers.

.. automodule:: up_ac.OAT_configurator
    :members:    

.. automodule:: up_ac.OAT_interface
    :members:
  

SMAC
----

SMAC (Sequential Model-Based Algorithm Configuration) optimizes algorithm parameters by employing a model-based approach, specifically Bayesian Optimization, to predict the performance of different configurations.
It then uses an aggressive racing mechanism to efficiently compare configurations and iteratively refine the model, directing the search towards regions of the space where better configurations are likely to be found.
In the autoconfiguration Smac can also make use of instance features to improve the predictions.

.. automodule:: up_ac.Smac_configurator
    :members:    

.. automodule:: up_ac.Smac_interface
    :members:
   