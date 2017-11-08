# -*- coding: utf-8 -*-


class Report(object):
    """ Class who define an report.

        :param: data: audit's data (dict loaded from picklefile).
        :arg: stats: statistics from data.
        :type: data: dict
        :type: stats: dict
        :return: Report Object
        :rtype: object
    """

    def __init__(self, data=None):
        self.data = data
        self.stats, self.pourcent, self.total, self.rule_output = self.generate_infos

    @property
    def generate_infos(self):
        """ Generate audit informations from data

        :return: informations from audit data.
        :rtype: dict
        """
        stats = {'fail': {}, 'success': {}, 'timeout': {}, 'error': {}}
        pourcent = {'fail': 0, 'success': 0, 'timeout': 0, 'error': 0}
        total = {'fail': 0, 'success': 0, 'timeout': 0, 'error': 0}
        rule_output = {}

        alltotal = 0
        for rtype, value in self.data.iteritems():
            rule_output[rtype] = {}
            stats['success'][rtype] = 0
            stats['fail'][rtype] = 0
            stats['timeout'][rtype] = 0
            stats['error'][rtype] = 0
            for rule_id, rule_ret in value.iteritems():
                rule_output[rtype][rule_id] = {}
                if rule_ret.get('out'):
                    rule_output[rtype][rule_id]['out'] = rule_ret.get('out')
                else:
                    rule_output[rtype][rule_id]['out'] = ''
                if rule_ret.get('err'):
                    rule_output[rtype][rule_id]['err'] = rule_ret.get('err')
                else:
                    rule_output[rtype][rule_id]['err'] = ''

                rule_output[rtype][rule_id]['ret_status'] = "success"
                rule_output[rtype][rule_id]['ret_code'] = []
                code = 0
                for retcode in rule_ret.get('return_code'):
                    if retcode != 0:
                        code = retcode
                        if retcode == 255:
                            rule_output[rtype][rule_id]['ret_status'] = "error"
                        elif retcode == 254:
                            rule_output[rtype][rule_id]['ret_status'] = "timeout"
                        else:
                            rule_output[rtype][rule_id]['ret_status'] = "fail"
                        rule_output[rtype][rule_id]['ret_code'].append(retcode)
                    else:
                        rule_output[rtype][rule_id]['ret_code'].append(0)
                if code == 0:
                    stats['success'][rtype] += 1
                    total['success'] += 1
                elif code == 255:
                    stats['error'][rtype] += 1
                    total['error'] += 1
                elif code == 254:
                    stats['timeout'][rtype] += 1
                    total['timeout'] += 1
                else:
                    stats['fail'][rtype] += 1
                    total['fail'] += 1
            alltotal += stats['success'][rtype] + stats['fail'][rtype] + stats['error'][rtype] + stats['timeout'][rtype]
        for rtype in stats.keys():
            if total:
                pourcent[rtype] = (float(total[rtype]) / float(alltotal) * 100)
        return stats, pourcent, total, rule_output
