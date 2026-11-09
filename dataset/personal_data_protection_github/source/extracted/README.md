# Replication kit

This repository accompanies the paper "The whos, whats, and whys of issues related to personal data and data protection in open source projects on GitHub" currently under review. The repository contains the data and the code to reproduce the results from the paper.

# Content

The repository contains the following files:
- The `data` directory contains the data used in the paper.
- The `analysis.ipynb` Jupyter notebook contains the code to for the analysis and the plots from the paper.

# Reproducing the results

To reproduce the results from the paper, you can use the `analysis.ipynb` Jupyter notebook. The notebook contains the code to load the data, compute the results, and generate the plots from the paper. You can run the notebook in your local environment or use a cloud-based Jupyter notebook service such as [Google Colab](https://colab.research.google.com/). For local execution with Ubuntu 22.04, you can use the following commands to install the required packages:

```bash
git clone git@github.com:aieng-lab/replication-kit-gh-privacy-issues.git
cd replication-kit-gh-privacy-issues
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You can then start Jupyter notebook with the following command:

```bash
jupyter-lab
```
