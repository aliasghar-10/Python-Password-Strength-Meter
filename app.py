# Description: A simple password strength meter web app built with Streamlit.
import re
import random
import streamlit as st

def evaluate_password(password):
    score = 0
    feedback = []
    blacklist = ["password123", "123456", "qwerty", "letmein", "admin"]

    # Check if password is blacklisted
    if password in blacklist:
        feedback.append("This password is too common and easily guessable. Please choose another.")
        return "Weak", 0, feedback

    # Custom scoring weights
    weights = {
        "length": 2,
        "case": 2,
        "digit": 1,
        "special": 1
    }

    # Check length
    if len(password) >= 8:
        score += weights["length"]
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Check for uppercase and lowercase letters
    if any(char.islower() for char in password) and any(char.isupper() for char in password):
        score += weights["case"]
    else:
        feedback.append("Password should contain both uppercase and lowercase letters.")

    # Check for digits
    if any(char.isdigit() for char in password):
        score += weights["digit"]
    else:
        feedback.append("Password should include at least one digit (0-9).")

    # Check for special characters
    if re.search(r'[!@#$%^&*]', password):
        score += weights["special"]
    else:
        feedback.append("Password should have at least one special character (!@#$%^&*).")

    # Determine strength
    if score <= 2:
        strength = "Weak"
    elif 3 <= score <= 5:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, score, feedback

def generate_password():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return ''.join(random.choices(characters, k=12))

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered", initial_sidebar_state="auto")

    st.markdown(
        """
        <style>
        body {
            background-color: #f0f0f0;
            color: black;
        }
        .stButton>button {
            background-color: #30b535;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: darkgreen;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🔐 Password Strength Meter")
    st.write("Evaluate the strength of your password and get suggestions to improve it.")

    password = st.text_input("Enter your password:", type="password")

    if st.button("Check Strength"):
        if password:
            strength, score, feedback = evaluate_password(password)

            st.subheader(f"Password Strength: {strength}")
            st.write(f"Score: {score}/6")

            if strength == "Weak":
                st.warning("Your password is weak. Here are some suggestions:")
                for suggestion in feedback:
                    st.write(f"- {suggestion}")
            elif strength == "Strong":
                st.success("Great job! Your password is strong.")
            else:
                st.info("Your password is moderate. Consider the suggestions below:")
                for suggestion in feedback:
                    st.write(f"- {suggestion}")
        else:
            st.error("Please enter a password to evaluate.")

    if st.button("Generate Strong Password"):
        strong_password = generate_password()
        st.success(f"Here is a strong password you can use: {strong_password}")

if __name__ == "__main__":
    main()
