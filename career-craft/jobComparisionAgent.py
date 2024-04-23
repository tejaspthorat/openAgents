from pydantic import BaseModel, ValidationError, Field
import json
from langchain.output_parsers import PydanticOutputParser
import os
from openai import OpenAI
import json
import requests
from utility import check_what_is_empty, add_non_empty_details, askLLM
from prompts import jobComparisation, filterComparisionResponse


class Request(BaseModel):
    jobDescription : str = Field(description= "Job description as requested")
    link : str = Field(description = "Link to the resume")

def jobComparision():
    """
    Function to compare job description with resume
    """
    ask_for = ["jobDescription", "link"]
    parser = PydanticOutputParser(pydantic_object=Request)

    jobComparisionDetails = Request(jobDescription="",
                                 link=""
                                )

    while len(ask_for) != 0:
        print(ask_for)
        prompt = jobComparisation(ask_for)
        completion = askLLM(prompt)
        print(completion)
        user_input = input("user: ")
        res = filterComparisionResponse(user_input, askLLM, parser)
        print(res)
        res = add_non_empty_details(jobComparisionDetails,res)
        jobComparisionDetails = res
        # print(coldMailingDetails)
        ask_for = check_what_is_empty(jobComparisionDetails)

    print("Thank you, working on your request")

    data = {
    "job_description": jobComparisionDetails.jobDescription,
    "resume_url": jobComparisionDetails.link
    }
    url = "http://127.0.0.1:5000/compare"

    response = requests.post(url, json=data)

    print("\n Resume Comparision: ",response.json()["response"])

    if response.status_code == 200:
        pass
    else:
        print(f"POST request failed with status code: {response.status_code}")

    return jobComparisionDetails

jobComparision()