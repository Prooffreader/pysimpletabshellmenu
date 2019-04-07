#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylama:ignore=W293,W291,W391,E302,E128,E127,E303,E501,W292 (will be fixed by black)

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

from copy import deepcopy

import pytest

import tabbedshellmenus.normalizer as normalizer

def freeze_config(normalized_config):
    lst = [':OUTER_LEVEL:']
    c = normalized_config
    for k in ['case_sensitive', 'screen_width']:
        lst.append(c[k])
    lst.append(':TAB:')
    for tab in c['tabs']:
        for k1 in ['header_choice_displayed_and_accepted', 'header_description', 'long_description']:
            lst.append(tab.get(k1, 'n/a'))
        for item in tab['items']:
            lst.append(':ITEM:')
            for k2 in ['choice_displayed', 'choice_description', 'returns']:
                lst.append(item[k2])
            lst.append(':ENTRIES:')
            for entry in item['valid_entries']:
                lst.append(entry)
    return lst


@pytest.mark.function
@pytest.mark.run(order=1)
def test__add_tabs_key_if_needed_multiple_nochange(input_config_multiple_only):
    """This function should not change a multiple or single_with_key schema type"""
    c = deepcopy(input_config_multiple_only)
    cprime = normalizer._add_tabs_key_if_needed(deepcopy(c))
    assert c == cprime

@pytest.mark.function
@pytest.mark.run(order=1)
def test__add_tabs_key_if_needed_single_with_key_nochange(input_config_single_with_key_only):
    """This function should not change a multiple or single_with_key schema type"""
    c = deepcopy(input_config_single_with_key_only)
    cprime = normalizer._add_tabs_key_if_needed(deepcopy(c))
    assert c == cprime

@pytest.mark.regression
@pytest.mark.run(order=1)
def test_regress__add_tabs_single_wo_key(data_regression, input_config_single_without_key_only):
    """Should switch items to tabs"""
    c = deepcopy(input_config_single_without_key_only)
    c = normalizer._add_tabs_key_if_needed(c)
    assert 'tabs' in c.keys()
    assert 'items' not in c.keys()
    c = freeze_config(c)
    data = {'data': c}
    data_regression.check(data)

@pytest.mark.regression
@pytest.mark.run(order=1)
def test_regress_normalize_all(data_regression, input_config_dict):
    """The function _walk_stringize_and_case() is not tested because the only other 'private' function
    is necessary for it to work, and the function normalize just wraps these two functions anyway"""
    c = deepcopy(input_config_dict)
    c = normalizer.normalize(c)
    c = freeze_config(c)
    data = {'data': c}
    data_regression.check(data)

