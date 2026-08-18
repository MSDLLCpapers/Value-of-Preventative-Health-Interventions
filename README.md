# Value-of-Preventative-Health-Interventions

This repository contains supplementary materials for the article "Does preventive health spending represent good value-for-money?" by Monica H. Carney, Joseph S. Knee, Julian C. Palladino, and David E. Bloom.



The repository's contents include the following files, which reproduce the analytical results presented in the manuscript:

* EU\_data\_visualizations.R
* European Spending Analysis and Exploration.py
* Masia Replication and Modification.py



The repository's contens also include the following sub-folders:

* **Data** - a folder containing all the raw data used in the analysis (necessary to run the above files).
* **Output** - a folder containing the analytical output that appears in the article.



## Usage
The Python code is tested to work on Python3.12.
First create a virtual environment with dependencies for the Python scripts:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

The `European Spending Analysis and Exploration.py` is meant to be run from repository root:

    python3 'European Spending Analysis and Exploration.py'

`Masia Replication and Modification.py` can be executed from the Data directory:

    cd Data
    python3 '../Masia Replication and Modification.py'



## Licensing

The analysis code and output produced by the authors — the three script files
listed above and the contents of `Output/` — are released under the Creative
Commons CC0 1.0 Universal public domain dedication ([LICENSE](LICENSE)).

The contents of `Data/` are **third-party datasets** redistributed here so that
the analysis can be reproduced. They were not created by the authors and are
**not** covered by the CC0 dedication. Each remains subject to the terms of its
original publisher, and some require attribution — the World Bank extracts, for
example, are licensed CC BY-4.0. Sources, licenses, and requested citations for
every dataset are documented in [ATTRIBUTIONS.md](ATTRIBUTIONS.md). Please
consult that file before reusing anything in `Data/`.

Reproducing the analysis requires third-party Python packages and R packages that
are **not** distributed with this repository and must be installed separately;
they are listed with their licenses in
[LICENSES_THIRD_PARTY](LICENSES_THIRD_PARTY).



For questions about this repository, please contact corresponding author Monica H. Carney: mcarney@datafordecisions.net.



This study was sponsored by Merck Sharp \& Dohme LLC, a subsidiary of Merck \& Co., Inc., Rahway, NJ, USA.

