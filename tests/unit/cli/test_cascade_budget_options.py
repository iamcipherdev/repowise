"""Parsing for --cascade-budget and the update.cascade_budget config key."""

from __future__ import annotations

import click
import pytest

from repowise.cli.commands.update_cmd.command import (
    _config_cascade_budget,
    _parse_cascade_budget_option,
)


def test_flag_parses_int_all_and_none() -> None:
    assert _parse_cascade_budget_option(None, None, None) is None
    assert _parse_cascade_budget_option(None, None, "50") == 50
    assert _parse_cascade_budget_option(None, None, "all") == "all"
    assert _parse_cascade_budget_option(None, None, "ALL") == "all"


def test_flag_rejects_junk_and_negatives() -> None:
    for bad in ("banana", "-1"):
        with pytest.raises(click.BadParameter):
            _parse_cascade_budget_option(None, None, bad)


def test_config_key_reads_nested_update_block() -> None:
    assert _config_cascade_budget({"update": {"cascade_budget": "all"}}) == "all"
    assert _config_cascade_budget({"update": {"cascade_budget": 100}}) == 100
    assert _config_cascade_budget({}) is None
    assert _config_cascade_budget({"update": None}) is None
    assert _config_cascade_budget({"update": {"other": 1}}) is None
