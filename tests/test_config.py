"""
Tests for configuration management.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from aicheck import config as config_module


def test_get_config_file():
    """Test that get_config_file returns a valid path."""
    config_file = config_module.get_config_file()
    assert isinstance(config_file, Path)
    assert config_file.name == 'config.json'
    # Config directory should be created
    assert config_file.parent.exists()


def test_save_and_load_renewal_day():
    """Test saving and loading renewal day."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'config.json'

        with patch('aicheck.config.get_config_file', return_value=config_file):
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

        with patch('aicheck.config.get_config_file', return_value=config_file):
            loaded = config_module.load_renewal_day()
            assert loaded is None


def test_load_renewal_day_invalid_json():
    """Test loading renewal day with invalid JSON in config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'config.json'
        config_file.write_text('invalid json{')

        with patch('aicheck.config.get_config_file', return_value=config_file):
            loaded = config_module.load_renewal_day()
            assert loaded is None


def test_save_renewal_day_preserves_other_config():
    """Test that saving renewal day preserves other config values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'config.json'

        with patch('aicheck.config.get_config_file', return_value=config_file):
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

        with patch('aicheck.config.get_config_file', return_value=config_file):
            # Save initial value
            config_module.save_renewal_day(10)
            assert config_module.load_renewal_day() == 10

            # Update it
            config_module.save_renewal_day(25)
            assert config_module.load_renewal_day() == 25
