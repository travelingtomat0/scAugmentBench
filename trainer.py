import logging

import numpy as np
import scanpy as sc
import wandb
import time

import torch
import lightning as pl
import hydra

from models.byol import BYOLModule
from models.barlowtwins import BarlowTwins
from models.moco import MoCo
from models.vicreg import VICReg
from models.simclr import SimCLR
from models.simsiam import SimSiam
from models.nnclr import NNCLR
from models.concerto import Concerto
#from models.dino import *
from evaluator import infer_embedding
from anndata.experimental.pytorch import AnnLoader
from data.dataset import OurDataset

from sklearn.metrics import f1_score, accuracy_score
from sklearn.neighbors import KNeighborsClassifier


_model_dict = {"BYOL": BYOLModule, "BarlowTwins": BarlowTwins, "MoCo": MoCo, "VICReg": VICReg, "SimCLR": SimCLR, "SimSiam": SimSiam, "NNCLR": NNCLR, "Concerto": Concerto}

def train_model(dataset, model_config, random_seed, batch_size, 
                num_workers, n_epochs, logger, cfg=None):
    model_name = model_config["model"]

    train_loader = torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            num_workers=num_workers,
            shuffle=True,
            drop_last=True)
    
    logger.info(f".. Dataloader ready. Now build {model_name}")

    model = _model_dict[str(model_name)](**model_config)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    trainer = pl.Trainer(max_epochs=n_epochs, accelerator=device) # cpu works for smaller tasks!!
    logger.info(f".. Model ready. Now train on {device}.")
    
    try:
        trainer.fit(
            model,
            train_loader,
        )
        logger.info(f".. Training done.")
    except Exception as error:
        # handle the exception
        logger.info(".. An exception occurred while training:", error)
    
    return model

def inference(model, val_loader):
    outs = []
    for x in val_loader:
        with torch.no_grad():
            outs.append(model.predict(x.layers['counts']))
    
    embedding = torch.concat(outs)
    embedding = np.array(embedding)
    return embedding

def train_clf(encoder, train_adata, val_adata, batch_size=256, num_workers=12, ctype_key='CellType'):
    train_loader = torch.utils.data.DataLoader(
        dataset=OurDataset(adata=train_adata, transforms=None, valid_ids=None),
        batch_size=batch_size, 
        num_workers=num_workers,
        shuffle=False, 
        drop_last=False
    )
    val_loader = torch.utils.data.DataLoader(
        dataset=OurDataset(adata=val_adata, transforms=None, valid_ids=None),
        batch_size=batch_size, 
        num_workers=num_workers,
        shuffle=False, 
        drop_last=False
    )

    start = time.time()
    train_X, val_X = infer_embedding(encoder, train_loader), infer_embedding(encoder, val_loader)
    train_y = train_adata.obs[ctype_key]
    val_y = val_adata.obs[ctype_key]
    
    clf = KNeighborsClassifier(n_neighbors=11)
    clf = clf.fit(train_X, train_y)
    run_time = time.time() - start
    
    y_pred = clf.predict(val_X)
    
    maavg_f1 = f1_score(val_y, y_pred, average='macro')
    accuracy = accuracy_score(val_y, y_pred)
    return clf, maavg_f1, accuracy, run_time