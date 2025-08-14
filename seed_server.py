from lib.server_endpoint import ServerEndpoint
from lib.server_status_checker import ServerStatusChecker
from lib.devpi_command_executor import DevpiCommandExecutor
import logging
import os

PASSWORD_ENV_VAR = 'BOOTSTRAP_USER_PASSWORD'
HOST_NAME = 'localhost'
PORT = 4040
USERNAME = 'bootstrap'
PASSWORD = os.environ.get(PASSWORD_ENV_VAR)
INDEX_NAME = 'cookiecutter'
ARTIFACT_DIR_PATH = './target_artifacts'

logging.basicConfig(
    level=logging.INFO,                  
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def seed_server(status_checker: ServerStatusChecker,
         executor: DevpiCommandExecutor,
         server_url: str,
         username: str,
         password: str,
         index_name: str,
         artifact_dir_path: str):
    
    server_is_running = status_checker.is_running()
    if not server_is_running:
        raise Exception('Server is not running')

    executor.use(server_url)
    executor.create_user(
        username=username,
        password=password
    )
    executor.login(
        username=username,
        password=password
    )
    executor.create_pypi_mirror_index(
        username=username,
        index_name=index_name
    )
    executor.use(f'{username}/{index_name}')
    executor.upload(artifact_dir_path)

if __name__ == '__main__':
    if not PASSWORD_ENV_VAR in os.environ:
        raise Exception(f'required env var [ {PASSWORD_ENV_VAR} ] is not set')
    
    server_endpoint: ServerEndpoint = ServerEndpoint(
        host_name=HOST_NAME,
        port=PORT
    )

    status_checker: ServerStatusChecker = ServerStatusChecker(
        server_endpoint=server_endpoint
    )

    executor: DevpiCommandExecutor = DevpiCommandExecutor()

    server_url = server_endpoint.get_url()

    seed_server(
        status_checker=status_checker,
        executor=executor,
        server_url=server_url,
        username=USERNAME,
        password=PASSWORD,
        index_name=INDEX_NAME,
        artifact_dir_path=ARTIFACT_DIR_PATH
    )