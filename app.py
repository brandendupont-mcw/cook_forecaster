import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
### Data URL



"""
# Cook County Justice System Forecaster
A tool to generate policy scenarios and their impact across system points.
"""

def main():

    ### Referral Leverls
    # Set up sidebar title
    st.sidebar.markdown('# Policy Levers')

    # set up brief explanation
    st.sidebar.markdown('Modify parameters to change various scenarios.')

    st.sidebar.markdown('### Narcotic Referrals')

    #add slider
    hour = st.sidebar.slider("Percent Increase or Decrease",  -100.0, 100.0, (0.0))

    #add percent change calc
    hour_calc = (hour + 100) / 100


    ### Conviction Lever
    st.sidebar.markdown('### Conviction Rate')

    #add number input to sidebar
    co_rate = st.sidebar.number_input('Change Conviction Rate', min_value=0.0, max_value=1.0, value=.62)

    ### Prison and Jail Lever
    st.sidebar.markdown('### Prison and Jail Rate')
    #add number input to sidebar
    snt_rate = st.sidebar.number_input('Change Jail and Prison Rate', min_value=0.0, max_value=1.0, value=.58)

    # conditional text
    def conditional_swithc(num):

        if num >=1:
            inc_dec = "increase"
        else:
            inc_dec = "decrease"
        return inc_dec

    # increase or decrease text
    inc_dec = conditional_swithc(hour_calc)

    # get narcotic data
    nf = get_data()

    #get co data
    new_data = get_co_data()

    #rename df
    co = new_data

    #subset
    cf = nf[['month', 'Direct Filing', 'Prediction']]

    """
    ### Narcotic Cases Forecast
    """
    #dynamic series calculation
    cf['Direct Filing'] = np.where(cf['Prediction'] == 'Forecasted',cf['Direct Filing'] * hour_calc, cf['Direct Filing'])

    # change in cases
    case_change = round(cf['Direct Filing'].sum() - nf['Direct Filing'].sum())

    # Explanation text
    st.write('Compared to a baseline 12 month estimate of', round(nf[nf['Prediction'] == 'Forecasted']['Direct Filing'].sum()),
            'a',hour,'percent change in referred cases', 'would', inc_dec, 'the amount of narcotic cases in Cook County by', case_change, '.')


    #diplay chart
    f = px.line(cf, x="month", y="Direct Filing", color='Prediction')
    f.update_xaxes(title="Predicted Narcotics")
    f.update_yaxes(title="Month")
    f.update_yaxes(showgrid=False, zeroline=False)
    st.plotly_chart(f, use_container_width=True)

    """
    ### Convicted Cases Forecast
    """

    co['convict_calc'] = (co['Direct Filing'] * hour_calc) * co_rate

    convict_change = co['convict_calc'].sum() - co['convict_baseline'].sum()

    # Explanation text
    st.write('Compared to a baseline 12 month estimate of', round(co['convict_baseline'].sum()),
            'this', 'would ' 'see the amount of convicted narcotic cases change in Cook County by', round(convict_change), '.')

    #tranform data
    co_t = co[['convict_baseline','convict_calc']]

    #diplay chart
    cf = px.bar(co[['convict_calc']], x='convict_calc')
    cf.update_yaxes(title="Month")
    st.plotly_chart(cf, use_container_width=True)


    """
    ### Sentenced Cases Forecast
    """

    co['sent_calc'] = ((co['Direct Filing'] * hour_calc) * co_rate) * snt_rate


    sent_change = co['sent_calc'].sum() - co['sent_baseline'].sum()

    # Explanation text
    st.write('Compared to a baseline 12 month estimate of', round(co['sent_baseline'].sum()),
            'this', 'would ' 'see the amount of narcotic cases sentenced to jail or prison change in Cook County by', round(sent_change), '.')


    #diplay chart
    cs = px.bar(co, x='sent_calc')
    cs.update_yaxes(title="Month")
    st.plotly_chart(cs, use_container_width=True)

# get narcotic referral predictions
@st.cache
def get_data():
    CSV_PATH = r'https://docs.google.com/spreadsheets/d/1vnYuOUq-uEt-v0OXgrFHLuA3pDnulF2mDC1aHYthmwM/export?format=csv&id=1vnYuOUq-uEt-v0OXgrFHLuA3pDnulF2mDC1aHYthmwM'
    return pd.read_csv(CSV_PATH, parse_dates=['month'])



def get_co_data():
    co_path = r'https://docs.google.com/spreadsheets/d/1vnYuOUq-uEt-v0OXgrFHLuA3pDnulF2mDC1aHYthmwM/export?gid=127052772&format=csv'
    return pd.read_csv(co_path)


if __name__ == "__main__":
    main()
