import base64
from pathlib import Path
import pandas as pd
import streamlit
import os
from pathlib import Path
import numpy as np
import pydeck as pdk
import random

import streamlit as st
from PIL import Image

file_dir = Path(os.path.dirname(os.path.abspath(__file__)))
DATE_TIME = "date/time"
DATA_URL = file_dir/"data.csv"

@st.cache(persist=True)
def load_data(DATA_URL, nrows=None):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    try:
        data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    except KeyError:
        pass
    return data

data = load_data(DATA_URL)
extra = load_data("/Users/CARLOSPARLOUR/Documents/Python/IncidenceReporting/heatmap-data.csv")
extra = extra.dropna()
# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": float(lat),
            "longitude": float(lon),
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lng", "lat"],
                radius=100,
                elevation_scale=50,
                elevation_range=[0, 3000],
                pickable=True,
                extruded=True,
                coverage=1,
            ),
        ]
    ))

zoom_level = 12
midpoint = (np.average(extra['lat']), np.average(extra['lng']))


def main():
    img = Image.open(file_dir/"Images"/"logo-print.png")
    st.image(img, width= 200,use_column_width=200)

    img2 = Image.open(file_dir/"Images"/"background.jpeg")
    st.image(img2,caption="No task is so important that we can’t take the time to do it safely. A safe company is a successful company.")

    # st.image(img2, width=1260)

    #Title
    st.header("Incidents Reporting")
    # test_data = pd.concat([data]*20, ignore_index=True)

    with st.form("my_form"):
        st.write("Please Fill Out the Information Below")
        # used for date in CSV file
        date = st.date_input("Enter Date")
        #Used for incidents csv file, DOES NOT PREVENT OR CHECK FOR IDENTICAL NUMBERS YET
        incident_number = random.randint(100000, 9999999)
        #Used to select incident typer
        incident_type = st.selectbox("Select Type or Incident", ( "Trip/Fall", "Heavy Equipment Violation", "Other"))
        #Used for
        description = st.text_area("Enter a brief description, Include time, Number of people Involved and if Medical attention was required.")
        submitted = st.form_submit_button("Submit")
        if submitted:
            #Fetch Data from db
            st.write("Submitted. Thank you for your Dedication to Safety.")

    # print(test_data[["lat", "lon"]])

    #used to display the map
    with st.form("my_map"):

        map_display = st.selectbox("View our current Incidents", ( "","Trip/Fall", "Heavy Equipment Violation", "Other"))
        submitted = st.form_submit_button("Submit")
        if submitted:
            if map_display == "Trip/Fall":
                # st.write("slider", slider_val, "checkbox", checkbox_val)
                map(extra, midpoint[0], midpoint[1], 11)
            if map_display == "Heavy Equipment Violation":
                st.text("not ready")
            if map_display == "other":
                st.text("not ready")
    # map(extra, midpoint[0], midpoint[1], 11)

if __name__ == "__main__":
    main()