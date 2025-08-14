import requests
import socket
import time
from typing import Dict, Any
from lib.server_endpoint import ServerEndpoint
    
class ServerStatusChecker:
    def __init__(self, server_endpoint: ServerEndpoint, timeout: int = 10):
        self.server_endpoint: ServerEndpoint = server_endpoint
        self.timeout = timeout
    
    def _check_port_open(self) -> bool:
        try:
            with socket.create_connection(
                    (self.server_endpoint.host_name, self.server_endpoint.port), 
                    timeout=self.timeout
                ):
                return True
                
        except (socket.error, ValueError, OSError):
            return False
    
    def _check_http_response(self) -> Dict[str, Any]:
        result = {
            'responding': False,
            'status_code': None,
            'error': None,
            'response_time': None
        }
        
        try:
            start_time = time.time()
            response = requests.get(self.server_endpoint.get_url(), timeout=self.timeout)
            response_time = time.time() - start_time
            
            result.update({
                'responding': True,
                'status_code': response.status_code,
                'response_time': round(response_time, 3)
            })
            
        except requests.exceptions.RequestException as e:
            result['error'] = str(e)
        
        return result
    
    def is_running(self) -> bool:
        port_open = self._check_port_open()
        if not port_open:
            return False
        
        http_check = self._check_http_response()
        return http_check['responding'] and http_check['status_code'] == 200