import streamlit as st
from main import run_recommendation

st.set_page_config(page_title="Last.fm Recommendation Engine", layout="wide")
st.title("Last.fm Recommendation Engine")
st.markdown("Get music recommendations based on Last.fm tag similarity.")

# User inputs
col1, col2 = st.columns(2)
with col1:
    track_name = st.text_input("Track Name", placeholder="e.g. Frisky")
with col2:
    artist_name = st.text_input("Artist Name", placeholder="e.g. Dominic Fike")

run_button = st.button("Get Recommendations", type="primary")

if run_button and track_name and artist_name:

    with st.spinner("Searching Last.fm..."):
        result = run_recommendation(
            user_artist_selection=artist_name.strip(), user_song_selection=track_name.strip()
        )

    if result is None:
        st.error("Could not generate recommendations. Check your inputs and try again.")
    else:
        st.success(f"Recommendations generated! CSV saved to: `{result[3]}`")

        top_recommendations = result[2]
        st.subheader(f"If you like: {result[0]} by {result[1]}")
        st.markdown("### You might also like:")

        # Display as interactive table
        import pandas as pd
        # Ensure results is a list-like structure for pandas (fixes type errors where results may be `object`)
        recs_df = pd.DataFrame(data=top_recommendations, columns=["Track Name", "Artist Name", "Similarity Score"])
        st.dataframe(recs_df, use_container_width=True, hide_index=True)

elif run_button:
    st.warning("Please enter both a track name and artist name.")