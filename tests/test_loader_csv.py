# SPDX-FileCopyrightText: ASSUME Developers
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime

import pandas as pd
import pytest

from assume.scenario.loader_csv import (
    load_config_and_create_forecaster,
    make_market_config,
)


def test_csv_loader_validation():
    with pytest.raises(
        ValueError,
        match="min_power and max_power must both be either negative or positive",
    ):
        load_config_and_create_forecaster(
            inputs_path="tests/fixtures", scenario="invalid_units", study_case="base"
        )
    with pytest.raises(
        ValueError, match="No power plant or no demand units were provided!"
    ):
        load_config_and_create_forecaster(
            inputs_path="tests/fixtures", scenario="missing_units", study_case="base"
        )


def test_make_market_config_invalid_datatypes():
    """
    Test that make_market_config raises appropriate errors when
    passed incorrect datatypes in market_params.
    """
    world_start = datetime(2025, 1, 1)
    world_end = datetime(2025, 1, 10)
    market_id = "test_market"

    # 1. Test invalid 'products' type (Expected: list of dicts, Given: int)
    invalid_params_products = {
        "opening_frequency": "h",
        "opening_duration": pd.Timedelta(hours=1),
        "market_mechanism": "auction",
        "products": 12345,  # Should be a list
    }
    with pytest.raises(TypeError):
        make_market_config(market_id, invalid_params_products, world_start, world_end)

    # 2. Test invalid 'opening_duration' (Expected: duration string/Timedelta, Given: list)
    invalid_params_duration = {
        "opening_frequency": "h",
        "opening_duration": pd.Timedelta(hours=1),  # Invalid for pd.Timedelta
        "market_mechanism": "auction",
        "products": [],
    }
    with pytest.raises((TypeError, ValueError)):
        make_market_config(market_id, invalid_params_duration, world_start, world_end)

    # 3. Test invalid 'start_date' format (Expected: date string, Given: unexpected object)
    invalid_params_date = {
        "opening_frequency": "h",
        "opening_duration": "1h",
        "market_mechanism": "auction",
        "products": [],
        "start_date": {"year": 2025},  # pd.Timestamp will fail here
    }
    with pytest.raises((TypeError, ValueError)):
        make_market_config(market_id, invalid_params_date, world_start, world_end)
