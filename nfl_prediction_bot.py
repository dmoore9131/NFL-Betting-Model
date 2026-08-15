# ============================================================
# NFL 2026 ADVANCED GAME PREDICTION BOT
# ============================================================
#
# Based on the user's original NFL prediction program.
#
# FEATURES
# ------------------------------------------------------------
# * All 32 NFL teams
# * Team dropdowns
# * 2026 preseason schedule
# * Historical game framework
# * Player statistics
# * Favorite targets
# * Injury reports
# * Advanced statistics
# * PFF-style grading framework
# * Defensive statistics
# * Coaching evaluation
# * QB evaluation
# * Offensive skill evaluation
# * Offensive line evaluation
# * Defensive line evaluation
# * Secondary evaluation
# * Experience/depth evaluation
# * Preseason adjustments
# * News evaluation
# * Quantitative matchup model
# * AI NFL Analyst Agent
# * AI web research
# * Confidence score
# * Upset warning
# * CSV export
#
# IMPORTANT:
# This program does NOT claim to reproduce proprietary PFF/NFL
# formulas. It creates a PFF/NFL-inspired analytical framework.
#
# ============================================================

import os
import json
import random
from datetime import datetime

import pandas as pd
import streamlit as st


# ============================================================
# OPTIONAL OPENAI AGENTS SDK
# ============================================================

try:
    from agents import Agent, Runner, function_tool
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False


# ============================================================
# CONFIGURATION
# ============================================================

APP_TITLE = "NFL 2026 AI Game Prediction System"

OPENAI_MODEL = os.getenv(
    "NFL_AI_MODEL",
    "gpt-5.6-sol"
)


# ============================================================
# ALL 32 NFL TEAMS
# ============================================================

NFL_TEAMS = [
    "Arizona Cardinals",
    "Atlanta Falcons",
    "Baltimore Ravens",
    "Buffalo Bills",
    "Carolina Panthers",
    "Chicago Bears",
    "Cincinnati Bengals",
    "Cleveland Browns",
    "Dallas Cowboys",
    "Denver Broncos",
    "Detroit Lions",
    "Green Bay Packers",
    "Houston Texans",
    "Indianapolis Colts",
    "Jacksonville Jaguars",
    "Kansas City Chiefs",
    "Las Vegas Raiders",
    "Los Angeles Chargers",
    "Los Angeles Rams",
    "Miami Dolphins",
    "Minnesota Vikings",
    "New England Patriots",
    "New Orleans Saints",
    "New York Giants",
    "New York Jets",
    "Philadelphia Eagles",
    "Pittsburgh Steelers",
    "San Francisco 49ers",
    "Seattle Seahawks",
    "Tampa Bay Buccaneers",
    "Tennessee Titans",
    "Washington Commanders",
]


# ============================================================
# TEAM ABBREVIATIONS
# ============================================================

TEAM_ABBREVIATIONS = {

    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS",
}


# ============================================================
# 2026 PRESEASON SCHEDULE
# ============================================================
#
# Keep this structure separate from the prediction engine so
# it can be replaced with a live NFL schedule/API later.
#
# ============================================================

PRESEASON_2026 = [

    {
        "Date": "2026-08-13",
        "Away": "Cincinnati Bengals",
        "Home": "Philadelphia Eagles",
    },

    {
        "Date": "2026-08-14",
        "Away": "Detroit Lions",
        "Home": "Miami Dolphins",
    },

    {
        "Date": "2026-08-14",
        "Away": "New York Jets",
        "Home": "Arizona Cardinals",
    },

    {
        "Date": "2026-08-14",
        "Away": "Green Bay Packers",
        "Home": "Indianapolis Colts",
    },

    {
        "Date": "2026-08-15",
        "Away": "Cleveland Browns",
        "Home": "Chicago Bears",
    },

    {
        "Date": "2026-08-15",
        "Away": "Buffalo Bills",
        "Home": "Carolina Panthers",
    },

    {
        "Date": "2026-08-15",
        "Away": "New England Patriots",
        "Home": "Tampa Bay Buccaneers",
    },

    {
        "Date": "2026-08-15",
        "Away": "Pittsburgh Steelers",
        "Home": "Jacksonville Jaguars",
    },

    {
        "Date": "2026-08-15",
        "Away": "Tennessee Titans",
        "Home": "Atlanta Falcons",
    },

    {
        "Date": "2026-08-15",
        "Away": "Minnesota Vikings",
        "Home": "Houston Texans",
    },

    {
        "Date": "2026-08-15",
        "Away": "Kansas City Chiefs",
        "Home": "Arizona Cardinals",
    },

    {
        "Date": "2026-08-16",
        "Away": "Dallas Cowboys",
        "Home": "Los Angeles Rams",
    },

]


# ============================================================
# TEAM BASELINE DATA
# ============================================================
#
# These are model placeholders / priors.
#
# They should eventually be replaced automatically with
# current 2026 statistics.
#
# IMPORTANT:
# Do not represent these as official PFF grades.
#
# ============================================================

def create_team_baseline(team):

    # Neutral baseline.
    # Every team starts at 70 and can be adjusted by live data.

    return {

        "Team": team,

        "QB Grade": 70.0,

        "RB Grade": 70.0,

        "WR Grade": 70.0,

        "TE Grade": 70.0,

        "OL Grade": 70.0,

        "DL Grade": 70.0,

        "LB Grade": 70.0,

        "CB Grade": 70.0,

        "S Grade": 70.0,

        "Offensive Grade": 70.0,

        "Defensive Grade": 70.0,

        "Coaching Grade": 70.0,

        "Experience Grade": 70.0,

        "Depth Grade": 70.0,

        "Health Grade": 70.0,

        "News Grade": 70.0,

        "EPA": 0.0,

        "YPP": 5.0,

        "YPC": 4.2,

        "Pass YPA": 7.0,

        "Pass EPA": 0.0,

        "Rush EPA": 0.0,

        "Pressure Rate": 0.20,

        "Sacks": 0,

        "Interceptions": 0,

        "Turnover Margin": 0,

    }


def fetch_team_baselines():

    rows = []

    for team in NFL_TEAMS:
        rows.append(
            create_team_baseline(team)
        )

    return pd.DataFrame(rows)


# ============================================================
# ORIGINAL FUNCTION:
# fetch_historical_game_data()
# ============================================================

def fetch_historical_game_data(
    home_team=None,
    away_team=None
):

    if home_team is None:
        home_team = "San Francisco 49ers"

    if away_team is None:
        away_team = "New York Jets"

    data = {

        "Game": [
            f"{home_team} vs {away_team}"
        ],

        "Home Team": [
            home_team
        ],

        "Away Team": [
            away_team
        ]
    }

    return pd.DataFrame(data)


# ============================================================
# ORIGINAL FUNCTION:
# fetch_player_stats()
# ============================================================

def fetch_player_stats(
    home_team=None,
    away_team=None
):

    if home_team is None:
        home_team = "San Francisco 49ers"

    if away_team is None:
        away_team = "New York Jets"

    data = {

        "Team": [
            home_team,
            away_team
        ],

        "Player": [
            "Current Starting QB",
            "Current Starting QB"
        ],

        "Position": [
            "QB",
            "QB"
        ],

        "Yards": [
            0,
            0
        ],

        "Touchdowns": [
            0,
            0
        ]
    }

    return pd.DataFrame(data)


# ============================================================
# ORIGINAL FUNCTION:
# fetch_favorite_targets()
# ============================================================

def fetch_favorite_targets(
    home_team=None,
    away_team=None
):

    if home_team is None:
        home_team = "San Francisco 49ers"

    if away_team is None:
        away_team = "New York Jets"

    data = {

        "Team": [
            home_team,
            away_team
        ],

        "Favorite Target": [
            "Primary WR / TE",
            "Primary WR / TE"
        ],

        "Target Stats (Yards)": [
            0,
            0
        ],

        "Target Stats (Receptions)": [
            0,
            0
        ],

        "Target Stats (TDs)": [
            0,
            0
        ]
    }

    return pd.DataFrame(data)


# ============================================================
# ORIGINAL FUNCTION:
# fetch_injury_reports()
# ============================================================

def fetch_injury_reports(
    home_team=None,
    away_team=None
):

    if home_team is None:
        home_team = "San Francisco 49ers"

    if away_team is None:
        away_team = "New York Jets"

    data = {

        "Team": [
            home_team,
            away_team
        ],

        "Player": [
            "No live injury data",
            "No live injury data"
        ],

        "Injury": [
            "Data required",
            "Data required"
        ],

        "Status": [
            "Unknown",
            "Unknown"
        ]
    }

    return pd.DataFrame(data)


# ============================================================
# ORIGINAL FUNCTION:
# advanced_stats()
# ============================================================

def advanced_stats(
    home_team=None,
    away_team=None
):

    if home_team is None:
        home_team = "San Francisco 49ers"

    if away_team is None:
        away_team = "New York Jets"

    data = {

        "Team": [
            home_team,
            away_team
        ],

        "YPP": [
            5.0,
            5.0
        ],

        "EPA": [
            0.0,
            0.0
        ],

        "YPC": [
            4.2,
            4.2
        ],

        "Pass YPA": [
            7.0,
            7.0
        ],

        "Pass EPA": [
            0.0,
            0.0
        ],

        "Rush YPA": [
            4.2,
            4.2
        ],

        "Pressure Rate": [
            0.20,
            0.20
        ]
    }

    return pd.DataFrame(data)


# ============================================================
# ORIGINAL FUNCTION:
# fetch_pff_data()
# ============================================================

def fetch_pff_data(
    home_team=None,
    away_team=None
):

    if home_team is None:
        home_team = "San Francisco 49ers"

    if away_team is None:
        away_team = "New York Jets"

    data = {

        "Team": [
            home_team,
            away_team
        ],

        # PFF-style framework, NOT official PFF grades.
        "Offensive Grade": [
            70,
            70
        ],

        "Defensive Grade": [
            70,
            70
        ],

        "Pass Blocking Grade": [
            70,
            70
        ],

        "Run Blocking Grade": [
            70,
            70
        ],

        "Pass Rush Grade": [
            70,
            70
        ],

        "Coverage Grade": [
            70,
            70
        ]
    }

    return pd.DataFrame(data)


# ============================================================
# ORIGINAL FUNCTION:
# fetch_external_predictions()
# ============================================================

def fetch_external_predictions(
    home_team=None,
    away_team=None
):

    if home_team is None:
        home_team = "San Francisco 49ers"

    if away_team is None:
        away_team = "New York Jets"

    data = {

        "Game": [
            f"{away_team} vs {home_team}"
        ],

        "Predicted Winner": [
            "Unavailable"
        ],

        "Predicted Margin": [
            0
        ],

        "Total Over/Under": [
            0
        ]
    }

    return pd.DataFrame(data)


# ============================================================
# ORIGINAL FUNCTION:
# fetch_defensive_stats()
# ============================================================

def fetch_defensive_stats(
    home_team=None,
    away_team=None
):

    if home_team is None:
        home_team = "San Francisco 49ers"

    if away_team is None:
        away_team = "New York Jets"

    data = {

        "Team": [
            home_team,
            away_team
        ],

        "Sacks": [
            0,
            0
        ],

        "Interceptions": [
            0,
            0
        ],

        "Fumbles Recovered": [
            0,
            0
        ],

        "Tackles for Loss": [
            0,
            0
        ],

        "Passes Defended": [
            0,
            0
        ],

        "Best Defensive Player": [
            "Data unavailable",
            "Data unavailable"
        ]
    }

    return pd.DataFrame(data)


# ============================================================
# COACHING DATA
# ============================================================

def fetch_coaching_data(
    home_team,
    away_team
):

    return pd.DataFrame({

        "Team": [
            home_team,
            away_team
        ],

        "Head Coach": [
            "Current coach - verify live",
            "Current coach - verify live"
        ],

        "Offensive Coordinator": [
            "Current coordinator - verify live",
            "Current coordinator - verify live"
        ],

        "Defensive Coordinator": [
            "Current coordinator - verify live",
            "Current coordinator - verify live"
        ],

        "QB Coach": [
            "Current QB coach - verify live",
            "Current QB coach - verify live"
        ],

        "Coaching Grade": [
            70,
            70
        ]
    })


# ============================================================
# TEAM PROFILE
# ============================================================

def build_team_profile(
    team,
    baseline_df
):

    row = baseline_df[
        baseline_df["Team"] == team
    ]

    if row.empty:

        return create_team_baseline(
            team
        )

    return row.iloc[0].to_dict()


# ============================================================
# ORIGINAL:
# calculate_injury_impact()
# ============================================================

def calculate_injury_impact(
    injury_reports,
    player_stats,
    defensive_stats
):

    impact = {}

    for _, row in injury_reports.iterrows():

        status = str(
            row["Status"]
        ).lower()

        if status in [
            "out",
            "inactive"
        ]:

            impact[
                row["Player"]
            ] = -1.0

        elif status in [
            "doubtful"
        ]:

            impact[
                row["Player"]
            ] = -0.70

        elif status in [
            "questionable"
        ]:

            impact[
                row["Player"]
            ] = -0.25

    return impact


# ============================================================
# IMPROVED INJURY SCORE
# ============================================================

def calculate_team_health(
    team,
    injury_reports
):

    team_injuries = injury_reports[
        injury_reports["Team"] == team
    ]

    score = 100.0

    for _, row in team_injuries.iterrows():

        status = str(
            row["Status"]
        ).lower()

        if status == "out":
            score -= 15

        elif status == "doubtful":
            score -= 10

        elif status == "questionable":
            score -= 5

    return max(
        40,
        min(100, score)
    )


# ============================================================
# ORIGINAL:
# calculate_experience_impact()
# ============================================================

def calculate_experience_impact(
    player_stats,
    defensive_stats
):

    experience_impact = {}

    for _, row in player_stats.iterrows():

        player = str(
            row["Player"]
        )

        if (
            "Rookie" in player
            or "New Addition" in player
        ):

            experience_impact[
                player
            ] = -0.1

    return experience_impact


# ============================================================
# PRESEASON ADJUSTMENT
# ============================================================

def preseason_adjustment():

    # Preseason is less predictable than regular season.
    #
    # Instead of adding random points, this reduces confidence.

    return 0.70


# ============================================================
# TEAM COMPOSITE SCORE
# ============================================================

def calculate_team_composite(
    profile
):

    offense = (

        profile["QB Grade"] * 0.20

        + profile["RB Grade"] * 0.08

        + profile["WR Grade"] * 0.10

        + profile["TE Grade"] * 0.07

        + profile["OL Grade"] * 0.15
    )

    defense = (

        profile["DL Grade"] * 0.12

        + profile["LB Grade"] * 0.08

        + profile["CB Grade"] * 0.08

        + profile["S Grade"] * 0.05
    )

    other = (

        profile["Coaching Grade"] * 0.04

        + profile["Experience Grade"] * 0.03
    )

    total = (
        offense
        + defense
        + other
    )

    return round(
        total,
        2
    )


# ============================================================
# MATCHUP ADVANTAGES
# ============================================================

def find_matchup_advantages(
    home,
    away
):

    factors = {

        "Quarterback":
            home["QB Grade"] -
            away["QB Grade"],

        "Running Back":
            home["RB Grade"] -
            away["RB Grade"],

        "Wide Receiver":
            home["WR Grade"] -
            away["WR Grade"],

        "Tight End":
            home["TE Grade"] -
            away["TE Grade"],

        "Offensive Line":
            home["OL Grade"] -
            away["OL Grade"],

        "Defensive Line":
            home["DL Grade"] -
            away["DL Grade"],

        "Linebacker":
            home["LB Grade"] -
            away["LB Grade"],

        "Cornerback":
            home["CB Grade"] -
            away["CB Grade"],

        "Safety":
            home["S Grade"] -
            away["S Grade"],

        "Coaching":
            home["Coaching Grade"] -
            away["Coaching Grade"],
    }

    return factors


# ============================================================
# IMPROVED PREDICT SCORE
# ============================================================

def predict_score(
    home_profile,
    away_profile,
    injury_impact,
    experience_impact,
    preseason=True
):

    home_base = calculate_team_composite(
        home_profile
    )

    away_base = calculate_team_composite(
        away_profile
    )

    # --------------------------------------------------------
    # Home field
    # --------------------------------------------------------

    home_base += 2.0

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    home_base += (
        home_profile["Health Grade"] - 70
    ) * 0.10

    away_base += (
        away_profile["Health Grade"] - 70
    ) * 0.10

    # --------------------------------------------------------
    # News
    # --------------------------------------------------------

    home_base += (
        home_profile["News Grade"] - 70
    ) * 0.05

    away_base += (
        away_profile["News Grade"] - 70
    ) * 0.05

    # --------------------------------------------------------
    # EPA
    # --------------------------------------------------------

    home_base += (
        home_profile["EPA"] * 12
    )

    away_base += (
        away_profile["EPA"] * 12
    )

    # --------------------------------------------------------
    # Convert model strength to score
    # --------------------------------------------------------

    home_score = 21 + (
        home_base - 70
    ) * 0.28

    away_score = 20 + (
        away_base - 70
    ) * 0.28

    # --------------------------------------------------------
    # Preseason
    # --------------------------------------------------------

    if preseason:

        # Do NOT add random points.
        #
        # Instead, preseason reduces confidence because
        # playing time and lineups are uncertain.

        home_score *= 0.95
        away_score *= 0.95

    home_score = max(
        10,
        round(home_score)
    )

    away_score = max(
        10,
        round(away_score)
    )

    return (
        home_score,
        away_score
    )


# ============================================================
# COMPLETE QUANTITATIVE PREDICTION
# ============================================================

def matchup_prediction(
    home_team,
    away_team,
    preseason=True
):

    baseline_df = fetch_team_baselines()

    home = build_team_profile(
        home_team,
        baseline_df
    )

    away = build_team_profile(
        away_team,
        baseline_df
    )

    injury_reports = fetch_injury_reports(
        home_team,
        away_team
    )

    injury_impact = calculate_injury_impact(
        injury_reports,
        fetch_player_stats(
            home_team,
            away_team
        ),
        fetch_defensive_stats(
            home_team,
            away_team
        )
    )

    experience_impact = calculate_experience_impact(
        fetch_player_stats(
            home_team,
            away_team
        ),
        fetch_defensive_stats(
            home_team,
            away_team
        )
    )

    home_score, away_score = predict_score(

        home,

        away,

        injury_impact,

        experience_impact,

        preseason
    )

    margin = (
        home_score -
        away_score
    )

    if margin > 0:

        winner = home_team

    elif margin < 0:

        winner = away_team

    else:

        winner = "TIE / TOO CLOSE TO CALL"

    difference = abs(margin)

    confidence = 50 + (
        difference * 4
    )

    if preseason:

        confidence *= (
            preseason_adjustment()
        )

    confidence = max(
        45,
        min(
            90,
            confidence
        )
    )

    advantages = find_matchup_advantages(
        home,
        away
    )

    return {

        "home": {

            "team": home_team,

            "composite":
                calculate_team_composite(
                    home
                ),

            "qb":
                home["QB Grade"],

            "skill":
                (
                    home["WR Grade"]
                    + home["TE Grade"]
                    + home["RB Grade"]
                ) / 3,

            "trenches":
                (
                    home["OL Grade"]
                    + home["DL Grade"]
                ) / 2,

            "defense":
                (
                    home["LB Grade"]
                    + home["CB Grade"]
                    + home["S Grade"]
                ) / 3,

            "injury":
                home["Health Grade"],

            "coaching":
                home["Coaching Grade"],

            "experience":
                home["Experience Grade"],

            "news":
                home["News Grade"],
        },

        "away": {

            "team": away_team,

            "composite":
                calculate_team_composite(
                    away
                ),

            "qb":
                away["QB Grade"],

            "skill":
                (
                    away["WR Grade"]
                    + away["TE Grade"]
                    + away["RB Grade"]
                ) / 3,

            "trenches":
                (
                    away["OL Grade"]
                    + away["DL Grade"]
                ) / 2,

            "defense":
                (
                    away["LB Grade"]
                    + away["CB Grade"]
                    + away["S Grade"]
                ) / 3,

            "injury":
                away["Health Grade"],

            "coaching":
                away["Coaching Grade"],

            "experience":
                away["Experience Grade"],

            "news":
                away["News Grade"],
        },

        "home_score":
            home_score,

        "away_score":
            away_score,

        "winner":
            winner,

        "margin":
            margin,

        "confidence":
            round(
                confidence,
                1
            ),

        "advantages":
            advantages,
    }


# ============================================================
# AI AGENT
# ============================================================

NFL_ANALYST_INSTRUCTIONS = """

You are an advanced NFL scouting and game-analysis AI.

You analyze NFL matchups using:

- current NFL news
- injuries
- roster changes
- depth charts
- quarterback situations
- coaching
- offensive coordinators
- defensive coordinators
- position coaches
- offensive line
- defensive line
- WR
- TE
- RB
- LB
- CB
- safety
- EPA
- success rate
- efficiency
- explosive plays
- pressure
- sacks
- turnovers
- red zone
- third down
- preseason playing-time expectations

You are reviewing a quantitative prediction model.

You are NOT allowed to invent information.

If data is unavailable say:

"Data unavailable."

Do not pretend that model estimates are official PFF grades.

The system is PFF-inspired, not a copy of proprietary PFF methodology.

For preseason games you MUST consider:

- expected starter snaps
- QB rotation
- backup QB quality
- roster battles
- young players
- players returning from injury
- coaching evaluation
- depth
- motivation
- preseason uncertainty

Your report must include:

1. Winner
2. Projected score
3. Confidence
4. Quarterback matchup
5. Running game
6. WR matchup
7. TE matchup
8. Offensive line
9. Defensive line
10. Linebackers
11. Secondary
12. Coaching
13. Injuries
14. Depth
15. Strengths
16. Weaknesses
17. Biggest matchup advantage
18. Biggest upset risk
19. Whether the quantitative model should be adjusted
20. Final verdict

Never claim a prediction is guaranteed.
"""


if AGENTS_AVAILABLE:

    @function_tool
    def research_current_nfl_information(
        query: str
    ) -> str:

        """
        Research current NFL information.
        """

        try:

            from openai import OpenAI

            client = OpenAI()

            response = client.responses.create(

                model=OPENAI_MODEL,

                tools=[
                    {
                        "type": "web_search"
                    }
                ],

                input=query
            )

            return response.output_text

        except Exception as e:

            return (
                "Research failed: "
                + str(e)
            )


def create_nfl_agent():

    if not AGENTS_AVAILABLE:

        return None

    return Agent(

        name="NFL 2026 Advanced Analyst",

        model=OPENAI_MODEL,

        instructions=
            NFL_ANALYST_INSTRUCTIONS,

        tools=[
            research_current_nfl_information
        ]
    )


def run_ai_nfl_analysis(
    prediction
):

    if not AGENTS_AVAILABLE:

        return (
            "AI Agent is not installed.\n\n"
            "Run:\n"
            "pip install openai-agents"
        )

    if not os.getenv(
        "OPENAI_API_KEY"
    ):

        return (
            "AI Agent is not configured.\n\n"
            "Set OPENAI_API_KEY first."
        )

    agent = create_nfl_agent()

    data = {
        "prediction":
            prediction
    }

    home = prediction[
        "home"
    ]["team"]

    away = prediction[
        "away"
    ]["team"]

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    prompt = f"""

Analyze this NFL matchup:

HOME:
{home}

AWAY:
{away}

DATE:
{today}

QUANTITATIVE MODEL:

{json.dumps(
    data,
    indent=2,
    default=str
)}

Before giving the final analysis:

- Research current news.
- Research current injuries.
- Research roster/depth changes.
- Research QB status.
- Research relevant coaching information.
- Consider preseason playing time.
- Check whether important starters are expected to play.
- Identify uncertainty.

Compare the current information with the quantitative model.

If the model is likely wrong, explain why.

Do NOT fabricate information.

Return:

WINNER:

PROJECTED SCORE:

CONFIDENCE:

QUANTITATIVE MODEL:

AI ADJUSTMENT:

QUARTERBACK:

RUNNING GAME:

WR:

TE:

OFFENSIVE LINE:

DEFENSIVE LINE:

LINEBACKERS:

SECONDARY:

COACHING:

INJURIES:

DEPTH:

STRENGTHS:

WEAKNESSES:

MATCHUP ADVANTAGE:

UPSET RISK:

FINAL VERDICT:
"""

    try:

        result = Runner.run_sync(

            agent,

            prompt,

            max_turns=8
        )

        return result.final_output

    except Exception as e:

        return (
            "AI analysis failed:\n\n"
            + str(e)
        )


# ============================================================
# AI CONFIDENCE ADJUSTMENT
# ============================================================

def ai_confidence_adjustment(
    prediction,
    ai_report
):

    confidence = prediction[
        "confidence"
    ]

    text = ai_report.lower()

    warning_phrases = [

        "starting quarterback out",

        "quarterback out",

        "multiple starters out",

        "major injury",

        "significant injury",

        "backup quarterback",

        "third-string quarterback",

        "uncertain quarterback",

        "limited starters",

    ]

    warnings = 0

    for phrase in warning_phrases:

        if phrase in text:

            warnings += 1

    confidence -= (
        warnings * 4
    )

    confidence = max(
        40,
        min(
            90,
            confidence
        )
    )

    return round(
        confidence,
        1
    )


# ============================================================
# SCHEDULE HELPERS
# ============================================================

def get_preseason_games():

    return pd.DataFrame(
        PRESEASON_2026
    )


def find_game(
    home_team,
    away_team
):

    for game in PRESEASON_2026:

        if (
            game["Home"] == home_team
            and
            game["Away"] == away_team
        ):

            return game

    return None


# ============================================================
# CSV EXPORT
# ============================================================

def create_prediction_csv(
    prediction
):

    row = {

        "Home Team":
            prediction[
                "home"
            ]["team"],

        "Away Team":
            prediction[
                "away"
            ]["team"],

        "Predicted Winner":
            prediction[
                "winner"
            ],

        "Home Score":
            prediction[
                "home_score"
            ],

        "Away Score":
            prediction[
                "away_score"
            ],

        "Projected Margin":
            prediction[
                "margin"
            ],

        "Confidence":
            prediction[
                "confidence"
            ],
    }

    return pd.DataFrame([
        row
    ])


# ============================================================
# STREAMLIT APPLICATION
# ============================================================

def main():

    st.set_page_config(

        page_title=
            APP_TITLE,

        page_icon="🏈",

        layout="wide"
    )

    st.title(
        "🏈 NFL 2026 AI Game Prediction System"
    )

    st.caption(
        "Quantitative NFL matchup model + AI scouting analyst"
    )

    # --------------------------------------------------------
    # Sidebar
    # --------------------------------------------------------

    st.sidebar.header(
        "Game Selection"
    )

    mode = st.sidebar.radio(

        "Select matchup mode",

        [
            "Choose Teams",
            "2026 Preseason Schedule"
        ]
    )

    # --------------------------------------------------------
    # TEAM SELECTION
    # --------------------------------------------------------

    if mode == "Choose Teams":

        home_team = st.sidebar.selectbox(

            "Home Team",

            NFL_TEAMS,

            index=
                NFL_TEAMS.index(
                    "Chicago Bears"
                )
        )

        away_team = st.sidebar.selectbox(

            "Away Team",

            NFL_TEAMS,

            index=
                NFL_TEAMS.index(
                    "Green Bay Packers"
                )
        )

        preseason = st.sidebar.checkbox(

            "Preseason Game",

            value=True
        )

    else:

        games = get_preseason_games()

        games["Matchup"] = (

            games["Away"]

            + " @ "

            + games["Home"]

            + " — "

            + games["Date"]
        )

        selected_game = st.sidebar.selectbox(

            "Select 2026 preseason game",

            games["Matchup"].tolist()
        )

        selected_row = games[
            games["Matchup"] ==
            selected_game
        ].iloc[0]

        home_team = selected_row[
            "Home"
        ]

        away_team = selected_row[
            "Away"
        ]

        preseason = True

    # --------------------------------------------------------
    # MAIN MATCHUP
    # --------------------------------------------------------

    st.header(

        f"{away_team} @ {home_team}"
    )

    # --------------------------------------------------------
    # RUN PREDICTION
    # --------------------------------------------------------

    if st.button(

        "🔮 Analyze Game",

        type="primary"
    ):

        with st.spinner(
            "Running quantitative NFL matchup model..."
        ):

            prediction = matchup_prediction(

                home_team,

                away_team,

                preseason
            )

        # Save prediction in session
        st.session_state[
            "prediction"
        ] = prediction

        # ----------------------------------------------------
        # BASIC RESULT
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📊 Quantitative Prediction"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "Predicted Winner",

                prediction[
                    "winner"
                ]
            )

        with col2:

            st.metric(

                "Home Score",

                prediction[
                    "home_score"
                ]
            )

        with col3:

            st.metric(

                "Away Score",

                prediction[
                    "away_score"
                ]
            )

        with col4:

            st.metric(

                "Model Confidence",

                f"{prediction['confidence']}%"
            )

        # ----------------------------------------------------
        # TEAM COMPARISON
        # ----------------------------------------------------

        st.subheader(
            "📈 Team Comparison"
        )

        comparison = pd.DataFrame({

            "Category": [

                "Overall",

                "Quarterback",

                "Skill Positions",

                "Trenches",

                "Defense",

                "Health",

                "Coaching",

                "Experience",

                "News"
            ],

            home_team: [

                prediction[
                    "home"
                ]["composite"],

                prediction[
                    "home"
                ]["qb"],

                prediction[
                    "home"
                ]["skill"],

                prediction[
                    "home"
                ]["trenches"],

                prediction[
                    "home"
                ]["defense"],

                prediction[
                    "home"
                ]["injury"],

                prediction[
                    "home"
                ]["coaching"],

                prediction[
                    "home"
                ]["experience"],

                prediction[
                    "home"
                ]["news"],
            ],

            away_team: [

                prediction[
                    "away"
                ]["composite"],

                prediction[
                    "away"
                ]["qb"],

                prediction[
                    "away"
                ]["skill"],

                prediction[
                    "away"
                ]["trenches"],

                prediction[
                    "away"
                ]["defense"],

                prediction[
                    "away"
                ]["injury"],

                prediction[
                    "away"
                ]["coaching"],

                prediction[
                    "away"
                ]["experience"],

                prediction[
                    "away"
                ]["news"],
            ]
        })

        st.dataframe(

            comparison,

            use_container_width=True,

            hide_index=True
        )

        # ----------------------------------------------------
        # MATCHUP ADVANTAGES
        # ----------------------------------------------------

        st.subheader(
            "⚔️ Matchup Advantages"
        )

        advantages = prediction[
            "advantages"
        ]

        advantage_rows = []

        for category, difference in advantages.items():

            if difference > 0:

                advantage_rows.append({

                    "Category":
                        category,

                    "Advantage":
                        home_team,

                    "Difference":
                        round(
                            difference,
                            2
                        )
                })

            elif difference < 0:

                advantage_rows.append({

                    "Category":
                        category,

                    "Advantage":
                        away_team,

                    "Difference":
                        round(
                            abs(difference),
                            2
                        )
                })

            else:

                advantage_rows.append({

                    "Category":
                        category,

                    "Advantage":
                        "Even",

                    "Difference":
                        0
                })

        advantage_df = pd.DataFrame(
            advantage_rows
        )

        st.dataframe(

            advantage_df,

            use_container_width=True,

            hide_index=True
        )

        # ----------------------------------------------------
        # AI ANALYST
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "🤖 AI NFL Analyst"
        )

        if AGENTS_AVAILABLE:

            st.success(
                "AI Agent installed"
            )

            with st.spinner(

                "AI agent researching current "
                "NFL news, injuries, rosters "
                "and matchup information..."
            ):

                ai_report = run_ai_nfl_analysis(
                    prediction
                )

            st.markdown(
                ai_report
            )

            # -----------------------------------------------
            # AI ADJUSTED CONFIDENCE
            # -----------------------------------------------

            final_confidence = (
                ai_confidence_adjustment(
                    prediction,
                    ai_report
                )
            )

            st.metric(

                "AI-Adjusted Confidence",

                f"{final_confidence}%"
            )

            # -----------------------------------------------
            # SAVE REPORT
            # -----------------------------------------------

            st.download_button(

                "📄 Download AI Report",

                data=ai_report,

                file_name=(

                    f"{away_team}_vs_"
                    f"{home_team}_AI_Report.txt"
                ),

                mime="text/plain"
            )

        else:

            st.warning(

                "AI Agent is not installed."
            )

            st.code(

                "pip install openai-agents"
            )

        # ----------------------------------------------------
        # ORIGINAL DATA TABLES
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📋 Historical Game Data"
        )

        historical_data = (
            fetch_historical_game_data(
                home_team,
                away_team
            )
        )

        st.dataframe(
            historical_data,
            use_container_width=True
        )

        st.subheader(
            "🏈 Player Stats"
        )

        player_stats = (
            fetch_player_stats(
                home_team,
                away_team
            )
        )

        st.dataframe(
            player_stats,
            use_container_width=True
        )

        st.subheader(
            "🎯 Favorite Targets"
        )

        favorite_targets = (
            fetch_favorite_targets(
                home_team,
                away_team
            )
        )

        st.dataframe(
            favorite_targets,
            use_container_width=True
        )

        st.subheader(
            "🚑 Injury Reports"
        )

        injuries = (
            fetch_injury_reports(
                home_team,
                away_team
            )
        )

        st.dataframe(
            injuries,
            use_container_width=True
        )

        st.subheader(
            "📊 Advanced Stats"
        )

        stats = (
            advanced_stats(
                home_team,
                away_team
            )
        )

        st.dataframe(
            stats,
            use_container_width=True
        )

        st.subheader(
            "📈 PFF-Style Model Data"
        )

        pff = (
            fetch_pff_data(
                home_team,
                away_team
            )
        )

        st.dataframe(
            pff,
            use_container_width=True
        )

        st.caption(
            "These are model-generated PFF-style grades, "
            "not official PFF grades."
        )

        st.subheader(
            "🛡️ Defensive Stats"
        )

        defense = (
            fetch_defensive_stats(
                home_team,
                away_team
            )
        )

        st.dataframe(
            defense,
            use_container_width=True
        )

        st.subheader(
            "🏈 Coaching"
        )

        coaching = (
            fetch_coaching_data(
                home_team,
                away_team
            )
        )

        st.dataframe(
            coaching,
            use_container_width=True
        )

        # ----------------------------------------------------
        # DOWNLOAD PREDICTION
        # ----------------------------------------------------

        prediction_csv = (
            create_prediction_csv(
                prediction
            )
        )

        st.download_button(

            "⬇️ Download Prediction CSV",

            data=
                prediction_csv.to_csv(
                    index=False
                ),

            file_name=(
                f"{away_team}_vs_"
                f"{home_team}_prediction.csv"
            ),

            mime="text/csv"
        )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()
