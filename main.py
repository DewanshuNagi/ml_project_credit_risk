import streamlit as st
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
from prediction_helper import predict

# Initialize session state for reset functionality
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

# Set the page configuration
st.set_page_config(
    page_title="Lauki Finance: Credit Risk Modelling",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
/* General background color */
body {
    background-color: #0c0d0e; /* Darker background to match the screenshot */
}

.stApp {
    background-color: #0c0d0e; /* Apply to the main app container */
}

.bank-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
}

.bank-building {
    width: 40px;
    height: 40px;
    margin-right: 10px;
}

/* Results container background and border */
.results-container {
    margin-top: 20px;
    padding: 15px;
    background-color: #1a1a1a; /* Darker background for the results section */
    border-radius: 10px;
    border: 1px solid #333; /* Darker border */
}

.metric-container {
    margin-bottom: 15px;
}

/* Fix for metric display - this targets st.metric, but we're using custom divs for results */
.stMetric {
    background-color: #1a1a1a; /* Darker background for default metrics if any */
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #333;
}

/* Custom metric for Loan to Income Ratio */
.custom-metric {
    background: #1a1a1a; /* Darker background */
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    margin: 10px 0;
    border: 2px solid #007bff; /* Changed to blue border */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.custom-metric h4 {
    color: #bbb; /* Lighter text for labels */
    margin: 0 0 5px 0;
    font-size: 14px;
    font-weight: normal;
}

.custom-metric h2 {
    color: #007bff; /* Blue for Loan to Income Ratio value */
    margin: 0;
    font-size: 24px;
    font-weight: bold;
}

/* Style for input fields to match dark theme */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background-color: #2b2b2b; /* Darker background for input fields */
    color: #eee; /* Lighter text color */
    border: 1px solid #444; /* Darker border */
    border-radius: 5px;
}

/* Style for labels */
.stTextInput label,
.stNumberInput label,
.stSelectbox label {
    color: #ccc; /* Lighter text for labels */
}

/* Style for subheader in results */
.st-emotion-blockquote { /* Targets st.subheader and similar elements */
    color: #eee; /* Lighter color for subheaders */
}

/* Specific styling for the prediction result metrics */
.result-metric-box {
    background: #1a1a1a; /* Darker background for result boxes */
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    width: 100%; /* Make each result box take full width */
    max-width: 400px; /* Optional: set a max-width if they get too wide on large screens */
    margin-left: auto; /* Center the box */
    margin-right: auto; /* Center the box */
}

.result-metric-box h4 {
    color: #bbb; /* Lighter text for labels */
    margin: 0 0 5px 0;
    font-size: 14px;
}

.result-metric-box h2 {
    margin: 0;
    font-size: 24px;
    font-weight: bold;
}

/* Specific colors for result metrics */
.result-metric-box.probability {
    border: 2px solid #007bff; /* Blue border */
}
.result-metric-box.probability h2 {
    color: #007bff; /* Blue text */
}

.result-metric-box.credit-score {
    border: 2px solid #007bff; /* Blue border */
}
.result-metric-box.credit-score h2 {
    color: #007bff; /* Blue text */
}

.result-metric-box.credit-rating {
    /* Border color will be set dynamically in Python */
}

/* Adjust button styling */
.stButton>button {
    background-color: #007bff; /* Blue background */
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.stButton>button:hover {
    background-color: #0056b3; /* Darker blue on hover */
}

</style>
""", unsafe_allow_html=True)

# Bank logo with building icon
st.markdown("""
<div class="bank-logo">
    <svg class="bank-building" viewBox="0 0 24 24" fill="#007bff">
        <path d="M12 1l9 4v2H3V5l9-4zM5 8h2v8H5V8zm4 0h2v8H9V8zm4 0h2v8h-2V8zm4 0h2v8h-2V8zM3 17h18v2H3v-2z"/>
        <text x="12" y="14" text-anchor="middle" fill="white" font-size="6" font-weight="bold">BANK</text>
    </svg>
    <h1 style="margin: 0; color: #007bff;">Lauki Finance: Credit Risk Modelling</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Define categorical options
categorical_options = {
    'Residence Type': ['Owned', 'Rented', 'Mortgage'],
    'Loan Purpose': ['Education', 'Home', 'Auto', 'Personal'],
    'Loan Type': ['Unsecured', 'Secured']
}

# Create four rows of three columns each
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

# Row 1: Personal Information
with row1[0]:
    age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28,
                          help="Enter your current age (18-100 years)",
                          key=f'age_{st.session_state.reset_key}')
with row1[1]:
    income = st.number_input('Income', min_value=0, value=1200000,
                             help="Enter your annual income",
                             key=f'income_{st.session_state.reset_key}')
with row1[2]:
    loan_amount = st.number_input('Loan Amount', min_value=0, value=2560000,
                                  help="Enter the requested loan amount",
                                  key=f'loan_amount_{st.session_state.reset_key}')

# Row 2: Loan Details
with row2[0]:
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=1, step=1, value=36,
                                         help="Loan tenure in months",
                                         key=f'tenure_{st.session_state.reset_key}')
with row2[1]:
    avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20,
                                              help="Average Days Past Due per delinquency",
                                              key=f'dpd_{st.session_state.reset_key}')
with row2[2]:
    delinquency_ratio = st.number_input('Delinquency Ratio', min_value=0, max_value=100, step=1, value=30,
                                        help="Delinquency ratio percentage",
                                        key=f'delinq_ratio_{st.session_state.reset_key}')

# Row 3: Financial Ratios and Accounts
with row3[0]:
    credit_utilization_ratio = st.number_input('Credit Utilization Ratio', min_value=0, max_value=100, step=1, value=30,
                                               help="Credit utilization percentage",
                                               key=f'credit_util_{st.session_state.reset_key}')
with row3[1]:
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2,
                                        help="Number of open loan accounts",
                                        key=f'open_accounts_{st.session_state.reset_key}')
with row3[2]:
    # Calculate and display loan to income ratio using custom HTML instead of st.metric
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    st.markdown(
        f"""
        <div class="custom-metric">
            <h4>Loan to Income Ratio</h4>
            <h2>{loan_to_income_ratio:.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Row 4: Categorical Variables
with row4[0]:
    residence_type = st.selectbox('Residence Type', categorical_options['Residence Type'], index=0,
                                  help="Type of residence",
                                  key=f'residence_{st.session_state.reset_key}')
with row4[1]:
    loan_purpose = st.selectbox('Loan Purpose', categorical_options['Loan Purpose'], index=0,
                                help="Purpose of the loan",
                                key=f'purpose_{st.session_state.reset_key}')
with row4[2]:
    loan_type = st.selectbox('Loan Type', categorical_options['Loan Type'], index=0,
                             help="Type of loan (secured/unsecured)",
                             key=f'type_{st.session_state.reset_key}')

# Create columns for buttons with better spacing
button_cols = st.columns([1, 1, 2])

# Add predict button
with button_cols[0]:
    if st.button('🔮 Calculate Risk', key='predict_button', use_container_width=True, type="primary"):
        # Basic validation
        if age < 18:
            st.error("Age must be at least 18 years.")
        elif income <= 0:
            st.error("Income must be greater than 0.")
        elif loan_amount <= 0:
            st.error("Loan amount must be greater than 0.")
        else:
            with st.spinner('Analyzing credit risk...'):
                try:
                    # Call the predict function from the helper module
                    probability, credit_score, rating = predict(
                        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
                        residence_type, loan_purpose, loan_type
                    )

                    # Create a proper results container
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)

                    # Display results one after another
                    st.subheader("📊 Risk Assessment Results")

                    st.markdown(
                        f"""
                        <div class="result-metric-box probability">
                            <h4>Default Probability</h4>
                            <h2>{probability:.1%}</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="result-metric-box credit-score">
                            <h4>Credit Score</h4>
                            <h2>{credit_score}</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Determine color based on rating
                    rating_color = {
                        'Poor': '#ff4444',
                        'Average': '#ff8800',
                        'Good': '#44aa44',
                        'Excellent': '#00aa44'
                    }.get(rating, '#666666')

                    st.markdown(
                        f"""
                        <div class="result-metric-box credit-rating" style="border: 2px solid {rating_color};">
                            <h4>Credit Rating</h4>
                            <h2 style="color: {rating_color};">{rating}</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown('</div>', unsafe_allow_html=True)

                    # Success message
                    st.success("✅ Credit risk analysis completed successfully!")

                except Exception as e:
                    st.error(f'Error during prediction: {str(e)}')
                    st.info("Please check your `prediction_helper.py` file and ensure all dependencies are installed.")

# Add reset button - FIXED: Remove st.rerun() to prevent infinite loop
with button_cols[1]:
    if st.button('🔄 Reset All Fields', key='reset_button', use_container_width=True):
        # Simply increment the reset key - Streamlit will automatically rerun
        # and all widgets will reset to their default values due to new keys
        st.session_state.reset_key += 1
        st.success("All fields have been reset to default values!")
        # REMOVED: st.rerun() - This was causing the infinite loop!