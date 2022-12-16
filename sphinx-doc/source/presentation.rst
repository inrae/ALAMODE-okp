Presentation
============
What is the ``okplm`` package?
------------------------------
``okplm`` (Ottosson-Kettle-Prats lake model) is a package in Python 3 used to
simulate the epilimnion and hypolimnion temperature of freshwater bodies using
the Ottosson-Kettle-Prats (OKP) lake model (Prats & Danis, 2019).

The OKP model simulates water
temperature at the daily frequency using air temperature [in ºC] and solar radiation
[in W m\ :sup:`2`\ ] as forcing data. The OKP model is the result of the combination
of the models presented by Ottosson & Abrahamsson (1998) and Kettle *et al.* (2004).
The development of the model was funded by the AFB (French Agency for Biodiversity,
previously ONEMA, French National Office for Water and Aquatic
Environments) and a preliminary version was presented in the report by Prats &
Danis (2015). The definitive version was published by Prats & Danis (2019).

To calculate water temperatures with ``okplm`` the values of a series of parameters
need to be defined. It is possible to use the default parameter values obtained for French
water bodies. These values are the result of the parameterisation as a function
of lake characteristics (latitude, altitude, maximum depth, surface area,
volume) proposed by Prats & Danis (2019). This parameterisation was derived by
analysing data from the French national measuring networks set up for the application
of the European Water Framework Directive for 414 French water bodies with surface area
larger than 0.06 km\ :sup:`2`\ . The following table summarises the range of values of
the characteristics of these water bodies and thus the domain of
applicability of the default parameterisation.

============================= ======== ========
**Variable**                  **Min.** **Max.**
============================= ======== ========
Altitude (m)                  0.0      2841
Latitude (ºN)                 41.47    50.87
Max. depth (m)                0.8      310
Max. surface (km\ :sup:`2`\ ) 0.06     580
Max. volume (hm\ :sup:`3`\ )  0.12     89000
============================= ======== ========

Parameter values can also be defined by the user. It is possible to find the values
of certain parameters for other geographical settings such as Swedish lakes
in the work by Ottosson & Abrahamsson (1998) or for the epilimnion
temperature of southwest Greenland lakes in the work by Kettle *et al.* (2004).

Finally, if field data is available, the parameter values can be calibrated by
the user using this package.

Authors
-------
* Jordi Prats-Rodríguez (jprats@segula.es)
* Pierre-Alain Danis (pierre-alain.danis@afbiodiversite.fr)

References
----------
* Kettle, H.; Thompson, R.; Anderson, N. J.; Livingstone, D. M. (2004)
  Empirical modeling of summer lake surface temperatures in southwest
  Greenland. *Limnology and Oceanography*, 49 (1), 271-282,
  doi: `10.4319/lo.2004.49.1.0271
  <https://doi.org/10.4319/lo.2004.49.1.0271>`_.
* Ottosson, F.; Abrahamsson, O. (1998) Presentation and analysis of a model
  simulating epilimnetic and hypolimnetic temperatures in lakes. *Ecological
  Modelling*, 110, 233-253, doi:
  `10.1016/S0304-3800(98)00067-2
  <https://doi.org/10.1016/S0304-3800(98)00067-2>`_.
* Prats, J.; Danis, P.-A. (2015) Optimisation du réseau national de suivi
  pérenne in situ de la température des plans d'eau: apport de la modélisation
  et des données satellitaires. Final report. Irstea-Onema, Aix-en-Provence.
  93 p. https://www.documentation.eauetbiodiversite.fr/notice/optimisation-du-reseau-national-de-suivi-perenne-in-situ-de-la-temperature-des-plans-d-eau-apport-de0
* Prats, J.; Danis, P.-A. (2019) An epilimnion and hypolimnion temperature
  model based on air temperature and lake characteristics. *Knowledge and
  Management of Aquatic Ecosystems*, 420, 8, doi:
  `10.1051/kmae/2019001 <https://doi.org/10.1051/kmae/2019001>`_.
