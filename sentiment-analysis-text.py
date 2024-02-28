# import streamlit as st
# # from audio_recorder_streamlit import audio_recorder

# # audio_bytes = audio_recorder(
# #     text="",
# #     recording_color="#e8b62c",
# #     neutral_color="#6aa36f",
# #     icon_name="user",
# #     icon_size="6x",
# # )
# # if audio_bytes:
# #     st.audio(audio_bytes, format="audio/wav")

# from st_audiorec import st_audiorec

# wav_audio_data = st_audiorec()

# # if wav_audio_data is not None:
# #     st.audio(wav_audio_data, format='audio/wav')

import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from testing_model import get_aspect_sentiment,get_sentiment


def reset_data():
    st.session_state.data = {"sentiment":[0,0,0,0,"Neutral"],"topic":["-"],"transcribed_text":""}
st.set_page_config(layout="wide",initial_sidebar_state="expanded")
st.sidebar.button("Reset All",on_click=reset_data)
st.write("<h2 style='text-align:center;'>SENTIMENT ANALYSIS TOOL</h2>",unsafe_allow_html=True)
st.header("",divider="rainbow")
col1,col2 = st.columns(2)
if 'data' not in st.session_state:
    st.session_state.data = {"sentiment":[0,0,0,0,"Neutral"],"topic":["-"],"transcribed_text":""}
with col1:
    with stylable_container(
        key="green_button",
        css_styles="""
            h3 {
                text-align : center;
            }
            button {
                background-color: green;
                color: white;
                border-radius: 20px;
                float: right;
            }""",):
        st.subheader("Enter a Review and Get Sentiment")
        review_text = st.text_area("Enter a review : ")
        if st.button("Analyse Review") and review_text:
            st.session_state.data['sentiment'] = get_sentiment(review_text.strip())
            st.session_state.data['topic'] = eval(get_aspect_sentiment(review_text.strip()))

with col2:
    with stylable_container(
        key="sentiment_button",
        css_styles="""
            h3 {
                text-align: center
            }
            p {
                float: center
            }
            """,):
        st.subheader("Sentiment")
        st.write("<br>",unsafe_allow_html=True)
        _,sc1,_,sc2 = st.columns(spec=[0.3,0.1,0.05,0.55])
        with sc1:
            st.image(f"images/{st.session_state.data['sentiment'][4]}.jpg",width=30)
        with sc2:
            cm = {
                "Positive" : "green",
                "Neutral" : "orange",
                "Negative" : "red"
            }
            st.write(f"<p style='color: {cm[st.session_state.data['sentiment'][4]]};font-size: 21px'>{st.session_state.data['sentiment'][4]}</p>", unsafe_allow_html=True)
        # st.write("""<p style='margin-left: 165px;'>Negative : 12%</p>
        #          <p style='margin-left: 165px;'>Neutral : 8%</p>
        #          <p style='margin-left: 165px;'>Positive : 80%</p>""",unsafe_allow_html=True)
        _,ssc1,ssc2,ssc3 = st.columns(4)
        ssc1.metric(label="Negative",value=f"{st.session_state.data['sentiment'][2]*100:.1f}%")
        ssc2.metric(label="Neutral",value=f"{st.session_state.data['sentiment'][3]*100:.1f}%")
        ssc3.metric(label="Positive",value=f"{st.session_state.data['sentiment'][1]*100:.1f}%")
        st.write("<br>",unsafe_allow_html=True)
    with stylable_container(
        key="review_about",
        css_styles="""
            h3 {
                text-align: center
            };
            p {
                float: center
            }
            """,):
        st.subheader("Review is talking about")
        st.write("<br>",unsafe_allow_html=True)
        st.write(f"""<p
                 style='margin-left:{125 if len(st.session_state.data['topic'])>1 else 250}px;text-align:justify;font-size:20px;'
                 >{" , ".join(st.session_state.data['topic'])}</p>""",unsafe_allow_html=True)