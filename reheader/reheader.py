# -*- coding: utf-8 -*-

import logging
from fuzzywuzzy import fuzz

MINIMUM_SCORE = 60
OPTIONAL_PREFIX = '?:'


def _normalize_whitespace(s):
    return ' '.join(s.strip().split())


def ratio(s1, s2):
    return fuzz.ratio(_normalize_whitespace(s1), _normalize_whitespace(s2))


def best_match(actual, expected, minimum_score):
    if expected:
        best = sorted(expected, key=lambda s: ratio(actual, s))[-1]
        score = ratio(actual, best)
        logging.debug('Max score for {} in {} is {}: {}'.format(
            actual, expected, best, score))
        if score >= minimum_score:
            return best
        else:
            logging.debug('Score < {}, not a match'.format(minimum_score))


def _row_requirements(headers, optional_prefix):
    result = {h.strip(): {'required': True,
        'regex': None}
              for h in headers if not h.strip().startswith(optional_prefix)}
    prefix_len = len(optional_prefix)
    result.update({h.strip()[prefix_len:]: {'required': False}
                   for h in headers if h.strip().startswith(optional_prefix)})
    return result


def reheadered(data,
               headers,
               keep_extra=False,
               minimum_score=MINIMUM_SCORE,
               optional_prefix=OPTIONAL_PREFIX):
    headers = [_normalize_whitespace(h) for h in headers]
    headers_in_data = None
    for (row_num, row) in enumerate(data):
        if not hasattr(row, 'keys'):
            if headers_in_data is None:
                # this was the header line
                headers_in_data = row
                continue
            else:
                row = {r[0]: r[1] for r in zip(headers_in_data, row)}
        result = {}
        row_requirements = _row_requirements(headers, optional_prefix)
        for col in row:  # now col is either the header value
            match = best_match(col, row_requirements, minimum_score)
            if match is not None:
                row_requirements.pop(match)
                result[match] = row[col]
            else:
                if keep_extra:
                    result[col] = row[col]
        unmet = [h for h in row_requirements if row_requirements[h]['required']]
        if unmet:
            err_msg = '{} not found in row #{}: {}'.format(unmet, row_num, row)
            raise KeyError(err_msg)
        yield result
