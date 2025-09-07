import streamlit as st
import pandas as pd
import altair as alt
from prediction_helper import prediction_helper

def main():
    st.set_page_config(page_title="AQI Categorizer", page_icon="🔍")

    # Sidebar
    st.sidebar.image(
        "C:\Users\SUNNY SANGWAN\AQI-Categorizer-APP\image\download.jpeg",
        use_container_width=True
    )
    st.sidebar.markdown("### 🔍 AQI Categorizer")
    st.sidebar.info("This tool helps you categorize Air Quality Index (AQI) values and pollutants.")

    # Title
    st.title("🔍 AQI Categorizer")
    st.write("Enter air quality details to know the pollution category.")

    # Inputs
    aqi_value = st.number_input("Enter AQI Value:", min_value=0, step=1)
    st.subheader("Pollutant Levels (µg/m³)")

    # Pollutants arranged in 3 rows × 2 columns
    col1, col2 = st.columns(2)
    with col1:
        pm25 = st.slider("PM2.5", 0, 500, 50)
        no2 = st.slider("NO₂", 0, 400, 30)
        co = st.slider("CO", 0, 50, 1)
    with col2:
        pm10 = st.slider("PM10", 0, 600, 80)
        so2 = st.slider("SO₂", 0, 400, 20)
        o3 = st.slider("O₃", 0, 500, 40)

    # Predict button
    with st.form(key="predict_form"):
        st.markdown(
            """
            <style>
            div.stButton > button {
                display: block;
                margin-left: auto;
                margin-right: auto;
                background: linear-gradient(90deg, #36D1DC, #5B86E5);
                color: white;
                padding: 16px 40px;
                border-radius: 30px;
                font-size: 22px;
                font-weight: bold;
                box-shadow: 0 6px 20px rgba(0,0,0,0.35);
                transition: all 0.3s ease;
            }
            div.stButton > button:hover {
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                transform: scale(1.05);
                background: linear-gradient(90deg, #5B86E5, #36D1DC);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        submitted = st.form_submit_button("🔮 Predict AQI")

        if submitted:
            result = prediction_helper(aqi_value, pm25, pm10, no2, so2, co, o3)

            # AQI result
            st.success(f"AQI Value: **{result['AQI Value']}** → Category: **{result['Predict']}**")

            # Pollutant overview
            st.subheader("📊 Pollutant Overview")
            pollutants = {
                "PM2.5": f"{pm25} µg/m³",
                "PM10": f"{pm10} µg/m³",
                "NO₂": f"{no2} µg/m³",
                "SO₂": f"{so2} µg/m³",
                "CO": f"{co} mg/m³",
                "O₃": f"{o3} µg/m³"
            }
            colors = ["#2ECC71", "#F1C40F", "#E67E22", "#E74C3C", "#8E44AD", "#3498DB"]

            cols = st.columns(len(pollutants))
            for i, (pollutant, value) in enumerate(pollutants.items()):
                with cols[i]:
                    st.markdown(
                        f"""
                        <div style='background-color:{colors[i]};
                                    padding:15px;
                                    border-radius:12px;
                                    text-align:center;
                                    color:white;
                                    font-weight:bold;'>
                            {pollutant}<br><span style='font-size:18px;'>{value}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Pollutant visualization (bar + line chart)
            st.subheader("📈 Pollutant Visualization")
            data = pd.DataFrame({
                "Pollutant": list(pollutants.keys()),
                "Concentration": [pm25, pm10, no2, so2, co, o3],
                "Color": colors
            })

            # Bar chart
            bar_chart = (
                alt.Chart(data)
                .mark_bar(size=50)
                .encode(
                    x=alt.X("Pollutant", sort=None),
                    y=alt.Y("Concentration", title="Concentration (µg/m³)"),
                    color=alt.Color("Pollutant", scale=alt.Scale(range=colors)),
                    tooltip=["Pollutant", "Concentration"]
                )
            )

            # Line chart overlay
            line_chart = (
                alt.Chart(data)
                .mark_line(point=True, size=3)
                .encode(
                    x="Pollutant",
                    y="Concentration",
                    tooltip=["Pollutant", "Concentration"]
                )
            )

            st.altair_chart(bar_chart + line_chart, use_container_width=True)

            # Health advice
            st.markdown(
                """
                <div style="
                    background-color: #FFEBE6;
                    color: #B71C1C;
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid #B71C1C;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    font-weight: bold;
                    font-size: 16px;
                    margin-top: 20px;
                ">
                    ⚠️ Always consider sensitive groups when AQI is high. Reduce outdoor activity if AQI &gt; 200.
                </div>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()

















