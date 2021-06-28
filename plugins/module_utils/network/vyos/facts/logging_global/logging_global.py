# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The vyos logging_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.rm_templates.logging_global import (
    Logging_globalTemplate,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.argspec.logging_global.logging_global import (
    Logging_globalArgs,
)


class Logging_globalFacts(object):
    """ The vyos logging_global facts class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Logging_globalArgs.argument_spec

    def get_logging_data(self, connection):
        return connection.get("show configuration commands | grep syslog")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Logging_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []
        data = "set system syslog console facility all\nset system syslog console facility local7 level 'err'\nset system syslog console facility news level 'debug'\nset system syslog file abc archive size '125'\nset system syslog file def archive file '2'\nset system syslog file def facility local7 level 'emerg'\nset system syslog global archive file '3'\nset system syslog global archive size '111'\nset system syslog global facility local7 level 'debug'\nset system syslog global marker interval '111'\nset system syslog global preserve-fqdn\nset system syslog host 10.0.2.12 facility all protocol 'udp'\nset system syslog host 10.0.2.15 facility all level 'all'\nset system syslog host 10.0.2.15 facility all protocol 'udp'\nset system syslog host 10.0.2.15 port '223'\nset system syslog user paul facility local7 level 'err'\nset system syslog user vyos facility local6 level 'alert'\nset system syslog user vyos facility local7 level 'debug'"
        if not data:
            data = self.get_logging_data(connection)

        # parse native config using the Logging_global template
        logging_global_parser = Logging_globalTemplate(
            lines=data.splitlines(), module=self._module
        )
        objs = list(logging_global_parser.parse().values())

        ansible_facts["ansible_network_resources"].pop("logging_global", None)

        params = utils.remove_empties(
            logging_global_parser.validate_config(
                self.argument_spec, {"config": objs[0]}, redact=True
            )
        )

        facts["logging_global"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts