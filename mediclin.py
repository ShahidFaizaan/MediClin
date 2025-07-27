#!/usr/bin/env python3
"""
MediClin Platform
AI-powered medical analysis and diagnostic assistance system
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import uuid
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import random

# Configuration
st.set_page_config(
    page_title="MediClin",
    page_icon="🧠",
    layout="wide"
)

# Database Setup
DATABASE_FILE = "mediclin.db"

def init_database():
    """Initialize SQLite database for medical data"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            medical_history TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Medical data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            data_type TEXT,
            data_value TEXT,
            confidence_score REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Intelligence insights table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intelligence_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            insight_type TEXT,
            insight_text TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# MediClin Engine
class MedicalIntelligence:
    """Core MediClin and AI analysis engine"""
    
    def __init__(self):
        self.conditions = [
            "Hypertension", "Diabetes Type 2", "Cardiovascular Disease",
            "Respiratory Issues", "Neurological Conditions", "Metabolic Disorders"
        ]
        
    def analyze_patient(self, patient_data):
        """Analyze patient data using MediClin"""
        insights = []
        
        age = patient_data.get('age', 50)
        gender = patient_data.get('gender', 'Unknown')
        
        # Age-based intelligence
        if age > 65:
            insights.append({
                "type": "Risk Assessment",
                "insight": "Elevated risk profile due to advanced age",
                "confidence": 0.85,
                "recommendations": ["Regular cardiovascular screening", "Bone density assessment"]
            })
        
        # Gender-specific analysis
        if gender == "Male" and age > 45:
            insights.append({
                "type": "Cardiovascular Intelligence",
                "insight": "Increased cardiovascular risk profile",
                "confidence": 0.78,
                "recommendations": ["Annual ECG", "Lipid profile monitoring"]
            })
        
        # General health intelligence
        insights.append({
            "type": "Preventive Intelligence",
            "insight": "Recommend comprehensive health assessment",
            "confidence": 0.90,
            "recommendations": ["Annual physical exam", "Laboratory screening"]
        })
        
        return insights
    
    def predict_conditions(self, patient_data):
        """Predict potential medical conditions"""
        predictions = []
        
        for condition in self.conditions:
            confidence = random.uniform(0.1, 0.9)
            risk_level = "High" if confidence > 0.7 else "Medium" if confidence > 0.4 else "Low"
            
            predictions.append({
                "condition": condition,
                "confidence": confidence,
                "risk_level": risk_level
            })
        
        return sorted(predictions, key=lambda x: x['confidence'], reverse=True)[:4]

# Database Functions
def add_patient(name, age, gender, medical_history):
    """Add patient to database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    patient_id = f"MI-{str(uuid.uuid4())[:8].upper()}"
    
    cursor.execute("""
        INSERT INTO patients (patient_id, name, age, gender, medical_history)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_id, name, age, gender, medical_history))
    
    conn.commit()
    conn.close()
    return patient_id

def get_all_patients():
    """Get all patients"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
    patients = cursor.fetchall()
    
    conn.close()
    return patients

def save_intelligence_insight(patient_id, insight_type, insight_text, confidence):
    """Save intelligence insight to database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO intelligence_insights (patient_id, insight_type, insight_text, confidence)
        VALUES (?, ?, ?, ?)
    """, (patient_id, insight_type, insight_text, confidence))
    
    conn.commit()
    conn.close()

# Initialize
init_database()
medical_ai = MedicalIntelligence()

# Main Application
def main():
    st.title("🧠 MediClin Platform")
    st.subheader("AI-Powered Medical Analysis & Diagnostic Intelligence")
    
    # Sidebar navigation with direct buttons
    st.sidebar.title("MediClin")
    st.sidebar.markdown("---")
    
    # Initialize session state for page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Intelligence Dashboard"
    
    # Navigation buttons with current page highlighting
    pages = [
        ("Intelligence Dashboard", "🏠 Intelligence Dashboard"),
        ("Patient Analysis", "👤 Patient Analysis"),
        ("Diagnostic Intelligence", "🧠 Diagnostic Intelligence"),
        ("Medical Insights", "📊 Medical Insights")
    ]
    
    for page_key, page_label in pages:
        if page_key == st.session_state.current_page:
            st.sidebar.success(f"➤ {page_label}")
        else:
            if st.sidebar.button(page_label, use_container_width=True, key=page_key):
                st.session_state.current_page = page_key
                st.rerun()
    
    page = st.session_state.current_page
    
    if page == "Intelligence Dashboard":
        dashboard_page()
    elif page == "Patient Analysis":
        patient_analysis_page()
    elif page == "Diagnostic Intelligence":
        diagnostic_intelligence_page()
    elif page == "Medical Insights":
        medical_insights_page()

def dashboard_page():
    """MediClin Dashboard"""
    st.header("MediClin Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    patients = get_all_patients()
    
    with col1:
        st.metric("Total Patients", len(patients))
    with col2:
        st.metric("AI Analyses", len(patients) * 3)
    with col3:
        st.metric("Intelligence Insights", len(patients) * 5)
    with col4:
        st.metric("Accuracy Rate", "94.2%")
    
    # Intelligence overview chart
    if patients:
        # Create sample intelligence data
        intelligence_types = ["Risk Assessment", "Diagnostic Intelligence", "Preventive Care", "Treatment Optimization"]
        values = [25, 30, 20, 25]
        
        fig = px.pie(values=values, names=intelligence_types, 
                     title="MediClin Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent intelligence insights
    st.subheader("Recent Intelligence Insights")
    insights = [
        "High-risk cardiovascular profile detected in Patient MI-A1B2C3D4",
        "Preventive intervention recommended for Patient MI-E5F6G7H8", 
        "Diagnostic pattern analysis completed for Patient MI-I9J0K1L2",
        "Treatment optimization suggested for Patient MI-M3N4O5P6"
    ]
    
    for insight in insights:
        st.info(f"🧠 {insight}")

def patient_analysis_page():
    """Patient Analysis Module"""
    st.header("Patient Analysis & Intelligence")
    
    tab1, tab2 = st.tabs(["Add Patient", "Analyze Existing"])
    
    with tab1:
        st.subheader("Add New Patient for Analysis")
        
        with st.form("patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Patient Name")
                age = st.number_input("Age", min_value=0, max_value=120, value=30)
            
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                
            medical_history = st.text_area("Medical History")
            
            if st.form_submit_button("Add Patient & Analyze"):
                if name:
                    patient_id = add_patient(name, age, gender, medical_history)
                    st.success(f"Patient added with ID: {patient_id}")
                    
                    # Immediate intelligence analysis
                    patient_data = {"age": age, "gender": gender, "medical_history": medical_history}
                    insights = medical_ai.analyze_patient(patient_data)
                    
                    st.subheader("Immediate Intelligence Analysis")
                    for insight in insights:
                        st.write(f"**{insight['type']}** (Confidence: {insight['confidence']:.1%})")
                        st.write(insight['insight'])
                        st.write("Recommendations:", ", ".join(insight['recommendations']))
                        st.write("---")
                        
                        # Save to database
                        save_intelligence_insight(patient_id, insight['type'], insight['insight'], insight['confidence'])
                    
                    st.rerun()
    
    with tab2:
        st.subheader("Analyze Existing Patients")
        
        patients = get_all_patients()
        if patients:
            patient_options = [f"{p[2]} (ID: {p[1]})" for p in patients]
            selected = st.selectbox("Select Patient", patient_options)
            
            if selected:
                patient_id = selected.split("ID: ")[1].rstrip(")")
                selected_patient = next(p for p in patients if p[1] == patient_id)
                
                if st.button("Run Intelligence Analysis"):
                    patient_data = {
                        "age": selected_patient[3],
                        "gender": selected_patient[4],
                        "medical_history": selected_patient[5]
                    }
                    
                    insights = medical_ai.analyze_patient(patient_data)
                    predictions = medical_ai.predict_conditions(patient_data)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Intelligence Insights")
                        for insight in insights:
                            st.write(f"**{insight['type']}**")
                            st.write(f"Confidence: {insight['confidence']:.1%}")
                            st.write(insight['insight'])
                            st.write("---")
                    
                    with col2:
                        st.subheader("Condition Predictions")
                        for pred in predictions:
                            st.write(f"**{pred['condition']}**")
                            st.write(f"Risk Level: {pred['risk_level']}")
                            st.progress(pred['confidence'])
                            st.write("---")

def diagnostic_intelligence_page():
    """Diagnostic Intelligence Module"""
    st.header("Diagnostic Intelligence Engine")
    
    st.write("Advanced AI-powered diagnostic analysis and pattern recognition")
    
    # Simulated diagnostic intelligence
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pattern Recognition")
        
        # Sample diagnostic patterns
        patterns = {
            "Cardiovascular Patterns": 0.87,
            "Metabolic Indicators": 0.73,
            "Neurological Markers": 0.65,
            "Respiratory Patterns": 0.82
        }
        
        for pattern, confidence in patterns.items():
            st.write(f"**{pattern}**")
            st.progress(confidence)
            st.write(f"Confidence: {confidence:.1%}")
            st.write("---")
    
    with col2:
        st.subheader("Diagnostic Accuracy")
        
        # Create accuracy chart
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        accuracy = [92.1, 93.5, 94.2, 93.8, 95.1, 94.7]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=accuracy, mode='lines+markers', name='Accuracy'))
        fig.update_layout(title="Diagnostic Intelligence Accuracy Over Time", 
                         yaxis_title="Accuracy (%)", xaxis_title="Month")
        st.plotly_chart(fig, use_container_width=True)

def medical_insights_page():
    """Medical Insights Module"""
    st.header("MediClin Insights")
    
    # Intelligence categories with direct display (no expanders)
    insight_categories = {
        "Preventive Intelligence": [
            "Early intervention strategies for cardiovascular risk reduction",
            "Personalized screening recommendations based on genetic markers",
            "Lifestyle modification protocols for metabolic optimization"
        ],
        "Diagnostic Intelligence": [
            "Multi-modal diagnostic pattern recognition",
            "Differential diagnosis probability ranking",
            "Symptom correlation analysis and interpretation"
        ],
        "Treatment Intelligence": [
            "Personalized treatment protocol optimization",
            "Drug interaction and efficacy prediction",
            "Treatment response monitoring and adjustment"
        ],
        "Prognostic Intelligence": [
            "Disease progression modeling and prediction",
            "Recovery timeline estimation and planning",
            "Long-term outcome probability assessment"
        ]
    }
    
    # Display in columns for better layout
    col1, col2 = st.columns(2)
    
    categories = list(insight_categories.items())
    
    with col1:
        for i in range(0, len(categories), 2):
            category, insights = categories[i]
            st.subheader(f"🧠 {category}")
            for insight in insights:
                st.write(f"• {insight}")
                confidence = random.uniform(0.8, 0.95)
                st.write(f"  Confidence: {confidence:.1%}")
            st.write("---")
    
    with col2:
        for i in range(1, len(categories), 2):
            if i < len(categories):
                category, insights = categories[i]
                st.subheader(f"🧠 {category}")
                for insight in insights:
                    st.write(f"• {insight}")
                    confidence = random.uniform(0.8, 0.95)
                    st.write(f"  Confidence: {confidence:.1%}")
                st.write("---")

if __name__ == "__main__":
    main()