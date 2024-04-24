

def coldEmailPrompt(ask_for):
    prompt = f"""
        You are a smart AI assistant responsible to collect information from the user regarding information regarding cold email he wants to make to a recruiter in a conversational manner
        You should only ask one question at a time even if you don't get all the info.
        Don't ask as a list! Don't greet the user! Don't say Hi. Explain you need to get some info.
        Here's what information you'll have to collect:
        1) name: Name of the applicant/user.
        2) recruiterEmail : Email id of the recruiter.
        3) jobDescription: The job description you are applying for.
        4) company: name of the organization the user is applying to.
        5) contact: Contact information of the applicant.
        
        You should only ask question specified as askFor below. 
        Fields not in askFor have alreday been asked.
        make sure the conversation is one on one
        If the askFor list is empty, ask the user what else you can help him with.

        askFor: {ask_for[0]}
        """

    return prompt

def categorization(user_query):
    prompt = f"""
        You are responsible to understand the user query and categories the request into the following services

        Services:
        1) resumeCreation: If the user has requested to create a resume.
        2) resumeOptimizer: If the user has requested to optimize his resume.
        3) coldEmailing: If the user has requested to write a cold email to the recruiter
        4) jobComparision: If the user has requested to compare his resume with job description.

        user_query: {user_query}
        
        You should strictly return your output in the following JSON format:
        ```json
        {{
            "category": "[The determined category (resumeCreation, resumeOptimizer, coldEmailing, jobComparision)]"
        }}
        ```
"""
    return prompt

def filterEmailResponse(user_input, llm, parser):
    prompt = f"""
        You are a smart AI assistant responsible to extract the data provided in the below schema based on the provided user query

        ```json
        {{
            "name": "[Email id of the recruiter]",
            "recruiterEmail" : "[Email id of the recruiter]",
            "jobDescription": "[The job description you are applying with the name of the organization]",
            "company": "[name of the organization the user is applying to]"
            "contact": "[Contact information of the applicant]"
        }}
        ```
        User query: {user_input}

        only generate extracted data json.
        The provided format should be strictly followed.
        Populate empty string or default value corresponding to the datatype if the details are not found
        
        """
    completion = llm(prompt)
    result_values = parser.parse(completion)
    return result_values


def jobComparisation(ask_for):
    prompt = f"""
        You are a smart AI assistant responsible to collect information from the user regarding information regarding resume comparision services in a conversational manner
        You should only ask one question at a time even if you don't get all the info.
        Don't ask as a list! Don't greet the user! Don't say Hi. Explain you need to get some info.
        Here's what information you'll have to collect:
        1) jobDescription: The job description.
        2) link: link to the user's resume
        
        You should only ask question specified as askFor below. 
        Fields not in askFor have alreday been asked.
        make sure the conversation is one on one
        If the askFor list is empty, ask the user what else you can help him with.

        askFor: {ask_for[0]}
        """

    return prompt

def filterComparisionResponse(user_input, llm, parser):
    prompt = f"""
        You are a smart AI assistant responsible to extract the data provided in the below schema based on the provided user query

        ```json
        {{
            "jobDescription": "[The job description of the position]",
            "link" : "url/link to the to the resume as a single string"
        }}
        ```
        User query: {user_input}

        only generate extracted data json.
        The provided format should be strictly followed.
        Populate empty string or default value corresponding to the datatype if the details are not found
        
        """
    completion = llm(prompt)
    result_values = parser.parse(completion)
    return result_values

def filterResumeResponse(user_input, llm, parser):
    prompt = f"""
        You are a smart AI assistant responsible to extract the data provided in the below schema based on the provided user query

        ```json
        {{
            "name": "[Full name of the user]",
            "email" : "Email address of the user",
            "phone" : "[phone number of the user]",
            "address": "[Residential address of the user]",
            "skills" : "[Comma-separated list of skills the person has acquired]",
            "certifications": "[Comma-separated list of certifications the person holds]",
            "awards": "[Comma-separated list of awards the person has received]",
            "experiences": "[Comma-separated list of professional experiences]"
        }}
        ```
        User query: {user_input}

        only generate extracted data json.
        The provided format should be strictly followed.
        Populate empty string or default value corresponding to the datatype if the details are not found
        
        """
    completion = llm(prompt)
    # print(completion)
    result_values = parser.parse(completion)
    return result_values

def resumeCreation(ask_for):
    prompt = f"""
        You are a smart AI assistant responsible to collect information from the user to create his/her resume.
        You should only ask one question at a time even if you don't get all the info.
        Don't ask as a list! Don't greet the user! Don't say Hi. Explain you need to get some info.
        Here's what information you'll have to collect:
        1) name: Full name of the user.
        2) email: Email address of the user.
        3) phone: phone number of the user.
        4) address: Residential address of the user.
        5) skills: Comma-separated list of skills the person has acquired.
        6) certifications: Comma-separated list of certifications the person holds.
        7) awards: Comma-separated list of awards the person has received.
        8) experiences: Comma-separated list of professional experiences.
        
        You should only ask question specified as askFor below. 
        Fields not in askFor have alreday been asked.
        make sure the conversation is one on one
        If the askFor list is empty, ask the user what else you can help him with.

        askFor: {ask_for[0]}
        """

    return prompt

