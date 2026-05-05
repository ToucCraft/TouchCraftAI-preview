import requests
import logging

class NPMManager:
    def __init__(self, api_url, email, password):
        self.api_url = api_url.rstrip('/')
        self.email = email
        self.password = password
        self.token = self._get_token()

    def _get_token(self):
        try:
            url = f"{self.api_url}/tokens"
            payload = {"identity": self.email, "secret": self.password}
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("token")
        except Exception as e:
            logging.error(f"❌ NPM Auth Error: {str(e)}")
            return None

    def create_proxy_host(self, domain, container_name, port=80):
        if not self.token:
            logging.error("❌ No NPM token available")
            return None

        url = f"{self.api_url}/nginx/proxy-hosts"
        headers = {"Authorization": f"Bearer {self.token}"}

        payload = {
            "domain_names": [domain],
            "forward_scheme": "http",
            "forward_host": container_name,
            "forward_port": port,
            "access_list_id": 0,
            "certificate_id": "new",
            "meta": {
                "letsencrypt_email": self.email,
                "letsencrypt_agree": True
            },
            "ssl_forced": True,
            "http2_support": True,
            "block_exploits": True,
            "caching_enabled": False,
            "allow_websocket_upgrade": True
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code in [200, 201]:
                host_data = response.json()
                host_id = host_data.get("id")
                cert_id = host_data.get("certificate_id")

                if host_id and cert_id:
                    update_url = f"{url}/{host_id}"
                    payload["certificate_id"] = cert_id
                    requests.put(update_url, json=payload, headers=headers, timeout=15)

                logging.info(f"✅ Proxy Host с SSL and Force SSL created for {domain}")
                return host_data
            else:
                logging.error(f"❌ Error NPM API: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logging.error(f"❌ NPM Request Failed: {str(e)}")
            return None

    def get_proxy_hosts(self):
        if not self.token:
            return []

        url = f"{self.api_url}/nginx/proxy-hosts"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            logging.error(f"❌ Error fetching hosts: {e}")
            return []
