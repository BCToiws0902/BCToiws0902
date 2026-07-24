import os
import datetime
import time
import requests
from dateutil import relativedelta
from PIL import Image

# Configuration
USER_NAME = "BCToiws0902"
BIRTHDAY = datetime.datetime(2001, 2, 9)
OS_INFO = "windows 11 iot, android 12, Ubuntu server 2019, ios 26"
HOST_INFO = "Home, Military"
KERNEL_INFO = "Admin System"
IDE_INFO = "Vscode, arduino ide, IntelliJ IDEA"
LANG_PROGRAMMING = "Holy Snake, java not java, C with pain, .md developer"
LANG_COMPUTER = "py, json, bat, js, html, css"
LANG_REAL = "Vietnamese, Eye language"
HOBBIES_SOFTWARE = "Scripting, ios jailbreak, mod GUI ubuntu, desktop supermini size"
HOBBIES_HARDWARE = "DIY Speakers, Custom Mechanical Keyboards"
EMAIL_CONTACT = "buicongtoi01@gmail.com"
FACEBOOK_CONTACT = "bct0902"
TELEGRAM_CONTACT = "bct0902"

# SVG Color Themes
THEMES = {
    "dark": {
        "bg_color": "#161b22",
        "text_color": "#c9d1d9",
        "key_color": "#ffa657",
        "value_color": "#a5d6ff",
        "comment_color": "#616e7f",
        "add_color": "#3fb950",
        "del_color": "#f85149",
        "ascii_color": "#c9d1d9",
        "header_color": "#c9d1d9",
    },
    "light": {
        "bg_color": "#f6f8fa",
        "text_color": "#24292f",
        "key_color": "#953800",
        "value_color": "#0550ae",
        "comment_color": "#57606a",
        "add_color": "#116329",
        "del_color": "#cf222e",
        "ascii_color": "#24292f",
        "header_color": "#24292f",
    }
}

SVG_TEMPLATE = """<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="1300px" height="530px" font-size="16px">
<style>
@font-face {{
  src: local('Consolas'), local('Consolas Bold');
  font-family: 'ConsolasFallback';
  font-display: swap;
  -webkit-size-adjust: 109%;
  size-adjust: 109%;
}}
.key {{fill: {key_color};}}
.value {{fill: {value_color};}}
.cc {{fill: {comment_color};}}
.add {{fill: {add_color};}}
.del {{fill: {del_color};}}
.ascii {{fill: {ascii_color};}}
.header {{fill: {header_color}; font-weight: bold;}}
text, tspan {{white-space: pre;}}
</style>
<rect width="1300px" height="530px" fill="{bg_color}" rx="15"/>
<text x="15" y="35" fill="{text_color}">
{content}
</text>
</svg>
"""

def format_plural(unit):
    return 's' if unit != 1 else ''

def calculate_uptime(birthday):
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return '{} {}, {} {}, {} {}{}'.format(
        diff.years, 'year' + format_plural(diff.years), 
        diff.months, 'month' + format_plural(diff.months), 
        diff.days, 'day' + format_plural(diff.days),
        ' 🎂' if (diff.months == 0 and diff.days == 0) else '')

def generate_ascii_art(image_path, width=42, invert=False):
    if not os.path.exists(image_path):
        print(f"Warning: {image_path} not found. Using empty spaces for ASCII.")
        return [" " * width] * 24
        
    try:
        img = Image.open(image_path)
        # Force exactly 24 lines height to align with stats
        height = 24
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img = img.convert("L")
        
        ascii_chars = '@%#*+=-:. '
        if invert:
            ascii_chars = ascii_chars[::-1]
            
        num_chars = len(ascii_chars)
        lines = []
        for y in range(img.height):
            line = ""
            for x in range(img.width):
                gray = img.getpixel((x, y))
                char_idx = int(gray * (num_chars - 1) / 255)
                line += ascii_chars[char_idx]
            lines.append(line)
        return lines
    except Exception as e:
        print(f"Error rendering ASCII from image: {e}")
        return [" " * width] * 24

def get_dots(key_label, total_len=25):
    colon_and_space = ": "
    dot_count = total_len - len(key_label) - len(colon_and_space)
    if dot_count < 0:
        dot_count = 0
    return colon_and_space + ("." * dot_count) + " "

def escape_xml(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def format_svg_line(y, ascii_part, stats_parts=None):
    # Escape characters for XML safety
    escaped_ascii = escape_xml(ascii_part)
    res = f'<tspan x="15" y="{y}" class="ascii">{escaped_ascii}</tspan>'
    
    if stats_parts:
        # First part starts at x=480, y=y
        text, cls = stats_parts[0]
        escaped_text = escape_xml(text)
        res += f'<tspan x="480" y="{y}" class="{cls}">{escaped_text}</tspan>'
        
        # Remaining parts flow horizontally
        for text, cls in stats_parts[1:]:
            escaped_text = escape_xml(text)
            res += f'<tspan class="{cls}">{escaped_text}</tspan>'
            
    return res

def fetch_github_stats():
    token = os.environ.get("ACCESS_TOKEN")
    if not token:
        print("ACCESS_TOKEN environment variable not found. Using mockup stats.")
        return {
            "repos_count": 18,
            "contrib_repos": 4,
            "stars_count": 12,
            "commits_count": 312,
            "followers_count": 5,
            "total_loc": 42750,
            "additions": 52100,
            "deletions": 9350
        }

    headers = {'authorization': 'token ' + token}
    
    # 1. Fetch user data (repos, contributors, followers, join date)
    query_user = """
    query($login: String!) {
      user(login: $login) {
        createdAt
        id
        repositories(first: 100, ownerAffiliations: [OWNER]) {
          totalCount
          nodes {
            name
            stargazers {
              totalCount
            }
            defaultBranchRef {
              target {
                ... on Commit {
                  history(first: 100) {
                    nodes {
                      additions
                      deletions
                      author {
                        user {
                          id
                          login
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
        repositoriesContributedTo(first: 100, contributionTypes: [COMMIT, PULL_REQUEST, ISSUE, REPOSITORY]) {
          totalCount
        }
        followers {
          totalCount
        }
      }
    }
    """
    
    try:
      r = requests.post('https://api.github.com/graphql', json={'query': query_user, 'variables': {'login': USER_NAME}}, headers=headers)
      if r.status_code != 200:
          raise Exception(f"GraphQL request failed: {r.status_code}\n{r.text}")
          
      res_data = r.json()
      if 'errors' in res_data:
          raise Exception(f"GraphQL error: {res_data['errors']}")
          
      user_data = res_data['data']['user']
      user_id = user_data['id']
      created_at = user_data['createdAt']
      join_year = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").year
      
      repos_count = user_data['repositories']['totalCount']
      contrib_repos = user_data['repositoriesContributedTo']['totalCount']
      followers_count = user_data['followers']['totalCount']
      
      # Sum stars and compute estimated lines of code from top 100 repos
      stars_count = 0
      additions = 0
      deletions = 0
      
      for repo in user_data['repositories']['nodes']:
          stars_count += repo['stargazers']['totalCount']
          
          if repo['defaultBranchRef'] and repo['defaultBranchRef']['target']:
              commits = repo['defaultBranchRef']['target']['history']['nodes']
              for commit in commits:
                  # Check if the commit author is the user
                  author_user = commit.get('author', {}).get('user')
                  if author_user and author_user['id'] == user_id:
                      additions += commit['additions']
                      deletions += commit['deletions']
                      
      total_loc = additions - deletions
      if total_loc < 0:
          total_loc = 0
          
      # 2. Get lifetime commit contributions
      commits_count = 0
      current_year = datetime.datetime.today().year
      for year in range(join_year, current_year + 1):
          start_date = f"{year}-01-01T00:00:00Z"
          end_date = f"{year}-12-31T23:59:59Z"
          
          query_commits = """
          query($login: String!, $from: DateTime!, $to: DateTime!) {
            user(login: $login) {
              contributionsCollection(from: $from, to: $to) {
                contributionCalendar {
                  totalContributions
                }
              }
            }
          }
          """
          r_commits = requests.post('https://api.github.com/graphql', 
                                    json={'query': query_commits, 'variables': {'login': USER_NAME, 'from': start_date, 'to': end_date}}, 
                                    headers=headers)
          if r_commits.status_code == 200:
              c_data = r_commits.json()
              try:
                  commits_count += c_data['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
              except Exception:
                  pass
          time.sleep(0.1)
          
      return {
          "repos_count": repos_count,
          "contrib_repos": contrib_repos,
          "stars_count": stars_count,
          "commits_count": commits_count,
          "followers_count": followers_count,
          "total_loc": total_loc,
          "additions": additions,
          "deletions": deletions
      }
      
    except Exception as e:
      print(f"Error fetching stats from API: {e}. Falling back to mock data.")
      return {
          "repos_count": 18,
          "contrib_repos": 4,
          "stars_count": 12,
          "commits_count": 312,
          "followers_count": 5,
          "total_loc": 42750,
          "additions": 52100,
          "deletions": 9350
      }

def build_svg(theme_name, stats, ascii_lines):
    theme = THEMES[theme_name]
    uptime_str = calculate_uptime(BIRTHDAY)
    
    # Define stats structure (exactly 24 lines)
    stats_structure = [
        # Line 0
        [("BCToiws0902", "header"), ("@", "cc"), ("Military", "value"), (" -------------------", "cc")],
        # Line 1
        [("OS", "key"), (get_dots("OS"), "cc"), (OS_INFO, "value")],
        # Line 2
        [("Uptime", "key"), (get_dots("Uptime"), "cc"), (uptime_str, "value")],
        # Line 3
        [("Host", "key"), (get_dots("Host"), "cc"), (HOST_INFO, "value")],
        # Line 4
        [("Kernel", "key"), (get_dots("Kernel"), "cc"), (KERNEL_INFO, "value")],
        # Line 5
        [("IDE", "key"), (get_dots("IDE"), "cc"), (IDE_INFO, "value")],
        # Line 6
        [("", "cc")],
        # Line 7
        [("Languages.Programming", "key"), (get_dots("Languages.Programming"), "cc"), (LANG_PROGRAMMING, "value")],
        # Line 8
        [("Languages.Computer", "key"), (get_dots("Languages.Computer"), "cc"), (LANG_COMPUTER, "value")],
        # Line 9
        [("Languages.Real", "key"), (get_dots("Languages.Real"), "cc"), (LANG_REAL, "value")],
        # Line 10
        [("", "cc")],
        # Line 11
        [("Hobbies.Software", "key"), (get_dots("Hobbies.Software"), "cc"), (HOBBIES_SOFTWARE, "value")],
        # Line 12
        [("Hobbies.Hardware", "key"), (get_dots("Hobbies.Hardware"), "cc"), (HOBBIES_HARDWARE, "value")],
        # Line 13
        [("", "cc")],
        # Line 14
        [("- Contact", "cc")],
        # Line 15
        [("Email.Personal", "key"), (get_dots("Email.Personal"), "cc"), (EMAIL_CONTACT, "value")],
        # Line 16
        [("Facebook", "key"), (get_dots("Facebook"), "cc"), (FACEBOOK_CONTACT, "value")],
        # Line 17
        [("Telegram", "key"), (get_dots("Telegram"), "cc"), (TELEGRAM_CONTACT, "value")],
        # Line 18
        [("", "cc")],
        # Line 19
        [("- GitHub Stats", "cc")],
        # Line 20
        [("Repos", "key"), (": .... ", "cc"), (str(stats["repos_count"]), "value"), 
         (" {Contributed: " + str(stats["contrib_repos"]) + "}", "cc"), (" | Stars", "key"), (": .......... ", "cc"), (str(stats["stars_count"]), "value")],
        # Line 21
        [("Commits", "key"), (": ...................... ", "cc"), (f"{stats['commits_count']:,}", "value"), 
         (" | Followers", "key"), (": ....... ", "cc"), (str(stats["followers_count"]), "value")],
        # Line 22
        [("Lines of Code on GitHub", "key"), (":. ", "cc"), (f"{stats['total_loc']:,}", "value"), 
         (" ( ", "cc"), (f"{stats['additions']:,}++", "add"), (",  ", "cc"), (f"{stats['deletions']:,}--", "del"), (" )", "cc")],
        # Line 23
        [("", "cc")]
    ]
    
    lines_content = []
    for i in range(24):
        y_pos = 35 + i * 21
        ascii_line = ascii_lines[i]
        stats_parts = stats_structure[i] if i < len(stats_structure) else None
        
        line_svg = format_svg_line(y_pos, ascii_line, stats_parts)
        lines_content.append(line_svg)
        
    content = "\n".join(lines_content)
    
    return SVG_TEMPLATE.format(
        bg_color=theme["bg_color"],
        text_color=theme["text_color"],
        key_color=theme["key_color"],
        value_color=theme["value_color"],
        comment_color=theme["comment_color"],
        add_color=theme["add_color"],
        del_color=theme["del_color"],
        ascii_color=theme["ascii_color"],
        header_color=theme["header_color"],
        content=content
    )

def main():
    print("Fetching statistics from GitHub...")
    stats = fetch_github_stats()
    print("GitHub statistics retrieved successfully:")
    print(stats)
    
    image_file = "logobct.png"
    
    # Build Dark Mode SVG
    print("\nGenerating dark_mode.svg...")
    dark_ascii = generate_ascii_art(image_file, width=42, invert=False)
    dark_svg = build_svg("dark", stats, dark_ascii)
    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print("dark_mode.svg saved successfully!")
    
    # Build Light Mode SVG
    print("Generating light_mode.svg...")
    light_ascii = generate_ascii_art(image_file, width=42, invert=True)
    light_svg = build_svg("light", stats, light_ascii)
    with open("light_mode.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("light_mode.svg saved successfully!")

if __name__ == "__main__":
    main()
