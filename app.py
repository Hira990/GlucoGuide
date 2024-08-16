import streamlit as st
import anthropic

# Initialize Anthropic client with API key
api_key = st.secrets["claude_api_key"]
client = anthropic.Client(api_key=api_key)

# Function to get a personalized meal plan from Claude AI
def get_meal_plan(fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences):
    # Prepare the prompt for Claude AI
    prompt = (
        f"\n\nHuman: My fasting sugar level is {fasting_sugar} mg/dL, "
        f"pre-meal sugar level is {pre_meal_sugar} mg/dL, "
        f"post-meal sugar level is {post_meal_sugar} mg/dL, "
        f"and my dietary preference is {dietary_preferences}. "
        "Can you suggest a personalized meal plan with calculated calories?\n\nAssistant:"
    )

    # Call the Claude AI model using the correct API method and arguments
    response = client.completions.create(
        model="claude-2",  # Adjust the model name according to the API you're using
        prompt=prompt,
        max_tokens_to_sample=500,  # Use max_tokens_to_sample instead of max_tokens
        temperature=0.7,
    )

    # Return the content of the response
    return response.completion.strip()  # Access the 'completion' attribute directly

# Streamlit app interface
st.title("GlucoGuide")

# Description of the app
st.markdown("""
    **Welcome to GlucoGuide!**

    App designed to help diabetic patients receive personalized meal suggestions based on blood sugar levels and dietary preferences. By entering your fasting, pre-meal, and post-meal sugar levels, along with your dietary preferences, you can get customized meal plans to help manage your diabetes more effectively.

""")

# Sidebar Inputs
st.sidebar.header("Enter Your Details")

# Input fields in the sidebar
fasting_sugar = st.sidebar.number_input("Fasting Sugar Level (mg/dL)", min_value=0, max_value=500, step=1)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Level (mg/dL)", min_value=0, max_value=500, step=1)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Level (mg/dL)", min_value=0, max_value=500, step=1)

# Dietary preferences dropdown
dietary_preferences = st.sidebar.selectbox(
    "Dietary Preferences",
    ("No Preference", "Vegetarian", "Vegan", "Low Carb", "High Protein", "Gluten-Free", "Other")
)

# Button to get a meal plan
if st.sidebar.button("Get Meal Plan"):
    # Ensure the API key is provided
    if not api_key:
        st.error("Please enter your Claude API key.")
    else:
        meal_plan = get_meal_plan(fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences)
        st.subheader("Your Personalized Meal Plan")
        st.write(meal_plan)

# Footer or additional information
st.markdown("---")
st.write("This app is for informational purposes only and is not a substitute for professional medical advice.")
