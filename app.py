import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import streamlit as st
import requests
# Load environment variables
load_dotenv()
# Set background image
def set_bg_image(image_path):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{image_path}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Set background color
def set_bg_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ADD8E6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# Sidebar Navigation
pages = ['Home', 'About', 'The Scanner', 'Your patient folder']
selection = st.sidebar.radio('Go to', pages)
#implement background color
set_bg_color()
# The elements inside the page selected in the sidebar
if selection == 'Home':
    st.title('Home')
    st.markdown('### Welcome to the Chest X-Ray Analyser! :hospital:')
    # Displaying the logo
    image = Image.open('/Users/sachamagier/Desktop/X-Ray ANALYSER.png')
    st.image(image,use_column_width=True)


elif selection == 'About':
    st.title('About')
    st.markdown('### Who we are ?')
    st.markdown('We are a team of data scientists and developers who have developed a model that can detect 14 different disease related to chest by analizing the X-ray images.')
   #create a subsection with the name and pictures of the team members all in the same row
    st.markdown('### Our Team')
    col1, col2, col3, col4= st.columns(4)
    with col1:
        st.markdown('**Arno Debelle**')
        st.image('/Users/sachamagier/Desktop/download-2.jpg', use_column_width=True)
    with col2:
        st.markdown('**Rick Van mol**')
        st.image('/Users/sachamagier/Desktop/istockphoto-1347495868-612x612.jpg', use_column_width=True)
    with col3:
        st.markdown('**Alexandre Perron**')
        st.image('/Users/sachamagier/Desktop/download.jpg', use_column_width=True)
    with col4:
        st.markdown('**Sacha Magier**')
        st.image('/Users/sachamagier/Desktop/download-2.jpg', use_column_width=True)
url = os.getenv('SERVICE_URL')


if selection == 'The Scanner':
    st.title('The Scanner')
    img_file_buffer = st.file_uploader("### Upload your chest X-ray and let our model Analyse it and showed you what he found :microbe:", type=["jpg", "jpeg", "png"])
    if img_file_buffer is not None:
        col1,col2 = st.columns(2)
        with col1:
            st.image(Image.open(img_file_buffer),caption=" here's the image you uploaded")
        with col2:
            with st.spinner("Wait for it..."):
                img_bytes = img_file_buffer.getvalue()
                res = requests.post(url,files={'img': img_bytes})
                if res.status_code == 200:
                    prediction = res.json().get('prediction')
                    st.write(f"### The model found {prediction}")
                    st.markdown(res.content)
                else:
                    st.markdown("**Oops**, something went wrong Please try again.")
                print(res.status_code,res.content)

    st.sidebar.title('Your Information')
    name = st.sidebar.text_input('Name')
    age = st.sidebar.number_input('Age', min_value=0, max_value=100)
    smoking = st.sidebar.checkbox('Do you smoke?')
    symptoms = st.sidebar.text_area('Symptoms')
    country = st.sidebar.selectbox('continent', ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'])
    if st.sidebar.button('Submit'):
        st.sidebar.success('Your information submitted successfully!')
        # Save User information in a file
        with open('user_info.txt', 'w') as f:
            f.write(f'Name: {name}\n')
            f.write(f'Age: {age}\n')
            f.write(f'Symptoms: {symptoms}\n')
            f.write(f'Smoking: {smoking}\n')
            f.write(f'Country: {country}\n')



if selection == 'Your patient folder':
    st.title('Your patient folder')
    #ask the user to upload a profile picture
    profile_picture = st.file_uploader('#### Upload your profile picture', type=['jpg', 'png'])
    if profile_picture:
        st.image(profile_picture, use_column_width=True)
    # create a pdf file with the user information his profile picture and the result of the analysis
    if st.button('Download your patient folder'):
        pass
