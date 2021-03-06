from invoke import task


@task
def publish(c):
    c.run('python setup.py sdist bdist_wheel')
    c.run('twine upload dist/*')
