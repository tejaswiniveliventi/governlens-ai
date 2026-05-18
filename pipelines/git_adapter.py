import requests
import yaml
import os
from typing import List

class GitRepositoryScanner:
    def __init__(self):
        # Load external rules file for target scanning extensions
        rules_path = os.path.join("config", "governance_rules.yaml")
        with open(rules_path, "r") as f:
            self.rules = yaml.safe_load(f)
        
        self.api_base = self.rules["rules_engine"]["github_api_base_url"]
        self.valid_exts = tuple(self.rules["rules_engine"]["supported_extensions"])

    def _parse_github_url(self, url: str) -> tuple:
        """Translates a public standard web URL into clean owner/repo metadata blocks."""
        clean_url = url.replace("https://github.com/", "").strip("/")
        parts = clean_url.split("/")
        owner = parts[0]
        repo = parts[1]
        return owner, repo

    def extract_schema_files(self, repo_url: str) -> str:
        """Scans the repository structures via API completely in-memory without cloning."""
        try:
            owner, repo = self._parse_github_url(repo_url)
            target_endpoint = f"{self.api_base}/{owner}/{repo}/contents"
            
            headers = {"Accept": "application/vnd.github.v3+json"}
            response = requests.get(target_endpoint, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"GitHub API returned error code status: {response.status_code}")
                
            contents = response.json()
            schema_payloads = []
            
            # Unpack file trees cleanly in memory strings
            for item in contents:
                if item["type"] == "file" and item["name"].endswith(self.valid_exts):
                    raw_download_url = item["download_url"]
                    file_res = requests.get(raw_download_url)
                    
                    if file_res.status_code == 200:
                        schema_payloads.append(f"--- File Node: {item['name']} ---\n{file_res.text}")
            
            if not schema_payloads:
                return f"# Warning: No explicit files matching extensions {self.valid_exts} located."
                
            return "\n\n".join(schema_payloads)
            
        except Exception as e:
            return f"# Failure occurred during automated in-memory Git API extraction track: {str(e)}"