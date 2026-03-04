import argparse
import logging
import requests
import json
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scan_github_repos(api_key, repo_list):
    """
    Scan GitHub repositories for API key leaks.

    Args:
        api_key (str): The API key to search for.
        repo_list (list): A list of GitHub repository URLs to scan.

    Returns:
        list: A list of repositories where the API key was found.
    """
    leaked_repos = []
    for repo in repo_list:
        try:
            response = requests.get(repo + '/contents/')
            if response.status_code == 200:
                contents = json.loads(response.content)
                for file in contents:
                    if api_key in file['name']:
                        leaked_repos.append(repo)
                        break
        except requests.exceptions.RequestException as e:
            logging.error(f"Error scanning repository {repo}: {e}")
    return leaked_repos

def monitor_exchange_api(api_key, exchange_url):
    """
    Monitor a cryptocurrency exchange API for suspicious activity.

    Args:
        api_key (str): The API key to monitor.
        exchange_url (str): The URL of the exchange API.

    Returns:
        bool: True if suspicious activity is detected, False otherwise.
    """
    try:
        response = requests.get(exchange_url, headers={'Authorization': f'Bearer {api_key}'})
        if response.status_code == 200:
            # Check for suspicious activity (e.g., unusual login locations)
            # For demonstration purposes, we'll just check for a specific IP address
            if '192.168.1.100' in response.content:
                return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Error monitoring exchange API {exchange_url}: {e}")
    return False

def create_dashboard(leaked_repos, suspicious_activity):
    """
    Create a dashboard to display leak detection results and provide alerts for potential security threats.

    Args:
        leaked_repos (list): A list of repositories where the API key was found.
        suspicious_activity (bool): True if suspicious activity is detected, False otherwise.
    """
    print("Dashboard:")
    print("==========")
    if leaked_repos:
        print("API key leaks detected in the following repositories:")
        for repo in leaked_repos:
            print(repo)
    else:
        print("No API key leaks detected.")
    if suspicious_activity:
        print("Suspicious activity detected on the exchange API.")
    else:
        print("No suspicious activity detected.")

def main():
    parser = argparse.ArgumentParser(description='Crypto API Key Leak Detector')
    parser.add_argument('--api-key', help='The API key to scan for', required=True)
    parser.add_argument('--repo-list', help='A list of GitHub repository URLs to scan', nargs='+', required=True)
    parser.add_argument('--exchange-url', help='The URL of the exchange API', required=True)
    args = parser.parse_args()

    try:
        leaked_repos = scan_github_repos(args.api_key, args.repo_list)
        suspicious_activity = monitor_exchange_api(args.api_key, args.exchange_url)
        create_dashboard(leaked_repos, suspicious_activity)
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == '__main__':
    main()