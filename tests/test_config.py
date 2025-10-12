"""
Tests for configuration management.
"""

import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from aiusage import config as config_module


@pytest.fixture(autouse=True)
def backup_and_restore_config():
    """
    Backup and restore the user's actual config file before and after tests.
    This ensures tests never permanently modify the user's real config.
    """
    config_file = config_module.get_config_file()
    backup_file = None

    # Backup existing config if it exists
    if config_file.exists():
        backup_file = config_file.with_suffix('.json.backup')
        shutil.copy2(config_file, backup_file)

    yield

    # Restore the backup after tests
    if backup_file and backup_file.exists():
        shutil.move(backup_file, config_file)
    elif config_file.exists() and not backup_file:
        # Config was created by tests but didn't exist before - remove it
        config_file.unlink()


def test_get_config_file():
    """Test that get_config_file returns a valid path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch('aiusage.config.user_config_dir', return_value=tmpdir):
            config_file = config_module.get_config_file()
            assert isinstance(config_file, Path)
            assert config_file.name == 'config.json'
            # Config directory should be created
            assert config_file.parent.exists()


def test_save_and_load_renewal_day():
    """Test saving and loading renewal day."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'config.json'

        with patch('aiusage.config.get_config_file', return_value=config_file):
            # Save a renewal day
            config_module.save_renewal_day(15)

            # Load it back
            loaded = config_module.load_renewal_day()
            assert loaded == 15

            # Verify the file contents
            with config_file.open('r') as f:
                config = json.load(f)
            assert config['renewal_day'] == 15


def test_load_renewal_day_no_file():
    """Test loading renewal day when no config file exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'nonexistent.json'

        with patch('aiusage.config.get_config_file', return_value=config_file):
            loaded = config_module.load_renewal_day()
            assert loaded is None


def test_load_renewal_day_invalid_json():
    """Test loading renewal day with invalid JSON in config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'config.json'
        config_file.write_text('invalid json{')

        with patch('aiusage.config.get_config_file', return_value=config_file):
            loaded = config_module.load_renewal_day()
            assert loaded is None


def test_save_renewal_day_preserves_other_config():
    """Test that saving renewal day preserves other config values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'config.json'

        with patch('aiusage.config.get_config_file', return_value=config_file):
            # Create a config with some other value
            config_file.write_text(json.dumps({'other_key': 'other_value'}))

            # Save renewal day
            config_module.save_renewal_day(20)

            # Load and verify both values exist
            with config_file.open('r') as f:
                config = json.load(f)

            assert config['renewal_day'] == 20
            assert config['other_key'] == 'other_value'


def test_save_renewal_day_updates_existing():
    """Test that saving renewal day updates an existing value."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'config.json'

        with patch('aiusage.config.get_config_file', return_value=config_file):
            # Save initial value
            config_module.save_renewal_day(10)
            assert config_module.load_renewal_day() == 10

            # Update it
            config_module.save_renewal_day(25)
            assert config_module.load_renewal_day() == 25
