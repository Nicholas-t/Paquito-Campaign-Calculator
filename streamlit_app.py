import streamlit as st
import math
# Custom CSS to match Paquito.ai style more closely
custom_css = """
<style>
    body {
        color: #FFFFFF;
        background-color: #1A1A1A;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background-color: #1A1A1A;
    }
    h1 {
        color: #4A4A4A;
        font-size: 36px;
        font-weight: normal;
        margin-bottom: 30px;
    }
    .input-label {
        color: #B19CD9;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        color: #FFFFFF;
        background-color: #2E2E2E;
        border: 1px solid #444;
        border-radius: 25px;
        font-size: 16px;
        padding: 10px 15px;
    }
    .stButton > button {
        color: #000000;
        background: linear-gradient(90deg, #EEA4CA 0%, #94BBE9 100%);
        border: none;
        border-radius: 25px;
        font-size: 18px;
        padding: 12px 24px;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        opacity: 0.8;
        box-shadow: 0 0 15px rgba(238, 164, 202, 0.5);
    }
    .stExpander {
        background-color: #2E2E2E;
        border: 1px solid #444;
        border-radius: 15px;
        overflow: hidden;
    }
    .title {
        color: #B19CD9;
        font-size: 16px;
        font-weight: normal;
        margin-bottom: 10px;
    }
</style>
"""
st.set_page_config(page_title="ROI Calculator", layout="wide")
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h1>ROI Calculator</h1>", unsafe_allow_html=True)

# Number of leads
st.markdown('<p class="title">Number of leads</p>', unsafe_allow_html=True)
lead_options = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
num_leads = st.selectbox("", options=lead_options, format_func=lambda x: f"{x:,}")

# Number emails per lead
st.markdown('<p class="title">Number emails per lead</p>', unsafe_allow_html=True)
emails_per_lead = st.number_input("", min_value=1, max_value=10, value=2, step=1)

# Campaign duration in months
st.markdown('<p class="title">Campaign duration in months</p>', unsafe_allow_html=True)
campaign_duration = st.number_input("", min_value=1, max_value=12, value=6, step=1)

# Social media to target
st.markdown('<p class="title">Social media to target</p>', unsafe_allow_html=True)
social_media_campaign = st.selectbox("", ["Linkedin", "Instagram", "Twitter"])

# Advanced Settings
with st.expander("Advanced Settings"):
    working_days = st.number_input("Working days per month", min_value=1, max_value=31, value=20, step=1)
    email_limit_per_day = st.number_input("Emails limit per day", min_value=1, max_value=1000, value=30, step=10)
    warmup_period = st.number_input("Warm up period in weeks", min_value=1, max_value=12, value=3, step=1)
    mailboxes_per_domain = st.number_input("Mailboxes / domain", min_value=1, max_value=10, value=2, step=1)
    cost_per_mailbox_per_month = st.number_input("Cost per mailbox / month", min_value=0, max_value=100, value=3, step=1)
    cost_per_domain = st.number_input("Cost per domain", min_value=0, max_value=100, value=13, step=1)

def calculate_roi():
    total_emails = num_leads * emails_per_lead
    campaign_duration_in_days = campaign_duration * working_days
    emails_per_day = total_emails / campaign_duration_in_days
    
    mailboxes_needed = math.ceil(emails_per_day / email_limit_per_day)
    domains_needed = math.ceil(mailboxes_needed / mailboxes_per_domain)
    
    # Mailforge, Google, Outlook
    mailboxes_needed_list = [mailboxes_needed / 3] * 3
    domains_needed_list = [domains_needed / 3] * 3
    mailboxes_price = [3, 6, 6] # Price for mailforge, google, outlook
    monthly_cost_mailbox_list = [num_mb * pr for (num_mb, pr) in zip(mailboxes_needed_list, mailboxes_price)]
    monthly_cost_domain_list = [num_dom * cost_per_domain for num_dom in domains_needed_list]
    print("Mailbox needed  MF, Google, Outlook : {}".format(", ".join(mailboxes_needed_list)))
    print("Domains needed  MF, Google, Outlook : {}".format(", ".join(mailboxes_needed_list)))

    monthly_cost_mailboxes = sum(monthly_cost_mailbox_list) #mailboxes_needed * cost_per_mailbox_per_month
    monthly_cost_domains = sum(monthly_cost_domain_list) #domains_needed * cost_per_domain
    
    total_monthly_cost = monthly_cost_mailboxes + monthly_cost_domains
    total_cost = total_monthly_cost * campaign_duration

    cost_per_lead = total_cost / num_leads

    # Apply 80% margin
    monthly_monthly_paying_client_pricing = total_monthly_cost * 3
    
    return {
        "total_emails": total_emails,
        "emails_per_day": int(emails_per_day),
        #"mailboxes_needed": mailboxes_needed,
        #"domains_needed": domains_needed,
        "monthly_cost": total_monthly_cost,
        "monthly_monthly_paying_client_pricing": monthly_monthly_paying_client_pricing
    }

if st.button("Calculate ROI"):
    results = calculate_roi()
    
    st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total emails", f"{results['total_emails']:,}")
        st.metric("Emails per day", f"{results['emails_per_day']:,}")
    #with col2:
        # st.metric("Mailboxes needed", results['mailboxes_needed'])
        # st.metric("Domains needed", results['domains_needed'])
    
    st.markdown("<h3>Pricing</h3>", unsafe_allow_html=True)
    st.metric("Monthly price", f"${results['monthly_monthly_paying_client_pricing']:.2f}")
    
    # Display different plans
    st.markdown("<h3>Plans</h3>", unsafe_allow_html=True)
    plans = {
        "Basic":5,
        "Pro": 7,
        "Enterprise": 9
    }
    
    for plan, multiplier in plans.items():
        plan_price = results['monthly_monthly_paying_client_pricing'] * multiplier
        st.metric(f"{plan} Plan", f"${plan_price:.2f}/month")
