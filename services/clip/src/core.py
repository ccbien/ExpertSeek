import numpy as np
from clip_client import Client


class CLIPEncoder:
    def __init__(self, endpoint, api_key):
        self.client = Client(
            endpoint,
            credential={"Authorization": api_key},
        )        
    
    def encode(self, text):
        embedding = self.client.encode([text])[0]
        embedding /= np.linalg.norm(embedding)
        return embedding.tolist()
