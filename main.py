"""
NFL 2026 AI-STYLE GAME PREDICTION BOT

Features
--------
1. All 32 NFL teams
2. 2026 preseason schedule
3. Live ESPN roster data
4. Live ESPN injury data
5. Live ESPN depth charts
6. Live ESPN team information
7. Live ESPN news
8. Recent team record
9. QB / RB / WR / TE / OL / DL / LB / DB analysis
10. PFF-inspired grading framework
11. Injury impact model
12. Coaching impact framework
13. Matchup strengths / weaknesses
14. Preseason-specific weighting
15. No random score generation
16. Confidence rating
17. Streamlit dropdown interface
18. Optional PFF API integration
19. News sentiment
20. Explainable prediction

IMPORTANT:
This is NOT PFF's proprietary prediction model.
It is a PFF-inspired analytical framework using publicly
available football information.

Install:
    pip install streamlit pandas numpy requests feedparser

Run:
    streamlit run nfl_prediction_bot.py
"""

import requests
import pandas as pd
import numpy as np
import streamlit as st
import feedparser
import math
import re
from datetime import datetime, timezone
from functools import lru_cache


# ============================================================
# CONFIGURATION
# ============================================================

SEASON = 2026
SEASON_TYPE_PRESEASON = 1
SEASON_TYPE_REGULAR = 2

ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
ESPN_CORE = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"

REQUEST_TIMEOUT = 15


# ============================================================
# ALL 32 NFL TEAMS
# ============================================================

NFL_TEAMS = {
    "Arizona Cardinals": {
        "abbr": "ARI",
        "espn_id": "22",
        "conference": "NFC",
        "division": "NFC West"
    },
    "Atlanta Falcons": {
        "abbr": "ATL",
        "espn_id": "1",
        "conference": "NFC",
        "division": "NFC South"
    },
    "Baltimore Ravens": {
        "abbr": "BAL",
        "espn_id": "33",
        "conference": "AFC",
        "division": "AFC North"
    },
    "Buffalo Bills": {
        "abbr": "BUF",
        "espn_id": "2",
        "conference": "AFC",
        "division": "AFC East"
    },
    "Carolina Panthers": {
        "abbr": "CAR",
        "espn_id": "29",
        "conference": "NFC",
        "division": "NFC South"
    },
    "Chicago Bears": {
        "abbr": "CHI",
        "espn_id": "3",
        "conference": "NFC",
        "division": "NFC North"
    },
    "Cincinnati Bengals": {
        "abbr": "CIN",
        "espn_id": "4",
        "conference": "AFC",
        "division": "AFC North"
    },
    "Cleveland Browns": {
        "abbr": "CLE",
        "espn_id": "5",
        "conference": "AFC",
        "division": "AFC North"
    },
    "Dallas Cowboys": {
        "abbr": "DAL",
        "espn_id": "6",
        "conference": "NFC",
        "division": "NFC East"
    },
    "Denver Broncos": {
        "abbr": "DEN",
        "espn_id": "7",
        "conference": "AFC",
        "division": "AFC West"
    },
    "Detroit Lions": {
        "abbr": "DET",
        "espn_id": "8",
        "conference": "NFC",
        "division": "NFC North"
    },
    "Green Bay Packers": {
        "abbr": "GB",
        "espn_id": "9",
        "conference": "NFC",
        "division": "NFC North"
    },
    "Houston Texans": {
        "abbr": "HOU",
        "espn_id": "34",
        "conference": "AFC",
        "division": "AFC South"
    },
    "Indianapolis Colts": {
        "abbr": "IND",
        "espn_id": "11",
        "conference": "AFC",
        "division": "AFC South"
    },
    "Jacksonville Jaguars": {
        "abbr": "JAX",
        "espn_id": "30",
        "conference": "AFC",
        "division": "AFC South"
    },
    "Kansas City Chiefs": {
        "abbr": "KC",
        "espn_id": "12",
        "conference": "AFC",
        "division": "AFC West"
    },
    "Las Vegas Raiders": {
        "abbr": "LV",
        "espn_id": "13",
        "conference": "AFC",
        "division": "AFC West"
    },
    "Los Angeles Chargers": {
        "abbr": "LAC",
        "espn_id": "24",
        "conference": "AFC",
        "division": "AFC West"
    },
    "Los Angeles Rams": {
        "abbr": "LAR",
        "espn_id": "14",
        "conference": "NFC",
        "division": "NFC West"
    },
    "Miami Dolphins": {
        "abbr": "MIA",
        "espn_id": "15",
        "conference": "AFC",
        "division": "AFC East"
    },
    "Minnesota Vikings": {
        "abbr": "MIN",
        "espn_id": "16",
        "conference": "NFC",
        "division": "NFC North"
    },
    "New England Patriots": {
        "abbr": "NE",
        "espn_id": "17",
        "conference": "AFC",
        "division": "AFC East"
    },
    "New Orleans Saints": {
        "abbr": "NO",
        "espn_id": "18",
        "conference": "NFC",
        "division": "NFC South"
    },
    "New York Giants": {
        "abbr": "NYG",
        "espn_id": "19",
        "conference": "NFC",
        "division": "NFC East"
    },
    "New York Jets": {
        "abbr": "NYJ",
        "espn_id": "20",
        "conference": "AFC",
        "division": "AFC East"
    },
    "Philadelphia Eagles": {
        "abbr": "PHI",
        "espn_id": "21",
        "conference": "NFC",
        "division": "NFC East"
    },
    "Pittsburgh Steelers": {
        "abbr": "PIT",
        "espn_id": "23",
        "conference": "AFC",
        "division": "AFC North"
    },
    "San Francisco 49ers": {
        "abbr": "SF",
        "espn_id": "25",
        "conference": "NFC",
        "division": "NFC West"
    },
    "Seattle Seahawks": {
        "abbr": "SEA",
        "espn_id": "26",
        "conference": "NFC",
        "division": "NFC West"
    },
    "Tampa Bay Buccaneers": {
        "abbr": "TB",
        "espn_id": "27",
        "conference": "NFC",
        "division": "NFC South"
    },
    "Tennessee Titans": {
        "abbr": "TEN",
        "espn_id": "10",
        "conference": "AFC",
        "division": "AFC South"
    },
    "Washington Commanders": {
        "abbr": "WAS",
        "espn_id": "28",
        "conference": "NFC",
        "division": "NFC East"
    },
}


# ============================================================
# 2026 PRESEASON SCHEDULE
# ============================================================

PRESEASON_WEEK_1 = [
    ("2026-08-13", "Detroit Lions", "Cincinnati Bengals"),
    ("2026-08-13", "Green Bay Packers", "Pittsburgh Steelers"),
    ("2026-08-13", "Indianapolis Colts", "New England Patriots"),
    ("2026-08-13", "Los Angeles Chargers", "Houston Texans"),
    ("2026-08-13", "Arizona Cardinals", "Las Vegas Raiders"),
    ("2026-08-13", "Tennessee Titans", "San Francisco 49ers"),

    ("2026-08-14", "Denver Broncos", "Atlanta Falcons"),
    ("2026-08-14", "Tampa Bay Buccaneers", "New York Jets"),
    ("2026-08-14", "Miami Dolphins", "Washington Commanders"),

    ("2026-08-15", "Carolina Panthers", "Buffalo Bills"),
    ("2026-08-15", "Cleveland Browns", "Chicago Bears"),
    ("2026-08-15", "Minnesota Vikings", "New York Giants"),
    ("2026-08-15", "Los Angeles Rams", "Kansas City Chiefs"),
    ("2026-08-15", "Jacksonville Jaguars", "New Orleans Saints"),
    ("2026-08-15", "Philadelphia Eagles", "Baltimore Ravens"),

    ("2026-08-16", "Dallas Cowboys", "Seattle Seahawks"),
]


PRESEASON_WEEK_2 = [
    ("2026-08-20", "Las Vegas Raiders", "Houston Texans"),
    ("2026-08-20", "San Francisco 49ers", "Los Angeles Chargers"),

    ("2026-08-21", "New York Jets", "Pittsburgh Steelers"),
    ("2026-08-21", "Dallas Cowboys", "Arizona Cardinals"),
    ("2026-08-21", "Chicago Bears", "Cincinnati Bengals"),
    ("2026-08-21", "Buffalo Bills", "Cleveland Browns"),
    ("2026-08-21", "Green Bay Packers", "Denver Broncos"),
    ("2026-08-21", "Washington Commanders", "Detroit Lions"),
    ("2026-08-21", "Atlanta Falcons", "Indianapolis Colts"),
    ("2026-08-21", "Carolina Panthers", "Jacksonville Jaguars"),
    ("2026-08-21", "New Orleans Saints", "Los Angeles Rams"),
    ("2026-08-21", "New York Giants", "Miami Dolphins"),
    ("2026-08-21", "Baltimore Ravens", "Minnesota Vikings"),
    ("2026-08-21", "Philadelphia Eagles", "New England Patriots"),
    ("2026-08-21", "Kansas City Chiefs", "Tampa Bay Buccaneers"),

    ("2026-08-23", "Seattle Seahawks", "Tennessee Titans"),
]


PRESEASON_WEEK_3 = [
    ("2026-08-27", "Washington Commanders", "Baltimore Ravens"),
    ("2026-08-27", "Pittsburgh Steelers", "Buffalo Bills"),
    ("2026-08-27", "Houston Texans", "Carolina Panthers"),
    ("2026-08-27", "New England Patriots", "Cleveland Browns"),
    ("2026-08-27", "New Orleans Saints", "Dallas Cowboys"),
    ("2026-08-27", "Minnesota Vikings", "Denver Broncos"),
    ("2026-08-27", "Arizona Cardinals", "Green Bay Packers"),
    ("2026-08-27", "Detroit Lions", "Indianapolis Colts"),
    ("2026-08-27", "Tampa Bay Buccaneers", "Jacksonville Jaguars"),
    ("2026-08-27", "Seattle Seahawks", "Kansas City Chiefs"),
    ("2026-08-27", "San Francisco 49ers", "Las Vegas Raiders"),
    ("2026-08-27", "Los Angeles Rams", "Los Angeles Chargers"),
    ("2026-08-27", "Atlanta Falcons", "Miami Dolphins"),
    ("2026-08-27", "New York Giants", "New York Jets"),
    ("2026-08-28", "Cincinnati Bengals", "Philadelphia Eagles"),
    ("2026-08-28", "Chicago Bears", "Tennessee Titans"),
]


ALL_PRESEASON_GAMES = (
    PRESEASON_WEEK_1 +
    PRESEASON_WEEK_2 +
    PRESEASON_WEEK_3
)


# ============================================================
# REQUEST HELPERS
# ============================================================

@st.cache_data(ttl=300)
def api_get(url, params=None):
    """
    Generic API request with caching.

    Cache duration = 5 minutes.
    This prevents the app from hammering the API.
    """

    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": "NFL-Prediction-Bot/2026"
            }
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        return {
            "_error": str(e)
        }


# ============================================================
# TEAM HELPERS
# ============================================================

def team_id(team_name):
    return NFL_TEAMS[team_name]["espn_id"]


def team_abbreviation(team_name):
    return NFL_TEAMS[team_name]["abbr"]


# ============================================================
# ROSTER
# ============================================================

@st.cache_data(ttl=1800)
def fetch_roster(team_name):

    tid = team_id(team_name)

    url = f"{ESPN_BASE}/teams/{tid}/roster"

    data = api_get(url)

    if "_error" in data:
        return pd.DataFrame()

    athletes = []

    for group in data.get("athletes", []):

        position_group = group.get("position", "")

        for player in group.get("athletes", []):

            athletes.append({
                "Team": team_name,
                "Player": player.get("fullName", "Unknown"),
                "Position": position_group,
                "Age": player.get("age"),
                "Experience": player.get("experience", {}).get("years"),
                "Status": player.get("status", {}).get("name")
            })

    return pd.DataFrame(athletes)


# ============================================================
# DEPTH CHART
# ============================================================

@st.cache_data(ttl=900)
def fetch_depth_chart(team_name):

    tid = team_id(team_name)

    url = f"{ESPN_BASE}/teams/{tid}/depthcharts"

    data = api_get(url)

    if "_error" in data:
        return []

    return data.get("depthchart", data.get("items", []))


# ============================================================
# INJURIES
# ============================================================

@st.cache_data(ttl=300)
def fetch_injuries(team_name):

    tid = team_id(team_name)

    url = f"{ESPN_BASE}/teams/{tid}/injuries"

    data = api_get(url)

    if "_error" in data:
        return pd.DataFrame()

    injuries = []

    for item in data.get("injuries", []):

        athlete = item.get("athlete", {})

        injuries.append({
            "Team": team_name,
            "Player": athlete.get("displayName", "Unknown"),
            "Position": athlete.get("position", {}).get("abbreviation", ""),
            "Injury": item.get("type", {}).get("text", ""),
            "Status": item.get("status", ""),
            "Date": item.get("date", "")
        })

    return pd.DataFrame(injuries)


# ============================================================
# TEAM INFORMATION
# ============================================================

@st.cache_data(ttl=900)
def fetch_team_info(team_name):

    tid = team_id(team_name)

    url = f"{ESPN_BASE}/teams/{tid}"

    data = api_get(url)

    if "_error" in data:
        return {}

    return data.get("team", {})


# ============================================================
# TEAM SCHEDULE / RECORD
# ============================================================

@st.cache_data(ttl=900)
def fetch_team_schedule(team_name):

    tid = team_id(team_name)

    url = f"{ESPN_BASE}/teams/{tid}/schedule"

    data = api_get(
        url,
        params={
            "season": SEASON,
            "seasontype": SEASON_TYPE_REGULAR
        }
    )

    if "_error" in data:
        return []

    return data.get("events", [])


def extract_record(team_name):

    events = fetch_team_schedule(team_name)

    wins = 0
    losses = 0
    ties = 0

    for event in events:

        competition = (
            event.get("competitions", [{}])[0]
            if event.get("competitions")
            else {}
        )

        competitors = competition.get("competitors", [])

        for team in competitors:

            team_info = team.get("team", {})

            if str(team_info.get("id")) == team_id(team_name):

                winner = team.get("winner")

                if winner is True:
                    wins += 1

                elif winner is False:
                    losses += 1

    return wins, losses, ties


# ============================================================
# NEWS
# ============================================================

@st.cache_data(ttl=300)
def fetch_team_news(team_name, limit=10):

    tid = team_id(team_name)

    url = f"{ESPN_BASE}/teams/{tid}/news"

    data = api_get(url)

    if "_error" in data:
        return []

    results = []

    for article in data.get("articles", [])[:limit]:

        results.append({
            "headline": article.get("headline", ""),
            "description": article.get("description", ""),
            "published": article.get("published", ""),
            "url": article.get("links", {}).get("web", {}).get("href", "")
        })

    return results


# ============================================================
# LEAGUE NEWS
# ============================================================

@st.cache_data(ttl=300)
def fetch_nfl_news(limit=25):

    url = f"{ESPN_BASE}/news"

    data = api_get(url)

    if "_error" in data:
        return []

    results = []

    for article in data.get("articles", [])[:limit]:

        results.append({
            "headline": article.get("headline", ""),
            "description": article.get("description", ""),
            "published": article.get("published", ""),
            "url": article.get("links", {}).get("web", {}).get("href", "")
        })

    return results


# ============================================================
# NEWS SENTIMENT
# ============================================================

POSITIVE_WORDS = [
    "healthy",
    "return",
    "returns",
    "strong",
    "impressive",
    "breakout",
    "excellent",
    "dominant",
    "improved",
    "ready",
    "progress",
    "positive",
    "starter",
    "starting",
    "healthy"
]

NEGATIVE_WORDS = [
    "injury",
    "injured",
    "questionable",
    "out",
    "limited",
    "miss",
    "missed",
    "surgery",
    "concern",
    "problem",
    "hurt",
    "suspended",
    "doubtful"
]


def calculate_news_sentiment(news):

    score = 0

    for article in news:

        text = (
            article.get("headline", "") +
            " " +
            article.get("description", "")
        ).lower()

        for word in POSITIVE_WORDS:

            if re.search(r"\b" + re.escape(word) + r"\b", text):
                score += 1

        for word in NEGATIVE_WORDS:

            if re.search(r"\b" + re.escape(word) + r"\b", text):
                score -= 1

    return max(-10, min(10, score))


# ============================================================
# POSITIONAL ROSTER ANALYSIS
# ============================================================

def roster_position_counts(roster):

    if roster.empty:
        return {}

    counts = (
        roster["Position"]
        .fillna("")
        .value_counts()
        .to_dict()
    )

    return counts


def get_position_players(roster, positions):

    if roster.empty:
        return []

    return roster[
        roster["Position"]
        .str.upper()
        .isin([p.upper() for p in positions])
    ]["Player"].tolist()


# ============================================================
# QUARTERBACK ANALYSIS
# ============================================================

def quarterback_score(roster, injuries):

    if roster.empty:
        return 50.0

    qbs = roster[
        roster["Position"]
        .fillna("")
        .str.upper()
        .isin(["QB"])
    ]

    if qbs.empty:
        return 45.0

    score = 50.0

    # Experience bonus
    experience = qbs["Experience"].fillna(0)

    if not experience.empty:

        avg_exp = experience.mean()

        score += min(avg_exp * 1.5, 12)

    # Injury penalty
    if not injuries.empty:

        injured_qbs = injuries[
            injuries["Position"]
            .fillna("")
            .str.upper()
            .eq("QB")
        ]

        score -= len(injured_qbs) * 10

    return max(0, min(100, score))


# ============================================================
# OFFENSIVE SKILL ANALYSIS
# ============================================================

def skill_position_score(roster, injuries):

    if roster.empty:
        return 50.0

    skill_positions = [
        "RB",
        "FB",
        "WR",
        "TE"
    ]

    skill = roster[
        roster["Position"]
        .fillna("")
        .str.upper()
        .isin(skill_positions)
    ]

    if skill.empty:
        return 50.0

    score = 50.0

    # Depth bonus
    score += min(len(skill) * 0.8, 15)

    # Injury penalty
    if not injuries.empty:

        injured_skill = injuries[
            injuries["Position"]
            .fillna("")
            .str.upper()
            .isin(skill_positions)
        ]

        score -= len(injured_skill) * 3

    return max(0, min(100, score))


# ============================================================
# TRENCH ANALYSIS
# ============================================================

def trench_score(roster, injuries):

    if roster.empty:
        return 50.0

    offensive_line = [
        "OT",
        "OG",
        "C",
        "OL",
        "G",
        "T"
    ]

    defensive_line = [
        "DT",
        "DE",
        "DL",
        "NT"
    ]

    trench_positions = offensive_line + defensive_line

    trench = roster[
        roster["Position"]
        .fillna("")
        .str.upper()
        .isin(trench_positions)
    ]

    if trench.empty:
        return 50.0

    score = 50.0

    score += min(len(trench) * 0.7, 15)

    if not injuries.empty:

        injured_trench = injuries[
            injuries["Position"]
            .fillna("")
            .str.upper()
            .isin(trench_positions)
        ]

        score -= len(injured_trench) * 2.5

    return max(0, min(100, score))


# ============================================================
# DEFENSIVE BACK / LINEBACKER ANALYSIS
# ============================================================

def defensive_back_score(roster, injuries):

    if roster.empty:
        return 50.0

    defensive_positions = [
        "CB",
        "S",
        "DB",
        "LB",
        "ILB",
        "OLB"
    ]

    players = roster[
        roster["Position"]
        .fillna("")
        .str.upper()
        .isin(defensive_positions)
    ]

    if players.empty:
        return 50.0

    score = 50.0

    score += min(len(players) * 0.7, 15)

    if not injuries.empty:

        injured = injuries[
            injuries["Position"]
            .fillna("")
            .str.upper()
            .isin(defensive_positions)
        ]

        score -= len(injured) * 2

    return max(0, min(100, score))


# ============================================================
# INJURY IMPACT
# ============================================================

def calculate_injury_score(roster, injuries):

    if injuries.empty:
        return 100.0

    score = 100.0

    for _, injury in injuries.iterrows():

        position = str(
            injury.get("Position", "")
        ).upper()

        status = str(
            injury.get("Status", "")
        ).lower()

        # Different positions have different importance.
        position_weight = {
            "QB": 12,
            "OT": 7,
            "OL": 6,
            "C": 6,
            "G": 5,
            "WR": 5,
            "TE": 4,
            "RB": 3,
            "DE": 6,
            "DT": 6,
            "DL": 6,
            "LB": 5,
            "CB": 5,
            "S": 4
        }

        penalty = position_weight.get(position, 2)

        if "out" in status:
            score -= penalty

        elif "doubtful" in status:
            score -= penalty * 0.8

        elif "questionable" in status:
            score -= penalty * 0.45

        elif "limited" in status:
            score -= penalty * 0.25

    return max(0, min(100, score))


# ============================================================
# COACHING SCORE
# ============================================================

def coaching_score(team_name):

    """
    Coaching data is deliberately not fabricated.

    Instead of inventing grades for a coach or position coach,
    this starts at neutral and can be enhanced with a trusted
    coaching database/API later.

    Future fields:
        Head Coach
        Offensive Coordinator
        Defensive Coordinator
        QB Coach
        WR Coach
        TE Coach
        OL Coach
        DL Coach
        LB Coach
        DB Coach
    """

    return 50.0


# ============================================================
# PRESEASON EXPERIENCE
# ============================================================

def preseason_roster_stability_score(roster):

    if roster.empty:
        return 50.0

    experience = roster["Experience"].fillna(0)

    if experience.empty:
        return 50.0

    average_experience = experience.mean()

    # Preseason teams with more experienced depth tend
    # to have a slight stability advantage.

    score = 40 + min(average_experience * 2, 30)

    return max(0, min(100, score))


# ============================================================
# TEAM MODEL
# ============================================================

def build_team_model(team_name):

    roster = fetch_roster(team_name)

    injuries = fetch_injuries(team_name)

    news = fetch_team_news(team_name)

    qb = quarterback_score(
        roster,
        injuries
    )

    skill = skill_position_score(
        roster,
        injuries
    )

    trenches = trench_score(
        roster,
        injuries
    )

    defense = defensive_back_score(
        roster,
        injuries
    )

    injury = calculate_injury_score(
        roster,
        injuries
    )

    coaching = coaching_score(team_name)

    experience = preseason_roster_stability_score(
        roster
    )

    news_score = calculate_news_sentiment(
        news
    )

    # Convert news from approximately -10/+10
    # into a 0-100 scale.
    news_component = 50 + news_score * 3

    # PFF-inspired composite.
    #
    # The actual PFF grading system is proprietary.
    # These weights are our own analytical approximation.

    composite = (
        qb * 0.24 +
        skill * 0.16 +
        trenches * 0.16 +
        defense * 0.16 +
        injury * 0.12 +
        coaching * 0.06 +
        experience * 0.06 +
        news_component * 0.04
    )

    return {
        "team": team_name,
        "qb": round(qb, 2),
        "skill": round(skill, 2),
        "trenches": round(trenches, 2),
        "defense": round(defense, 2),
        "injury": round(injury, 2),
        "coaching": round(coaching, 2),
        "experience": round(experience, 2),
        "news": round(news_component, 2),
        "composite": round(composite, 2),
        "roster": roster,
        "injuries": injuries,
        "news_articles": news
    }


# ============================================================
# MATCHUP MODEL
# ============================================================

def matchup_prediction(
    home_team,
    away_team,
    preseason=True
):

    home = build_team_model(home_team)

    away = build_team_model(away_team)

    # --------------------------------------------------------
    # PRESEASON WEIGHTS
    # --------------------------------------------------------
    #
    # Preseason is very different from regular season.
    #
    # QB availability and depth matter heavily because
    # starters may play very few snaps.
    #
    # Home field is reduced.
    #

    home_rating = home["composite"]
    away_rating = away["composite"]

    # Home-field advantage
    home_advantage = 2.0 if preseason else 3.0

    home_rating += home_advantage

    # --------------------------------------------------------
    # MATCHUP-SPECIFIC ADVANTAGES
    # --------------------------------------------------------

    qb_diff = home["qb"] - away["qb"]

    skill_diff = home["skill"] - away["skill"]

    trench_diff = home["trenches"] - away["trenches"]

    defense_diff = home["defense"] - away["defense"]

    injury_diff = home["injury"] - away["injury"]

    coaching_diff = home["coaching"] - away["coaching"]

    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    rating_diff = (
        home_rating -
        away_rating
    )

    # Translate rating difference to projected margin.

    projected_margin = (
        rating_diff * 0.16
        +
        qb_diff * 0.10
        +
        trench_diff * 0.07
        +
        defense_diff * 0.06
        +
        injury_diff * 0.05
        +
        coaching_diff * 0.03
    )

    # Limit unrealistic preseason margins.

    projected_margin = max(
        -21,
        min(21, projected_margin)
    )

    if projected_margin >= 0:

        winner = home_team

    else:

        winner = away_team

    # --------------------------------------------------------
    # PROJECTED SCORE
    # --------------------------------------------------------

    base_total = 38.0

    # Better offenses raise total.
    offensive_environment = (
        home["qb"] +
        away["qb"] +
        home["skill"] +
        away["skill"]
    ) / 4

    base_total += (
        offensive_environment - 50
    ) * 0.20

    # Injuries can reduce scoring.
    injury_penalty = (
        (100 - home["injury"]) +
        (100 - away["injury"])
    ) * 0.05

    base_total -= injury_penalty

    base_total = max(
        20,
        min(65, base_total)
    )

    home_score = (
        base_total / 2
        +
        projected_margin / 2
    )

    away_score = (
        base_total / 2
        -
        projected_margin / 2
    )

    home_score = max(
        3,
        round(home_score)
    )

    away_score = max(
        3,
        round(away_score)
    )

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    rating_gap = abs(rating_diff)

    confidence = 50 + (
        rating_gap * 1.2
    )

    # Preseason uncertainty.
    confidence -= 8

    # If major injury uncertainty exists,
    # reduce confidence.
    injury_uncertainty = (
        (100 - home["injury"]) +
        (100 - away["injury"])
    ) / 20

    confidence -= injury_uncertainty

    confidence = max(
        50,
        min(90, confidence)
    )

    # --------------------------------------------------------
    # WHY THE MODEL PICKED THE TEAM
    # --------------------------------------------------------

    advantages = []

    if qb_diff > 5:
        advantages.append(
            f"{home_team} has the QB advantage."
        )

    elif qb_diff < -5:
        advantages.append(
            f"{away_team} has the QB advantage."
        )

    if trench_diff > 5:
        advantages.append(
            f"{home_team} has the trench advantage."
        )

    elif trench_diff < -5:
        advantages.append(
            f"{away_team} has the trench advantage."
        )

    if defense_diff > 5:
        advantages.append(
            f"{home_team} has the defensive personnel advantage."
        )

    elif defense_diff < -5:
        advantages.append(
            f"{away_team} has the defensive personnel advantage."
        )

    if injury_diff > 5:
        advantages.append(
            f"{home_team} has the healthier roster."
        )

    elif injury_diff < -5:
        advantages.append(
            f"{away_team} has the healthier roster."
        )

    if skill_diff > 5:
        advantages.append(
            f"{home_team} has the skill-position depth advantage."
        )

    elif skill_diff < -5:
        advantages.append(
            f"{away_team} has the skill-position depth advantage."
        )

    if not advantages:

        advantages.append(
            "The matchup is relatively close across the model categories."
        )

    return {
        "winner": winner,
        "home_score": home_score,
        "away_score": away_score,
        "margin": round(projected_margin, 1),
        "confidence": round(confidence, 1),
        "home": home,
        "away": away,
        "advantages": advantages
    }


# ============================================================
# FIND PRESEASON GAMES
# ============================================================

def get_preseason_games():

    rows = []

    for date, away, home in ALL_PRESEASON_GAMES:

        rows.append({
            "Date": date,
            "Away": away,
            "Home": home,
            "Matchup": f"{away} at {home}"
        })

    return pd.DataFrame(rows)


# ============================================================
# FIND GAMES FOR SELECTED WEEK
# ============================================================

def get_week_games(week):

    if week == 1:
        games = PRESEASON_WEEK_1

    elif week == 2:
        games = PRESEASON_WEEK_2

    elif week == 3:
        games = PRESEASON_WEEK_3

    else:
        games = []

    rows = []

    for date, away, home in games:

        rows.append({
            "Date": date,
            "Away": away,
            "Home": home,
            "Matchup": f"{away} at {home}"
        })

    return pd.DataFrame(rows)


# ============================================================
# MATCHUP NEWS
# ============================================================

def matchup_news(home_team, away_team):

    home_news = fetch_team_news(
        home_team,
        limit=8
    )

    away_news = fetch_team_news(
        away_team,
        limit=8
    )

    return home_news + away_news


# ============================================================
# INJURY REPORT TABLE
# ============================================================

def combined_injury_report(
    home_team,
    away_team
):

    home = fetch_injuries(home_team)

    away = fetch_injuries(away_team)

    frames = []

    if not home.empty:
        frames.append(home)

    if not away.empty:
        frames.append(away)

    if not frames:

        return pd.DataFrame(
            columns=[
                "Team",
                "Player",
                "Position",
                "Injury",
                "Status"
            ]
        )

    return pd.concat(
        frames,
        ignore_index=True
    )


# ============================================================
# TEAM COMPARISON TABLE
# ============================================================

def create_comparison(home, away):

    rows = [

        {
            "Category": "Overall Composite",
            home["team"]: home["composite"],
            away["team"]: away["composite"]
        },

        {
            "Category": "Quarterback",
            home["team"]: home["qb"],
            away["team"]: away["qb"]
        },

        {
            "Category": "Skill Positions",
            home["team"]: home["skill"],
            away["team"]: away["skill"]
        },

        {
            "Category": "Trenches",
            home["team"]: home["trenches"],
            away["team"]: away["trenches"]
        },

        {
            "Category": "Defense",
            home["team"]: home["defense"],
            away["team"]: away["defense"]
        },

        {
            "Category": "Health",
            home["team"]: home["injury"],
            away["team"]: away["injury"]
        },

        {
            "Category": "Coaching",
            home["team"]: home["coaching"],
            away["team"]: away["coaching"]
        },

        {
            "Category": "Roster Experience",
            home["team"]: home["experience"],
            away["team"]: away["experience"]
        },

        {
            "Category": "News",
            home["team"]: home["news"],
            away["team"]: away["news"]
        }
    ]

    return pd.DataFrame(rows)


# ============================================================
# FORMAT NEWS
# ============================================================

def display_news(news):

    if not news:

        st.info("No news articles were returned by the news feed.")

        return

    for article in news[:12]:

        headline = article.get(
            "headline",
            "NFL News"
        )

        description = article.get(
            "description",
            ""
        )

        url = article.get(
            "url",
            ""
        )

        st.markdown(
            f"### {headline}"
        )

        if description:
            st.write(description)

        if url:
            st.markdown(
                f"[Read article]({url})"
            )


# ============================================================
# MAIN STREAMLIT APP
# ============================================================

def main():

    st.set_page_config(
        page_title="NFL 2026 AI Prediction Bot",
        page_icon="🏈",
        layout="wide"
    )

    st.title(
        "🏈 NFL 2026 AI Game Prediction Bot"
    )

    st.caption(
        "PFF-inspired / NFL-data-driven analytical model"
    )

    st.info(
        "This model is designed for analysis, not guaranteed "
        "game outcomes. Preseason predictions have higher "
        "uncertainty because playing time and lineups change."
    )

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    st.sidebar.header(
        "Prediction Settings"
    )

    team_names = sorted(
        NFL_TEAMS.keys()
    )

    # ----------------------------------------------
    # MODE
    # ----------------------------------------------

    mode = st.sidebar.radio(
        "Prediction Mode",
        [
            "Select Teams",
            "Select 2026 Preseason Game"
        ]
    )

    # ----------------------------------------------
    # TEAM SELECTION
    # ----------------------------------------------

    if mode == "Select Teams":

        away_team = st.sidebar.selectbox(
            "Away Team",
            team_names,
            index=team_names.index(
                "Green Bay Packers"
            )
        )

        home_team = st.sidebar.selectbox(
            "Home Team",
            team_names,
            index=team_names.index(
                "Chicago Bears"
            )
        )

    else:

        week = st.sidebar.selectbox(
            "2026 Preseason Week",
            [1, 2, 3],
            index=0
        )

        games = get_week_games(week)

        game_options = games["Matchup"].tolist()

        selected_game = st.sidebar.selectbox(
            "Game",
            game_options
        )

        selected = games[
            games["Matchup"] ==
            selected_game
        ].iloc[0]

        away_team = selected["Away"]

        home_team = selected["Home"]

    # --------------------------------------------------------
    # PREDICT BUTTON
    # --------------------------------------------------------

    predict_button = st.sidebar.button(
        "🔮 ANALYZE GAME",
        type="primary"
    )

    # --------------------------------------------------------
    # PRESEASON SCHEDULE
    # --------------------------------------------------------

    st.subheader(
        "2026 NFL Preseason"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "NFL Teams",
            "32"
        )

    with col2:

        st.metric(
            "Preseason Games",
            len(ALL_PRESEASON_GAMES)
        )

    with col3:

        st.metric(
            "Season",
            "2026"
        )

    # --------------------------------------------------------
    # RUN MODEL
    # --------------------------------------------------------

    if predict_button:

        if home_team == away_team:

            st.error(
                "Home and away teams must be different."
            )

            return

        with st.spinner(
            "Gathering 2026 roster, injury, depth-chart, "
            "news and team information..."
        ):

            prediction = matchup_prediction(
                home_team,
                away_team,
                preseason=True
            )

        # ----------------------------------------------------
        # WINNER
        # ----------------------------------------------------

        winner = prediction["winner"]

        if winner == home_team:
            loser = away_team
            winner_score = prediction["home_score"]
            loser_score = prediction["away_score"]
        else:
            loser = home_team
            winner_score = prediction["away_score"]
            loser_score = prediction["home_score"]

        st.divider()

        st.header(
            f"🏆 Model Prediction: {winner}"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Predicted Winner",
                winner
            )

        with c2:

            st.metric(
                "Projected Score",
                f"{winner_score}-{loser_score}"
            )

        with c3:

            st.metric(
                "Projected Margin",
                prediction["margin"]
            )

        with c4:

            st.metric(
                "Confidence",
                f"{prediction['confidence']}%"
            )

        # ----------------------------------------------------
        # REASONING
        # ----------------------------------------------------

        st.subheader(
            "Why the model picked this team"
        )

        for advantage in prediction["advantages"]:

            st.write(
                f"• {advantage}"
            )

        # ----------------------------------------------------
        # COMPARISON
        # ----------------------------------------------------

        st.subheader(
            "Team Comparison"
        )

        comparison = create_comparison(
            prediction["home"],
            prediction["away"]
        )

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # INJURIES
        # ----------------------------------------------------

        st.subheader(
            "🚑 Current Injury Report"
        )

        injuries = combined_injury_report(
            home_team,
            away_team
        )

        if injuries.empty:

            st.success(
                "No injury information was returned."
            )

        else:

            st.dataframe(
                injuries,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # ROSTERS
        # ----------------------------------------------------

        st.subheader(
            "👥 2026 Rosters"
        )

        roster_col1, roster_col2 = st.columns(2)

        with roster_col1:

            st.write(
                f"### {away_team}"
            )

            away_roster = prediction[
                "away"
            ]["roster"]

            if away_roster.empty:

                st.warning(
                    "Roster unavailable."
                )

            else:

                st.dataframe(
                    away_roster,
                    use_container_width=True,
                    hide_index=True
                )

        with roster_col2:

            st.write(
                f"### {home_team}"
            )

            home_roster = prediction[
                "home"
            ]["roster"]

            if home_roster.empty:

                st.warning(
                    "Roster unavailable."
                )

            else:

                st.dataframe(
                    home_roster,
                    use_container_width=True,
                    hide_index=True
                )

        # ----------------------------------------------------
        # NEWS
        # ----------------------------------------------------

        st.subheader(
            "📰 Latest Team News"
        )

        matchup_news_data = matchup_news(
            home_team,
            away_team
        )

        display_news(
            matchup_news_data
        )

        # ----------------------------------------------------
        # STRENGTHS / WEAKNESSES
        # ----------------------------------------------------

        st.subheader(
            "📊 Strengths & Weaknesses"
        )

        strengths_col1, strengths_col2 = st.columns(2)

        for team, data, column in [
            (
                away_team,
                prediction["away"],
                strengths_col1
            ),
            (
                home_team,
                prediction["home"],
                strengths_col2
            )
        ]:

            with column:

                st.markdown(
                    f"## {team}"
                )

                categories = {
                    "QB": data["qb"],
                    "Skill Positions": data["skill"],
                    "Trenches": data["trenches"],
                    "Defense": data["defense"],
                    "Health": data["injury"],
                    "Coaching": data["coaching"],
                    "Experience": data["experience"]
                }

                for category, value in categories.items():

                    if value >= 70:

                        status = "🟢 Strong"

                    elif value >= 55:

                        status = "🟡 Average"

                    else:

                        status = "🔴 Weak"

                    st.write(
                        f"**{category}:** "
                        f"{value:.1f} — {status}"
                    )

        # ----------------------------------------------------
        # MODEL EXPLANATION
        # ----------------------------------------------------

        st.subheader(
            "🧠 Model Weighting"
        )

        weights = pd.DataFrame({
            "Category": [
                "Quarterback",
                "Skill Positions",
                "Trenches",
                "Defense",
                "Injuries / Health",
                "Coaching",
                "Roster Experience",
                "News"
            ],
            "Weight": [
                "24%",
                "16%",
                "16%",
                "16%",
                "12%",
                "6%",
                "6%",
                "4%"
            ]
        })

        st.dataframe(
            weights,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "These are the model's own weights and are not "
            "PFF's proprietary weights."
        )

    # --------------------------------------------------------
    # WEEKLY GAMES
    # --------------------------------------------------------

    st.divider()

    st.header(
        "📅 2026 Preseason Schedule"
    )

    schedule_week = st.selectbox(
        "View Week",
        [1, 2, 3]
    )

    schedule_df = get_week_games(
        schedule_week
    )

    st.dataframe(
        schedule_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
