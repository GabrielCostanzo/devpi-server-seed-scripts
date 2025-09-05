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
            logger.error(f'{e.stdout}\n{e.stderr}')
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
    
    def create_user(self, user):
        users = self.get_users()
        if user.name in users:
            return
        self._run_command(
            ['devpi', 'user', '-c', user.name, f'password={user.get_password()}']
        )

    def create_index(self, index):
        indices = self.get_indices()
        if index.get_use_str() in indices:
            return

        # Convert kwargs dict to list of "key=value" strings
        extra_args = []
        if index.details:
            extra_args = [f"{key}={value}" for key, value in index.details.items()]

        self._run_command(
            ['devpi', 'index', '-c', index.name] + extra_args
        )

    def login(self, user):
        self._run_command(
            ['devpi', 'login', user.name, '--password', user.get_password()]
        )

    def use(self, arg):
        self._run_command(
            ['devpi', 'use', arg]
        )

    def upload(self, artifact_dir_path):
        if not artifact_dir_path:
            logger.info(f'no configured files to upload')
            return
        files_to_upload = glob.glob(f"{artifact_dir_path}/*")
        if not files_to_upload:
            raise ValueError(f"No files found in {artifact_dir_path}")
        logger.info(f'uploading {len(files_to_upload)} files')
        self._run_command(
            ['devpi', 'upload', *files_to_upload]
        )
        logger.info(f'successfully uploaded files')


