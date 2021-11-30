from invoke import task
import os
import shutil

@task
def start(ctx):
    ctx.run("python3 src/index.py")

@task
def test(ctx):
    os.chdir('./src')
    ctx.run("pytest")

@task
def coverage(ctx):
    os.chdir('./src')
    ctx.run("coverage run --branch -m pytest")
    os.remove("../.coverage")
    shutil.move(".coverage", "..")
    os.chdir('..')

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")

#There's a quick workaround here to make test run correctly to find png files -> should update to a better way of doing this