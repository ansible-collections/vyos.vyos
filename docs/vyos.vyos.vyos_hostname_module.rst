.. _vyos.vyos.vyos_hostname_module:


***********************
vyos.vyos.vyos_hostname
***********************

**Manages hostname resource module**


Version added: 2.8.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the hostname attribute of Vyos network devices




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hostname configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hostname</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>set hostname for VYOS.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>running_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option is used only with state <em>parsed</em>.</div>
                        <div>The value of this option should be the output received from the vyos device by executing the command <b>&quot;show configuration commands | grep host-name&quot;</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>replaced</li>
                                    <li>overridden</li>
                                    <li>deleted</li>
                                    <li>gathered</li>
                                    <li>parsed</li>
                                    <li>rendered</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The states <em>merged</em>, <em>replaced</em> and <em>overridden</em> have identical behaviour for this module.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show configuration commands | grep host-name</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against vyos 1.1.8
   - This module works with connection ``network_cli``.
   - The Configuration defaults of the Vyos network devices are supposed to hinder idempotent behavior of plays



Examples
--------

.. code-block:: yaml

    # Using merged
    #
    # Before state:
    # -------------
    # test#show configuration commands | grep host-name
    # set system host-name 'vyostest'

    - name: Apply the provided configuration
      vyos.vyos.vyos_hostname:
        config:
          hostname: vyos
        state: merged

    # Commands Fired:
    # ---------------
    # "commands": [
    #         "hostname vyos",
    # ],
    #
    # After state:
    # ------------
    # test#show configuration commands | grep host-name
    # set system host-name 'vyos'

    # Using deleted
    #
    # Before state:
    # -------------
    # test#show configuration commands | grep host-name
    # set system host-name 'vyos'
    #
    - name: Remove all existing configuration
      vyos.vyos.vyos_hostname:
        state: deleted

    # Commands Fired:
    # ---------------
    # "commands": [
    #     "no hostname vyosTest",
    # ],
    #
    # After state:
    # ------------
    # test#show configuration commands | grep host-name

    # Using overridden
    #
    # Before state:
    # -------------
    # test#show configuration commands | grep host-name
    # set system host-name 'vyos'

    - name: Override commands with provided configuration
      vyos.vyos.vyos_hostname:
        config:
          hostname: vyosTest
        state: overridden

    # Commands Fired:
    # ---------------
    # "commands": [
    #       "hostname vyosTest",
    #     ],
    #
    # After state:
    # ------------
    # test#show configuration commands | grep host-name
    # set system host-name 'vyosTest'

    # Using replaced
    #
    # Before state:
    # -------------
    # test#show configuration commands | grep host-name
    # set system host-name 'vyosTest'

    - name: Replace commands with provided configuration
      vyos.vyos.vyos_hostname:
        config:
          hostname: vyos
        state: replaced

    # After state:
    # ------------
    # test#show configuration commands | grep host-name
    # set system host-name 'vyos'

    # Using gathered
    #
    # Before state:
    # -------------
    # test#show configuration commands | grep host-name
    # set system host-name 'vyos'

    - name: Gather listed hostname config
      vyos.vyos.vyos_hostname:
        state: gathered

    # Module Execution Result:
    # ------------------------
    #   "gathered": {
    #      "hostname": "vyos"
    #     },

    # Using state: rendered
    # Rendered play:
    # --------------
    - name: Render the commands for provided configuration
      vyos.vyos.vyos_hostname:
        config:
          hostname: vyosTest
        state: rendered
    # Module Execution Result:
    # ------------------------
    # "rendered": [
    #     "set system host-name vyosTest",
    # ]

    # Using state: parsed
    # File: parsed.cfg
    # ----------------
    # set system host-name 'vyos'
    # Parsed play:
    # ------------
    - name: Parse the provided configuration with the existing running configuration
      vyos.vyos.vyos_hostname:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed
    # Module Execution Result:
    # ------------------------
    #  "parsed": {
    #     "hostname": "vyos"
    # }



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>after</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when changed</td>
                <td>
                            <div>The resulting configuration after module execution.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>before</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code> or <code>purged</code></td>
                <td>
                            <div>The configuration prior to the module execution.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code> or <code>purged</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;sample command 1&#x27;, &#x27;sample command 2&#x27;, &#x27;sample command 3&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>gathered</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>gathered</code></td>
                <td>
                            <div>Facts about the network resource gathered from the remote device as structured data.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>parsed</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>parsed</code></td>
                <td>
                            <div>The device native config provided in <em>running_config</em> option parsed into structured data as per module argspec.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>rendered</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>rendered</code></td>
                <td>
                            <div>The provided configuration in the task rendered in device-native format (offline).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;sample command 1&#x27;, &#x27;sample command 2&#x27;, &#x27;sample command 3&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Gomathi Selvi Srinivasan (@GomathiselviS)
