#!/usr/bin/env python

from ansible import errors


def read_opml(path):
    try:
        import listparser
    except Exception:
        raise errors.AnsibleFilterError('the "opml" filter requires the \
                "listparser" python module, install with `pip install \
                listparser`')

    try:
        result = listparser.parse(path)
    except Exception as e:
        raise errors.AnsibleFilterError('error while parsing opml file: "%s"' %
                                        str(e))

    feeds = result['feeds']
    for index, feed in enumerate(feeds):
        feeds[index]['folder'] = [item for sublist in feed.pop('categories')
                                  for item in sublist]
    return feeds


class FilterModule(object):
    def filters(self):
        return {
            'opml': read_opml
        }
