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

import unittest
from ansible_collections.vyos.vyos.plugins.cliconf_utils.vyosconf import (
    VyosConf,
)


class TestListElements(unittest.TestCase):
    def test_add(self):
        conf = VyosConf()
        conf.set_entry(["a", "b"], "c")
        self.assertEqual(conf.config, {"a": {"b": {"c": {}}}})
        conf.set_entry(["a", "b"], "d")
        self.assertEqual(conf.config, {"a": {"b": {"c": {}, "d": {}}}})
        conf.set_entry(["a", "c"], "b")
        self.assertEqual(
            conf.config, {"a": {"b": {"c": {}, "d": {}}, "c": {"b": {}}}}
        )
        conf.set_entry(["a", "c", "b"], "d")
        self.assertEqual(
            conf.config,
            {"a": {"b": {"c": {}, "d": {}}, "c": {"b": {"d": {}}}}},
        )

    def test_del(self):
        conf = VyosConf()
        conf.set_entry(["a", "b"], "c")
        conf.set_entry(["a", "c", "b"], "d")
        conf.set_entry(["a", "b"], "d")
        self.assertEqual(
            conf.config,
            {"a": {"b": {"c": {}, "d": {}}, "c": {"b": {"d": {}}}}},
        )
        conf.del_entry(["a", "c", "b"], "d")
        self.assertEqual(conf.config, {"a": {"b": {"c": {}, "d": {}}}})
        conf.set_entry(["a", "b", "c"], "d")
        conf.del_entry(["a", "b", "c"], "d")
        self.assertEqual(conf.config, {"a": {"b": {"d": {}}}})

    def test_parse(self):
        conf = VyosConf()
        self.assertListEqual(
            conf.parse_line("set a b c"), ["set", ["a", "b"], "c"]
        )
        self.assertListEqual(
            conf.parse_line('set a b "c"'), ["set", ["a", "b"], "c"]
        )
        self.assertListEqual(
            conf.parse_line("set a b 'c d'"), ["set", ["a", "b"], "c d"]
        )
        self.assertListEqual(
            conf.parse_line("set a b 'c'"), ["set", ["a", "b"], "c"]
        )
        self.assertListEqual(
            conf.parse_line("delete a b 'c'"), ["delete", ["a", "b"], "c"]
        )
        self.assertListEqual(
            conf.parse_line("del a b 'c'"), ["del", ["a", "b"], "c"]
        )
        self.assertListEqual(
            conf.parse_line("set a b '\"c'"), ["set", ["a", "b"], '"c']
        )
        self.assertListEqual(
            conf.parse_line("set a b 'c' #this is a comment"),
            ["set", ["a", "b"], "c"],
        )
        self.assertListEqual(
            conf.parse_line("set a b '#c'"), ["set", ["a", "b"], "#c"]
        )

    def test_run_commands(self):
        self.assertEqual(
            VyosConf(["set a b 'c'", "set a c 'b'"]).config,
            {"a": {"b": {"c": {}}, "c": {"b": {}}}},
        )
        self.assertEqual(
            VyosConf(["set a b c 'd'", "set a c 'b'", "del a b c d"]).config,
            {"a": {"c": {"b": {}}}},
        )

    def test_build_commands(self):
        self.assertEqual(
            sorted(
                VyosConf(
                    [
                        "set a b 'c a'",
                        "set a c a",
                        "set a c b",
                        "delete a c a",
                    ]
                ).build_commands()
            ),
            sorted(["set a b 'c a'", "set a c b"]),
        )
        self.assertEqual(
            sorted(
                VyosConf(
                    [
                        "set a b 10.0.0.1/24",
                        "set a c ABCabc123+/=",
                        "set a d $6$ABC.abc.123.+./=..",
                    ]
                ).build_commands()
            ),
            sorted(
                [
                    "set a b 10.0.0.1/24",
                    "set a c 'ABCabc123+/='",
                    "set a d '$6$ABC.abc.123.+./=..'",
                ]
            ),
        )

    def test_check_commands(self):
        conf = VyosConf(["set a b 'c a'", "set a c b"])
        self.assertListEqual(
            conf.check_commands(
                ["set a b 'c a'", "del a c b", "set a b 'c'", "del a a a"]
            ),
            [True, False, False, True],
        )

    def test_diff_commands_to(self):
        conf = VyosConf(["set a b 'c a'", "set a c b"])

        self.assertListEqual(
            conf.diff_commands_to(VyosConf(["set a c b"])), ["delete a b"]
        )
        self.assertListEqual(
            conf.diff_commands_to(VyosConf(["set a b 'c a'", "set a c b"])), []
        )

        self.assertListEqual(
            conf.diff_commands_to(
                VyosConf(
                    [
                        "set a b ...",
                    ]
                )
            ),
            ["delete a c"],
        )
        self.assertListEqual(
            conf.diff_commands_to(VyosConf(["set a ...", "set a d e"])),
            ["set a d e"],
        )
        self.assertListEqual(
            conf.diff_commands_to(VyosConf(["set a b", "set a c b"])),
            ["delete a b 'c a'"],
        )

        self.assertListEqual(
            conf.diff_commands_to(VyosConf(["set a b 'a c'", "set a c b"])),
            ["delete a b 'c a'", "set a b 'a c'"],
        )

        self.assertListEqual(
            VyosConf(
                ["set a b c d", "set a b c e", "set a b d"]
            ).diff_commands_to(VyosConf(["set a b c d", "set a b ..."])),
            ["delete a b c e"],
        )


if __name__ == "__main__":
    unittest.main()
