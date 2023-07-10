#!/usr/bin/python3
# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0


# outputs a CHANGELOG blurb based on go.mod changes in the working dir

import subprocess

output = subprocess.check_output(
    r"""git diff HEAD^ -- go.mod | cat | grep -ve indirect | grep -P '^[-+]\t'""", shell=True
)

minus = {}
plus = {}

for l in output.decode("utf8").strip().split("\n"):
    if l.startswith("-"):
        name, version = l[1:].strip().split(" ")
        minus[name] = version
    elif l.startswith("+"):
        name, version = l[1:].strip().split(" ")
        plus[name] = version

keys = sorted(set(minus.keys()) | set(plus.keys()))
print("IMPROVEMENTS:")
print("* Updated dependencies:")
for key in keys:
    if key in minus and plus:
        print(f"   * `{key}` {minus[key]} -> {plus[key]}")
    elif key in minus:
        print(f"   * `{key}` {minus[key]} removed")
    else:
        print(f"   * `{key}` {plus[key]} added")
