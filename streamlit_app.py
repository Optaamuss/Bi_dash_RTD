import subprocess
import sys


try:
    import plotly  # noqa: F401
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly>=5.24.1"])


from dashboard.app import *  # noqa: F401,F403
