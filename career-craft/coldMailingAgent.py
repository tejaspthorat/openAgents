from pydantic import BaseModel, ValidationError, Field
import json
from langchain.output_parsers import PydanticOutputParser
import os
from openai import OpenAI
import json
import requests
from utility import check_what_is_empty, add_non_empty_details, askLLM

from prompts import coldEmailPrompt, filterEmailResponse


# Pydantic classes
# class Category(BaseModel):
#     category: str

class ColdEmail(BaseModel):
    name : str= Field(description = "Full name of the applicant")
    recruiterEmail : str=Field(description = "Email of the recruiter")
    jobDescription : str=Field(description= "Job Description")
    company : str = Field(description = "name of the organization you are applying to")
    contact: str = Field(description="Contact information of the applicant")

# class Request(BaseModel):
#     jobDescription : str = Field(description= "Job description as requested")
#     link : str = Field(description = "Link to the resume")


# def categorise_request(input_query):
#     parser = PydanticOutputParser(pydantic_object=Category)
#     prompt = categorization(input_query)
#     completion = askLLM(prompt)
#     final_result = parser.parse(completion)
#     return final_result


def coldEmailingAgent():
    """
    Function to send cold emails
    """
    ask_for = ["name", "recruiterEmail", "jobDescription", "company", "contact"]
    parser = PydanticOutputParser(pydantic_object=ColdEmail)

    coldMailingDetails = ColdEmail(name="",
                                   recruiterEmail="",
                                   jobDescription="",
                                   company="",
                                   contact=""
                                   )

    while len(ask_for) != 0:
        # print(ask_for)
        prompt = coldEmailPrompt(ask_for)
        completion = askLLM(prompt)
        print(completion)
        user_input = input("user: ")
        res = filterEmailResponse(user_input, askLLM, parser)
        # print(res)
        res = add_non_empty_details(coldMailingDetails,res)
        coldMailingDetails = res
        # print(coldMailingDetails)
        ask_for = check_what_is_empty(coldMailingDetails)

    print("Thank you, working on your request")

    data = {
    "sendTo": coldMailingDetails.recruiterEmail,
    "name": coldMailingDetails.name,
    "job_description": coldMailingDetails.jobDescription,
    "company": coldMailingDetails.company,
    "phone": coldMailingDetails.contact
    }
    url = "http://127.0.0.1:5000/sendEmail"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Email sent successfully")
    else:
        print(f"POST request failed with status code: {response.status_code}")

    return coldMailingDetails


# category = categorise_request(input("user: "))

# if category.category == "coldEmailing":
coldEmailingAgent()



