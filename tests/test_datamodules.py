from pathlib import Path

import autorootcwd
import pytest
import torch
from omegaconf import OmegaConf

from src.data.chess_datamodule import ChessDataModule

cfg = OmegaConf.load("configs/experiment/md1.yaml")


def test_chess_datamodule() -> None:
    """Tests `ChessDataModule` to verify that it can be downloaded correctly, that the necessary
    attributes were created (e.g., the dataloader objects), and that dtypes and batch sizes
    correctly match.

    :param batch_size: Batch size of the data to be loaded by the dataloader.
    """
    gen_data = True  # Force to generate data
    cfg.data.dataset.train.case_nums = 10
    cfg.data.dataset.validation.case_nums = 5
    cfg.data.dataset.test.case_nums = 5

    num_workers = cfg.data.num_workers
    pin_memory = cfg.data.pin_memory
    dataset = cfg.data.dataset
    batch_size = cfg.data.batch_size

    dm = ChessDataModule(
        dataset=dataset,
        gen_data=gen_data,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    dm.prepare_data()

    assert not dm.data_train and not dm.data_val and not dm.data_test

    dm.setup()
    assert dm.data_train and dm.data_val and dm.data_test
    assert dm.train_dataloader() and dm.val_dataloader() and dm.test_dataloader()

    batch = next(iter(dm.train_dataloader()))
    x, y = batch
    assert len(x) == batch_size
    assert len(y) == batch_size
    assert x.dtype == torch.float32
    assert y.dtype == torch.float32
