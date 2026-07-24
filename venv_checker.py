import sys

def is_venv():
    # Modern Python (venv) check
    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True
    # Legacy virtualenv check
    if hasattr(sys, "real_prefix"):
        return True
    return False

if is_venv():
    print("Running inside a virtual environment.")
else:
    print("Running globally / outside a virtual environment.")