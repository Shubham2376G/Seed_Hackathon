import ast
import tempfile
import pymupdf4llm
import pymupdf
from autogen import ConversableAgent
import streamlit as st

# Initialize patient history in session state
if "patient_history" not in st.session_state:
    st.session_state.patient_history = {}

# Sidebar: Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Form Page", "Document Query", "History"])

# Main content
if page == "Form Page":
    # Form Page
    st.title("🩺 Patient Diagnosis Form")
    st.write("Please fill in the following details to help us better assess your condition.")

    # Patient Details Section
    st.header("1. Patient Details")
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Name:", placeholder="Enter your full name")
    with col2:
        gender = st.selectbox("Gender:", ["Male", "Female", "Other", "Prefer not to say"])
    with col3:
        age = st.number_input("Age:", min_value=0, max_value=120, step=1, format="%d")

    # Symptoms Section
    st.header("2. Patient Symptoms")
    symptoms = st.text_area(
        "Describe your symptoms in detail:",
        placeholder="E.g., fever, cough, chest pain, etc."
    )

    # Upload Blood Test Report Section
    st.header("3. Upload Blood Test Report")
    blood_test = st.file_uploader(
        "Upload your blood test report (optional):",
        type=["pdf", "jpg", "png", "jpeg"],
        help="Supported formats: PDF, JPG, PNG, JPEG"
    )

    # Upload Imaging Section
    st.header("4. Upload Imaging Files")
    imaging_files = st.file_uploader(
        "Upload your imaging files (optional):",
        type=["pdf", "jpg", "png", "jpeg", "dcm"],
        accept_multiple_files=True,
        help="Supported formats: PDF, JPG, PNG, JPEG, DICOM"
    )

    model_category = st.selectbox(
        "Select inference model:",
        ["Medllama2", "Meditron", "Mistral", "Chatgpt (API)"]
    )
    # Submission Button
    if st.button("Submit"):
        if not name:
            st.error("Please provide your name.")
        elif not age:
            st.error("Please provide your age.")
        elif not symptoms:
            st.error("Please describe your symptoms.")
        else:
            st.success("Form submitted successfully!")
            st.write("### Summary of Your Submission:")
            st.write(f"**Patient:** {name}, {gender}, {age} ")
            st.write(f"**Symptoms Described:** {symptoms}")
            st.write(f"**Model:** {model_category}")

            if model_category == "Medllama2":
                !ollama
                pull
                medllama2
            elif model_category == "Meditron":
                !ollama
                pull
                meditron
            elif model_category == "Mistral":
                !ollama
                pull
                mistral
            elif model_category == "Chatgpt (API)":
                !ollama
                pull
                chatgpt

            if blood_test:
                st.write("**Blood Test Report:** Uploaded")
                data = blood_test.getvalue()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(data)
                    cbc_report = pymupdf4llm.to_markdown(temp_file.name)
                    # cbc_report = cbc_agent.generate_reply(messages=[{"content": cbc_report, "role": "user"}])

            else:
                st.write("**Blood Test Report:** Not provided")
                cbc_report = "not provided"

            if imaging_files:
                st.write(f"**Imaging Files:** {len(imaging_files)} file(s) uploaded:")
                for i, file in enumerate(imaging_files, 1):
                    st.write(f"  {i}. {file.name}")

                data_xray = imaging_files.getvalue()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file_xray:
                    temp_file_xray.write(data_xray)



            else:
                st.write("**Imaging Files:** Not provided")
                xray = "not provided"

            doctor_report = doctor_agent.generate_reply(messages=[{
                                                                      "content": f"patient history are {gender} ,age {age} , {symptoms} , blood test report is {cbc_report} , and xray result {xray} ",
                                                                      "role": "user"}])
            # st.write(cbc_report) logs
            st.write("### Diagnosis Report:")

            data_dict[0] = name
            data_dict[1] = age
            data_dict[2] = gender
            data_dict[3] = symptoms
            data_dict[4] = doctor_report["content"]
            data_dict[5] = str(datetime.datetime.now().date())
            data_dict[6] = doctor_report["content"]
            fillpdfs.write_fillable_pdf("/content/final_diagnosis.pdf", "new.pdf", data_dict)
            file_path = "new.pdf"
            # st.write(doctor_report["content"])

            with open(file_path, "rb") as file:
                file_data = file.read()

            # Add a download button
            st.download_button(
                label="Download AI Diagnosis PDF",
                data=file_data,
                file_name="final_diagnosis.pdf",
                mime="application/pdf"
            )


elif page == "Document Query":
    # Dynamic Page
    st.title("📑 Document Query")
    st.write("Query over you documents here")

    rag = st.file_uploader(
        "Upload your document here",
        type=["pdf", "jpg", "png", "jpeg"],
        help="Supported formats: PDF, JPG, PNG, JPEG")

    query = st.text_area(
        "Enter your query:",
        placeholder="E.g., what is the diagnosis test for"
    )

    if st.button("Submit"):
        if not rag:
            st.error("Please provide a document")
        else:
            st.success("submitted successfully! Querying... ")
            st.write("### Summary of Your Submission:")







elif page == "History":
    # Dynamic Page
    st.title("📊 Patient Statistics & Insights")
    st.write("This page dynamically displays aggregated patient data.")

    if st.session_state.patient_history:
        st.write("### Patient History Overview")
        for name, data in st.session_state.patient_history.items():
            st.write(f"**Name:** {name}")
            st.write(f"**Age:** {data['age']} | **Gender:** {data['gender']}")
            st.write(f"**Symptom Category:** {data['symptom_category']}")
            st.write("---")
    else:
        st.warning("No patient data available. Please add patients from the Form Page.")

# Footer
st.markdown("---")
st.markdown("""
**Disclaimer:** This application is for demonstration purposes only.
Please consult a licensed healthcare professional for medical advice.
""")

