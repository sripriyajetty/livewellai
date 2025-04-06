import streamlit as st

# Title
st.title("🥗 AI Meal Planner")

# Description
st.write("Plan your meals based on your daily calorie requirement.")

# Calorie input
calories = st.slider("Select your daily calorie goal:", 1000, 4000, 2000, step=100)

# Example meal database (You can replace this with a more dynamic or AI-based one)
meals = {
    1500: {
        "Breakfast": "Oatmeal with banana and almond butter",
        "Lunch": "Grilled chicken salad with olive oil vinaigrette",
        "Dinner": "Baked salmon, brown rice, and steamed broccoli",
        "Snacks": "Greek yogurt with honey"
    },
    2000: {
        "Breakfast": "Avocado toast and boiled eggs",
        "Lunch": "Turkey sandwich on whole wheat bread, side salad",
        "Dinner": "Stir-fried tofu and veggies with quinoa",
        "Snacks": "Protein shake and an apple"
    },
    2500: {
        "Breakfast": "Protein pancakes with berries and peanut butter",
        "Lunch": "Grilled chicken burrito bowl with beans and rice",
        "Dinner": "Beef stir-fry with veggies and noodles",
        "Snacks": "Mixed nuts and banana"
    },
    3000: {
        "Breakfast": "Smoothie bowl with granola, nuts, and fruit",
        "Lunch": "Chicken pasta with pesto and veggies",
        "Dinner": "Grilled steak, mashed potatoes, and asparagus",
        "Snacks": "Cottage cheese, trail mix"
    },
    3500: {
        "Breakfast": "Omelette with cheese, spinach, and whole wheat toast",
        "Lunch": "Double chicken wrap with hummus and veggies",
        "Dinner": "Salmon, sweet potato fries, and sautéed spinach",
        "Snacks": "Protein bar and dried fruits"
    },
    4000: {
        "Breakfast": "Full English breakfast with fruit smoothie",
        "Lunch": "Double beef burger with whole grain bun, salad and avocado",
        "Dinner": "High-calorie pasta with meatballs and side of garlic bread",
        "Snacks": "Nut butter sandwich, granola bars, trail mix"
    }
}

# Get closest plan available
closest_cal = min(meals.keys(), key=lambda x: abs(x - calories))
plan = meals[closest_cal]

st.subheader(f"📋 Meal Plan for {closest_cal} Calories")

# Show meal plan
for meal_time, meal_desc in plan.items():
    st.markdown(f"{meal_time}: {meal_desc}")

# Extra customization (optional)
st.write("---")
st.write("📌 This is a general plan. For medical conditions or allergies, consult a nutritionist.")