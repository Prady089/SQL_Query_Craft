import os
import sys

# Find project root by walking upwards until a marker file exists (app.py, requirements.txt, or .git)
def find_project_root(start_dir: str) -> str | None:
    cur = os.path.abspath(start_dir)
    while True:
        if (
            os.path.exists(os.path.join(cur, "app.py"))
            or os.path.exists(os.path.join(cur, "requirements.txt"))
            or os.path.exists(os.path.join(cur, ".git"))
        ):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


ROOT = find_project_root(os.path.dirname(__file__))
if ROOT and ROOT not in sys.path:
    sys.path.insert(0, ROOT)
