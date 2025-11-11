"""Tests unitaires pour le client Twitter."""

import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api_clients.twitter_client import TwitterClient


def test_twitter_client_initialization():
    """Tester l'initialisation du client (nécessite credentials)."""
    try:
        client = TwitterClient()
        assert client.client is not None
    except ValueError as e:
        # Normal si les credentials ne sont pas configurés
        assert "TWITTER_BEARER_TOKEN" in str(e)


def test_search_tweets_empty_query():
    """Tester la recherche avec une requête vide."""
    try:
        client = TwitterClient()
        results = client.search_tweets("", max_results=10, save_raw=False)
        assert isinstance(results, list)
    except ValueError:
        pytest.skip("Credentials Twitter non configurés")
