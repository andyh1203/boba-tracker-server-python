from invoke import task


@task
def dev(c):
    c.run("uvicorn main:app --reload --app-dir src")


def start(c):
    c.run("uvicorn main:app")
