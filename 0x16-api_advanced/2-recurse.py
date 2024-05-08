#!/usr/bin/python3
"""
Using reddit's API
"""
import requests
after = None

def recurse(subreddit, hot_list=[], after=None):
  """Recursively retrieves titles of all hot articles for a subreddit.

  Args:
      subreddit: The name of the subreddit (without 'r/').
      hot_list: An empty list or list containing previously retrieved titles (default: []).
      after: The value of the 'after' parameter for pagination (default: None).

  Returns:
      A list containing titles of all hot articles or None for invalid subreddits.
  """
  user_agent = {'User-Agent': 'your_app_name 1.0'}  # Replace with your User Agent
  url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
  params = {'after': after, 'limit': 100}  # Limit to 100 posts per request

  response = requests.get(url, params=params, headers=user_agent, allow_redirects=False)

  if response.status_code == 200:
    data = response.json().get('data', {})
    children = data.get('children', [])

    # Extract titles and add to list
    hot_list.extend([post.get('data', {}).get('title') for post in children])

    # Check for next page and recurse if available
    after_data = data.get('after')
    if after_data:
      return recurse(subreddit, hot_list, after_data)  # Recursive call with updated after
    else:
      return hot_list  # No more pages, return complete list
  else:
    return None  # Handle non-200 status codes

# Example usage (assuming 2-main.py exists)
subreddit = sys.argv[1] if len(sys.argv) > 1 else None
if subreddit:
  result = recurse(subreddit)
  if result is not None:
    print(len(result))
  else:
    print("None")
