import streamlit as st
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pdf_report import generate_pdf

st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Industrial Predictive Maintenance Dashboard")

st.info(
    f"""
**Machine ID:** MTR-001 |
**Plant:** Production Line A |
**Last Update:** {datetime.now().strftime("%d-%m-%Y %H:%M:%S")} |
**Communication:** 🟢 Connected
"""
)

st_autorefresh(interval=30000, key="refresh")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, "data", "machine_log.csv")

if not os.path.exists(CSV_FILE):
    st.warning("No machine data found.")
    st.stop()

df = pd.read_csv(CSV_FILE)

latest = df.iloc[-1]

history = df.tail(50)

if len(history) > 1:
    previous = history.iloc[-2]
else:
    previous = latest

status = latest["Status"]

if status == "HEALTHY":
    st.success("🟢 Machine Status : HEALTHY")

elif status == "WARNING":
    st.warning("🟡 Machine Status : WARNING")

else:
    st.error("🔴 Machine Status : CRITICAL")

with st.sidebar:

    st.markdown("## Machine")

    st.write("MTR-001")

    st.markdown("---")

    st.metric(
        "Current Status",
        status
    )

    st.metric(
        "❤️ Health",
        f"{latest['Health Score']:.1f}%"
    )

    st.metric(
        "🌡 Temperature",
        f"{latest['Temperature']:.2f}°C"
    )

    st.metric(
        "⚙ Efficiency",
        f"{latest['Efficiency']:.1f}%"
    )

    st.metric(
        "🔋 RUL",
        f"{latest['Remaining Useful Life']:.1f}%"
    )

history = history.copy()

status_map = {
    "HEALTHY":0,
    "WARNING":1,
    "CRITICAL":2
}

history["Status Code"] = history["Status"].map(status_map)

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Executive Overview",
    "🤖 AI Analytics",
    "📈 Machine Trends",
    "📄 Reports"
])

with tab1:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📈 Temperature",
        f"{latest['Temperature']:.3f}"
    )

    col2.metric(
        "📈 RMS",
        f"{latest['RMS']:.3f}"
    )

    col3.metric(
        "⚡ Peak",
        f"{latest['Peak']:.2f}"
    )

    col4.metric(
        "🎯 AI Confidence",
        f"{latest['Confidence']:.1f}%"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "❤️ Health Score",
            f"{latest['Health Score']:.1f}%"
        )
        st.progress(latest["Health Score"]/100)

    with col2:
        st.metric(
            "⚙ Efficiency",
            f"{latest['Efficiency']:.1f}%"
        )
        st.progress(latest["Efficiency"]/100)

    with col3:
        st.metric(
            "⏳ Remaining Useful Life",
            f"{latest['Remaining Useful Life']:.1f}%"
        )
        st.progress(latest["Remaining Useful Life"]/100)

    st.divider()

    col1,col2,col3=st.columns(3)

    with col1:

        if status=="HEALTHY":
            st.success("### 🟢 HEALTHY")

        elif status=="WARNING":
            st.warning("### 🟡 WARNING")

        else:
            st.error("### 🔴 CRITICAL")

    with col2:
        st.info(f"""
        ### AI Predicted Fault

        🔧 **{latest['AI Fault']}**
        """)

    with col3:
        action={
            "HEALTHY":"Routine Inspection",
            "WARNING":"Preventive Maintenance",
            "CRITICAL":"Immediate Shutdown"
        }

        st.info(f"""
        ### Recommended Maintenance

        🛠 **{action[status]}**
        """)

with tab2:

    st.subheader("🤖 AI Analytics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Rule Engine",
        latest["Status"],
        delta=latest["Actual Fault"]
    )

    col2.metric(
        "AI Model",
        latest["AI Prediction"],
        delta=f"{latest['Confidence']:.1f}% Confidence"
    )

    st.subheader("🔍 Fault Detection")

    col1, col2 = st.columns(2)

    col1.metric(
        "Rule-Based Fault",
        latest["Actual Fault"]
    )

    col2.metric(
        "AI Fault",
        latest["AI Fault"]
    )

    st.subheader("📊 Fault Probabilities")

    prob_df = pd.DataFrame({
        "Fault": [
            "Healthy",
            "Bearing",
            "Imbalance",
            "Misalignment",
            "Critical"
        ],
        "Probability": [
            latest["Healthy %"],
            latest["Bearing %"],
            latest["Imbalance %"],
            latest["Misalignment %"],
            latest["Critical %"]
        ]
    })
    prob_df = prob_df.sort_values(
        by="Probability",
        ascending=True
    )

    fig=px.bar(
        prob_df,
        x="Probability",
        y="Fault",
        orientation="h",
        color="Fault",
        color_discrete_map={
            "Healthy": "#2ECC71",        # Green
            "Bearing": "#F1C40F",        # Yellow
            "Imbalance": "#E67E22",      # Orange
            "Misalignment": "#3498DB",   # Blue
            "Critical": "#E74C3C"        # Red
        }
    )

    fig.update_layout(
        height=350,
        showlegend=False,
        xaxis_title="Probability (%)",
        yaxis_title="",
        template="plotly",
        margin=dict(l=20,r=20,t=40,b=20)
    )

    fig.update_traces(
        texttemplate="%{x:.1f}%",
        textposition="outside"
    )

    fig.update_xaxes(
        range=[0,100],
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("🎯 AI Confidence")

    col1, col2 = st.columns(2)

    col1.metric(
        "Status Confidence",
        f"{latest['Confidence']:.1f}%"
    )

    col2.metric(
        "Fault Confidence",
        f"{latest['Fault Confidence']:.1f}%"
    )

    st.divider()

    st.subheader("🧠 AI Recommendation")

    recommendation = {
        "HEALTHY": {
            "action": "Routine Inspection",
            "details": "Machine operating normally. Schedule the next inspection after 30 days."
        },
        "WARNING": {
            "action": "Preventive Maintenance",
            "details": "Performance degradation detected. Perform inspection within the next 7 days."
        },
        "CRITICAL": {
            "action": "Immediate Shutdown",
            "details": "Critical operating conditions detected. Stop the machine immediately and perform corrective maintenance."
        }
    }

    st.info(f"""
    ### 🛠 Recommended Action

    **{recommendation[status]["action"]}**

    {recommendation[status]["details"]}
    """)

    st.subheader("🚨 Active Alerts")

    if status == "CRITICAL":

        st.error(f"""
    • 🌡 **Temperature:** {latest['Temperature']:.1f} °C

    • ❤️ **Health Score:** {latest['Health Score']:.1f}%

    • 🔧 **Detected Fault:** {latest['AI Fault']}

    • 👨‍🔧 **Action:** Notify the maintenance team immediately.
    """)

    elif status == "WARNING":

        st.warning(f"""
    • ⚠ Performance degradation detected.

    • 🌡 Temperature: {latest['Temperature']:.1f} °C

    • ❤️ Health Score: {latest['Health Score']:.1f}%

    • 🛠 Schedule preventive maintenance within 7 days.
    """)

    else:

        st.success("""
    ✅ No active alarms.

    Machine is operating within normal limits.
    """)

with tab3:
    
    col1, col2 = st.columns(2)

    col1.metric(
        "⚙ Machine Efficiency",
        f"{latest['Efficiency']:.1f}%"
    )

    col2.metric(
        "⏳ Remaining Useful Life",
        f"{latest['Remaining Useful Life']:.1f}%"
    )

    st.divider()

    st.subheader("🌡 Temperature Analysis")

    col1, col2 = st.columns(2)

    with col1:

        temp_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest["Temperature"],
            number={"suffix":" °C"},
            title={"text":"Current Temperature"},
            gauge={
                "axis":{"range":[20,60]},
                "bar":{
                    "color":"darkblue"
                },
                "steps":[
                    {"range":[30,40],"color":"green"},
                    {"range":[40,45],"color":"yellow"},
                    {"range":[45,60],"color":"red"}
                ],
                "threshold":{
                    "line":{"color":"black","width":4},
                    "value":45
                }
            }
        ))

        temp_gauge.update_layout(height=320)

        st.plotly_chart(temp_gauge, use_container_width=True)

    with col2:

        temp_trend = px.line(
            history,
            x="Timestamp",
            y="Temperature",
            markers=True,
            title="Temperature Trend",
        )
        temp_trend.update_traces(line_shape="spline", line_width=3)

        temp_trend.update_layout(height=320)

        st.plotly_chart(temp_trend, use_container_width=True)

    st.subheader("📈 Vibration Analysis")

    col1, col2 = st.columns(2)

    with col1:

        rms_fig = px.line(
            history,
            x="Timestamp",
            y="RMS",
            markers=True,
            title="RMS Trend"
        )
        rms_fig.update_traces(line_shape="spline", line_width=3)

        rms_fig.update_layout(height=320)

        st.plotly_chart(rms_fig, use_container_width=True)

    with col2:

        peak_fig = px.line(
            history,
            x="Timestamp",
            y="Peak",
            markers=True,
            title="Peak Trend"
        )
        peak_fig.update_traces(line_shape="spline", line_width=3)

        peak_fig.update_layout(height=320)

        st.plotly_chart(peak_fig, use_container_width=True)

    st.subheader("❤️ Machine Health")

    col1, col2 = st.columns(2)

    with col1:

        health_gauge = go.Figure(go.Indicator(

            mode="gauge+number",

            value=latest["Health Score"],

            title={"text":"Machine Health"},

            gauge={
                "axis":{"range":[0,100]},
                "bar":{
                    "color":"darkblue"
                },
                "steps":[
                    {"range":[0,40],"color":"red"},
                    {"range":[40,70],"color":"yellow"},
                    {"range":[70,100],"color":"green"}
                ],
                "threshold":{
                    "line":{"color":"black","width":4},
                    "value":70
                }
            }
        ))

        health_gauge.update_layout(height=320)

        st.plotly_chart(health_gauge, use_container_width=True)

    with col2:

        status_fig = px.line(
            history,
            y="Status Code",
            title="Status Trend",
            markers=True
        )
        status_fig.update_traces(
            line=dict(width=4),
            marker=dict(size=10)
        )

        status_fig.update_yaxes(
            tickvals=[0,1,2],
            ticktext=["Healthy","Warning","Critical"]
        )

        status_fig.update_layout(height=320)

        st.plotly_chart(status_fig, use_container_width=True)

    st.subheader("⚙ Performance")

    col1, col2 = st.columns(2)

    with col1:

        efficiency_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest["Efficiency"],
            title={"text":"Efficiency"},
            gauge={
                "axis":{"range":[50,100]},
                "bar":{
                    "color":"darkblue"
                },
                "steps":[
                    {"range":[50,70],"color":"red"},
                    {"range":[70,85],"color":"yellow"},
                    {"range":[85,100],"color":"green"}
                ],
                "threshold":{
                    "line":{"color":"black","width":4},
                    "value":70
                }
            }
        ))

        efficiency_gauge.update_layout(height=320)

        st.plotly_chart(efficiency_gauge, use_container_width=True)

    with col2:

        rul_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest["Remaining Useful Life"],
            title={"text":"Remaining Useful Life"},
            gauge={
                "axis":{"range":[0,100]},
                "bar":{
                    "color":"darkblue"
                },
                "steps":[
                    {"range":[0,30],"color":"red"},
                    {"range":[30,60],"color":"yellow"},
                    {"range":[60,100],"color":"green"}
                ],
                "threshold":{
                    "line":{"color":"black","width":4},
                    "value":30
                }
            }
        ))

        rul_gauge.update_layout(height=320)

        st.plotly_chart(rul_gauge, use_container_width=True)

with tab4:
    st.subheader("📄 Machine Report") 
    try: 
        pdf = generate_pdf() 
        st.success("✔ Latest Maintenance Report Generated Successfully") 
        st.markdown("### Report Contents")
        st.markdown(
            """ 
            - ✔ Machine Summary 
            - ✔ AI Prediction 
            - ✔ Fault Diagnosis 
            - ✔ Maintenance Recommendation 
            - ✔ Machine Health Assessment 
            """
        ) 
        
        c1,c2,c3,c4, c5 = st.columns(5)

        c1.metric(
            "Health Score",
            f"{latest['Health Score']:.1f}%"
        )

        c2.metric(
            "Efficiency",
            f"{latest['Efficiency']:.1f}%"
        )

        c3.metric(
            "Current Status",
            latest["Status"]
        )

        c4.metric(
            "Predicted Fault",
            latest["AI Fault"]
        )

        c5.metric(
            "Generated",
            datetime.now().strftime("%H:%M")
        )

        st.download_button(
            "📥 Export Maintenance Report", 
            pdf, 
            file_name="Machine_Report.pdf", 
            mime="application/pdf"
        ) 
    except Exception as e: 
        st.error(e) 
    
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

st.divider()

st.markdown(
    """
<div style="text-align:center; color:#808080; font-size:14px; line-height:1.6;">

<b>Industrial Predictive Maintenance Dashboard</b><br>
Real-Time Machine Health Monitoring • AI Fault Prediction • Predictive Maintenance | Powered by ESP32 • ThingSpeak • Scikit-Learn • Streamlit • Plotly<br>
© 2026 UVCE Smart Factory

</div>
""",
    unsafe_allow_html=True
)
