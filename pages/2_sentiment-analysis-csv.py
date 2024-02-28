import streamlit as st
import io
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
from testing_model import process_file
from wordcloud import WordCloud


def reset_data():
    st.session_state.fdata = {"input_file":None,"analysed_df":None,"a":None,"b":None}
st.sidebar.button("Reset All",on_click=reset_data)
def color_func(word,**kwargs):
    df = st.session_state.fdata["a"]
    sentiment = df[df['Word'] == word]['Sentiment'].iloc[0]
    if sentiment >= 0:
        return 'green'
    else:
        return 'red'

st.write("<h2 style='text-align:center;'>SENTIMENT ANALYSIS TOOL</h2>",unsafe_allow_html=True)
st.header("",divider="rainbow")
col1,col2 = st.columns(2)
if "fdata" not in st.session_state:
    st.session_state.fdata = {"input_file":None,"analysed_df":None,"a":None,"b":None} 
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
        st.subheader("Upload CSV File and Get Sentiments")
        file = st.file_uploader(label="Upload CSV File")
        cl1,_,cl2 = st.columns(spec=[0.35,0.15,0.5])
        if file and cl1.button("Analyse All Reviews"):
            review_df = pd.read_excel(io.BytesIO(file.getvalue())).head()
            with st.spinner("Analysing Reviews..."):
                result_df,a,b = process_file(review_df)
            st.dataframe(result_df)
            st.session_state.fdata = {"input_file":file.name,"analysed_df":result_df,"a":a,"b":b}
            st.rerun()
        if st.session_state.fdata["analysed_df"] is not None:
            excel_data = io.BytesIO()
            st.session_state.fdata["analysed_df"].to_excel(excel_data,index=False)
            cl2.download_button("Download Results",
                                 file_name=st.session_state.fdata["input_file"],
                                 data=excel_data)

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
        # _,c1,_ = st.columns(spec=[0.2,0.6,0.2])
        # _,c1=st.columns(spec=[0.1,0.9])
        if st.session_state.fdata["a"] is not None:
            with st.spinner("Creating..."):
                word_freq_dict = dict(zip(st.session_state.fdata["a"]['Word'], st.session_state.fdata["a"]['Frequency']))
                wordcloud = WordCloud(color_func=color_func,background_color="#D2D9DF").generate_from_frequencies(word_freq_dict)
            # plt.imshow(wordcloud, interpolation='bilinear')
            # plt.axis("off")
            # plt.show()
            st.image(wordcloud.to_array(), use_column_width=True)
        else:
            # wordcloud = WordCloud().generate_from_text("Good Bad")
            _,ci1 = st.columns(spec=[0.4,0.6])
            ci1.image("images/word_cloud_icon.png",width=100)
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
        # _,c2,_ = st.columns(spec=[0.2,0.6,0.2])
        if st.session_state.fdata["b"] is not None:
            with st.spinner("Creating..."):
                word_freq_dict = dict(zip(st.session_state.fdata["b"]['Word'], st.session_state.fdata["b"]['Frequency']))
                wordcloud = WordCloud(contour_width=10,background_color="#D2D9DF").generate_from_frequencies(word_freq_dict)
            # plt.imshow(wordcloud, interpolation='bilinear')
            # plt.axis("off")
            # plt.show()
            st.image(wordcloud.to_array(), use_column_width=True)
        else:
            _,ci2 = st.columns(spec=[0.4,0.6])
            ci2.image("images/word_cloud_icon.png",width=100)
        