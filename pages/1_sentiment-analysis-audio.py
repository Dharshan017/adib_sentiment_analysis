import streamlit as st
import os
from testing_model import get_aspect_sentiment,get_sentiment
from st_audiorec import st_audiorec
import assemblyai as aai
aai.settings.api_key = "421aa8310c4f49a298b475b0e32205d3"
transcriber = aai.Transcriber()

from streamlit_extras.stylable_container import stylable_container

def reset_data():
    st.session_state.data = {"sentiment":[0,0,0,0,"Neutral"],"topic":["-"],"transcribed_text":""}
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
        st.subheader("Record Audio and Get Sentiment")
        wav_audio_data = st_audiorec()
        ta,_,tt = st.columns(spec=[0.35,0.15,0.5])
        if wav_audio_data is not None and st.session_state.data["transcribed_text"]=="":
            # if ta.button("Transcribe the Audio"):
            fp = os.path.dirname(os.path.abspath(__file__))
            with open(fp+"/recorded_audio.mp3","wb") as wo:
                wo.write(wav_audio_data)
            with st.spinner("Transcription In Progress.."):
                transcript = transcriber.transcribe("pages/recorded_audio.mp3")
            st.write(transcript.text)
            st.session_state.data["transcribed_text"] = transcript.text
            os.remove(fp+"/recorded_audio.mp3")
        # if st.session_state.data["transcribed_text"] and tt.button("Analyse the Transcribed text"):
            with st.spinner("Anlysing The Transcribed Text.."):
                st.session_state.data['sentiment'] = get_sentiment(st.session_state.data["transcribed_text"].strip())
                # st.rerun()
                st.session_state.data['topic'] = eval(get_aspect_sentiment(st.session_state.data["transcribed_text"].strip()))

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