import openai
import os

import streamlit as st
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]


def generate_segment_description(cypher_query):
    """
    Generate a description of the Cypher query with a focus on demographics or individuals
    represented by the segment, using GPT-4.
    """
    try:
        # Updated prompt with a clearer definition of 'segment'
        prompt = f"""
        The following Cypher query represents a segment of individuals or demographics:
        {cypher_query}
        
        Please describe what this segment represents in a concise and human-readable manner. 
        Use the word 'segment' instead of 'query' when referring to it.
        """
        
        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        
        # Safely accessing the response content
        message_content = response["choices"][0]["message"]["content"].strip() if "choices" in response and len(response["choices"]) > 0 else "No valid response from the API."
        return message_content
    
    except openai.OpenAIError as e:
        # Log and return user-friendly OpenAI error message
        return f"OpenAI API error: {str(e)}"
    
    except Exception as e:
        # General error handling with more details
        return f"An unexpected error occurred: {str(e)}"


def generate_marketing_email(prompt, company_name, query_description=None):
    """
    Generate a personalized marketing email based on the user prompt and the query description.
    """
    try:
        full_prompt = return_full_email_prompt(prompt, query_description, company_name)
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": full_prompt}],
        )
        return response["choices"][0]["message"]["content"].strip()
    except openai.OpenAIError as e:
        return f"OpenAI API error: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def return_full_email_prompt(prompt, company_name, segment_info, query_description=None):
    base_email_prompt = f"""
        You are a professional sales marketing expert who creates campaigns,
        User is interested in creating a marketing email campaign for following individuals:
        {segment_info}
        
        {f"The target audience is described by the following segment’s purpose: {query_description}" if query_description else ""}
        Use the following prompt for additional context:
        {prompt}

        Craft a professional, personalized marketing email that highlights the value of the product/service 
        in a way that is relevant to the audience described.
        Ensure the tone is positive, empathetic, and sensitive, without focusing on financial or personal details.
        Address the email to '$Username' and end it with 'Best regards' followed by the company name: {company_name}.
    """
    return base_email_prompt.strip()


def return_full_image_prompt(prompt, company_name):
    base_image_prompt = f"""
         Create an image for email advertisemnt based on the idea from prompt.
        For example : If the prompt is Generate a email for vacation plan to Italy for high income people.
        Then generate a image having italy travel destination.

        For example: If the prompt is Generate a email for gym membership for the user.
        Then generate a image having gym equipements or people working out in gym.

        So like this you need to generate images. Make the images less graphic and make them more realistic. Avoid text on image. 

        Main idea: {prompt} Ignore the target audience and make a generic image.
        Company Name: {company_name}
    """
    return base_image_prompt.strip()


def generate_marketing_image(prompt, company_name):
    """
    Generate a clean and minimalistic marketing image using the DALL-E API based on the input prompt and company name.
    """
    try:
        # Format the simplified prompt
        complete_prompt = f"""
        Create a image for email advertisemnt based on the idea from prompt.
        For example : If the prompt is Generate a email for vacation plan to Italy for high income people.
        Then generate a image having italy travel destination.

        For example: If the prompt is Generate a email for gym membership for the user.
        Then generate a image having gym equipements or people working out in gym.

        So like this you need to generate images. Make the images less graphic and make them more realistic. Avoid unnecessary text. 

        Main idea: {prompt} Ignore the target audience and make a generic image.
        Company Name: {company_name}
        """


        # Generate the image using DALL-E API
        response = openai.Image.create(
            model="dall-e-3",
            prompt=complete_prompt,
            n=1
        )

        return response["data"][0]["url"]

    except openai.OpenAIError as e:
        # Handle OpenAI API errors
        return f"OpenAI API error: {str(e)}"

    except Exception as e:
        # Handle other unexpected errors
        return f"An unexpected error occurred: {str(e)}"
