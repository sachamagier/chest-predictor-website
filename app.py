import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import streamlit as st
import requests
import datetime
#import fpdf
from fpdf import FPDF
#import datetime


# Load environment variables
load_dotenv()
url = os.getenv('https://chestpredict-final-l5vxuce2ea-ew.a.run.app/predictions')
#url = "https://chestpredict-final-l5vxuce2ea-ew.a.run.app/predictions"

# Set background image
# def set_bg_image(image_path):
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("data:image/png;base64,{image_path}");
#             background-size: cover;
#             background-repeat: no-repeat;
#             background-attachment: fixed;

#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )


def set_bg_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;  # Set background color to white
            color: black;             # Set text color to black
        }
        </style>
        """, unsafe_allow_html=True)


# Function to send the image to the FastAPI server and get the result
# def analyze_image(image_file):
#     files = {'img': image_file}
#     response = requests.post(url, files=files)
#     return response.json()

def analyze_image(image):
    url = "https://chestpredict-final-l5vxuce2ea-ew.a.run.app/predictions"
    files = {"img": image}
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()  # Raises an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        st.error(f"Response content: {response.content}")
        return None

# Sidebar Navigation
pages = ['The Scanner', 'Your patient folder', 'Disease Information']
selection = st.sidebar.radio('Go to', pages)

# Implement background color
set_bg_color()
# The elements inside the page selected in the sidebar
# if selection == 'Home':
#     st.title('Home')
#     st.markdown('### Welcome to X-RAI, your X-Ray second opinion by AI! 🏥')
    # Displaying the logo
    #image = Image.open('Website-Images/Logo.png')
    #st.image(image, use_column_width=True)

# elif selection == 'About':
#     st.title('About')
#     st.markdown('### Who we are ?')
#     st.markdown('We are a team of data scientists who have developed a model that can detect 14 different chest diseases  by analyzing X-ray images.')
#     # Create a subsection with the name and pictures of the team members all in the same row
#     st.markdown('### Our Team')
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         st.markdown('**Arno Debelle**')
#         #st.image('', use_column_width=True)
#     with col2:
#         st.markdown('**Rick Van mol**')
#         #st.image('/Users/sachamagier/Desktop/istockphoto-1347495868-612x612.jpg', use_column_width=True)
#     with col3:
#         st.markdown('**Alexandre Perron**')
#         #st.image('/Users/sachamagier/Desktop/download.jpg', use_column_width=True)
#     with col4:
#         st.markdown('**Sacha Magier**')
#         #st.image('/Users/sachamagier/Desktop/download-2.jpg', use_column_width=True)

# Function to create a PDF

def create_pdf(profile_picture, name, age, smoking, symptoms, country, analysis_results):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", 'B', 14)
            self.cell(0, 10, "Patient Report", 0, 1, 'C')
            self.set_font("Arial", 'I', 10)
            self.cell(0, 10, f'Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 0, 'R')
            self.ln(20)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()} / {{nb}}', 0, 0, 'C')
            self.cell(0, 10, f'Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 0, 'R')

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if profile_picture:
        # Add profile picture to PDF
        image = Image.open(profile_picture)
        image_path = "profile_picture.png"
        image.save(image_path)
        pdf.image(image_path, x=10, y=40, w=33)
        pdf.ln(40)  # Move down after image

    # Add user information
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Patient Information", 0, 1, 'L')
    pdf.set_font("Arial", size=12)

    pdf.cell(50, 10, "Name:", 0, 0, 'L')
    pdf.cell(0, 10, name, 0, 1, 'L')

    pdf.cell(50, 10, "Age:", 0, 0, 'L')
    pdf.cell(0, 10, str(age), 0, 1, 'L')

    pdf.cell(50, 10, "Smoking:", 0, 0, 'L')
    pdf.cell(0, 10, "Yes" if smoking else "No", 0, 1, 'L')

    pdf.cell(50, 10, "Symptoms:", 0, 0, 'L')
    pdf.multi_cell(0, 10, symptoms)

    pdf.cell(50, 10, "Country:", 0, 0, 'L')
    pdf.cell(0, 10, country, 0, 1, 'L')

    # Add analysis results
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Analysis Results", 0, 1, 'L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, analysis_results)

    # Save the PDF to a string
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

# Scanner section
if selection == 'The Scanner':
    st.title('The Scanner')
    img_file_buffer = st.file_uploader("### Upload your chest X-ray and let our model analyse it and show you what it found 🦠", type=["jpg", "jpeg", "png"])

#create a button to submit the image
    if img_file_buffer:
        image = Image.open(img_file_buffer)
        st.image(image, use_column_width=True)
        img_bytes = img_file_buffer.getvalue()
        if st.button('Submit'):
            #display the results of the analysis
            result = analyze_image(img_bytes)

            # Optionally, display the analysis results on the Scanner page in bigger font

            #make it bigger size and bold
            st.markdown(f'<p style="font-size: 35px;">Analysis results:</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 35px; font-weight: bold;">{result}</p>', unsafe_allow_html=True)


            #st.write(f"Analysis results: {result}")

        # if st.button("Is it fake?"):
        #         res = requests.post(url, files={'img': image})
        #         response = res.json()

        # Save the results to a file (if needed)


if selection == 'Your patient folder':
    st.title('Your patient folder')
    profile_picture = st.file_uploader('#### Upload your profile picture', type=['jpg', 'png'])
    if profile_picture:
        st.image(profile_picture, use_column_width=True)

    st.sidebar.title('Your Informations')
    name = st.sidebar.text_input('Name')
    age = st.sidebar.number_input('Age', min_value=0, max_value=100)
    smoking = st.sidebar.checkbox('Do you smoke?')
    symptoms = st.sidebar.text_area('Symptoms')
    country = st.sidebar.selectbox('Country', ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina",
    "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
    "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana",
    "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon",
    "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the",
    "Congo, Republic of the", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti",
    "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea",
    "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
    "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland",
    "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan",
    "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos",
    "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar",
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico",
    "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru",
    "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan",
    "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania",
    "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
    "Slovenia", "Solomon Islands", "Somalia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Sudan, South", "Suriname",
    "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago",
    "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"])

    if st.sidebar.button('Submit'):
        st.sidebar.success('Your information submitted successfully!')
        # Here you would add the analysis logic and results
        analysis_results = "Here you will have the analysis results from the ML model."
        #display the result from the analysis made on the scanner page
        st.write(f"Analysis results: {analysis_results}")



        # Optionally, display the analysis results on the Scanner page
        #st.write(f"Analysis results for {name}: {analysis_results}")

        # Save the user information to a file (if needed)
        with open('user_info.txt', 'w') as f:
            f.write(f'Name: {name}\n')
            f.write(f'Age: {age}\n')
            f.write(f'Smoking: {smoking}\n')
            f.write(f'Symptoms: {symptoms}\n')
            f.write(f'Country: {country}\n')


    if st.button('Download your patient folder'):
        analysis_results = "Here you will have the analysis results from the ML model."
        pdf_data = create_pdf(profile_picture, name, age, smoking, symptoms, country, analysis_results)
        st.download_button(label="Download your patient folder", data=pdf_data, file_name="patient_folder.pdf", mime='application/pdf')


if selection == 'Disease Information':
    st.title('Disease Information')

    disease_info = {
        "Atelectasis": {
            "description": """
                Atelectasis is the complete or partial collapse of a lung or a section (lobe) of a lung. It occurs when the alveoli within the lung become deflated or possibly filled with alveolar fluid.
                This condition can be the result of a blockage of the airways or pressure from outside the lung. It can be a complication of other respiratory problems or surgeries.
            """,
            "symptoms": """
                Symptoms of atelectasis can vary depending on the severity and cause. Common symptoms include difficulty breathing, chest pain, and a cough.
                Rapid shallow breathing and low oxygen levels may also be observed, and severe cases can cause cyanosis, where the skin turns a bluish color due to lack of oxygen.
            """,
            "causes": """
                Atelectasis can be caused by a variety of factors including:
                - Post-surgical complications, particularly after chest or abdominal surgery, due to shallow breathing or mucus buildup.
                - Mucus plug that blocks an airway.
                - Foreign body in the airway, commonly seen in children.
                - Tumor inside the airway.
                - Pleural effusion, which is fluid buildup between the tissues lining the lungs and the chest.
            """,
            "risk_factors": """
                Several factors increase the risk of developing atelectasis:
                - Smoking: Damages the lungs and increases mucus production.
                - Recent surgery, particularly chest or abdominal surgery, due to anesthesia and postoperative pain leading to shallow breathing.
                - Respiratory infections that cause excessive mucus production.
                - Conditions that affect swallowing or coughing, such as neurological disorders, increasing the risk of aspiration.
            """,
            "diagnosis": """
                Diagnosis of atelectasis may involve:
                - Chest X-ray: The most common test to identify areas of lung collapse.
                - CT scan: Provides more detailed images of the lungs.
                - Ultrasound: Sometimes used, particularly in children.
                - Bronchoscopy: A procedure where a thin tube with a camera is inserted into the airways to see and possibly remove blockages.
            """,
            "treatment": """
                Treatment for atelectasis depends on the underlying cause:
                - Breathing exercises and chest physiotherapy to help expand the lungs.
                - Bronchoscopy to remove mucus plugs or foreign objects.
                - Positive pressure ventilation to help re-expand the lung.
                - In severe cases, surgery may be necessary to remove tumors or correct structural problems.
            """,
            "prevention": """
                Prevention strategies include:
                - Performing deep breathing exercises and using incentive spirometry post-surgery to keep the airways open.
                - Maintaining good lung health by avoiding smoking and managing chronic respiratory conditions.
                - Ensuring proper hygiene and vaccination to prevent respiratory infections.
            """,
        },
        "Consolidation": {
            "description": """
                Consolidation refers to the solidification of the lung tissue due to accumulation of solid and liquid material in the air spaces that would have normally been filled by gas.
                This condition often results from an infection such as pneumonia, but can also occur due to pulmonary edema or pulmonary hemorrhage.
            """,
            "symptoms": """
                Symptoms of consolidation can include:
                - Cough that may produce sputum.
                - Fever and chills.
                - Shortness of breath and difficulty breathing.
                - Chest pain that worsens with deep breaths.
                - Fatigue and weakness.
            """,
            "causes": """
                Consolidation can be caused by several conditions including:
                - Pneumonia: Infection that inflames the air sacs in one or both lungs.
                - Pulmonary edema: Condition caused by excess fluid in the lungs.
                - Pulmonary hemorrhage: Bleeding into the lung tissue.
                - Aspiration of foreign material, such as food or liquid, into the lungs.
            """,
            "risk_factors": """
                Risk factors for consolidation include:
                - Chronic lung diseases like COPD or bronchiectasis.
                - Smoking, which damages the lungs and reduces their ability to clear infections.
                - Weakened immune system due to conditions like HIV/AIDS, chemotherapy, or steroid use.
                - Hospitalization, especially in the intensive care unit, due to the higher risk of ventilator-associated pneumonia.
            """,
            "diagnosis": """
                Diagnosis involves:
                - Chest X-ray: To detect areas of consolidation in the lungs.
                - CT scan: Provides a more detailed image of the lung tissue.
                - Sputum culture: To identify infectious agents.
                - Blood tests: To check for signs of infection.
            """,
            "treatment": """
                Treatment depends on the cause of consolidation:
                - Antibiotics for bacterial infections such as pneumonia.
                - Supportive care including oxygen therapy for those with difficulty breathing.
                - Treatment of underlying causes such as heart failure or pulmonary edema.
                - In severe cases, hospitalization may be required.
            """,
            "prevention": """
                Preventive measures include:
                - Vaccinations against pneumonia and influenza.
                - Good hygiene practices to prevent infections.
                - Avoiding smoking and managing chronic conditions effectively.
                - Ensuring proper swallowing techniques in those at risk of aspiration.
            """,
        },
        "Infiltration": {
            "description": """
                Infiltration in the lung refers to a substance denser than air, such as pus, blood, or protein, which lingers within the lung parenchyma.
                It is usually indicative of an inflammatory process or infection.
            """,
            "symptoms": """
                Symptoms of lung infiltration can include:
                - Persistent cough, which may produce mucus or phlegm.
                - Fever and chills.
                - Shortness of breath and wheezing.
                - Chest pain that worsens with deep breathing or coughing.
                - Fatigue and weakness.
            """,
            "causes": """
                Causes of lung infiltration include:
                - Bacterial, viral, or fungal infections leading to pneumonia or bronchitis.
                - Lung cancer or metastatic disease.
                - Autoimmune diseases such as sarcoidosis or rheumatoid arthritis.
                - Interstitial lung disease.
                - Aspiration of foreign material.
            """,
            "risk_factors": """
                Risk factors for lung infiltration include:
                - Chronic lung diseases such as COPD, asthma, or bronchiectasis.
                - Immunocompromised state due to HIV/AIDS, chemotherapy, or organ transplantation.
                - Exposure to environmental toxins and pollutants.
                - Smoking, which damages the lung tissue and impairs immune response.
            """,
            "diagnosis": """
                Diagnosis involves:
                - Chest X-ray: To detect areas of infiltration in the lungs.
                - CT scan: Provides a more detailed view of the lung tissue.
                - Sputum culture: To identify infectious organisms.
                - Blood tests: To check for markers of infection or inflammation.
                - Bronchoscopy: Allows direct visualization of the airways and collection of tissue samples.
            """,
            "treatment": """
                Treatment depends on the underlying cause of infiltration:
                - Antibiotics, antivirals, or antifungals for infections.
                - Corticosteroids or immunosuppressants for autoimmune conditions.
                - Chemotherapy or targeted therapy for cancer.
                - Supportive care including oxygen therapy and pain management.
            """,
            "prevention": """
                Preventive measures include:
                - Vaccinations to prevent respiratory infections.
                - Avoiding smoking and exposure to lung irritants.
                - Regular medical check-ups to monitor and manage chronic lung conditions.
                - Practicing good hygiene to reduce the risk of infections.
            """,
        },
        "Pneumothorax": {
            "description": """
                Pneumothorax is the presence of air or gas in the cavity between the lungs and the chest wall, causing the lung to collapse.
                This can occur spontaneously or as a result of trauma or medical procedures.
            """,
            "symptoms": """
                Symptoms of pneumothorax may include:
                - Sudden, sharp chest pain that may radiate to the shoulder or back.
                - Shortness of breath and difficulty breathing.
                - Rapid heart rate.
                - Fatigue and a feeling of tightness in the chest.
            """,
            "causes": """
                Causes of pneumothorax include:
                - Chest injury from trauma or surgery.
                - Underlying lung diseases such as COPD, asthma, or cystic fibrosis.
                - Ruptured air blisters (blebs) on the lung surface.
                - Mechanical ventilation, which can create pressure imbalances in the chest.
            """,
            "risk_factors": """
                Risk factors for pneumothorax include:
                - Smoking, which increases the risk of lung diseases and blebs.
                - Genetic predisposition to developing blebs or lung diseases.
                - Certain lung diseases like COPD, tuberculosis, and pneumonia.
                - Mechanical ventilation, particularly with high pressure settings.
            """,
            "diagnosis": """
                Diagnosis typically involves:
                - Chest X-ray: The primary diagnostic tool to visualize air in the pleural space.
                - CT scan: Provides a detailed view of the chest and can help identify underlying causes.
                - Ultrasound: Used in some cases to detect air in the pleural space.
            """,
            "treatment": """
                Treatment for pneumothorax depends on its severity:
                - Observation for small pneumothorax that may resolve on its own.
                - Needle aspiration or chest
                - tube insertion to remove air from the pleural space.
                - Pleurodesis or surgery to prevent recurrence in severe or recurrent cases.
            """,
            "prevention": """
                Preventive measures include:
                - Avoiding smoking and exposure to lung irritants.
                - Treating underlying lung diseases promptly.
                - Avoiding scuba diving or flying at high altitudes with known lung conditions.
                - Monitoring and managing mechanical ventilation settings carefully.
            """,
        },
                "Edema": {
            "description": """
                Pulmonary edema is a condition caused by excess fluid in the lungs. This fluid collects in the numerous air sacs in the lungs, making it difficult to breathe.
                Pulmonary edema can be caused by heart problems (cardiogenic pulmonary edema) or by other conditions, such as pneumonia, exposure to certain toxins and medications, trauma to the chest wall, and exercising or living at high elevations.
            """,
            "symptoms": """
                Symptoms of pulmonary edema can include:
                - Shortness of breath, especially when lying down or during physical activity.
                - Difficulty breathing (dyspnea).
                - A feeling of suffocating or drowning.
                - Wheezing or gasping for breath.
                - Anxiety, restlessness, or a sense of apprehension.
                - Cough that produces frothy sputum that may be tinged with blood.
                - Excessive sweating and pale skin.
                - Rapid, irregular heartbeat (palpitations).
            """,
            "causes": """
                Causes of pulmonary edema include:
                - Congestive heart failure: When the heart's left ventricle cannot pump out enough of the blood it receives from the lungs, causing fluid to back up into the lungs.
                - Acute respiratory distress syndrome (ARDS): A severe inflammation of the lungs due to an injury or infection.
                - High altitude: Fluid leaks from the capillaries into the lungs due to high pressure changes.
                - Kidney failure: Can lead to fluid overload in the body.
                - Certain medications and toxins that can damage the lungs.
                - Severe infections such as pneumonia or sepsis.
            """,
            "risk_factors": """
                Risk factors for pulmonary edema include:
                - Heart disease and high blood pressure.
                - Kidney disease.
                - Living or traveling to high altitudes.
                - Exposure to certain toxins and medications.
                - Smoking and excessive alcohol consumption.
            """,
            "diagnosis": """
                Diagnosis involves:
                - Chest X-ray to see fluid in the lungs.
                - Blood tests to check for conditions such as heart failure or infection.
                - Echocardiogram to look at the heart's structure and function.
                - Pulse oximetry to measure the oxygen level in the blood.
                - Electrocardiogram (ECG) to check for heart problems.
            """,
            "treatment": """
                Treatment for pulmonary edema includes:
                - Oxygen therapy to improve oxygen levels in the blood.
                - Medications such as diuretics to remove excess fluid, and medications to treat underlying heart conditions.
                - In severe cases, mechanical ventilation may be required to support breathing.
                - Addressing the underlying cause, such as treating heart disease, managing kidney failure, or reducing exposure to high altitudes.
            """,
            "prevention": """
                Preventive measures include:
                - Managing underlying health conditions such as heart disease and high blood pressure.
                - Avoiding smoking and excessive alcohol consumption.
                - Taking medications as prescribed to manage chronic conditions.
                - Monitoring and adjusting activities when traveling to high altitudes.
            """,
        },
        "Emphysema": {
            "description": """
                Emphysema is a type of chronic obstructive pulmonary disease (COPD) involving damage to the air sacs (alveoli) in the lungs.
                Over time, the inner walls of the air sacs weaken and rupture, creating larger air spaces instead of many small ones. This reduces the surface area of the lungs and, in turn, the amount of oxygen that reaches the bloodstream.
            """,
            "symptoms": """
                Symptoms of emphysema include:
                - Shortness of breath, especially during physical activities.
                - Chronic cough that produces mucus.
                - Wheezing.
                - Fatigue and muscle weakness.
                - Weight loss and loss of appetite.
                - Anxiety and depression due to chronic illness.
            """,
            "causes": """
                The main cause of emphysema is long-term exposure to airborne irritants, including:
                - Tobacco smoke.
                - Marijuana smoke.
                - Air pollution.
                - Chemical fumes and dust from the environment or workplace.
            """,
            "risk_factors": """
                Risk factors for emphysema include:
                - Smoking: The most significant risk factor, with a higher risk the more and longer you smoke.
                - Age: Most people with emphysema begin to experience symptoms of the disease between the ages of 40 and 60.
                - Exposure to secondhand smoke.
                - Occupational exposure to fumes or dust.
                - Genetics: A rare inherited deficiency of a protein called alpha-1-antitrypsin.
            """,
            "diagnosis": """
                Diagnosis involves:
                - Pulmonary function tests to measure the lungs' ability to exchange air.
                - Chest X-ray to rule out other lung conditions.
                - CT scan to detect emphysema and determine its extent.
                - Blood tests to check for alpha-1-antitrypsin deficiency.
            """,
            "treatment": """
                There is no cure for emphysema, but treatments can help relieve symptoms and slow the progression of the disease:
                - Medications such as bronchodilators, inhaled steroids, and antibiotics if there is an infection.
                - Pulmonary rehabilitation to improve breathing techniques and overall lung function.
                - Oxygen therapy for those with severe emphysema.
                - Surgery or lung transplant in advanced cases.
                - Lifestyle changes, including quitting smoking and avoiding lung irritants.
            """,
            "prevention": """
                Preventive measures include:
                - Not smoking and avoiding secondhand smoke.
                - Wearing a mask to protect against fumes, dust, and other airborne pollutants.
                - Regular medical check-ups to monitor lung health.
                - Getting vaccinated against respiratory infections such as influenza and pneumonia.
            """,
        },
        "Fibrosis": {
            "description": """
                Pulmonary fibrosis is a lung disease that occurs when lung tissue becomes damaged and scarred.
                This thickened, stiff tissue makes it more difficult for the lungs to work properly. As the lung tissue becomes more scarred, it becomes harder to breathe deeply. Over time, the lungs become unable to take in enough oxygen.
            """,
            "symptoms": """
                Symptoms of pulmonary fibrosis can include:
                - Shortness of breath, especially during or after physical activity.
                - A dry, persistent cough.
                - Fatigue and weakness.
                - Chest discomfort or pain.
                - Unexplained weight loss.
                - Clubbing (widening and rounding) of the tips of the fingers or toes.
            """,
            "causes": """
                Pulmonary fibrosis can be caused by a variety of factors, including:
                - Long-term exposure to certain toxins and pollutants, such as silica dust, asbestos fibers, grain dust, and bird and animal droppings.
                - Certain medical conditions, such as rheumatoid arthritis, scleroderma, and lupus.
                - Radiation treatments for lung or breast cancer.
                - Some medications, including chemotherapy drugs, certain heart medications, and some antibiotics.
                - Genetics: Some forms of pulmonary fibrosis run in families.
            """,
            "risk_factors": """
                Risk factors for pulmonary fibrosis include:
                - Age: Pulmonary fibrosis is more likely to affect middle-aged and older adults.
                - Gender: In some forms of pulmonary fibrosis, men are affected more than women.
                - Smoking: Increases the risk of developing pulmonary fibrosis.
                - Occupational exposure to pollutants and toxins.
                - Genetic factors.
            """,
            "diagnosis": """
                Diagnosis involves:
                - Chest X-ray to detect lung changes.
                - High-resolution CT scan to provide a detailed image of the lungs.
                - Pulmonary function tests to measure the lungs' ability to transfer oxygen and carbon dioxide.
                - Blood tests to rule out other conditions.
                - Lung biopsy to analyze lung tissue samples.
            """,
            "treatment": """
                There is no cure for pulmonary fibrosis, but treatments can help manage symptoms and improve quality of life:
                - Medications to slow the progression of the disease and reduce lung inflammation.
                - Oxygen therapy to help maintain oxygen levels in the blood.
                - Pulmonary rehabilitation to improve lung function and overall fitness.
                - Lung transplant in severe cases.
                - Supportive care to manage symptoms and improve quality of life.
            """,
            "prevention": """
                Preventive measures include:
                - Avoiding smoking and exposure to secondhand smoke.
                - Wearing protective gear when working with harmful substances.
                - Getting vaccinated against respiratory infections.
                - Regular medical check-ups to monitor lung health.
                - Managing underlying health conditions effectively.
            """,
        },
        "Nodule": {
            "description": """
                A lung nodule is a small, round or oval-shaped growth in the lung. It may also be called a pulmonary nodule or a coin lesion.
                Lung nodules are usually about 0.2 inch (5 millimeters) to 1.2 inches (30 millimeters) in size. If your doctor sees a lung nodule on an imaging test, don't panic.
                Lung nodules are common, and most are noncancerous (benign).
            """,
            "symptoms": """
                Lung nodules do not typically cause symptoms. They are usually discovered incidentally when a chest X-ray or CT scan is performed for another reason.
                In some cases, a nodule may cause symptoms if it grows large enough to press on the airways or other structures in the chest.
            """,
            "causes": """
                Lung nodules can have many causes, including:
                - Infection: Inflammatory lung nodules can be caused by infections such as tuberculosis or fungal infections.
                - Inflammation: Nodules can develop as a result of inflammation in the lung tissue.
                - Benign tumors: Noncancerous tumors can form nodules in the lungs.
                - Malignant tumors: Lung cancer can present as a nodule in the lung.
                - Granulomas: Small areas of inflammation can form nodules in the lungs.
            """,
            "risk_factors": """
                Risk factors for lung nodules include:
                - Smoking: The most significant risk factor for developing lung cancer and lung nodules.
                - Exposure to radon gas, asbestos, or other carcinogens.
                - Family history of lung cancer or other lung diseases.
                - Previous history of cancer or radiation therapy.
                - Chronic lung diseases such as COPD or pulmonary fibrosis.
            """,
            "diagnosis": """
                Diagnosis involves:
                - Chest X-ray: The initial test to identify lung nodules.
                - CT scan: Provides more detailed images of the nodules.
                - PET scan: Used to determine if the nodule is cancerous.
                - Biopsy: A sample of the nodule may be taken for analysis.
                - Monitoring: Some nodules may be monitored over time to see if they change.
            """,
            "treatment": """
                Treatment for lung nodules depends on the underlying cause
                - Observation: Small, benign nodules may be monitored over time.
                - Antibiotics: If the nodule is caused by an infection.
                - Surgery: To remove cancerous or suspicious nodules.
                - Radiation therapy or chemotherapy: For cancerous nodules.
                - Follow-up: Regular monitoring to ensure the nodule does not change.
            """,
            "prevention": """
                Preventive measures include:
                - Avoiding smoking and exposure to secondhand smoke.
                - Reducing exposure to carcinogens and pollutants.
                - Regular medical check-ups to monitor lung health.
                - Early detection and treatment of lung diseases.
            """,
        },
                "Mass": {
            "description": """
                A lung mass refers to an abnormal growth or nodule in the lung that is typically larger than 3 centimeters in diameter. Lung masses can be benign (non-cancerous) or malignant (cancerous), and determining the nature of the mass is crucial for appropriate treatment.
            """,
            "symptoms": """
                Symptoms of a lung mass can vary depending on its size, location, and whether it is benign or malignant. Common symptoms may include:
                - Persistent cough that doesn't go away.
                - Coughing up blood (hemoptysis).
                - Shortness of breath.
                - Chest pain that may worsen with deep breathing or coughing.
                - Unexplained weight loss.
                - Fatigue and weakness.
                - Hoarseness or changes in voice.
            """,
            "causes": """
                Causes of lung masses can include:
                - Lung cancer: Both primary lung cancer and metastasis from other cancers.
                - Benign tumors: Such as hamartomas or lipomas.
                - Infections: Like tuberculosis or fungal infections that form granulomas.
                - Inflammatory conditions: Such as rheumatoid arthritis or sarcoidosis.
                - Congenital abnormalities: Such as bronchogenic cysts.
            """,
            "risk_factors": """
                Risk factors for developing lung masses include:
                - Smoking: The most significant risk factor for lung cancer.
                - Exposure to secondhand smoke.
                - Occupational exposure to carcinogens such as asbestos, radon, and certain chemicals.
                - Family history of lung cancer or other cancers.
                - Previous history of lung infections or chronic lung diseases.
            """,
            "diagnosis": """
                Diagnosis of a lung mass involves:
                - Chest X-ray: Initial imaging to detect the presence of a mass.
                - CT scan: Provides detailed images of the mass and surrounding tissues.
                - PET scan: To assess metabolic activity of the mass and help differentiate between benign and malignant growths.
                - Biopsy: Tissue sample obtained through bronchoscopy, needle biopsy, or surgery for histopathological examination.
                - Blood tests: To assess overall health and detect markers of infection or cancer.
            """,
            "treatment": """
                Treatment depends on the nature of the mass (benign or malignant) and its cause:
                - Observation: For small, asymptomatic benign masses.
                - Surgery: To remove benign tumors or malignant masses, sometimes combined with other treatments.
                - Chemotherapy and/or radiation therapy: For malignant masses, either alone or in combination with surgery.
                - Antibiotics or antifungal medications: For infections causing the mass.
                - Steroids or immunosuppressants: For inflammatory conditions causing the mass.
            """,
            "prevention": """
                Preventive measures include:
                - Avoiding smoking and exposure to secondhand smoke.
                - Reducing occupational exposure to carcinogens with proper protective equipment and safety protocols.
                - Regular medical check-ups and lung screenings, especially for high-risk individuals.
                - Vaccination and proper treatment of lung infections.
            """,
        },
        "Hernia": {
            "description": """
                A hernia occurs when an organ or fatty tissue squeezes through a weak spot in a surrounding muscle or connective tissue called fascia. There are several types of hernias, including inguinal, femoral, umbilical, hiatal, and incisional hernias, each occurring in different parts of the body.
            """,
            "symptoms": """
                Symptoms of a hernia can vary depending on its type and location, but common symptoms include:
                - A noticeable lump or bulge in the affected area, which may disappear when lying down.
                - Pain or discomfort at the hernia site, especially when bending over, coughing, or lifting.
                - Weakness, pressure, or a feeling of heaviness in the abdomen.
                - Burning or aching sensation at the bulge.
                - In severe cases, nausea, vomiting, and constipation if the hernia is strangulated.
            """,
            "causes": """
                Causes of hernias can include:
                - Increased pressure within the abdomen due to heavy lifting, straining during bowel movements, or persistent coughing or sneezing.
                - Weakness in the abdominal wall from birth, aging, or previous surgeries.
                - Obesity, which puts additional pressure on the abdominal wall.
                - Chronic conditions such as cystic fibrosis or chronic obstructive pulmonary disease (COPD) that increase intra-abdominal pressure.
                - Pregnancy, which can weaken the abdominal muscles and increase pressure within the abdomen.
            """,
            "risk_factors": """
                Risk factors for developing hernias include:
                - Family history of hernias.
                - Chronic cough or constipation.
                - Being overweight or obese.
                - Being pregnant.
                - Engaging in heavy lifting or strenuous activity.
                - Previous surgeries, particularly abdominal surgeries.
            """,
            "diagnosis": """
                Diagnosis of a hernia involves:
                - Physical examination: To detect a bulge and assess its reducibility.
                - Imaging studies: Such as abdominal ultrasound, CT scan, or MRI to confirm the diagnosis and evaluate the extent of the hernia.
                - Endoscopy: In cases of hiatal hernia, to visualize the esophagus and stomach.
            """,
            "treatment": """
                Treatment for hernias depends on the type and severity:
                - Watchful waiting: For small, asymptomatic hernias that do not require immediate intervention.
                - Surgical repair: The main treatment for symptomatic or large hernias, which can be performed via open surgery or minimally invasive laparoscopic surgery.
                - Lifestyle modifications: Such as weight management, avoiding heavy lifting, and treating underlying conditions like chronic cough or constipation.
                - Medications: To relieve symptoms associated with hiatal hernias, such as antacids or proton pump inhibitors for acid reflux.
            """,
            "prevention": """
                Preventive measures include:
                - Maintaining a healthy weight to reduce pressure on the abdominal wall.
                - Using proper lifting techniques to avoid straining the abdomen.
                - Treating and managing chronic cough and constipation.
                - Strengthening abdominal muscles through regular exercise.
                - Avoiding smoking, which can contribute to chronic cough and weaken the abdominal wall.
            """,
        },
                "Pleural Thickening": {
            "description": """
                Pleural thickening refers to the thickening of the pleura, which is the thin membrane that covers the lungs and lines the inside of the chest cavity. This condition can restrict lung expansion and make breathing difficult. Pleural thickening is often associated with chronic inflammation, infection, or exposure to asbestos.
            """,
            "symptoms": """
                Symptoms of pleural thickening can include:
                - Shortness of breath, especially during physical activity.
                - Chest pain or discomfort.
                - Chronic cough.
                - Reduced lung capacity and difficulty breathing deeply.
                - Fatigue and weakness.
            """,
            "causes": """
                Causes of pleural thickening include:
                - Asbestos exposure: A significant risk factor, particularly in occupational settings.
                - Infections: Such as tuberculosis or bacterial pneumonia.
                - Chronic inflammation: Due to conditions like rheumatoid arthritis or lupus.
                - Pleural effusion: Accumulation of fluid in the pleural space that leads to scarring.
                - Previous lung surgery or trauma to the chest.
            """,
            "risk_factors": """
                Risk factors for pleural thickening include:
                - Occupational exposure to asbestos or other harmful particles.
                - History of lung infections or pleural effusion.
                - Chronic inflammatory conditions like rheumatoid arthritis.
                - History of chest surgery or trauma.
                - Smoking, which can contribute to lung damage and inflammation.
            """,
            "diagnosis": """
                Diagnosis of pleural thickening involves:
                - Chest X-ray: Initial imaging to detect thickened pleura.
                - CT scan: Provides detailed images of the pleura and lung tissues.
                - Ultrasound: To evaluate the pleura and detect any fluid accumulation.
                - Pulmonary function tests: To assess lung capacity and function.
                - Biopsy: In some cases, to determine the cause of pleural thickening.
            """,
            "treatment": """
                Treatment for pleural thickening depends on the underlying cause:
                - Addressing the underlying cause: Such as treating infections or managing chronic inflammatory conditions.
                - Medications: To reduce inflammation and manage symptoms.
                - Pulmonary rehabilitation: To improve lung function and breathing techniques.
                - Surgery: In severe cases, to remove fibrous tissue or treat underlying conditions.
            """,
            "prevention": """
                Preventive measures include:
                - Avoiding exposure to asbestos and other harmful particles.
                - Quitting smoking and avoiding secondhand smoke.
                - Promptly treating lung infections and inflammatory conditions.
                - Regular medical check-ups to monitor lung health, especially for individuals at risk.
            """,
        },
        "Cardiomegaly": {
            "description": """
                Cardiomegaly, also known as an enlarged heart, is a condition in which the heart is larger than normal. This condition can result from various underlying health issues, including high blood pressure, heart valve disease, cardiomyopathy, and chronic lung disease. An enlarged heart may not pump blood effectively, leading to heart failure and other complications.
            """,
            "symptoms": """
                Symptoms of cardiomegaly can include:
                - Shortness of breath, especially with exertion or when lying flat.
                - Swelling in the legs, ankles, and feet (edema).
                - Fatigue and weakness.
                - Palpitations or irregular heartbeats.
                - Dizziness or lightheadedness.
                - Chest pain or discomfort.
                - Weight gain due to fluid retention.
            """,
            "causes": """
                Causes of cardiomegaly include:
                - High blood pressure (hypertension): Forces the heart to work harder, causing the heart muscle to thicken and enlarge.
                - Heart valve disease: Damage to the heart valves can cause the heart to enlarge.
                - Cardiomyopathy: Diseases of the heart muscle that cause it to enlarge.
                - Chronic lung disease: Conditions such as chronic obstructive pulmonary disease (COPD) can lead to an enlarged heart.
                - Congenital heart defects: Structural problems present at birth.
                - Coronary artery disease: Reduced blood flow to the heart muscle can cause it to enlarge.
                - Anemia or thyroid disorders: Conditions that increase the workload of the heart.
            """,
            "risk_factors": """
                Risk factors for cardiomegaly include:
                - High blood pressure.
                - Family history of heart disease or cardiomyopathy.
                - Congenital heart defects.
                - Chronic lung diseases.
                - Coronary artery disease.
                - Obesity, which increases the risk of high blood pressure and heart disease.
                - Use of substances that can damage the heart, such as alcohol or cocaine.
            """,
            "diagnosis": """
                Diagnosis of cardiomegaly involves:
                - Physical examination: To detect signs of heart enlargement and related symptoms.
                - Chest X-ray: To visualize the size and shape of the heart.
                - Echocardiogram: An ultrasound of the heart to assess its structure and function.
                - Electrocardiogram (ECG): To measure the heart's electrical activity and detect abnormalities.
                - CT scan or MRI: To provide detailed images of the heart and surrounding structures.
                - Blood tests: To check for underlying conditions such as thyroid disease or anemia.
            """,
            "treatment": """
                Treatment for cardiomegaly depends on the underlying cause and severity:
                - Medications: To manage blood pressure, reduce fluid retention, and improve heart function.
                - Lifestyle changes: Such as a heart-healthy diet, regular exercise, quitting smoking, and limiting alcohol intake.
                - Treating underlying conditions: Such as managing high blood pressure, treating heart valve disease, or controlling thyroid disorders.
                - Surgery: In severe cases, procedures such as valve repair or replacement, coronary artery bypass surgery, or heart transplantation may be necessary.
                - Use of devices: Such as pacemakers or implantable cardioverter-defibrillators (ICDs) to regulate heart rhythm.
            """,
            "prevention": """
                Preventive measures include:
                - Managing high blood pressure and cholesterol levels through diet, exercise, and medication.
                - Avoiding smoking and limiting alcohol consumption.
                - Maintaining a healthy weight and managing conditions like diabetes.
                - Regular medical check-ups to monitor heart health and detect problems early.
                - Treating underlying conditions that can lead to cardiomegaly.
            """,
        },
         "Effusion":{
            "description": """
                Pleural effusion, sometimes referred to as "water on the lungs," is the build-up of excess fluid between the layers of the pleura outside the lungs.
                The pleura are thin membranes that line the lungs and the inside of the chest cavity and act to lubricate and facilitate breathing. Pleural effusion can result from a variety of underlying conditions including infections, heart failure, and malignancies.
            """,
            "symptoms": """
                Symptoms of pleural effusion can include:
                - Shortness of breath, especially when lying down.
                - Chest pain, typically a sharp pain that worsens with deep breathing or coughing.
                - Cough.
                - Fever, if the effusion is due to an infection.
                - Hiccups, due to irritation of the diaphragm.
                - Reduced breath sounds or dullness to percussion on the affected side.
            """,
            "causes": """
                Causes of pleural effusion include:
                - Congestive heart failure: The most common cause, where fluid backs up into the lungs.
                - Pneumonia: Infection that can lead to fluid accumulation in the pleural space.
                - Pulmonary embolism: Blood clot in the lung that can cause fluid buildup.
                - Cancer: Particularly lung cancer, breast cancer, and lymphoma.
                - Kidney or liver disease: Can cause fluid imbalance and effusion.
                - Autoimmune diseases: Such as lupus or rheumatoid arthritis that cause inflammation.
            """,
            "risk_factors": """
                Risk factors for pleural effusion include:
                - Chronic heart or lung diseases.
                - Infections, particularly of the lungs.
                - Cancer.
                - History of blood clots or pulmonary embolism.
                - Kidney or liver disease.
                - Autoimmune conditions.
            """,
            "diagnosis": """
                Diagnosis involves:
                - Chest X-ray: Initial imaging to detect fluid in the pleural space.
                - Ultrasound: To locate and assess the amount of fluid.
                - CT scan: Provides detailed images of the chest and pleura.
                - Thoracentesis: Needle is used to remove fluid for analysis.
                - Blood tests: To look for underlying causes such as infection or inflammation.
            """,
            "treatment": """
                Treatment for pleural effusion depends on the underlying cause:
                - Draining the fluid through thoracentesis.
                - Treating the underlying condition, such as antibiotics for an infection or diuretics for heart failure.
                - Pleurodesis: A procedure that uses chemicals to adhere the pleura together and prevent fluid build-up.
                - Surgery: In severe cases to remove part of the pleura or to insert a shunt.
            """,
            "prevention": """
                Preventive measures include:
                - Managing underlying health conditions effectively, particularly heart and lung diseases.
                - Regular medical check-ups to monitor for signs of pleural effusion.
                - Avoiding infections by maintaining good hygiene and getting vaccinated.
                - Following treatment plans for chronic conditions such as cancer or autoimmune diseases.
            """,
        },
        "Pneumonia": {
            "description": """
                Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus (purulent material), causing a cough with phlegm or pus, fever, chills, and difficulty breathing. Various organisms, including bacteria, viruses, and fungi, can cause pneumonia. It ranges in seriousness from mild to life-threatening and is most serious for infants and young children, people older than age 65, and those with health problems or weakened immune systems.
            """,
            "symptoms": """
                Symptoms of pneumonia can vary from mild to severe and include:
                - Chest pain when breathing or coughing.
                - Confusion or changes in mental awareness (in adults age 65 and older).
                - Cough, which may produce phlegm.
                - Fatigue.
                - Fever, sweating, and shaking chills.
                - Lower than normal body temperature (in adults older than age 65 and people with weak immune systems).
                - Nausea, vomiting, or diarrhea.
                - Shortness of breath.
            """,
            "causes": """
                Causes of pneumonia include:
                - Bacteria: The most common cause of bacterial pneumonia in the U.S. is Streptococcus pneumoniae.
                - Viruses: Viruses that infect the respiratory tract may cause pneumonia. Influenza (flu) viruses, respiratory syncytial virus (RSV), and coronaviruses are common causes.
                - Fungi: Pneumonia can be caused by fungi, especially in people with weakened immune systems or chronic health problems.
                - Mycoplasma: These organisms are not viruses or bacteria but have traits common to both. They typically produce milder symptoms.
            """,
            "risk_factors": """
                Risk factors for pneumonia include:
                - Age: Pneumonia is more common in infants and young children, as well as in people older than age 65.
                - Chronic disease: You're more likely to get pneumonia if you have asthma, chronic obstructive pulmonary disease (COPD), or heart disease.
                - Weakened or suppressed immune system: People who have HIV/AIDS, those who have had an organ transplant, or who receive chemotherapy or long-term steroids are at risk.
                - Smoking: Smoking damages your body's natural defenses against the bacteria and viruses that cause pneumonia.
                - Being hospitalized: Especially if you are in an intensive care unit of a hospital and are using a ventilator.
            """,
            "diagnosis": """
                Diagnosis of pneumonia involves:
                - Physical examination: A doctor will listen to your lungs with a stethoscope for abnormal sounds.
                - Chest X-ray: To confirm the presence of pneumonia and determine the extent and location of the infection.
                - Blood tests: To confirm the infection and try to identify the type of organism causing the infection.
                - Pulse oximetry: To measure the level of oxygen in your blood.
                - Sputum test: To analyze a sample of sputum (from a deep cough) to pinpoint the cause of the infection.
            """,
            "treatment": """
                Treatment for pneumonia depends on the type and severity:
                - Antibiotics: For bacterial pneumonia.
                - Antiviral medications: For viral pneumonia, though most cases of viral pneumonia improve on their own.
                - Antifungal treatments: For fungal pneumonia.
                - Over-the-counter (OTC) medications: To relieve fever and pain.
                - Hospitalization: For severe cases that may require intravenous antibiotics, oxygen therapy, and other supportive measures.
            """,
            "prevention": """
                Preventive measures include:
                - Vaccination: Vaccines are available to prevent some types of pneumonia and the flu.
                - Good hygiene: Wash your hands regularly, use hand sanitizer, and avoid touching your face.
                - Don’t smoke: Smoking damages your lungs' natural defenses against respiratory infections.
                - Keep your immune system strong: Get enough sleep, exercise regularly, and eat a healthy diet.
            """,
        },}



    disease = st.selectbox('Select a disease to learn more', list(disease_info.keys()))

    if disease:
        st.header(disease)
        st.write(disease_info[disease]["description"])
        st.subheader("Symptoms")
        st.write(disease_info[disease]["symptoms"])
        st.subheader("Causes")
        st.write(disease_info[disease]["causes"])
        st.subheader("Risk Factors")
        st.write(disease_info[disease]["risk_factors"])
        st.subheader("Diagnosis")
        st.write(disease_info[disease]["diagnosis"])
        st.subheader("Treatment")
        st.write(disease_info[disease]["treatment"])
        st.subheader("Prevention")
        st.write(disease_info[disease]["prevention"])
