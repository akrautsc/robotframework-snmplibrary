import pathlib
import subprocess
from invoke import task
# from SnmpLibrary import __version__ as VERSION
import inspect

if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

ROOT = pathlib.Path(__file__).parent.resolve().as_posix()

@task
def libdoc(context):
    source = f"{ROOT}/SnmpLibrary/"
    target = f"{ROOT}/docs/SnmpLibrary.html"
    cmd = [
        "libdoc",
        "-n SnmpLibrary",
        # f"-v {VERSION}",
        source,
        target,
    ]
    subprocess.run(" ".join(cmd), shell=True)

@task
def atests(context):
    cmd = [
        "coverage",
        "run",
        "--source=SnmpLibrary",
        "-p",
        "-m",
        "robot",
        "-P SnmpLibrary",
        "--loglevel=TRACE",
        "--listener RobotStackTracer",
        "-d results",
        f"{ROOT}/test/atest"
    ]
    global atests_completed_process
    atests_completed_process = subprocess.run(" ".join(cmd), shell=True, check=False)

@task
def utests(context):
    cmd = [
        "coverage",
        "run",
        "--source=SnmpLibrary",
        "-p",
        "-m",
        "pytest",
        f"{ROOT}/test/utest"
    ]
    global atests_completed_process
    atests_completed_process = subprocess.run(" ".join(cmd), shell=True, check=False)

@task(utests, atests)
def tests(context):
    subprocess.run("coverage combine", shell=True, check=False)
    subprocess.run("coverage report", shell=True, check=False)
    subprocess.run("coverage html -d results/htmlcov", shell=True, check=False)
    if atests_completed_process.returncode != 0:
        raise Exception("Tests failed")

@task
def coverage_report(context):
    subprocess.run("coverage combine", shell=True, check=False)
    subprocess.run("coverage report", shell=True, check=False)
    subprocess.run("coverage html -d results/htmlcov", shell=True, check=False)