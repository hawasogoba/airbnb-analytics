import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Airbnb Analytics", layout="wide")
con = duckdb.connect('../dbt_project/airbnb.duckdb', read_only=True)

st.title("🏠 Airbnb Analytics Platform")

tables = con.execute("SHOW TABLES").fetchall()
st.sidebar.write("Tables disponibles :", [t[0] for t in tables])

st.header("📊 Logements par type")
try:
    df_listings = con.execute("SELECT * FROM gold_kpis_listings").df()
    st.bar_chart(df_listings.set_index("room_type")["nb_listings"])
except Exception as e:
    st.warning(f"Table gold_kpis_listings pas encore prête : {e}")

st.header("🏆 Top hôtes")
try:
    df_hosts = con.execute("SELECT * FROM gold_kpis_hosts LIMIT 10").df()
    st.dataframe(df_hosts)
except Exception as e:
    st.warning(f"Table gold_kpis_hosts pas encore prête : {e}")

st.header("🌕 Impact de la pleine lune sur les avis")
try:
    df_moon = con.execute("SELECT * FROM gold_full_moon_impact").df()
    st.dataframe(df_moon)
    pivot = df_moon.pivot(index='is_full_moon_night', columns='sentiment', values='nb_reviews').fillna(0)
    st.bar_chart(pivot)
except Exception as e:
    st.warning(f"Erreur : {e}")

st.header("📊 Logements par type")
try:
    df_listings = con.execute("SELECT * FROM gold_kpis_listings").df()
    selected_types = st.multiselect("Filtrer par type de logement", df_listings['room_type'].unique(), default=list(df_listings['room_type'].unique()))
    filtered = df_listings[df_listings['room_type'].isin(selected_types)]
    st.bar_chart(filtered.set_index("room_type")["nb_listings"])
except Exception as e:
    st.warning(f"Table gold_kpis_listings pas encore prête : {e}")