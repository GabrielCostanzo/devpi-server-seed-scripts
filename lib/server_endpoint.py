from dataclasses import dataclass

@dataclass
class ServerEndpoint:
    host_name: str
    port: int

    def get_url(self):
        return f'http://{self.host_name}:{self.port}'