import requests
import re
import yaml
from typing import Dict, Any

class GitRepositoryScanner:
    def __init__(self):
        with open("config/governance_rules.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        self.api_base = "https://api.github.com/repos"
        
    def _parse_url(self, url: str) -> tuple:
        parsed = re.sub(r"https?://(www\.)?github\.com/", "", url).strip("/")
        parts = parsed.split("/")
        if len(parts) < 2:
            raise ValueError("Malformed GitHub URL mapping format target.")
        return parts[0], parts[1]

    def extract_schema_files(self, repo_url: str) -> str:
        owner, repo = self._parse_url(repo_url)
        endpoint = f"{self.api_base}/{owner}/{repo}/contents"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        response = requests.get(endpoint, headers=headers, timeout=10)
        if response.status_code != 200:
            return ""
            
        combined_payload = []
        for asset in response.json():
            if asset["type"] == "file" and asset["name"].endswith(('.sql', '.prisma', '.py')):
                file_raw = requests.get(asset["download_url"], timeout=10)
                if file_raw.status_code == 200:
                    combined_payload.append(f"--- FILE: {asset['name']} ---\n{file_raw.text}")
                    
        return "\n\n".join(combined_payload)