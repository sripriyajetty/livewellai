import streamlit as st
import random

class SymptomCheckerBot:
    def __init__(self):

        # Database of symptoms and associated conditions
        # Format: {condition: {symptom1: weight, symptom2: weight, ...}}
        self.disease_database = {
            "Common Cold": {
                "runny nose": 0.8, 
                "sneezing": 0.9, 
                "cough": 0.7, 
                "sore throat": 0.6, 
                "headache": 0.5,
                "mild fever": 0.4,
                "fatigue": 0.3
            },
            "Influenza": {
                "fever": 0.9, 
                "chills": 0.8,
                "body aches": 0.8, 
                "fatigue": 0.9, 
                "cough": 0.7,
                "headache": 0.6,
                "sore throat": 0.5
            },
            "COVID-19": {
                "fever": 0.7, 
                "dry cough": 0.8, 
                "fatigue": 0.7, 
                "loss of taste": 0.9, 
                "loss of smell": 0.9,
                "shortness of breath": 0.7,
                "body aches": 0.6
            },
            "Migraine": {
                "intense headache": 0.9, 
                "sensitivity to light": 0.8, 
                "nausea": 0.7,
                "visual disturbances": 0.6,
                "sensitivity to sound": 0.7
            },
            "Allergies": {
                "sneezing": 0.8, 
                "runny nose": 0.7, 
                "itchy eyes": 0.9, 
                "watery eyes": 0.8,
                "congestion": 0.6
            },
            "Food Poisoning": {
                "nausea": 0.8, 
                "vomiting": 0.9, 
                "diarrhea": 0.9, 
                "abdominal cramps": 0.8,
                "fever": 0.5
            },
            "Gastroenteritis": {
                "nausea": 0.7, 
                "vomiting": 0.7, 
                "diarrhea": 0.9, 
                "abdominal pain": 0.8,
                "mild fever": 0.5,
                "fatigue": 0.6
            },
            "Bronchitis": {
                "persistent cough": 0.9, 
                "mucus production": 0.8, 
                "fatigue": 0.6, 
                "shortness of breath": 0.7,
                "chest discomfort": 0.7,
                "mild fever": 0.5
            },
            "Pneumonia": {
                "high fever": 0.8, 
                "cough with phlegm": 0.9, 
                "shortness of breath": 0.8, 
                "chest pain": 0.7,
                "fatigue": 0.7,
                "confusion": 0.5
            },
            "Urinary Tract Infection": {
                "frequent urination": 0.9, 
                "burning sensation during urination": 0.9, 
                "cloudy urine": 0.7,
                "strong-smelling urine": 0.7,
                "pelvic pain": 0.6
            }
        }
        
        # Disclaimer for medical advice
        self.disclaimer = ("IMPORTANT: This chatbot provides general information only and is not a substitute "
                          "for professional medical advice. Please consult a healthcare provider for proper diagnosis "
                          "and treatment.")
        
        # Follow-up questions
        self.follow_up_questions = [
            "How long have you been experiencing these symptoms?",
            "Are you currently taking any medications?",
            "Do you have any known allergies or medical conditions?",
            "Has anyone around you been sick with similar symptoms?",
            "Have you traveled recently to any areas with known outbreaks?"
        ]
    
    def analyze_symptoms(self, symptoms):
        """Analyze provided symptoms and determine possible conditions"""
        if not symptoms:
            return "I don't have any symptoms to analyze yet. Could you please describe what you're experiencing?"
        
        # Calculate scores for each disease based on matching symptoms
        disease_scores = {}
        
        for disease, disease_symptoms in self.disease_database.items():
            score = 0
            matches = 0
            matched_symptoms = []
            
            for patient_symptom in symptoms:
                for db_symptom, weight in disease_symptoms.items():
                    # Check if patient symptom contains database symptom
                    if db_symptom in patient_symptom.lower():
                        score += weight
                        matches += 1
                        matched_symptoms.append(db_symptom)
                        break
            
            # Only include diseases with at least one matching symptom
            if matches > 0:
                # Normalize score by the number of symptoms in the disease
                disease_scores[disease] = {
                    "score": score / len(disease_symptoms),
                    "matches": matches,
                    "matched_symptoms": matched_symptoms
                }
        
        # Sort diseases by score
        sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1]["score"], reverse=True)
        
        if not sorted_diseases:
            return ("Based on the symptoms you've described, I couldn't identify any specific conditions from my database. "
                   "This could mean your symptoms are too general or associated with conditions not in my knowledge base. "
                   "Please consult a healthcare professional for proper diagnosis and advice.")
        
        # Format response
        response = "Based on the symptoms you've described, here are some possible conditions to consider:\n\n"
        
        for i, (disease, data) in enumerate(sorted_diseases[:3], 1):
            confidence = data["score"] * 100
            response += f"{i}. {disease} (Confidence: {confidence:.1f}%)\n"
            response += f"   Matching symptoms: {', '.join(data['matched_symptoms'])}\n\n"
        
        response += f"\n{self.disclaimer}"
        
        return response, sorted_diseases[:3]

def main():
    st.set_page_config(
        page_title="Medical Symptom Checker",
        page_icon="🩺",
        layout="centered"
    )
    #st.write("Bot object:", st.session_state.bot)
    #st.write("Available methods:", dir(st.session_state.bot))

    # Initialize the bot
    if 'bot' not in st.session_state:
        st.session_state.bot = SymptomCheckerBot()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    # Initialize state variables
    if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []
    if 'current_follow_up' not in st.session_state:
        st.session_state.current_follow_up = 0
    if 'follow_up_answers' not in st.session_state:
        st.session_state.follow_up_answers = {}
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # App header
    st.title("Medical Symptom Checker")
    st.markdown(f"{st.session_state.bot.disclaimer}")
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Initial message
    if not st.session_state.messages:
        initial_message = "Hello! I'm a symptom checker chatbot designed to help identify possible conditions based on your symptoms. Please describe the symptoms you're experiencing. Try to be specific and include all symptoms, even ones that seem minor."
        st.session_state.messages.append({"role": "assistant", "content": initial_message})
        with st.chat_message("assistant"):
            st.markdown(initial_message)
    
    # Get user input
    if user_input := st.chat_input("Type your symptoms here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Process user input based on the current state
        if not st.session_state.symptoms:
            # First input: collect initial symptoms
            st.session_state.symptoms = [symptom.strip() for symptom in user_input.split(',')]
            
            # Perform initial analysis
            analysis, results = st.session_state.bot.analyze_symptoms(st.session_state.symptoms)
            st.session_state.analysis_results = results
            
            # Ask first follow-up question
            next_question = st.session_state.bot.follow_up_questions[st.session_state.current_follow_up]
            response = f"{analysis}\n\nTo help refine the assessment, I'd like to ask a few follow-up questions:\n\n{next_question}"
            
        elif st.session_state.current_follow_up < len(st.session_state.bot.follow_up_questions):
            # Record answer to current follow-up question
            current_question = st.session_state.bot.follow_up_questions[st.session_state.current_follow_up]
            st.session_state.follow_up_answers[current_question] = user_input
            st.session_state.current_follow_up += 1
            
            # If we have more follow-up questions, ask them
            if st.session_state.current_follow_up < len(st.session_state.bot.follow_up_questions):
                next_question = st.session_state.bot.follow_up_questions[st.session_state.current_follow_up]
                response = next_question
            else:
                # Final analysis
                st.session_state.analysis_complete = True
                analysis, _ = st.session_state.bot.analyze_symptoms(st.session_state.symptoms)
                
                response = "Based on all the information you've provided:\n\n"
                response += analysis
                
                response += "\n\nYour additional information:\n"
                for question, answer in st.session_state.follow_up_answers.items():
                    response += f"- {question} {answer}\n"
                
                response += ("\n\nWhat you should do next:\n"
                           "1. Consult with a healthcare professional for proper diagnosis\n"
                           "2. Share this preliminary assessment with your doctor\n"
                           "3. Monitor your symptoms and seek immediate care if they worsen\n\n"
                           "Would you like to add more symptoms or start a new assessment?")
        
        elif "new" in user_input.lower() or "start" in user_input.lower() or "again" in user_input.lower() or "reset" in user_input.lower():
            # Reset the session
            st.session_state.symptoms = []
            st.session_state.current_follow_up = 0
            st.session_state.follow_up_answers = {}
            st.session_state.analysis_complete = False
            st.session_state.analysis_results = None
            response = "Let's start a new assessment. Please describe the symptoms you're experiencing."
        
        else:
            # Add new symptoms
            new_symptoms = [symptom.strip() for symptom in user_input.split(',')]
            st.session_state.symptoms.extend(new_symptoms)
            analysis, results = st.session_state.bot.analyze_symptoms(st.session_state.symptoms)
            st.session_state.analysis_results = results
            response = f"{analysis}\n\nWould you like to add more symptoms or start a new assessment?"
        
        # Display assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    # Display sidebar with additional information
    with st.sidebar:
        st.header("About This Tool")
        st.write("This symptom checker uses basic pattern matching to suggest possible conditions based on reported symptoms.")
        
        st.divider()
        
        st.subheader("Current Assessment")
        if st.session_state.symptoms:
            st.write("Reported symptoms:")
            for symptom in st.session_state.symptoms:
                st.write(f"- {symptom}")
            
            if st.session_state.analysis_results:
                st.divider()
                st.subheader("Top Matches")
                for i, (disease, data) in enumerate(st.session_state.analysis_results, 1):
                    confidence = data["score"] * 100
                    st.write(f"{disease} ({confidence:.1f}%)")
        else:
            st.write("No symptoms reported yet.")
            
        st.divider()
        
        st.caption("Remember: This tool is for educational purposes only and does not replace professional medical advice.")
        
        if st.button("Start New Assessment"):
            # Reset all session state
            st.session_state.symptoms = []
            st.session_state.current_follow_up = 0
            st.session_state.follow_up_answers = {}
            st.session_state.analysis_complete = False
            st.session_state.analysis_results = None
            st.session_state.messages = [{"role": "assistant", "content": "Let's start a new assessment. Please describe the symptoms you're experiencing."}]
            st.rerun()

if __name__ == "__main__":
    main()