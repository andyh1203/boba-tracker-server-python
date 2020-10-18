from invoke import task


@task
def dev(c):
    c.run("uvicorn app.main:app --reload")


def start(c):
    c.run("uvicorn main:app")
