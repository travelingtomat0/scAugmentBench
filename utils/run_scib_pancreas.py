import random
import scanpy as sc
import pandas as pd
import numpy as np

import anndata as ad

from scib_metrics.benchmark import Benchmarker
from scib_metrics.benchmark import Benchmarker, BioConservation, BatchCorrection


_BIO_METRICS = BioConservation(isolated_labels=True, 
                            nmi_ari_cluster_labels_leiden=True, 
                            nmi_ari_cluster_labels_kmeans=False, 
                            silhouette_label=True, 
                            clisi_knn=True
                            )
_BATCH_METRICS = BatchCorrection(graph_connectivity=True, 
                                kbet_per_label=True, 
                                ilisi_knn=True, 
                                pcr_comparison=True, 
                                silhouette_batch=True
                                )

def evaluate_model(adata, batch_key, cell_type_label, names_obs):
    bm = Benchmarker(
                adata,
                batch_key=batch_key,
                label_key=cell_type_label,
                embedding_obsm_keys=names_obs,
                bio_conservation_metrics=_BIO_METRICS,
                batch_correction_metrics=_BATCH_METRICS,
                n_jobs=4,
            )
    bm.benchmark()
    a = bm.get_results(False, True)
    results = a.round(decimals=4)
    return results


names_obs = ['X_new']

# RNA_data = sc.read_h5ad('/home/baunsgaard/scBench/scButterfly/Olga_Data/Pancreas.h5ad')
# RNA_data.obsm["X_new"] = sc.read_h5ad('/home/baunsgaard/scBench/scAugmentBench/philip_emb/embedding-Pancreas.h5ad').X


# batch_key = "batchlb"
# ct = "CellType"

# print(RNA_data)

# results = evaluate_model(adata=RNA_data, batch_key=batch_key, cell_type_label=ct, names_obs=names_obs)
# results.to_csv(f'metrics_pancreas.csv')

# RNA_data = sc.read_h5ad('/home/baunsgaard/scBench/scButterfly/Olga_Data/PBMC.h5ad')
# RNA_data.obsm["X_new"] = sc.read_h5ad('/home/baunsgaard/scBench/scAugmentBench/philip_emb/embedding-PBMC.h5ad').X


# batch_key = "batchlb"
# ct = "CellType"

# print(RNA_data)

# results = evaluate_model(adata=RNA_data, batch_key=batch_key, cell_type_label=ct, names_obs=names_obs)
# results.to_csv(f'geneformer_metrics_pbmc.csv')

RNA_data = sc.read_h5ad('/home/baunsgaard/scBench/scButterfly/Olga_Data/ImmuneAtlas.h5ad')
RNA_data.obsm["X_new"] = sc.read_h5ad('/home/baunsgaard/scBench/scAugmentBench/philip_emb/embedding-ImmuneAtlas.h5ad').X


batch_key = "batchlb"
ct = "CellType"

print(RNA_data)

results = evaluate_model(adata=RNA_data, batch_key=batch_key, cell_type_label=ct, names_obs=names_obs)
results.to_csv(f'geneformer_metrics_immune_atlas.csv')
