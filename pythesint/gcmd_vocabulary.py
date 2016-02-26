from __future__ import absolute_import

from collections import OrderedDict

from pythesint.json_vocabulary import JSONVocabulary, openURL


class GCMDVocabulary(JSONVocabulary):
    def _fetch_online_data(self):
        ''' Return list of GCMD standard keywords
            self.url and self.categories must be set
        '''
        response = openURL(self.url)
        gcmd_list = []
        _read_revision(response.readline(), gcmd_list)
        _check_categories(response.readline(), self.categories)
        for line in response.readlines():
            _read_line(line, gcmd_list, self.categories)

        return gcmd_list


def _read_revision(line, gcmd_list):
    # TODO: Cast exception if not found?
    if 'Keyword Version' and 'Revision' in line:
        meta = line.split('","')
        gcmd_list.append({'Revision': meta[1][10:]})


def _check_categories(line, categories):
    kw_groups = line.split(',')
    kw_groups.pop(-1)
    # Make sure the group items are as expected
    if kw_groups != categories:
        raise TypeError('%s is not equal to %s' % (kw_groups, categories))


def _read_line(line, gcmd_list, categories):
    gcmd_keywords = line.split('","')
    gcmd_keywords[0] = gcmd_keywords[0].strip('"')
    if gcmd_keywords[0] == 'NOT APPLICABLE':
        return
    # Remove last item (the ID is not needed)
    gcmd_keywords.pop(-1)
    if len(gcmd_keywords) != len(categories):
        return
    line_kw = OrderedDict()
    for i, key in enumerate(categories):
        line_kw[key] = gcmd_keywords[i]
    gcmd_list.append(line_kw)
