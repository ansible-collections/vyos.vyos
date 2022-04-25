#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

KEEP_EXISTING_VALUES = "..."


class VyosConf:
    def __init__(self, commands=None):
        self.config = {}
        if type(commands) is list:
            self.run_commands(commands)

    def set_entry(self, path, leaf):
        """
        This function sets a value in the configuration given a path.
        :param path: list of strings to traveser in the config
        :param leaf: value to set at the destination
        :return: dict
        """
        target = self.config
        path = path + [leaf]
        for key in path:
            if key not in target or type(target[key]) is not dict:
                target[key] = {}
            target = target[key]
        return self.config

    def del_entry(self, path, leaf):
        """
        This function deletes a value from the configuration given a path
        and also removes all the parents that are now empty.
        :param path: list of strings to traveser in the config
        :param leaf: value to delete at the destination
        :return: dict
        """
        target = self.config
        firstNoSiblingKey = None
        for key in path:
            if key not in target:
                return self.config
            if len(target[key]) <= 1:
                if firstNoSiblingKey is None:
                    firstNoSiblingKey = [target, key]
            else:
                firstNoSiblingKey = None
            target = target[key]

        if firstNoSiblingKey is None:
            firstNoSiblingKey = [target, leaf]

        target = firstNoSiblingKey[0]
        targetKey = firstNoSiblingKey[1]
        del target[targetKey]
        return self.config

    def check_entry(self, path, leaf):
        """
        This function checks if a value exists in the config.
        :param path: list of strings to traveser in the config
        :param leaf: value to check for existence
        :return: bool
        """
        target = self.config
        path = path + [leaf]
        existing = []
        for key in path:
            if key not in target or type(target[key]) is not dict:
                return False
            existing.append(key)
            target = target[key]
        return True

    def parse_line(self, line):
        """
        This function parses a given command from string.
        :param line: line to parse
        :return: [command, path, leaf]
        """
        line = (
            re.match(r"^('(.*)'|\"(.*)\"|([^#\"']*))*", line).group(0).strip()
        )
        path = re.findall(r"('.*?'|\".*?\"|\S+)", line)
        leaf = path[-1]
        if leaf.startswith('"') and leaf.endswith('"'):
            leaf = leaf[1:-1]
        if leaf.startswith("'") and leaf.endswith("'"):
            leaf = leaf[1:-1]
        return [path[0], path[1:-1], leaf]

    def run_command(self, command):
        """
        This function runs a given command string.
        :param command: command to run
        :return: dict
        """
        [cmd, path, leaf] = self.parse_line(command)
        if cmd.startswith("set"):
            self.set_entry(path, leaf)
        if cmd.startswith("del"):
            self.del_entry(path, leaf)
        return self.config

    def run_commands(self, commands):
        """
        This function runs a a list of command strings.
        :param commands: commands to run
        :return: dict
        """
        for c in commands:
            self.run_command(c)
        return self.config

    def check_command(self, command):
        """
        This function checkes a command for existance in the config.
        :param command: command to check
        :return: bool
        """
        [cmd, path, leaf] = self.parse_line(command)
        if cmd.startswith("set"):
            return self.check_entry(path, leaf)
        if cmd.startswith("del"):
            return not self.check_entry(path, leaf)
        return True

    def check_commands(self, commands):
        """
        This function checkes a list of commands for existance in the config.
        :param commands: list of commands to check
        :return: [bool]
        """
        return [self.check_command(c) for c in commands]

    def quote_key(self, key):
        """
        This function adds quotes to key if quotes are needed for correct parsing.
        :param key: str to wrap in quotes if needed
        :return: str
        """
        if len(key) == 0:
            return ""
        if '"' in key:
            return "'" + key + "'"
        if "'" in key:
            return '"' + key + '"'
        if not re.match(r"^[a-zA-Z0-9./-]*$", key):
            return "'" + key + "'"
        return key

    def build_commands(self, structure=None, nested=False):
        """
        This function builds a list of commands to recreate the current configuration.
        :return: [str]
        """
        if type(structure) is not dict:
            structure = self.config
        if len(structure) == 0:
            return [""] if nested else []
        commands = []
        for (key, value) in structure.items():
            quoted_key = self.quote_key(key)
            for c in self.build_commands(value, True):
                commands.append((quoted_key + " " + c).strip())
        if nested:
            return commands
        return ["set " + c for c in commands]

    def diff_to(self, other, structure):
        if type(other) is not dict:
            other = {}
            if len(structure) == 0:
                return ([], [""])
        if type(structure) is not dict:
            structure = {}
            if len(other) == 0:
                return ([""], [])
        if len(other) == 0 and len(structure) == 0:
            return ([], [])

        toset = []
        todel = []
        for key in structure.keys():
            quoted_key = self.quote_key(key)
            if key in other:
                # keys in both configs, pls compare subkeys
                (subset, subdel) = self.diff_to(other[key], structure[key])
                for s in subset:
                    toset.append(quoted_key + " " + s)
                for d in subdel:
                    todel.append(quoted_key + " " + d)
            else:
                # keys only in this, delete if KEEP_EXISTING_VALUES not set
                if KEEP_EXISTING_VALUES not in other:
                    todel.append(quoted_key)
                continue  # del
        for (key, value) in other.items():
            if key == KEEP_EXISTING_VALUES:
                continue
            quoted_key = self.quote_key(key)
            if key not in structure:
                # keys only in other, pls set all subkeys
                (subset, subdel) = self.diff_to(other[key], None)
                for s in subset:
                    toset.append(quoted_key + " " + s)

        return (toset, todel)

    def diff_commands_to(self, other):
        """
        This function calculates the required commands to change the current into
        the given configuration.
        :param other: VyosConf
        :return: [str]
        """
        (toset, todel) = self.diff_to(other.config, self.config)
        return ["delete " + c.strip() for c in todel] + [
            "set " + c.strip() for c in toset
        ]
