from dataclasses import dataclass
import sys
import os
from typing import Optional

@dataclass
class User:
    name: str
    password_env_var: str

    def __post_init__(self):
        if not self.password_env_var in os.environ:
            print(f'Failed to create user [ {self.name} ]\npassword env var [ {self.password_env_var} ] is not set')
            sys.exit(1)

    def get_password(self):
        return os.environ.get(self.password_env_var)
    
    def add_prod_index(self, index_name):
        return IndexConfigurationBuilder(self, index_name).volatile(False)
    
    def add_volatile_index(self, index_name):
        return IndexConfigurationBuilder(self, index_name).volatile(True)
        
@dataclass
class IndexConfiguration:
    user: User
    name: str
    details: dict
    artifact_dir_path: Optional[str]

    def get_use_str(self):
        return f'{self.user.name}/{self.name}'

class IndexConfigurationBuilder():
    def __init__(self, user, name):
        self.user: User = user
        self.name: str = name
        self.set_volatile: bool = True
        self.bases: list[IndexConfiguration | str] = []
        self.artifact_dir_path: Optional[str] = None

    def volatile(self, volatility: bool) -> 'IndexConfigurationBuilder':
        self.volatile = volatility
        return self

    def with_base(self, base: IndexConfiguration | str)  -> 'IndexConfigurationBuilder':
        if isinstance(base, IndexConfiguration):
            self.bases.append(f'{base.user.name}/{base.name}')
        else:
            self.bases.append(base)
        return self

    def with_artifacts(self, artifact_dir_path: str)  -> 'IndexConfigurationBuilder':
        self.artifact_dir_path = artifact_dir_path
        return self

    def build(self) -> IndexConfiguration:
        return IndexConfiguration(
            user=self.user,
            name=self.name,
            details={
                'volatile': self.set_volatile,
                'bases': ','.join(self.bases)
            },
            artifact_dir_path=self.artifact_dir_path
        )
    