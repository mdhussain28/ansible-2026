#!/usr/bin/python

DOCUMENTATION = r'''
---
module: check_disk_usage
short_description: Check disk usage percentage against a threshold
description:
  - Checks used disk space percentage for a given path
  - Fails if usage exceeds the given threshold
options:
  path:
    description: Filesystem path to check
    required: true
    type: str
  threshold:
    description: Maximum allowed usage percentage
    required: false
    type: int
    default: 80
author:
  - ShopEase DevOps Team
'''

EXAMPLES = r'''
- name: Check disk usage on root
  check_disk_usage:
    path: /
    threshold: 75
'''

RETURN = r'''
used_percent:
  description: Actual disk usage percentage
  type: int
  returned: always
threshold:
  description: Threshold that was checked against
  type: int
  returned: always
'''

import os
import shutil
from ansible.module_utils.basic import AnsibleModule


def get_disk_usage(path):
    total, used, free = shutil.disk_usage(path)
    percent_used = int((used / total) * 100)
    return percent_used


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        threshold=dict(type='int', required=False, default=80),
    )

    result = dict(
        changed=False,
        used_percent=0,
        threshold=0,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    threshold = module.params['threshold']

    if not os.path.exists(path):
        module.fail_json(msg=f"Path {path} does not exist", **result)

    used_percent = get_disk_usage(path)
    result['used_percent'] = used_percent
    result['threshold'] = threshold

    if used_percent > threshold:
        module.fail_json(
            msg=f"Disk usage {used_percent}% exceeds threshold {threshold}% on {path}",
            **result
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
