"""Tests for core calculation functions."""

from datetime import datetime

from aicheck.core import calculate_progress, ordinal_suffix


def test_ordinal_suffix():
    """Test ordinal suffix generation."""
    assert ordinal_suffix(1) == '1st'
    assert ordinal_suffix(2) == '2nd'
    assert ordinal_suffix(3) == '3rd'
    assert ordinal_suffix(4) == '4th'
    assert ordinal_suffix(11) == '11th'
    assert ordinal_suffix(12) == '12th'
    assert ordinal_suffix(13) == '13th'
    assert ordinal_suffix(21) == '21st'
    assert ordinal_suffix(22) == '22nd'
    assert ordinal_suffix(23) == '23rd'
    assert ordinal_suffix(24) == '24th'


def test_calculate_progress_basic():
    """Test basic progress calculation."""
    # Test with a known date: October 12, 2025, renewal day 24th
    test_date = datetime(2025, 10, 12)
    result = calculate_progress(25.0, current_date=test_date, target_day=24)

    assert result['current_percentage'] == 25.0
    assert result['target_day'] == 24
    assert result['current_day'] == 12
    assert result['days_since_renewal'] == 18  # Oct 12 - Sep 24 = 18 days
    assert result['days_in_billing_cycle'] == 30  # Sep 24 to Oct 24


def test_calculate_progress_conserving():
    """Test when conserving credits (using slower than time)."""
    test_date = datetime(2025, 10, 12)
    result = calculate_progress(25.0, current_date=test_date, target_day=24)

    assert result['ratio'] < 1.0
    assert result['status'] == 'conserving well'
    assert result['difference_percentage'] < 0
    assert result['projected_remaining'] > 0


def test_calculate_progress_using_fast():
    """Test when using credits too fast."""
    test_date = datetime(2025, 10, 12)
    result = calculate_progress(75.0, current_date=test_date, target_day=24)

    assert result['ratio'] > 1.0
    assert result['status'] == 'using too fast'
    assert result['difference_percentage'] > 0
    assert result['projected_usage'] > 100


def test_calculate_progress_default_date():
    """Test that it works with default (current) date."""
    result = calculate_progress(50.0, target_day=24)

    assert result is not None
    assert 'status' in result
    assert 'projected_usage' in result
