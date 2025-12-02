import grpc
import json
from proto import checker_pb2, checker_pb2_grpc

class GRPCClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = checker_pb2_grpc.CookieCheckerStub(self.channel)
    
    def check_cookie(self, service, file_path, cookies, proxy='', use_stealth=False):
        try:
            request = checker_pb2.CookieRequest(
                service=service,
                file_path=file_path,
                cookies=cookies,
                proxy=proxy,
                use_stealth=use_stealth
            )
            
            response = self.stub.CheckCookie(request, timeout=30)
            return response
            
        except grpc.RpcError as e:
            return None
    
    def check_batch(self, requests):
        try:
            batch_request = checker_pb2.BatchRequest(requests=requests)
            responses = self.stub.CheckBatch(batch_request)
            return list(responses)
            
        except grpc.RpcError as e:
            return []
    
    def close(self):
        self.channel.close()