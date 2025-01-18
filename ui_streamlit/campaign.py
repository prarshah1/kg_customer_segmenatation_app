import streamlit as st
import os
from dotenv import load_dotenv
from llm_handler import generate_segment_description, generate_marketing_email, generate_marketing_image, \
    return_full_email_prompt, return_full_image_prompt
import requests  # For handling image URLs

# Load environment variables
load_dotenv()


def campaign_generation():
    # Initialize session state for generated email and image
    if "generated_email" not in st.session_state:
        st.session_state.generated_email = ""
    if "generated_image" not in st.session_state:
        st.session_state.generated_image = None

    # App title with a stylish header
    if not str(st.session_state.selected_segment).startswith("L"):
        st.header("Select a segment from 'Customer Segmentation' section to generate campaign")
    st.markdown(f"<h1 style='text-align: center;'>Personalized Campaign Generation for Segment: {st.session_state.selected_segment}</h1>", unsafe_allow_html=True)

    # Create a visually appealing layout
    # st.markdown("<style>div.row-widget.stButton > button {width: 100%;}</style>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 8, 1])  # Adjust the width ratios for centering

    with col2:
        # Input for project name
        campaign_name = st.text_input("Campaign Name", placeholder="Enter your campaign name",
                                      help="Name your campaign for easy identification.")

        # Input for company name
        company_name = st.text_input("Company Name", placeholder="Enter your company name",
                                     help="Specify the company for which the campaign is being created.")

        # Input for prompt with settings and AI Generate buttons on the same line
        col1, col2, col3 = st.columns([18, 6, 6], vertical_alignment="bottom")
        with col1:
            prompt = st.text_input("Prompt", placeholder="Generate template for prompting",
                                   help="Provide a prompt to guide the campaign generation.")
        with col2:
            if st.button("⚙️ Configure template", key="settings_button"):
                st.session_state.show_settings = not st.session_state.get("show_settings", False)  # Toggle visibility
        with col3:
            ai_generate_prompt = st.button("**AI Generate**", help="Click to generate the campaign using AI.",
                                           key="ai_generate_button", use_container_width=True, type="primary", icon="🤖")

        # Settings popup for selecting options
        if st.session_state.get("show_settings", False):  # Check if settings should be displayed
            with st.expander("Settings", expanded=True):  # Display as an expander
                st.text("Select the prompt you want to edit:")

                # List of options to choose
                options = ["Edit Email Prompt", "Edit Image Prompt"]
                selected_option = st.radio("Choose an option:", options, index=0, key="settings_option")

                if selected_option == "Edit Email Prompt":
                    email_prompt = st.text_area(
                        "Edit Email Prompt",
                        value=st.session_state.get("custom_email_prompt",
                                                   return_full_email_prompt(prompt, company_name, None)),
                        height=150,
                        key="editable_email_prompt_area"
                    )
                elif selected_option == "Edit Image Prompt":
                    image_prompt = st.text_area(
                        "Edit Image Prompt",
                        value=st.session_state.get("custom_image_prompt",
                                                   return_full_image_prompt(prompt, company_name)),
                        height=150,
                        key="editable_image_prompt_area"
                    )

                # Save changes
                if st.button("Save Changes"):
                    if selected_option == "Edit Email Prompt":
                        st.session_state["custom_email_prompt"] = email_prompt
                    elif selected_option == "Edit Image Prompt":
                        st.session_state["custom_image_prompt"] = image_prompt
                    st.session_state.show_settings = False  # Close popup after saving
                    st.success("Prompt updated successfully.")

        # Generate and display the result for Prompt-Based Workflow
        if ai_generate_prompt:
            if prompt.strip() and company_name.strip():  # Ensure prompt and company name are not empty
                custom_email_prompt = st.session_state.get("custom_email_prompt", prompt)  # Get the custom email prompt

                with st.spinner("Generating campaign message..."):
                    try:
                        # Generate marketing email using the custom email prompt
                        marketing_email = generate_marketing_email(custom_email_prompt, company_name, None)
                        st.session_state.generated_email = marketing_email

                    except Exception as e:
                        st.error(f"Error generating campaign: {e}")
            else:
                st.warning("Please enter a valid prompt and company name to generate a message.")

        # Display generated email and image
        if st.session_state.generated_email:
            st.subheader("Generated Campaign Marketing Email:")
            st.text_area("Generated Email", value=st.session_state.generated_email, height=300,
                         key="generated_email_area")

            # Provide download button for the email content
            st.download_button(
                label="Download Campaign Email",
                data=st.session_state.generated_email,
                file_name="campaign_email.txt",
                mime="text/plain"
            )
        if ai_generate_prompt:
            if prompt.strip() and company_name.strip():  # Ensure prompt and company name are not empty
                custom_image_prompt = st.session_state.get("custom_image_prompt", prompt)  # Get the custom image prompt

                with st.spinner("Generating campaign message..."):
                    try:
                        # Generate marketing image using the custom image prompt
                        image = generate_marketing_image(custom_image_prompt, company_name)

                        if image:  # Ensure the function returns image URL or binary content
                            if isinstance(image, str):  # If it's a URL, fetch the binary content
                                response = requests.get(image)
                                if response.status_code == 200:
                                    image_data = response.content  # Binary content of the image
                                else:
                                    st.warning("Failed to fetch the image.")
                                    image_data = None
                            else:  # Assume `image` is already binary data
                                image_data = image

                            st.session_state.generated_image = image_data

                    except Exception as e:
                        st.error(f"Error generating campaign: {e}")
            else:
                st.warning("Please enter a valid prompt and company name to generate a message.")

        if st.session_state.generated_image:
            st.subheader("Generated Marketing Image:")
            st.image(st.session_state.generated_image, caption="Generated Image", use_container_width=True)
            st.download_button(
                label="Download Campaign Image",
                data=st.session_state.generated_image,
                file_name="campaign_image.png",
                mime="image/png"
            )
