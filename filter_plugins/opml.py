#!/usr/bin/env python

import collections

from ansible import errors


def read_opml(path):
    try:
        import listparser
    except Exception:
        raise errors.AnsibleFilterError(
            'the "opml" filter requires the "listparser" python module,'
            + "install with `pip install listparser`"
        )

    try:
        result = listparser.parse(path)
    except Exception as e:
        raise errors.AnsibleFilterError(
            'error while parsing opml file: "%s"' % str(e)
        )

    feeds = result["feeds"]
    for index, feed in enumerate(feeds):
        feeds[index]["folder"] = [
            item for sublist in feed.pop("categories") for item in sublist
        ]
    return feeds


# Taken from https://stackoverflow.com/questions/6027558/
def dict_flatten(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(dict_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class FilterModule(object):
    def filters(self):
        return {"opml": read_opml, "dict_flatten": dict_flatten}
