# tests/api/test_api.py
#
# API tests against JSONPlaceholder — a free, public fake REST API.
# Great for learning because it requires no account or API key.
#
# Base URL: https://jsonplaceholder.typicode.com
# Docs:     https://jsonplaceholder.typicode.com/guide/

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ---------------------------------------------------------------------------
# Test 1 – successful GET (list of posts)
# ---------------------------------------------------------------------------
# Scenario: fetch all posts and verify the response looks healthy.
# This is the most basic API check: "did the server respond correctly?"

def test_get_all_posts():
    response = requests.get(f"{BASE_URL}/posts")

    # HTTP 200 means "OK" — the request succeeded
    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    posts = response.json()  # parse the JSON body into a Python list

    # JSONPlaceholder always returns exactly 100 posts
    assert isinstance(posts, list), "Response body should be a JSON array"
    assert len(posts) == 100, f"Expected 100 posts, got {len(posts)}"

    # Spot-check: every item must have the fields we depend on
    for post in posts:
        assert "id" in post,     "Each post must have an 'id' field"
        assert "title" in post,  "Each post must have a 'title' field"
        assert "body" in post,   "Each post must have a 'body' field"
        assert "userId" in post, "Each post must have a 'userId' field"


# ---------------------------------------------------------------------------
# Test 2 – single-resource validation (GET /posts/1)
# ---------------------------------------------------------------------------
# Scenario: fetch one specific post and validate its exact field values.
# This pattern is useful when you want to pin down a known good record.

def test_get_single_post():
    post_id = 1
    response = requests.get(f"{BASE_URL}/posts/{post_id}")

    # The resource exists so we expect 200
    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    post = response.json()  # parse JSON body into a Python dict

    # Validate the shape — all expected keys must be present
    assert "id" in post
    assert "userId" in post
    assert "title" in post
    assert "body" in post

    # Validate the values — the API is deterministic for known IDs
    assert post["id"] == post_id, (
        f"Expected post id {post_id}, got {post['id']}"
    )
    assert post["userId"] == 1, (
        f"Expected userId 1, got {post['userId']}"
    )

    # Title must be a non-empty string
    assert isinstance(post["title"], str) and len(post["title"]) > 0, (
        "Post title should be a non-empty string"
    )
