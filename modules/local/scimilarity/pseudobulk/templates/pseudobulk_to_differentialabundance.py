#!/usr/bin/env python3

import os
import platform

os.environ["NUMBA_CACHE_DIR"] = "./tmp/numba"
os.environ["MPLCONFIGDIR"] = "./tmp/mpl"

import anndata as ad
import pandas as pd
import scipy.sparse as sp
import yaml

adata = ad.read_h5ad("${h5ad}")

counts_layer = "${counts_layer}"

mat = adata.X if counts_layer == "X" else adata.layers[counts_layer]
if sp.issparse(mat):
    mat = mat.toarray()

sample_ids = adata.obs.index.astype(str)

counts_df = pd.DataFrame(
    mat.T,
    index=adata.var_names.astype(str),
    columns=sample_ids
)
counts_df.index.name = "feature"

metadata_df = adata.obs.copy()
metadata_df.insert(0, "sample_id", sample_ids.values)
metadata_df.index = sample_ids
metadata_df.index.name = "sample_id"

counts_df.to_csv("${prefix}.counts_matrix.tsv", sep="\t")
metadata_df.to_csv("${prefix}.sample_metadata.tsv", sep="\t")

versions = {
    "${task.process}": {
        "python": platform.python_version(),
        "anndata": ad.__version__,
        "pandas": pd.__version__,
    }
}

with open("versions.yml", "w") as f:
    yaml.dump(versions, f)