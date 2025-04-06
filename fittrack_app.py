import streamlit as st
import pandas as pd
import os
from datetime import date

# -------------------- UTILS --------------------

def load_data(file, columns):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=columns)

def save_data(df, file):
    df.to_csv(file, index=False)

# -------------------- FILE PATHS --------------------

WORKOUT_FILE = "workouts.csv"
CALORIES_FILE = "calories.csv"
WEIGHT_FILE = "weight.csv"
GOALS_FILE = "goals.csv"

# -------------------- PAGE CONFIG --------------------

st.set_page_config(page_title="FitTrack Assistant", layout="wide")

st.title("🏋‍♂ FitTrack Assistant")
st.sidebar.header("📊 Dashboard & Logs")

# -------------------- TABS --------------------

tabs = st.sidebar.radio("Navigate", ["Dashboard", "Log Workout", "Log Calories", "Track Weight", "Set Goals"])

today = str(date.today())

# -------------------- LOG WORKOUT --------------------

if tabs == "Log Workout":
    st.header("📝 Log Workout")
    workout_type = st.selectbox("Workout Type", ["Cardio", "Strength", "Yoga", "HIIT", "Other"])
    duration = st.number_input("Duration (in minutes)", min_value=1)
    calories_burned = st.number_input("Calories Burned", min_value=0)
    note = st.text_input("Notes", "")

    if st.button("Save Workout"):
        workout_data = load_data(WORKOUT_FILE, ["Date", "Type", "Duration", "Calories", "Note"])
        new_row = pd.DataFrame([[today, workout_type, duration, calories_burned, note]], columns=["Date", "Type", "Duration", "Calories", "Note"])
        workout_data = pd.concat([workout_data, new_row], ignore_index=True)
        save_data(workout_data, WORKOUT_FILE)
        st.success("Workout logged!")

# -------------------- LOG CALORIES --------------------

elif tabs == "Log Calories":
    st.header("🍔 Log Calorie Intake")
    food = st.text_input("Food Item")
    calories = st.number_input("Calories", min_value=0)
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])

    if st.button("Save Meal"):
        cal_data = load_data(CALORIES_FILE, ["Date", "Food", "Calories", "Meal Type"])
        new_row = pd.DataFrame([[today, food, calories, meal_type]], columns=["Date", "Food", "Calories", "Meal Type"])
        cal_data = pd.concat([cal_data, new_row], ignore_index=True)
        save_data(cal_data, CALORIES_FILE)
        st.success("Meal logged!")

# -------------------- TRACK WEIGHT --------------------

elif tabs == "Track Weight":
    st.header("⚖ Track Your Weight")
    weight = st.number_input("Today's Weight (kg)", min_value=0.0, step=0.1)

    if st.button("Save Weight"):
        weight_data = load_data(WEIGHT_FILE, ["Date", "Weight"])
        new_row = pd.DataFrame([[today, weight]], columns=["Date", "Weight"])
        weight_data = pd.concat([weight_data, new_row], ignore_index=True)
        save_data(weight_data, WEIGHT_FILE)
        st.success("Weight logged!")

# -------------------- SET GOALS --------------------

elif tabs == "Set Goals":
    st.header("🎯 Set Your Fitness Goals")

    target_weight = st.number_input("Target Weight (kg)", min_value=0.0, step=0.1)
    weekly_workouts = st.number_input("Target Workouts per Week", min_value=0, max_value=14)

    if st.button("Save Goals"):
        goal_data = pd.DataFrame([[target_weight, weekly_workouts]], columns=["Target Weight", "Workouts/Week"])
        save_data(goal_data, GOALS_FILE)
        st.success("Goals saved!")

# -------------------- DASHBOARD --------------------

elif tabs == "Dashboard":
    st.header("📈 Your Fitness Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Workout Summary")
        workout_data = load_data(WORKOUT_FILE, ["Date", "Type", "Duration", "Calories", "Note"])
        if not workout_data.empty:
            st.dataframe(workout_data.tail(5))
            st.line_chart(workout_data.set_index("Date")[["Calories"]])
        else:
            st.info("No workout data available.")

    with col2:
        st.subheader("🍽 Calorie Intake Summary")
        cal_data = load_data(CALORIES_FILE, ["Date", "Food", "Calories", "Meal Type"])
        if not cal_data.empty:
            st.dataframe(cal_data.tail(5))
            st.bar_chart(cal_data.groupby("Meal Type")["Calories"].sum())
        else:
            st.info("No calorie data available.")

    st.subheader("📉 Weight Tracking")
    weight_data = load_data(WEIGHT_FILE, ["Date", "Weight"])
    if not weight_data.empty:
        st.line_chart(weight_data.set_index("Date"))
    else:
        st.info("No weight tracking data available.")

    st.subheader("🎯 Current Goals")
    goals = load_data(GOALS_FILE, ["Target Weight", "Workouts/Week"])
    if not goals.empty:
        st.write(goals.iloc[-1])
    else:
        st.info("No goals set yet.")
