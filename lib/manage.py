from lib.utils.cli import CLI

from lib.commands.load_iris import load_iris
from lib.commands.load_geofon import load_geofon
from lib.commands.load_fdsn import load_fdsn
from lib.commands.run_loader import run_loader
from lib.commands.run_server import run_server

cli = CLI(commands=[
    load_iris, load_geofon, run_loader, load_fdsn, run_server
])

