from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

# Importing File Function Modules
from config.constants import WORK_DIR_DOCKER,TIMEOUT_DOCKER
def getDockerCommandLineExecutor():
    docker=DockerCommandLineCodeExecutor(
        work_dir=WORK_DIR_DOCKER,
        timeout=TIMEOUT_DOCKER
    )
    return docker

async def start_docker_container(docker):
    print(f"Starting Docker Container.")
    await docker.start()
    print(f"Starting Docker Started.")

async def stop_docker_container(docker):
    print(f"Ending Docker Container.")
    await docker.stop()
    print(f"Docker Stopped.")
