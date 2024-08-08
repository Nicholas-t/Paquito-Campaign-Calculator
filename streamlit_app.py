
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import random 
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stApp {
    background-color: black
}

[data-testid='stVerticalBlock'] > .element-container > div[class*=Input] {
    padding: 10px;
    max-width: 90%;
    color: rgba(255,255,255,0.588);
    border: solid 1px #FAFAFA;
    border-radius: 20px;
    background-color: transparent;
    width: 100%;
}
[data-testid='stMarkdownContainer']{
  color: rgb(238,174,202);
}
div.stButton button [data-testid='stMarkdownContainer']{
  color: black;
}
div.stButton button {
    color: black !important;
    background: rgb(238,174,202);
    background: linear-gradient(90deg, rgba(238,174,202,1) 0%, rgba(148,187,233,1) 100%);
    -webkit-box-shadow: 1px 9px 38px 0px rgb(238,174,202); 
    box-shadow: 1px 9px 38px 0px rgb(238,174,202);   
    width: 100%;
    font-size: 20px;
    font-weight: 400;
    padding: 10px 10px;
    border-radius: 20px;
    cursor: pointer;
    margin-bottom: 10px;
    transition: 0.3s;
}
div.stButton  button:hover{
    background: white !important;
    color: black;
    border: 2px solid #E8ACAC;
}

[data-testid='stMetricValue']{
    color: white;
}
</style>
"""


import math
def calculate_num_mailbox(total_email):
    if (total_email > 1000):
        num_need = 5
        return num_need + math.ceil(total_email / 10000 * 15)
    else:
        return 5

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.title("ROI Calculator") 

NUM_OF_LEADS = st.number_input("Number of leads", step=1, value=10000, max_value=100000)
EMAILS_PER_LEAD = st.number_input("Number emails per lead", step=1, value=4)
CAMPAIGN_DURATION = st.number_input("Campaign duration in months", step=1, value=6)

SOCIAL_MEDIA_COST_DIC = {
    "Linkedin" : 0.005,
    "Instagram" : 0.003,
    "Twitter" : 0.002
}

SOCIAL_MEDIA_CAMPAIGN_TO_INCLUDE = st.selectbox("Social media to target", SOCIAL_MEDIA_COST_DIC.keys())


with st.expander("Advanced Settings"):
    WORKING_DAYS = st.number_input("Working days per month", value=20)
    EMAIL_LIMIT_PER_DAY = st.number_input("Working days per month", value=30)
    WARMUP_PERIOD = st.number_input("Warm up period in weeks", value=3, min_value=2)
    MAILBOXES_PER_DOMAIN = st.number_input("Mailboxes / domain",  value=2)
    COST_PER_MAILBOX_PER_MONTH = st.number_input("Cost per mailbox / month", value=3, disabled=True)
    COST_PER_DOMAIN = st.number_input("Cost per domain", value=13, disabled=True)


if st.button("Calculate ROI"):
    TOTAL_EMAILS = NUM_OF_LEADS * EMAILS_PER_LEAD
    CAMPAIGN_DURATION_IN_DAYS_POST_WARM_UP = CAMPAIGN_DURATION * WORKING_DAYS - WARMUP_PERIOD * 5
    EMAILS_PER_SENDING_DAY = TOTAL_EMAILS / CAMPAIGN_DURATION_IN_DAYS_POST_WARM_UP

    NUMBER_EMAILS_SENT_PER_MONTH = TOTAL_EMAILS/CAMPAIGN_DURATION
    MAILBOX_NEEDED_BY_MAILFORGE = calculate_num_mailbox(NUMBER_EMAILS_SENT_PER_MONTH)
    DOMAINS_NEEDED = math.ceil(MAILBOX_NEEDED_BY_MAILFORGE / MAILBOXES_PER_DOMAIN)
    MONTHLY_COST_FOR_MAILBOX = MAILBOX_NEEDED_BY_MAILFORGE * COST_PER_MAILBOX_PER_MONTH
    MONTHLY_COST_FOR_DOMAIN = DOMAINS_NEEDED * COST_PER_DOMAIN
    MONTHLY_COST  = MONTHLY_COST_FOR_MAILBOX + MONTHLY_COST_FOR_DOMAIN
    TOTAL_COST_MAILFORGE = MONTHLY_COST * (CAMPAIGN_DURATION + 1) # For warmup
    TOTAL_COST_SOCIAL_MEDIA = SOCIAL_MEDIA_COST_DIC[SOCIAL_MEDIA_CAMPAIGN_TO_INCLUDE] * NUM_OF_LEADS
    
    TOTAL_COST = int((TOTAL_COST_MAILFORGE + TOTAL_COST_SOCIAL_MEDIA ) * 1.8)

    col11, col12 = st.columns(2)
    with col11:
        st.metric("Emails sent / day", int(EMAILS_PER_SENDING_DAY))
    with col12:
        st.metric("Total emails to be sent", TOTAL_EMAILS)
    col21, col22, col23 = st.columns(3)
    with col21:
        st.metric("Total cost mailforge ", "$" + str(TOTAL_COST_MAILFORGE))
    with col22:
        st.metric("Total cost social media", "$" + str(TOTAL_COST_SOCIAL_MEDIA))
    with col23:
        st.metric("Total cost","$" + str(TOTAL_COST))


