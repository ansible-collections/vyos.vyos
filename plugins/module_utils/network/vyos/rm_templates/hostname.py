# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Hostname parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class HostnameTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        prefix = {"set": "set", "remove": "delete"}
        super(HostnameTemplate, self).__init__(
            lines=lines,
            tmplt=self,
            prefix=prefix,
            module=module,
        )

    # fmt: off
    PARSERS = [
        # service snmp community <>
        {
            "name": "hostname",
            "getval": re.compile(
                r"""
                ^set\ssystem\shost-name
                \s+(?P<name>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "system host-name {{ hostname }}",
            "result": {
                "hostname": "{{ name }}",
            },
        },
    ]
    # fmt: on
