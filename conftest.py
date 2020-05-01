import docker
import pytest
import subprocess

# dclient = docker.DockerClient(base_url='unix://var/run/docker.sock')
dclient = docker.from_env()


def check_dir_start(build=True):
    command = ['docker-compose', 'up', "-d", "--force-recreate"]
    if build:
        command.append('--build')

    subprocess.run(command, stdout=subprocess.DEVNULL)

@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    print("\n====SETUP====")
    check_dir_start()
    yield

    print("\n====CLEANUP====")
    for container in dclient.containers.list(filters={"label":"qe.test.containers=true"}):
        print("container", container)
        try:
            container.stop()
            container.remove()

        except Exception as e:
            print("Error: ", e)

    # images = dclient.images.list()
    # print("images: ", images)
    # if len(images) > 0:
    #     for image in images:
    #         tag = image.tags[0]
    #         dclient.images.remove(image=tag, force=True)
