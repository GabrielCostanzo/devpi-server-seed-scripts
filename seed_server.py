from lib.server_endpoint import ServerEndpoint
from lib.server_status_checker import ServerStatusChecker
from lib.devpi_command_executor import DevpiCommandExecutor
from lib.index_configuration import IndexConfiguration, User
import logging

HOST_NAME = 'localhost'
PORT = 4040

INDEX_PYPI_MIRROR_DEFAULT = 'root/pypi'

USER_CACHE = User('cache', 'CACHE_USER_PASSWORD')
USER_DEV = User('costanga', 'DEV_USER_PASSWORD')

INDEX_CACHE_PRIVATE: IndexConfiguration = (
    USER_CACHE.add_volatile_index('private')
    .with_artifacts('./target_artifacts')
    .build()
)
INDEX_CACHE_PROD: IndexConfiguration = (
    USER_CACHE.add_volatile_index('prod')
    .with_base(INDEX_PYPI_MIRROR_DEFAULT)
    .with_base(INDEX_CACHE_PRIVATE)
    .build()
)
INDEX_DEV: IndexConfiguration = (
    USER_DEV.add_volatile_index('dev')
    .build()
)

INDICIES = [
    INDEX_CACHE_PRIVATE,
    INDEX_CACHE_PROD,
    INDEX_DEV
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"                  
    #format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def seed_index(server_url:str, 
               executor: DevpiCommandExecutor,
               status_checker: ServerStatusChecker,
               index: IndexConfiguration):
    
    server_is_running = status_checker.is_running()
    if not server_is_running:
        raise Exception('Server is not running')

    logger.info(f'Seeding index [ {index.get_use_str()} ]')
    executor.use(server_url)
    executor.create_user(index.user)
    executor.login(index.user)
    executor.create_index(index)
    executor.use(index.get_use_str())
    executor.upload(index.artifact_dir_path)

if __name__ == '__main__':
    server_endpoint: ServerEndpoint = ServerEndpoint(
        host_name=HOST_NAME,
        port=PORT
    )

    status_checker: ServerStatusChecker = ServerStatusChecker(
        server_endpoint=server_endpoint
    )

    executor: DevpiCommandExecutor = DevpiCommandExecutor()

    server_url = server_endpoint.get_url()

    for index in INDICIES:
        seed_index(
            server_url=server_url,
            executor=executor,
            status_checker=status_checker,
            index=index
        )