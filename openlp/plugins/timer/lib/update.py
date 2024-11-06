"""
The :mod:`upgrade` module provides the migration path for the OLP Paths database
"""
import json
import logging
import shutil
from pathlib import Path

from sqlalchemy import Column, ForeignKey, MetaData, Table, inspect, select
from sqlalchemy.orm import Session
from sqlalchemy.types import Integer, Unicode

from openlp.core.common import sha256_file_hash
from openlp.core.common.applocation import AppLocation
from openlp.core.common.json import OpenLPJSONEncoder, OpenLPJSONDecoder
from openlp.core.db.types import PathType
from openlp.core.db.upgrades import get_upgrade_op


log = logging.getLogger(__name__)
__version__ = 4

def upgrade_1(session: Session, metadata: MetaData):
    """
    Version 1 upgrade - old db might/might not be versioned.
    """
    log.debug('Skipping upgrade_1 of files DB - not used')