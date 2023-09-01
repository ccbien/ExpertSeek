import requests


class ZillizClient:
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {api_key}"
        }
    
    
    def search(self, collection_name, vector, limit):
        data = {
            "collectionName": collection_name,
            "vector": vector,
            "limit": limit,
            "output_fields": "string_id"
        }
        res_data = self._request(data, "/v1/vector/search")
        ids = [item["id"] for item in res_data]
        string_ids = self.get_string_ids(collection_name, ids)
        for item, string_id in zip(res_data, string_ids):
            item["id"] = string_id
        return res_data
    
    
    def get_string_ids(self, collection_name, ids):
        data = {
            "collectionName": collection_name,
            "id": ids
        }
        res_data = self._request(data, "/v1/vector/get")
        return [item["string_id"] for item in res_data]
    
    
    def _request(self, data, route):
        res = requests.post(
            self.endpoint + route,
            headers=self.headers,
            json=data
        ).json()
        
        if res["code"] != 200:
            raise Exception("Zilliz API error")
        
        return res["data"]