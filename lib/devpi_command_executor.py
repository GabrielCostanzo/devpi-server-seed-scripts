import subprocess
import glob
import logging
import sys

logger = logging.getLogger(__name__)

class DevpiCommandExecutor():
    def __init__(self):
        pass

    def _run_command(self, cmd: list[str]) -> subprocess.CompletedProcess:
        try:
            result = subprocess.run(
                cmd,
                text=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            result.check_returncode() 
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f'ERROR: {e.stdout}')
            sys.exit(1)

    def get_users(self):
        result = self._run_command(
            ['devpi', 'user', '-l']
        )
        return set(result.stdout.strip().split('\n'))

    def get_indices(self):
        result = self._run_command(
            ['devpi', 'index', '-l']
        )
        return set(result.stdout.strip().split('\n'))
    
    def create_user(self, username, password):
        users = self.get_users()
        if username in users:
            return
        self._run_command(
            ['devpi', 'user', '-c', username, '--password', password]
        )

    def create_pypi_mirror_index(self, username, index_name):
        indices = self.get_indices()
        if f'{username}/{index_name}' in indices:
            return
        self._run_command(
            ['devpi', 'index', '-c', index_name, 'bases=root/pypi']
        )

    def login(self, username, password):
        self._run_command(
            ['devpi', 'login', username, '--password', password]
        )

    def use(self, arg):
        self._run_command(
            ['devpi', 'use', arg]
        )

    def upload(self, artifact_dir_path):
        files_to_upload = glob.glob(f"{artifact_dir_path}/*")
        if not files_to_upload:
            raise ValueError(f"No files found in {artifact_dir_path}")
        logger.info(f'uploading {len(files_to_upload)} files')
        self._run_command(
            ['devpi', 'upload', *files_to_upload]
        )
        logger.info(f'successfully uploaded files')


