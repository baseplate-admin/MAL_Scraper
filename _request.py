import requests
from requests.adapters import HTTPAdapter, Retry


session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=0.1,
    status_forcelist=[
        429,
        400,
    ],
)

session.mount("http://", HTTPAdapter(max_retries=retries))
