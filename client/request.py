import requests


BASE = "http://localhost"
PORT_SQL = 8000
PORT_CLIP = 8001
PORT_VECDB = 8002


def search_authors(name, org):
    res = requests.get(
        f"{BASE}:{PORT_SQL}/search/authors",
        params={"name": name, "org": org, "limit": 10}
    )
    return res.json()["authors"]


def get_all_paper(author_id):
    res = requests.get(
        f"{BASE}:{PORT_SQL}/get/all-papers",
        params={"author_id": author_id}
    )
    pids = [item["paper_id"] for item in  res.json()["papers"]]
    
    papers = []
    for pid in pids:
        res = requests.get(
            f"{BASE}:{PORT_SQL}/get/paper",
            params={"paper_id": pid}
        )
        papers.append(res.json()["paper"])
    return papers


def get_top_coauthor(author_id):
    res = requests.get(
        f"{BASE}:{PORT_SQL}/get/top-coauthor",
        params={"author_id": author_id, "limit": 10}
    )
    aids = [item["author_id"] for item in res.json()["authors"]]
    
    authors = []
    for aid in aids:
        res = requests.get(
            f"{BASE}:{PORT_SQL}/get/author",
            params={"author_id": aid}
        )
        authors.append(res.json()["author"])
    return authors


def search_authors_kw(text):
    res = requests.get(
        f"{BASE}:{PORT_CLIP}/encode",
        params={"text": text}
    )
    embedding = res.json()["embedding"]

    res = requests.post(
        f"{BASE}:{PORT_VECDB}/search/paper",
        json={
            "vector": embedding,
            "limit": 10,
        }
    )
    pids = [item["id"] for item in res.json()["data"]]
    
    aids = set()
    for pid in pids:
        res = requests.get(
            f"{BASE}:{PORT_SQL}/get/first-author",
            params={"paper_id": pid}
        )
        aids.add(res.json()["author_id"])
        
    authors = []
    for aid in aids:
        res = requests.get(
            f"{BASE}:{PORT_SQL}/get/author",
            params={"author_id": aid}
        )
        authors.append(res.json()["author"])
    return authors


search_authors_kw("diffusions")