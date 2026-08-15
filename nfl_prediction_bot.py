# ============================================================
# COLAB FIX – install + run Streamlit with public URL
# ============================================================
!pip install -q streamlit pandas openai-agents  # openai-agents optional

# Write the full bot code to a file
with open("cardinals_raiders_bot.py", "w") as f:
    f.write(r'''
# ============================================================
# NFL 2026 ADVANCED GAME PREDICTION BOT
# Arizona Cardinals @ Las Vegas Raiders ONLY
# ============================================================
import os
import json
from datetime import datetime
import pandas as pd
import streamlit as st

try:
    from agents import Agent, Runner, function_tool
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False

APP_TITLE = "NFL 2026 AI Game Prediction System — Cardinals @ Raiders"
OPENAI_MODEL = os.getenv("NFL_AI_MODEL", "gpt-5.6-sol")

NFL_TEAMS = ["Arizona Cardinals", "Las Vegas Raiders"]
TEAM_ABBREVIATIONS = {"Arizona Cardinals": "ARI", "Las Vegas Raiders": "LV"}

PRESEASON_2026 = [
    {"Date": "2026-08-13", "Away": "Arizona Cardinals", "Home": "Las Vegas Raiders"},
]

def create_team_baseline(team):
    base = {
        "Team": team, "QB Grade": 70.0, "RB Grade": 70.0, "WR Grade": 70.0,
        "TE Grade": 70.0, "OL Grade": 70.0, "DL Grade": 70.0, "LB Grade": 70.0,
        "CB Grade": 70.0, "S Grade": 70.0, "Offensive Grade": 70.0,
        "Defensive Grade": 70.0, "Coaching Grade": 70.0, "Experience Grade": 70.0,
        "Depth Grade": 70.0, "Health Grade": 70.0, "News Grade": 70.0,
        "EPA": 0.0, "YPP": 5.0, "YPC": 4.2, "Pass YPA": 7.0,
        "Pass EPA": 0.0, "Rush EPA": 0.0, "Pressure Rate": 0.20,
        "Sacks": 0, "Interceptions": 0, "Turnover Margin": 0,
    }
    if team == "Arizona Cardinals":
        base.update({
            "QB Grade": 74.0, "RB Grade": 78.0, "WR Grade": 86.0, "TE Grade": 88.0,
            "OL Grade": 68.0, "DL Grade": 67.0, "LB Grade": 70.0, "CB Grade": 66.0,
            "S Grade": 76.0, "Offensive Grade": 80.0, "Defensive Grade": 66.0,
            "Coaching Grade": 76.0, "Experience Grade": 72.0, "Depth Grade": 71.0,
            "Health Grade": 64.0, "News Grade": 73.0, "EPA": 0.04, "YPP": 5.6,
            "YPC": 4.6, "Pass YPA": 7.6, "Pass EPA": 0.08, "Rush EPA": 0.03,
            "Pressure Rate": 0.18,
        })
    elif team == "Las Vegas Raiders":
        base.update({
            "QB Grade": 72.0, "RB Grade": 79.0, "WR Grade": 64.0, "TE Grade": 87.0,
            "OL Grade": 74.0, "DL Grade": 78.0, "LB Grade": 75.0, "CB Grade": 62.0,
            "S Grade": 68.0, "Offensive Grade": 73.0, "Defensive Grade": 72.0,
            "Coaching Grade": 74.0, "Experience Grade": 70.0, "Depth Grade": 69.0,
            "Health Grade": 71.0, "News Grade": 72.0, "EPA": 0.01, "YPP": 5.2,
            "YPC": 4.5, "Pass YPA": 6.9, "Pass EPA": 0.02, "Rush EPA": 0.04,
            "Pressure Rate": 0.24,
        })
    return base

def fetch_team_baselines():
    return pd.DataFrame([create_team_baseline(t) for t in NFL_TEAMS])

def fetch_historical_game_data(home_team=None, away_team=None):
    home_team = home_team or "Las Vegas Raiders"
    away_team = away_team or "Arizona Cardinals"
    return pd.DataFrame({
        "Game": [f"{away_team} @ {home_team}"],
        "Home Team": [home_team],
        "Away Team": [away_team],
    })

def fetch_player_stats(home_team=None, away_team=None):
    return pd.DataFrame({
        "Team": ["Arizona Cardinals"]*5 + ["Las Vegas Raiders"]*5,
        "Player": [
            "Jacoby Brissett", "Gardner Minshew", "Marvin Harrison Jr.",
            "Trey McBride", "Jeremiyah Love",
            "Kirk Cousins", "Fernando Mendoza", "Brock Bowers",
            "Michael Mayer", "Ashton Jeanty",
        ],
        "Position": ["QB","QB","WR","TE","RB","QB","QB","TE","TE","RB"],
        "Yards": [0]*10, "Touchdowns": [0]*10,
    })

def fetch_favorite_targets(home_team=None, away_team=None):
    return pd.DataFrame({
        "Team": ["Arizona Cardinals"]*3 + ["Las Vegas Raiders"]*3,
        "Favorite Target": [
            "Marvin Harrison Jr.", "Trey McBride", "Michael Wilson",
            "Brock Bowers", "Michael Mayer", "Ashton Jeanty",
        ],
        "Target Stats (Yards)": [0]*6,
        "Target Stats (Receptions)": [0]*6,
        "Target Stats (TDs)": [0]*6,
    })

def fetch_injury_reports(home_team=None, away_team=None):
    return pd.DataFrame({
        "Team": ["Arizona Cardinals"]*5 + ["Las Vegas Raiders"]*2,
        "Player": [
            "Josh Sweat", "Carson Beck", "Chase Bisontis",
            "James Conner", "Baron Browning",
            "Maxx Crosby", "Jermod McCoy",
        ],
        "Injury": [
            "Knee (PUP)", "Ribs", "Knee", "Foot/Ankle", "Undisclosed (day-to-day)",
            "Knee (managed)", "Knee",
        ],
        "Status": ["Out", "Questionable", "Questionable", "Doubtful", "Doubtful",
                   "Questionable", "Questionable"],
    })

def advanced_stats(home_team=None, away_team=None):
    baseline = fetch_team_baselines()
    home_row = baseline[baseline["Team"] == (home_team or "Las Vegas Raiders")].iloc[0]
    away_row = baseline[baseline["Team"] == (away_team or "Arizona Cardinals")].iloc[0]
    return pd.DataFrame({
        "Team": [home_team or "Las Vegas Raiders", away_team or "Arizona Cardinals"],
        "YPP": [home_row["YPP"], away_row["YPP"]],
        "EPA": [home_row["EPA"], away_row["EPA"]],
        "YPC": [home_row["YPC"], away_row["YPC"]],
        "Pass YPA": [home_row["Pass YPA"], away_row["Pass YPA"]],
        "Pass EPA": [home_row["Pass EPA"], away_row["Pass EPA"]],
        "Rush YPA": [home_row["YPC"], away_row["YPC"]],
        "Pressure Rate": [home_row["Pressure Rate"], away_row["Pressure Rate"]],
    })

def fetch_pff_data(home_team=None, away_team=None):
    baseline = fetch_team_baselines()
    home_row = baseline[baseline["Team"] == (home_team or "Las Vegas Raiders")].iloc[0]
    away_row = baseline[baseline["Team"] == (away_team or "Arizona Cardinals")].iloc[0]
    return pd.DataFrame({
        "Team": [home_team or "Las Vegas Raiders", away_team or "Arizona Cardinals"],
        "Offensive Grade": [home_row["Offensive Grade"], away_row["Offensive Grade"]],
        "Defensive Grade": [home_row["Defensive Grade"], away_row["Defensive Grade"]],
        "Pass Blocking Grade": [home_row["OL Grade"], away_row["OL Grade"]],
        "Run Blocking Grade": [home_row["OL Grade"]-2, away_row["OL Grade"]-1],
        "Pass Rush Grade": [home_row["DL Grade"], away_row["DL Grade"]],
        "Coverage Grade": [
            (home_row["CB Grade"] + home_row["S Grade"]) / 2,
            (away_row["CB Grade"] + away_row["S Grade"]) / 2,
        ],
    })

def fetch_external_predictions(home_team=None, away_team=None):
    return pd.DataFrame({
        "Game": [f"{away_team or 'Arizona Cardinals'} @ {home_team or 'Las Vegas Raiders'}"],
        "Predicted Winner": ["Unavailable"],
        "Predicted Margin": [0],
        "Total Over/Under": [0],
    })

def fetch_defensive_stats(home_team=None, away_team=None):
    return pd.DataFrame({
        "Team": [home_team or "Las Vegas Raiders", away_team or "Arizona Cardinals"],
        "Sacks": [0, 0], "Interceptions": [0, 0], "Fumbles Recovered": [0, 0],
        "Tackles for Loss": [0, 0], "Passes Defended": [0, 0],
        "Best Defensive Player": ["Maxx Crosby", "Budda Baker / Walter Nolen"],
    })

def fetch_coaching_data(home_team, away_team):
    return pd.DataFrame({
        "Team": [home_team, away_team],
        "Head Coach": ["Klint Kubiak", "Mike LaFleur"],
        "Offensive Coordinator": [
            "Andrew Janocko (Kubiak – TE / play-action)",
            "Nathaniel Hackett (LaFleur – space & skill volume)",
        ],
        "Defensive Coordinator": ["Rob Leonard", "Nick Rallis"],
        "QB Coach": ["Raiders QB coach", "Cardinals QB coach"],
        "Coaching Grade": [74, 76],
    })

def build_team_profile(team, baseline_df):
    row = baseline_df[baseline_df["Team"] == team]
    return row.iloc[0].to_dict() if not row.empty else create_team_baseline(team)

def calculate_injury_impact(injury_reports, player_stats, defensive_stats):
    impact = {}
    for _, row in injury_reports.iterrows():
        status = str(row["Status"]).lower()
        if status in ["out", "inactive"]:
            impact[row["Player"]] = -1.0
        elif status == "doubtful":
            impact[row["Player"]] = -0.70
        elif status == "questionable":
            impact[row["Player"]] = -0.25
    return impact

def calculate_team_health(team, injury_reports):
    score = 100.0
    for _, row in injury_reports[injury_reports["Team"] == team].iterrows():
        status = str(row["Status"]).lower()
        if status == "out": score -= 15
        elif status == "doubtful": score -= 10
        elif status == "questionable": score -= 5
    return max(40, min(100, score))

def calculate_experience_impact(player_stats, defensive_stats):
    return {}

def preseason_adjustment():
    return 0.70

def calculate_team_composite(profile):
    offense = (profile["QB Grade"]*0.20 + profile["RB Grade"]*0.08 +
               profile["WR Grade"]*0.10 + profile["TE Grade"]*0.07 +
               profile["OL Grade"]*0.15)
    defense = (profile["DL Grade"]*0.12 + profile["LB Grade"]*0.08 +
               profile["CB Grade"]*0.08 + profile["S Grade"]*0.05)
    other = profile["Coaching Grade"]*0.04 + profile["Experience Grade"]*0.03
    return round(offense + defense + other, 2)

def find_matchup_advantages(home, away):
    return {
        "Quarterback": home["QB Grade"] - away["QB Grade"],
        "Running Back": home["RB Grade"] - away["RB Grade"],
        "Wide Receiver": home["WR Grade"] - away["WR Grade"],
        "Tight End": home["TE Grade"] - away["TE Grade"],
        "Offensive Line": home["OL Grade"] - away["OL Grade"],
        "Defensive Line": home["DL Grade"] - away["DL Grade"],
        "Linebacker": home["LB Grade"] - away["LB Grade"],
        "Cornerback": home["CB Grade"] - away["CB Grade"],
        "Safety": home["S Grade"] - away["S Grade"],
        "Coaching": home["Coaching Grade"] - away["Coaching Grade"],
    }

def predict_score(home_profile, away_profile, injury_impact, experience_impact, preseason=True):
    home_base = calculate_team_composite(home_profile) + 2.0
    away_base = calculate_team_composite(away_profile)
    home_base += (home_profile["Health Grade"] - 70) * 0.10
    away_base += (away_profile["Health Grade"] - 70) * 0.10
    home_base += (home_profile["News Grade"] - 70) * 0.05
    away_base += (away_profile["News Grade"] - 70) * 0.05
    home_base += home_profile["EPA"] * 12
    away_base += away_profile["EPA"] * 12
    home_score = 21 + (home_base - 70) * 0.28
    away_score = 20 + (away_base - 70) * 0.28
    if preseason:
        home_score *= 0.95
        away_score *= 0.95
    return max(10, round(home_score)), max(10, round(away_score))

def matchup_prediction(home_team, away_team, preseason=True):
    baseline_df = fetch_team_baselines()
    home = build_team_profile(home_team, baseline_df)
    away = build_team_profile(away_team, baseline_df)
    injury_reports = fetch_injury_reports(home_team, away_team)
    injury_impact = calculate_injury_impact(injury_reports, None, None)
    experience_impact = {}
    home_score, away_score = predict_score(home, away, injury_impact, experience_impact, preseason)
    margin = home_score - away_score
    winner = home_team if margin > 0 else (away_team if margin < 0 else "TIE / TOO CLOSE TO CALL")
    confidence = 50 + abs(margin) * 4
    if preseason:
        confidence *= preseason_adjustment()
    confidence = max(45, min(90, confidence))
    return {
        "home": {
            "team": home_team, "composite": calculate_team_composite(home),
            "qb": home["QB Grade"],
            "skill": (home["WR Grade"] + home["TE Grade"] + home["RB Grade"]) / 3,
            "trenches": (home["OL Grade"] + home["DL Grade"]) / 2,
            "defense": (home["LB Grade"] + home["CB Grade"] + home["S Grade"]) / 3,
            "injury": home["Health Grade"], "coaching": home["Coaching Grade"],
            "experience": home["Experience Grade"], "news": home["News Grade"],
        },
        "away": {
            "team": away_team, "composite": calculate_team_composite(away),
            "qb": away["QB Grade"],
            "skill": (away["WR Grade"] + away["TE Grade"] + away["RB Grade"]) / 3,
            "trenches": (away["OL Grade"] + away["DL Grade"]) / 2,
            "defense": (away["LB Grade"] + away["CB Grade"] + away["S Grade"]) / 3,
            "injury": away["Health Grade"], "coaching": away["Coaching Grade"],
            "experience": away["Experience Grade"], "news": away["News Grade"],
        },
        "home_score": home_score, "away_score": away_score,
        "winner": winner, "margin": margin, "confidence": round(confidence, 1),
        "advantages": find_matchup_advantages(home, away),
    }

def create_prediction_csv(prediction):
    return pd.DataFrame([{
        "Home Team": prediction["home"]["team"],
        "Away Team": prediction["away"]["team"],
        "Predicted Winner": prediction["winner"],
        "Home Score": prediction["home_score"],
        "Away Score": prediction["away_score"],
        "Projected Margin": prediction["margin"],
        "Confidence": prediction["confidence"],
    }])

def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="🏈", layout="wide")
    st.title("🏈 Cardinals @ Raiders — 2026 AI Prediction")
    st.caption("Single-matchup quantitative model (Cardinals & Raiders only)")

    st.sidebar.header("Game Selection")
    home_team = st.sidebar.selectbox("Home Team", NFL_TEAMS, index=1)
    away_team = st.sidebar.selectbox("Away Team", NFL_TEAMS, index=0)
    preseason = st.sidebar.checkbox("Preseason Game", value=True)

    st.header(f"{away_team} @ {home_team}")

    if st.button("🔮 Analyze Game", type="primary"):
        with st.spinner("Running quantitative matchup model..."):
            prediction = matchup_prediction(home_team, away_team, preseason)
        st.session_state["prediction"] = prediction

        st.divider()
        st.subheader("📊 Quantitative Prediction")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Predicted Winner", prediction["winner"])
        c2.metric("Home Score", prediction["home_score"])
        c3.metric("Away Score", prediction["away_score"])
        c4.metric("Model Confidence", f"{prediction['confidence']}%")

        st.subheader("📈 Team Comparison")
        comparison = pd.DataFrame({
            "Category": ["Overall","Quarterback","Skill Positions","Trenches",
                         "Defense","Health","Coaching","Experience","News"],
            home_team: [prediction["home"][k] for k in
                        ["composite","qb","skill","trenches","defense","injury","coaching","experience","news"]],
            away_team: [prediction["away"][k] for k in
                        ["composite","qb","skill","trenches","defense","injury","coaching","experience","news"]],
        })
        st.dataframe(comparison, use_container_width=True, hide_index=True)

        st.subheader("⚔️ Matchup Advantages")
        rows = []
        for cat, diff in prediction["advantages"].items():
            if diff > 0:
                rows.append({"Category": cat, "Advantage": home_team, "Difference": round(diff, 2)})
            elif diff < 0:
                rows.append({"Category": cat, "Advantage": away_team, "Difference": round(abs(diff), 2)})
            else:
                rows.append({"Category": cat, "Advantage": "Even", "Difference": 0})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("📋 Data Tables")
        st.dataframe(fetch_historical_game_data(home_team, away_team), use_container_width=True)
        st.subheader("🏈 Key Players")
        st.dataframe(fetch_player_stats(), use_container_width=True)
        st.subheader("🎯 Favorite Targets")
        st.dataframe(fetch_favorite_targets(), use_container_width=True)
        st.subheader("🚑 Injury Reports")
        st.dataframe(fetch_injury_reports(), use_container_width=True)
        st.subheader("📊 Advanced Stats")
        st.dataframe(advanced_stats(home_team, away_team), use_container_width=True)
        st.subheader("📈 PFF-Style Model Data")
        st.dataframe(fetch_pff_data(home_team, away_team), use_container_width=True)
        st.caption("Model-generated grades — not official PFF grades.")
        st.subheader("🛡️ Defensive Stats")
        st.dataframe(fetch_defensive_stats(home_team, away_team), use_container_width=True)
        st.subheader("🏈 Coaching")
        st.dataframe(fetch_coaching_data(home_team, away_team), use_container_width=True)

        csv = create_prediction_csv(prediction)
        st.download_button("⬇️ Download Prediction CSV",
                           data=csv.to_csv(index=False),
                           file_name=f"{away_team}_vs_{home_team}_prediction.csv",
                           mime="text/csv")

if __name__ == "__main__":
    main()
''')

print("✅ Bot file written: cardinals_raiders_bot.py")

# Launch Streamlit with a public URL (works in Colab)
!streamlit run cardinals_raiders_bot.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false &

import time
time.sleep(8)

# Get the public URL (Colab proxy)
from google.colab.output import eval_js
print("\n" + "="*60)
print("OPEN THIS URL IN A NEW TAB:")
print(eval_js("google.colab.kernel.proxyPort(8501)"))
print("="*60)
