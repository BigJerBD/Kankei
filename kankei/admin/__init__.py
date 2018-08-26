import inspect
import itertools
import sys

from admin.converts import *
from admin.resets import *
from admin.imports import *


def get_admin_actions(action_type=""):
    return {name: action for name, action in
            itertools.chain(
                inspect.getmembers(sys.modules["admin.converts"], inspect.isfunction),
                inspect.getmembers(sys.modules["admin.imports"], inspect.isfunction),
                inspect.getmembers(sys.modules["admin.resets"], inspect.isfunction))
            if not name.startswith(f"_") and (name.startswith(action_type) or not action_type)
            }
