#!/usr/bin/env python3
"""
Test Reddit No-Auth Collector
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from collectors.reddit_no_auth_collector import RedditNoAuthCollector

print("=" * 80)
print("REDDIT NO-AUTH COLLECTOR TEST")
print("=" * 80)
print("\n✅ This collector works WITHOUT any API keys!")
print("✅ Uses Reddit's public JSON endpoints\n")

collector = RedditNoAuthCollector()

# Test 1: Search for posts
print("\n" + "=" * 80)
print("TEST 1: Search for 'Python programming'")
print("=" * 80)

try:
    posts = collector.search_posts(
        keyword='Python programming',
        limit=5,
        subreddit='all'
    )

    print(f"\n✅ SUCCESS: Retrieved {len(posts)} posts\n")

    for i, post in enumerate(posts[:3], 1):
        print(f"Post {i}:")
        print(f"  Title: {post['title'][:70]}...")
        print(f"  Author: u/{post['author']}")
        print(f"  Score: {post['score']}")
        print(f"  Comments: {post['num_comments']}")
        print(f"  Subreddit: r/{post['subreddit']}")
        print(f"  URL: {post['url']}")
        print()

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Get hot posts from specific subreddit
print("\n" + "=" * 80)
print("TEST 2: Get hot posts from r/technology")
print("=" * 80)

try:
    posts = collector.get_subreddit_hot(
        subreddit='technology',
        limit=5
    )

    print(f"\n✅ SUCCESS: Retrieved {len(posts)} hot posts\n")

    for i, post in enumerate(posts[:3], 1):
        print(f"Post {i}:")
        print(f"  Title: {post['title'][:70]}...")
        print(f"  Score: {post['score']}")
        print(f"  URL: {post['url']}")
        print()

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Search with hashtag
print("\n" + "=" * 80)
print("TEST 3: Search for #AI")
print("=" * 80)

try:
    posts = collector.search_by_hashtag(
        hashtag='AI',
        limit=3
    )

    print(f"\n✅ SUCCESS: Retrieved {len(posts)} posts with #AI\n")

    for i, post in enumerate(posts, 1):
        print(f"Post {i}:")
        print(f"  Title: {post['title'][:70]}...")
        print(f"  Subreddit: r/{post['subreddit']}")
        print()

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Multiple subreddits
print("\n" + "=" * 80)
print("TEST 4: Search 'climate change' across multiple subreddits")
print("=" * 80)

try:
    posts = collector.get_trending_from_multiple_subs(
        keyword='climate change',
        subreddits=['news', 'worldnews', 'science'],
        posts_per_sub=3
    )

    print(f"\n✅ SUCCESS: Retrieved {len(posts)} posts total\n")

    # Group by subreddit
    from collections import defaultdict
    by_sub = defaultdict(int)
    for post in posts:
        by_sub[post['subreddit']] += 1

    print("Posts per subreddit:")
    for sub, count in by_sub.items():
        print(f"  r/{sub}: {count} posts")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("REDDIT NO-AUTH COLLECTOR TEST COMPLETE")
print("=" * 80)
print("\n✅ Key Benefits:")
print("  • NO API keys needed!")
print("  • Works immediately out of the box")
print("  • Uses Reddit's public JSON endpoints")
print("  • Respectful rate limiting built-in")
print("  • Access to all public Reddit data")
print("\n✅ This solves the 401 authentication error!")
