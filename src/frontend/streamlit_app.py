import streamlit as st
import requests
from PIL import Image
import io
import base64
import time
from typing import List, Tuple
import os
import sys

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Page configuration
st.set_page_config(
    page_title="🌱 KissanAI - Crop Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/anasdev-10/KisanAI',
        'Report a bug': 'https://github.com/anasdev-10/KisanAI/issues',
        'About': '# KissanAI - Advanced Crop Disease Detection using AI'
    }
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Green Theme with Enhanced Design */
    .main-header {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%);
        padding: 3rem;
        border-radius: 25px;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        box-shadow: 0 15px 40px rgba(34, 197, 94, 0.4);
        border: 3px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .main-header h1 {
        font-size: 3.5em;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.5em;
        opacity: 0.95;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .upload-area {
        border: 4px dashed #22c55e;
        border-radius: 25px;
        padding: 4rem;
        text-align: center;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%);
        margin: 2rem 0;
        transition: all 0.5s ease;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .upload-area::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(34, 197, 94, 0.1) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .upload-area:hover {
        border-color: #16a34a;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 50%, #a7f3d0 100%);
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(34, 197, 94, 0.3);
    }
    
    .result-card {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%);
        padding: 3rem;
        border-radius: 30px;
        margin: 2rem 0;
        border: none;
        box-shadow: 0 20px 50px rgba(34, 197, 94, 0.4);
        color: white;
        font-size: 1.4em;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(15px);
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #fbbf24, #f59e0b, #d97706, #fbbf24);
        animation: shimmer 2.5s infinite;
    }
    
    .result-card h4 {
        color: white;
        font-size: 1.8em;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .result-card p {
        color: white;
        font-size: 1.5em;
        margin: 1rem 0;
        font-weight: 600;
        line-height: 1.8;
    }
    
    .result-card strong {
        color: #fbbf24;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-size: 1.1em;
    }
    
    .prediction-highlight {
        background: rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        border-left: 8px solid #fbbf24;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .confidence-highlight {
        background: rgba(251, 191, 36, 0.25);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        border-left: 8px solid #fbbf24;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Light Theme Styles */
    .light-theme {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%);
        color: #1f2937;
    }
    
    .light-theme .upload-area {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 50%, #dcfce7 100%);
        border-color: #22c55e;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.25);
    }
    
    .light-theme .result-card {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%);
        box-shadow: 0 20px 50px rgba(34, 197, 94, 0.5);
    }
    
    /* Dark Theme Styles */
    .dark-theme {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
        color: white;
    }
    
    .dark-theme .upload-area {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
        border-color: #22c55e;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4);
    }
    
    .dark-theme .result-card {
        background: linear-gradient(135deg, #15803d 0%, #16a34a 50%, #22c55e 100%);
        box-shadow: 0 20px 50px rgba(34, 197, 94, 0.6);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #22c55e, #16a34a, #15803d);
        border-radius: 20px;
        height: 20px;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
    }
    
    .file-uploader {
        margin: 2rem 0;
    }
    
    .success-message {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 12px 35px rgba(34, 197, 94, 0.4);
        border: 3px solid rgba(255, 255, 255, 0.2);
        font-size: 1.2em;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #b91c1c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 12px 35px rgba(239, 68, 68, 0.4);
        border: 3px solid rgba(255, 255, 255, 0.2);
        font-size: 1.2em;
    }
    
    .results-section {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(22, 163, 74, 0.15) 50%, rgba(21, 128, 61, 0.15) 100%);
        padding: 3rem;
        border-radius: 30px;
        margin: 3rem 0;
        border: 4px solid #22c55e;
        box-shadow: 0 15px 40px rgba(34, 197, 94, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .results-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(34, 197, 94, 0.1) 0%, transparent 50%);
    }
    
    .results-title {
        color: #15803d;
        font-size: 3em;
        font-weight: 900;
        text-align: center;
        margin-bottom: 3rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #15803d, #16a34a, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
    }
    
    .summary-card {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%);
        color: white;
        padding: 3rem;
        border-radius: 25px;
        margin: 3rem 0;
        text-align: center;
        box-shadow: 0 15px 40px rgba(34, 197, 94, 0.4);
        border: 3px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .summary-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: rotate 15s linear infinite;
    }
    
    .summary-card h3 {
        color: #fbbf24;
        font-size: 2.2em;
        margin-bottom: 1.5rem;
        font-weight: bold;
        position: relative;
        z-index: 1;
    }
    
    .summary-card p {
        font-size: 1.4em;
        margin: 1rem 0;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }
    
    .summary-card strong {
        color: #fbbf24;
        font-weight: bold;
        font-size: 1.1em;
    }
    
    /* Fix for code formatting issue */
    .result-card * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%);
        border: none;
        border-radius: 20px;
        padding: 1rem 2.5rem;
        font-weight: bold;
        font-size: 1.1em;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 35px rgba(34, 197, 94, 0.6);
    }
    
    /* Theme toggle button */
    .theme-toggle {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 1rem 2rem;
        font-weight: bold;
        font-size: 1.1em;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4);
        transition: all 0.4s ease;
        cursor: pointer;
    }
    
    .theme-toggle:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 35px rgba(34, 197, 94, 0.6);
    }
    
    /* Enhanced icons and text */
    .icon-large {
        font-size: 2em;
        margin: 0 0.5rem;
    }
    
    .text-large {
        font-size: 1.3em;
        font-weight: 600;
    }
    
    /* Improved spacing */
    .section-spacing {
        margin: 3rem 0;
        padding: 2rem 0;
    }
    
    /* Enhanced text visibility */
    .stMarkdown {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    .stMarkdown strong {
        color: #15803d !important;
        font-weight: 800 !important;
    }
    
    /* Better contrast for all text */
    .stText {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* Enhanced button text visibility */
    .stButton > button {
        color: white !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Better visibility for file uploader text */
    .stFileUploader {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* Enhanced progress text */
    .stProgress > div > div > div > div {
        color: white !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False  # Light theme as default
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'results' not in st.session_state:
    st.session_state.results = []

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

def predict_disease(image_bytes: bytes, filename: str) -> Tuple[str, float]:
    """Send image to FastAPI backend for prediction"""
    try:
        files = {"file": (filename, image_bytes, "image/jpeg")}
        response = requests.post("http://127.0.0.1:8000/predict/", files=files)
        
        if response.status_code == 200:
            data = response.json()
            predicted_class = data.get("predicted_class", "Unknown")
            confidence = float(data.get("confidence", "0").replace("%", ""))
            
            # Enhanced success message
            st.markdown(f"""
            <div class="success-message">
                ✅ <strong>{filename}</strong><br>
                🌱 Disease: <strong>{predicted_class}</strong><br>
                📊 Confidence: <strong>{confidence:.2f}%</strong>
            </div>
            """, unsafe_allow_html=True)
            
            return predicted_class, confidence
        else:
            st.markdown(f"""
            <div class="error-message">
                ❌ API Error for {filename}<br>
                Status: {response.status_code}
            </div>
            """, unsafe_allow_html=True)
            return "Error", 0.0
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ Error predicting {filename}<br>
            {str(e)}
        </div>
        """, unsafe_allow_html=True)
        return "Error", 0.0

def display_header():
    """Display the main header with dark mode toggle"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>🌱 KissanAI - Crop Disease Detection</h1>
            <p>Upload multiple leaf images to detect plant diseases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Show correct button text based on current theme
        button_text = "🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"
        if st.button(button_text, key="theme_toggle"):
            toggle_dark_mode()
            st.rerun()

def display_upload_section():
    """Display file upload section"""
    st.markdown("### 📁 Upload Leaf Images")
    
    # File uploader with key to control state
    uploaded_files = st.file_uploader(
        "Choose image files",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        help="Upload multiple images for batch prediction",
        key="file_uploader"
    )
    
    # Update session state when files are uploaded
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
    
    # Display files from session state
    if st.session_state.uploaded_files:
        # Display image previews with proper sizing
        st.markdown("### 📸 Image Previews")
        
        # Calculate number of columns based on number of images
        num_cols = min(4, len(st.session_state.uploaded_files))
        cols = st.columns(num_cols)
        
        for idx, file in enumerate(st.session_state.uploaded_files):
            col_idx = idx % num_cols
            with cols[col_idx]:
                # Display image with controlled size
                st.image(
                    file, 
                    caption=file.name, 
                    width=200,  # Fixed width
                    use_container_width=False  # Don't use full container width
                )
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🗑️ Clear All", type="secondary", key="clear_all"):
                # Clear all session state
                st.session_state.uploaded_files = []
                st.session_state.results = []
                # Clear the file uploader widget
                st.session_state.file_uploader = None
                st.rerun()
        
        with col2:
            if st.button("🔍 Predict Diseases", type="primary", key="predict"):
                return True
        
        with col3:
            st.write(f"📊 {len(st.session_state.uploaded_files)} images selected")
    
    return False

def run_predictions():
    """Run predictions on uploaded files"""
    if not st.session_state.uploaded_files:
        st.warning("Please upload images first!")
        return
    
    # Progress bar for overall process
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    total_files = len(st.session_state.uploaded_files)
    
    for idx, file in enumerate(st.session_state.uploaded_files):
        status_text.text(f"Processing {file.name}... ({idx + 1}/{total_files})")
        
        # Read file bytes
        file_bytes = file.read()
        file.seek(0)  # Reset file pointer
        
        # Predict
        predicted_class, confidence = predict_disease(file_bytes, file.name)
        
        results.append({
            'filename': file.name,
            'predicted_class': predicted_class,
            'confidence': confidence
        })
        
        # Update progress
        progress_bar.progress((idx + 1) / total_files)
        time.sleep(0.1)  # Small delay for visual feedback
    
    status_text.text("✅ All predictions completed!")
    time.sleep(1)
    status_text.empty()
    progress_bar.empty()
    
    # Store results and rerun to display them
    st.session_state.results = results
    st.rerun()

def display_results():
    """Display prediction results"""
    if st.session_state.results and len(st.session_state.results) > 0:
        # Create a prominent results section
        st.markdown("""
        <div class="results-section">
            <div class="results-title">🎯 PREDICTION RESULTS</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display each result with enhanced styling
        for idx, result in enumerate(st.session_state.results):
            with st.container():
                # Main result card with enhanced styling
                st.markdown(f"""
                <div class="result-card">
                    <h4>📄 {result['filename']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Use Streamlit components for prediction details with better visibility
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🌱 DISEASE DETECTED:**")
                    # Use a custom styled info box for better visibility
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); 
                                color: white; 
                                padding: 1.5rem; 
                                border-radius: 15px; 
                                border: 3px solid #fbbf24; 
                                box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4);
                                font-size: 1.3em; 
                                font-weight: bold; 
                                text-align: center;
                                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        {result['predicted_class']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**📊 CONFIDENCE LEVEL:**")
                    # Use a custom styled success box for better visibility
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); 
                                color: #1f2937; 
                                padding: 1.5rem; 
                                border-radius: 15px; 
                                border: 3px solid #22c55e; 
                                box-shadow: 0 8px 25px rgba(251, 191, 36, 0.4);
                                font-size: 1.3em; 
                                font-weight: bold; 
                                text-align: center;
                                text-shadow: 1px 1px 2px rgba(255,255,255,0.5);">
                        {result['confidence']:.2f}%
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced progress bar
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(result['confidence'] / 100)
                with col2:
                    st.markdown(f"**{result['confidence']:.1f}%**")
                
                # Add spacing between results
                st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary section
        total_results = len(st.session_state.results)
        avg_confidence = sum(r['confidence'] for r in st.session_state.results) / total_results
        
        st.markdown(f"""
        <div class="summary-card">
            <h3>📈 SUMMARY</h3>
            <p><strong>Total Images Processed:</strong> {total_results}</p>
            <p><strong>Average Confidence:</strong> {avg_confidence:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear results button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Clear All Results", type="secondary", use_container_width=True):
                st.session_state.results = []
                st.rerun()

def main():
    """Main application function"""
    # Apply theme based on session state
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%);
                color: #1f2937;
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Display header
    display_header()
    
    # Main content area
    with st.container():
        # Upload section
        should_predict = display_upload_section()
        
        # Run predictions if requested
        if should_predict:
            run_predictions()
        
        # Display results
        display_results()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%); color: white; border-radius: 15px; box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4); border: 3px solid rgba(255, 255, 255, 0.2); font-size: 1.2em; font-weight: bold;">
        🚀 Developed by Muhammad Anas
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 