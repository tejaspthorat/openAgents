from pydantic import BaseModel, ValidationError, Field
import json
from langchain.output_parsers import PydanticOutputParser
import os
from openai import OpenAI
import json
import requests
from utility import check_what_is_empty, add_non_empty_details, askLLM
from prompts import resumeCreation, filterResumeResponse

class Resume(BaseModel):
    name: str = Field(description="Full name of the user")
    email: str = Field(description="Email address of the user")
    phone: str = Field(description="phone number of the user")
    address: str = Field(description="Residential address of the user")
    skills: str = Field(description="Comma-separated list of skills the person has acquired.")
    certifications: str = Field(description="Comma-separated list of certifications the person holds.")
    awards: str = Field(description="Comma-separated list of awards the person has received")
    experiences: str = Field(description="Comma-separated list of professional experiences")

def resumeCreationAgent():
    """
    Function to create resume based on job description
    """
    ask_for = ["name", "email", "phone", "address", "skills", "certifications", "awards", "experiences"]
    parser = PydanticOutputParser(pydantic_object=Resume)

    resumeCreationDetails = Resume(name="",
                                 email="",
                                 phone="",
                                 address="",
                                 skills="",
                                 certifications="",
                                 awards="",
                                 experiences=""
                                )

    while len(ask_for) != 0:
        print(ask_for)
        prompt = resumeCreation(ask_for)
        completion = askLLM(prompt)
        print(completion)
        user_input = input("user: ")
        res = filterResumeResponse(user_input, askLLM, parser)
        print(res)
        res = add_non_empty_details(resumeCreationDetails,res)
        resumeCreationDetails = res
        # print(coldMailingDetails)
        ask_for = check_what_is_empty(resumeCreationDetails)

    print("Thank you, working on your request")

    body = {
            "name": resumeCreationDetails.name,
            "email":resumeCreationDetails.email,
            "phone": resumeCreationDetails.phone,
            "address": resumeCreationDetails.address,
            "skills": resumeCreationDetails.skills,
            "certifications": resumeCreationDetails.certifications,
            "awards": resumeCreationDetails.awards,
            "experiences": resumeCreationDetails.experiences
        }
    
    url = "https://webweaver-model.onrender.com/generation"

    response = requests.post(url, json=body)

    print("\n Resume Comparision: ",response.json()["response"])

    if response.status_code == 200:
        pass
    else:
        print(f"POST request failed with status code: {response.status_code}")

    return resumeCreationDetails

resumeCreationAgent()