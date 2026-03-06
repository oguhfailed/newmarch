#!/usr/bin/env python3
"""
Display free courses available on Coursera using their public API.
Falls back to sample data when the network is unavailable.
"""

import json
import urllib.request
import urllib.parse
import sys


COURSERA_API_URL = "https://api.coursera.org/api/courses.v1"
FIELDS = "name,slug,workload,primaryLanguages"

# Sample data shown when the network is unavailable
SAMPLE_COURSES = [
    {"name": "Machine Learning", "slug": "machine-learning", "workload": "7-10 hours/week", "primaryLanguages": ["en"]},
    {"name": "Python for Everybody", "slug": "python", "workload": "4-6 hours/week", "primaryLanguages": ["en"]},
    {"name": "The Science of Well-Being", "slug": "the-science-of-well-being", "workload": "3-5 hours/week", "primaryLanguages": ["en"]},
    {"name": "Google IT Support", "slug": "google-it-support", "workload": "5-7 hours/week", "primaryLanguages": ["en"]},
    {"name": "Programming for Everybody (Python)", "slug": "python4everybody", "workload": "4-6 hours/week", "primaryLanguages": ["en"]},
    {"name": "Excel Skills for Business", "slug": "excel-skills-business-essentials", "workload": "4-6 hours/week", "primaryLanguages": ["en"]},
    {"name": "Deep Learning Specialization", "slug": "deep-learning", "workload": "8-10 hours/week", "primaryLanguages": ["en"]},
    {"name": "Data Science: Foundations using R", "slug": "data-science-foundations-r", "workload": "5-6 hours/week", "primaryLanguages": ["en"]},
    {"name": "Introduction to HTML5", "slug": "html", "workload": "2-3 hours/week", "primaryLanguages": ["en"]},
    {"name": "Financial Markets", "slug": "financial-markets-global", "workload": "4-6 hours/week", "primaryLanguages": ["en"]},
]


def fetch_free_courses(query="free", limit=20):
    """Fetch free courses from Coursera API."""
    params = {
        "q": "search",
        "query": query,
        "fields": FIELDS,
        "limit": limit,
        "start": 0,
    }
    url = f"{COURSERA_API_URL}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            courses = data.get("elements", [])
            if courses:
                return courses, False  # False = not sample data
    except Exception:
        pass  # Fall through to sample data

    return SAMPLE_COURSES[:limit], True  # True = sample data


def display_courses(courses, is_sample=False):
    """Print course details in a readable format."""
    if not courses:
        print("No courses found.")
        return

    source = "(sample data — network unavailable)" if is_sample else "(live data from Coursera API)"
    print("=" * 62)
    print(f"  FREE COURSES ON COURSERA  [{len(courses)} results]")
    print(f"  {source}")
    print("=" * 62)

    for i, course in enumerate(courses, start=1):
        name = course.get("name", "N/A")
        slug = course.get("slug", "")
        workload = course.get("workload", "N/A")
        languages = ", ".join(course.get("primaryLanguages", [])) or "N/A"
        url = f"https://www.coursera.org/learn/{slug}" if slug else "N/A"

        print(f"\n{i:>2}. {name}")
        print(f"    URL      : {url}")
        print(f"    Workload : {workload}")
        print(f"    Language : {languages}")

    print("\n" + "=" * 62)
    if is_sample:
        print("Tip: Run this script with internet access to get live results.")
        print('     Usage: python3 coursera_free_courses.py [query] [limit]')
        print('     Example: python3 coursera_free_courses.py "data science" 10')


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "free"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    print(f"Fetching free courses on Coursera (query: '{query}')...\n")
    courses, is_sample = fetch_free_courses(query=query, limit=limit)
    display_courses(courses, is_sample=is_sample)


if __name__ == "__main__":
    main()
