"""
Init file for scrapers module
"""
from . import csv_to_mongo
from . import comtrade_loader
from . import clinicaltrials_loader

__all__ = [
    "csv_to_mongo",
    "comtrade_loader",
    "clinicaltrials_loader"
]