#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# pylint: skip-file

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################
"""
The arg spec for the vyos_firewall_global module
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class Firewall_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the vyos_firewall_global module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "options": {
                "config_trap": {"type": "bool"},
                "group": {
                    "options": {
                        "address_group": {
                            "elements": "dict",
                            "options": {
                                "description": {"type": "str"},
                                "members": {
                                    "elements": "dict",
                                    "options": {"address": {"type": "str"}},
                                    "type": "list",
                                },
                                "name": {"required": True, "type": "str"},
                            },
                            "type": "list",
                        },
                        "network_group": {
                            "elements": "dict",
                            "options": {
                                "description": {"type": "str"},
                                "members": {
                                    "elements": "dict",
                                    "options": {"address": {"type": "str"}},
                                    "type": "list",
                                },
                                "name": {"required": True, "type": "str"},
                            },
                            "type": "list",
                        },
                        "port_group": {
                            "elements": "dict",
                            "options": {
                                "description": {"type": "str"},
                                "members": {
                                    "elements": "dict",
                                    "options": {"port": {"type": "str"}},
                                    "type": "list",
                                },
                                "name": {"required": True, "type": "str"},
                            },
                            "type": "list",
                        },
                    },
                    "type": "dict",
                },
                "log_martians": {"type": "bool"},
                "ping": {
                    "options": {
                        "all": {"type": "bool"},
                        "broadcast": {"type": "bool"},
                    },
                    "type": "dict",
                },
                "route_redirects": {
                    "elements": "dict",
                    "options": {
                        "afi": {
                            "choices": ["ipv4", "ipv6"],
                            "required": True,
                            "type": "str",
                        },
                        "icmp_redirects": {
                            "options": {
                                "receive": {"type": "bool"},
                                "send": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "ip_src_route": {"type": "bool"},
                    },
                    "type": "list",
                },
                "state_policy": {
                    "elements": "dict",
                    "options": {
                        "action": {
                            "choices": ["accept", "drop", "reject"],
                            "type": "str",
                        },
                        "connection_type": {
                            "choices": ["established", "invalid", "related"],
                            "type": "str",
                        },
                        "log": {"type": "bool"},
                    },
                    "type": "list",
                },
                "syn_cookies": {"type": "bool"},
                "twa_hazards_protection": {"type": "bool"},
                "validation": {
                    "choices": ["strict", "loose", "disable"],
                    "type": "str",
                },
            },
            "type": "dict",
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "deleted",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
