from lib.server_endpoint import ServerEndpoint
from lib.server_status_checker import ServerStatusChecker
from lib.devpi_command_executor import DevpiCommandExecutor
import logging
import os

PASSWORD_ENV_VAR = 'DEFAULT_DEVPI_USER_PASSWORD'
HOST_NAME = 'localhost'
PORT = 4040
PASSWORD = os.environ.get(PASSWORD_ENV_VAR)
ARTIFACT_DIR_PATH = './target_artifacts'

USERNAME = 'cache'
INDEX_NAME = 'public'
INDEX_KWARGS = {
    'bases': 'root/pypi',
    'volatile': 'true'
}

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
         index_kwargs: dict,
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
    executor.create_index(
        username=username,
        index_name=index_name,
        kwargs=index_kwargs
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
        index_kwargs=INDEX_KWARGS,
        artifact_dir_path=ARTIFACT_DIR_PATH
    )