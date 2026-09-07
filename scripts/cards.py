#!/usr/bin/env python3
"""
Card Generator: Creates SVG project cards, skill radar, and stats from GitHub API.
"""

import json
import os
import requests
from github import Github
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# GitHub API Setup
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)
user = g.get_user()

# Load configurations
with open("assets/projects.json") as f:
    projects = json.load(f)

with open("assets/skills.json") as f:
    skills = json.load(f)

def fetch_repo_stats(repo_path):
    """Fetch repository stats from GitHub API."""
    try:
        repo = g.get_repo(repo_path)
        return {
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language or "Unknown",
            "description": repo.description or ""
        }
    except Exception as e:
        print(f"Error fetching {repo_path}: {e}")
        return {"stars": 0, "forks": 0, "language": "Unknown", "description": ""}

def generate_project_card(project, theme="dark"):
    """Generate SVG card for a project."""
    stats = fetch_repo_stats(project["repo"])
    
    bg_color = "#1e1e2e" if theme == "dark" else "#ffffff"
    text_color = "#ffffff" if theme == "dark" else "#000000"
    accent_color = "#a78bfa"
    border_color = "#3d3d5c" if theme == "dark" else "#e0e0e0"
    
    svg = f"""<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="200" fill="{bg_color}" stroke="{border_color}" stroke-width="2" rx="8"/>
  <text x="20" y="40" font-size="20" font-weight="bold" fill="{accent_color}">{project['name']}</text>
  <text x="20" y="70" font-size="13" fill="{text_color}">{project['description']}</text>
  <text x="20" y="100" font-size="11" fill="{text_color}">⭐ {stats['stars']} | 🍴 {stats['forks']} | 🔤 {stats['language']}</text>
  <g>
"""
    
    y_offset = 120
    for tag in project["tags"][:4]:
        svg += f'  <rect x="20" y="{y_offset}" width="80" height="20" rx="3" fill="{accent_color}" opacity="0.2"/>' 
        svg += f'  <text x="25" y="{y_offset + 14}" font-size="10" fill="{accent_color}">{tag}</text>'
        y_offset += 25
    
    svg += """  </g>
</svg>"""
    
    return svg

def generate_skill_radar(theme="dark"):
    """Generate skill radar chart SVG."""
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    categories = list(skills.keys())
    values = list(skills.values())
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    
    bg_color = "#1e1e2e" if theme == "dark" else "#ffffff"
    text_color = "#ffffff" if theme == "dark" else "#000000"
    line_color = "#a78bfa"
    
    ax.plot(angles, values, 'o-', linewidth=2, color=line_color, label="Skills")
    ax.fill(angles, values, alpha=0.25, color=line_color)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=9, color=text_color)
    ax.set_ylim(0, 100)
    ax.set_facecolor(bg_color)
    fig.patch.set_facecolor(bg_color)
    ax.grid(color=line_color, alpha=0.3)
    
    filename = f"assets/radar-{theme}.svg"
    plt.savefig(filename, format="svg", bbox_inches="tight", facecolor=bg_color)
    plt.close()
    print(f"Generated: {filename}")

def generate_stats_card(theme="dark"):
    """Generate GitHub stats card."""
    repos = user.get_repos()
    total_stars = sum(repo.stargazers_count for repo in repos)
    total_repos = user.public_repos
    
    bg_color = "#1e1e2e" if theme == "dark" else "#ffffff"
    text_color = "#ffffff" if theme == "dark" else "#000000"
    accent_color = "#a78bfa"
    border_color = "#3d3d5c" if theme == "dark" else "#e0e0e0"
    
    svg = f"""<svg width="400" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="150" fill="{bg_color}" stroke="{border_color}" stroke-width="2" rx="8"/>
  <text x="20" y="40" font-size="22" font-weight="bold" fill="{accent_color}">GitHub Stats</text>
  <text x="20" y="80" font-size="16" fill="{text_color}">Repositories: {total_repos}</text>
  <text x="20" y="110" font-size="16" fill="{text_color}">Total Stars: ⭐ {total_stars}</text>
</svg>"""
    
    filename = f"assets/card-stats-{theme}.svg"
    with open(filename, "w") as f:
        f.write(svg)
    print(f"Generated: {filename}")

# Main execution
if __name__ == "__main__":
    print("🎨 Generating project cards...")
    for project in projects:
        for theme in ["dark", "light"]:
            svg = generate_project_card(project, theme)
            filename = f"assets/card-{project['name'].lower()}-{theme}.svg"
            with open(filename, "w") as f:
                f.write(svg)
            print(f"Generated: {filename}")
    
    print("\n📊 Generating skill radar...")
    for theme in ["dark", "light"]:
        generate_skill_radar(theme)
    
    print("\n📈 Generating stats card...")
    for theme in ["dark", "light"]:
        generate_stats_card(theme)
    
    print("\n✅ Card generation complete!")
