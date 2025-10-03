import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import uuid
import io

st.set_page_config(page_title="Project Ksheersagar – Farmer Booklet", layout="wide")

# --- Global Configuration and Data ---
CSV_FILE = "fgd_farmer_survey.csv"
QUESTIONS = {
    "Identification": {
        "Name of the Dairy Partner": None,
        "Name of the BMC": None,
        "State": None,
        "District": None,
        "Village": None,
        "Name of the interviewer": None,
        "Signature of the interviewer": None,
        "Start and end time of the FGD": {
            "Start time": None,
            "End time": None,
        },
    },
    "A. Background Information": {
        "Tell me a little bit about your background information such as age, education, experience as a dairy farmer.": {
            "Number of Respondents": 10,
            "fields": [
                {"label": "Name", "key": "name"},
                {"label": "Age", "key": "age"},
                {"label": "Highest level of education", "key": "education"},
                {"label": "Number of years working as a dairy farmer", "key": "years_as_farmer"},
            ],
        },
    },
    "B. Basic Household Information": {
        "1. What are the primary economic activities that you are involved in? (Multiple Answers Possible)": [
            "a. Agriculture", "b. Dairy Farming", "c. Livestock Rearing", "d. Fisheries", "e. Daily Labor", "f. Private sector employment", "g. Government employment", "h. Trade/Shopkeeper", "i. Other.",
        ],
        "2. Approximately, what percentage of households in this area have dairy farming as their primary source of income?": [
            "a. 5-20%", "b. 20-50%", "c. 50-70%", "d. 70-90%", "e. More than 90%",
        ],
        "3. How did you acquire your dairy farm land?": [
            "a. Given by Parents", "b. Given by Government", "c. Given by Relatives", "d. Rented", "e. Purchased",
        ],
        "If Rented, what rent do you pay for your land (mention per month/per year)?": None,
        "4. What livestock are raised within the area? Please mention their composition as well. (Multiple Answers Possible)": [
            "a. Cows", "b. Buffaloes", "c. Hens", "d. Goats", "e. Other.",
        ],
        "5. What are the animals mainly used for?": [
            "a. Economic purpose", "b. Household consumption", "c. Other.",
        ],
        "6. Who are the major clients of the dairy in this area?": None,
        "7. What do they purchase? (Multiple Answers Possible)": [
            "a. Raw Milk", "b. Milk products like cheese, curd paneer etc", "c. Milk Powder", "d. Other...",
        ],
        "8. What type of breeds do you have in your dairy farm? (Multiple Answers Possible)": [
            "a. Local", "b. Cross breeds", "c. Pure breeds",
        ],
        "9. Which breeds of cows do you have? Please mention composition as well. (Multiple Answers Possible)": [
            "a. Holstein Friesian (HF)", "b. Gir", "c. Jersey", "d. Red Sindhi", "e. Sahiwal", "f. Other.",
        ],
        "10. What are the difficulties in procuring higher quality breed cows? (Multiple Answers Possible)": [
            "a. Buying cost", "b. Maintenance Cost", "c. Difficulty in Maintaining", "d. Lack of Space", "e. Lack of access to higher quality breeds",
        ],
        "11. Where do you buy your cows from?": None,
        "12. What is your source of money to conduct dairy farming activities?": [
            "a. Personal Finances", "b. Borrowing from relatives/ friends", "c. Bank Loans", "d. Government funds", "e. Other.",
        ],
    },
    "Animal Care": {"1. Vaccination": {"I know what vaccinations are and how they will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know yearly vaccination schedule for atleast 6 vaccines, and whom to approach for vaccinating my cattle": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of vaccinations to cattle health and want to vaccinate my cattle as per prescribed schedule": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to atleast 3 vaccination dosages for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford vaccination dosages for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly affordable"], "I have 100% timely access to vaccination and vaccinate my cattle according to prescribed vaccination schedule": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to vaccination in close proximity (doorstep/BMC/ in village/ nearby villages) and vaccinate my cattle according to prescribed vaccination schedule": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "2. Deworming": {"I know what deworming is and how it will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know yearly deworming schedule, and whom to approach for vaccinating my cattle": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of deworming to cattle health and want to deworm my cattle as per prescribed schedule": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to deworming tablets for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford deworming services for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to deworming and deworm my cattle according to prescribed vaccination schedule": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to deworming in close proximity (doorstep/BMC/ in village/ nearby villages) and deworming my cattle according to prescribed vaccination schedule": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "3. Tick Control": {"I know what tick control is and how it will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know deticking methods and how to detick my cattle": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of deticking to cattle health and want to detick my cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to deticking services for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford deticking services for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to deticking services and detick my cattle": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to deticking services in close proximity (doorstep/BMC/in village/ nearby villages) and detick my cattle": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "4. Preventive Check-ups": {"I know what preventive check ups are and how they will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know yearly preventive check up schedule, and whom to approach for checking my cattle": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of preventive check ups to cattle health and want to check my cattle as per prescribed schedule": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to preventive checkups for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford preventive check ups for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to preventive check ups and conduct checkups for my cattle according to prescribed schedule": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to check ups in close proximity (doorstep/BMC/in village/ nearby villages) and check my cattle according to prescribed schedule": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "5. Sick Animal Segregation": {"I know what is segregation of sick animals and how it will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know segregation protocols and methods": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of segregating sick animals for cattle health and want to segregate sick animals from healthy cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have space available to segregate sick animals from healthy cattle": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to space for segregating sick animals from healthy cattle": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford segregation of sick animals from healthy animals for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"]}, "6. New Cattle Introduction and Testing": {"I know what is testing of new cattle before introducing them into the herd and how it will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know testing protocols and methods": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of testing new cattle before introducing them into the herd for cattle health and want to test new cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to space for quarantine and testing new animals before introducing them into the herd": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford quarantining and testing of new cattle before introducing them into the herd for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% access to quarantine and test new cattle before introducing them in the herd in close proximity (doorstep/BMC/in village/ nearby villages) and quarantine and test my cattle accordingly": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "7. Feeding of Colustrum": {"I know what is feeding of colostrum to newborn calves and how it will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know how feeding milk replacers to calf will benefit them": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know protocols and methodology for feeding colustrum& Milk replacers to newborn calves": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of feeding colostrum & Milk replacers to new born calves and want to feed the newborn calves with milk replacers": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have milk replacers available to use for calves": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to Milk replacers (via DP/ Paravert at door step)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford feeding colustrum to 100% of the new born calves on my farm": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I feed colustrum in a timely manner as per prescribed norms, to 100% of the new born calves on my farm": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "8. Use of Herbal Remedies": {"I know what herbal remedies are and know how they will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know herbal remedies for most common preventive diseases": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of herbal remedies for my cattle and want to use herbal remedies to prevent diseases for my cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "Herbal remedies are available to me (via home preparation/ herbal gardens in village/ nearby villages)": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to herbal remedies (via herbal gardens, in villages, nearby villages, micro training centres etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford getting herbal raw materials/ ready to use herbal medicines and herbal remedies for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have timely access to herbal remedies and use it to prevent diseases that maybe harmful for 100% of my catle": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to herbal remedies in close proximity (doorstep/BMC/in village/ nearby villages) and use them to prevent diseases for my cattle": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "9. Post Dipping": {"I know what is post dipping and how it will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know post dipping solution application methods/types (Spray/cups)": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of post-dipping to cattle health and want to perform post-dipping my cattle as per the prescribed norms": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have dipping solution and dip cups available to me": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to post-dipping solutions for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford post-dipping chemicals for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to post-dipping chemicals and apply them to my cattle according to the prescribed norms": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to post-dipping chemicals in close proximity (doorstep/BMC/in village/ nearby villages) and apply them to my cattle according to the prescribed norms": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "10. Assessing Healthy and Sick Animals (Body Scoring)": {"I know what is body scoring and how it will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know assessing of healthy and sick animals for 5 criteria based on body scoring": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of body scoring to cattle health and want to perform body scoring my cattle as per the prescribed norms": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"]}, "11. Mastitis Testing and Prevention": {"I know what is mastitis and how its testing and prevention will benefit my cattle's health": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know the symptoms of mastitis and its prevention using California Mastitis Test (CMT) results": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of the California Mastitis Test (CMT) to cattle health and want to perform California Mastitis Test (CMT) for my cattle as per the prescribed norms": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have CMT solution available to me": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to post-dipping solutions for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford California Mastitis Test (CMT) chemicals for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to California Mastitis Test (CMT) chemicals and perform California Mastitis Test (CMT) to my cattle according to the prescribed norms": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to California Mastitis Test (CMT) chemicals in close proximity (doorstep/BMC/ in village/ nearby villages) and apply them to my cattle according to the prescribed norms": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "12. Access to Diagnostic Services": {"I know what diagnostic services are and how it will benefit my cattle's health": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know the actions to be taken up immediately post-diagnosis like getting in touch with a Veterinarian and starting appropriate treatment protocol, taking the animal to a diagnostic facility etc": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of diagnostic facilities to cattle health and want to access diagnostic services for my cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to diagnostic services for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford diagnostic services for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to diagnostic facilities": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to diagnostic facilities in close proximity (doorstep/BMC/ in village/ nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "13. Veterinarian Services": {"I know what are veterinary services and how they will benefit my cattle's health": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know what the services provided by para-vet and qualified veterinary doctor": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of veterinary services to cattle health and want to access veterinary services for my cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "Doorstep services and Veterinary Hospitals are available": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to veterinary services for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I can afford veterinary services for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to veterinary services": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to veterinary services in close proximity (doorstep/BMC/ in village/ nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "14. Accessibility to medicines": {"I know what medicines are and how it will benefit my cattle's health": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know the standardized treatment protocols and medicines to be used to treat the general diseases (Fever, cough/respiratory problems, lameness etc.)": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of high-quality medicines to cattle health and want to access high-quality medicines for my cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to high-quality medicines for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I can afford high-quality medicines for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to high-quality medicines": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to high-quality medicines in close proximity (doorstep/BMC/ in village/ nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "15. Isolation of sick animals": {"I know what is isolation of sick animals and how it will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know isolation protocols and methods": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of isolating sick animals for cattle health and want to isolate sick animals from healthy cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "There is space available for me to isolate my sick animals from healthy cattle": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to space for isolating sick animals from healthy cattle": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I can afford isolation of sick animals from healthy animals for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"]}, "16. Ethno veterinary medicine (RTU (Ready To Use) EVM)": {"I know what RTU EVM are and know how they will benefit my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know RTU EVM for most common diseases": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of RTU EVM for my cattle and want to use RTU EVM to cure diseases for my cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "Herbs for EVM and EVM medicine is available to me": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to RTU EVM (via herbal gardens, in villages, nearby villages, micro training centers etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford to get RTU EVM for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have timely access to RTU EVM and use them to cure diseases for 100% of my cattle": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to RTU EVM in close proximity (doorstep/BMC/in village/ nearby villages) and use them to cure diseases for my cattle": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}},
    "Cattle Breeding": {"1. Cattle Breed and Identification": {"I know how to identify different cattle breeds": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know that different cattle breeds' production capacities, diseases resistance, and which breed is suitable for my locality": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of different cattle breeds and want to introduce new cattle in the herd": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "There are various types of breeds available in my area to procure": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to new cattle breeds (via veterinarians, para vets, government cattle schemes or DP team etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I can afford new cattle breed introduction and its management in the herd": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"]}, "2. Disease Prevention": {"I know what difficulties are faced by cattle during calving and how they will affect my cattle": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know difficulties are faced by cattle during calving, and whom to approach for preventing": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of preventing difficulties faced by cattle during calving and want to vaccinate my cattle as per prescribed schedule": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to prevent/treat difficulties faced by cattle during calving for my cattle (via veterinarians, para vets or government health camps etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I can afford to prevent difficulties are faced by cattle during calving for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"]}, "3. Reproductive Management Practices": {"I know what reproductive management practices and how it will benefit my cattle's production": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know how to maintain a successful reproductive cycle of my cattle": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of reproductive management to cattle production and want to access in all aspects like veterinary support, feed, health for my cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to veterinary support in reproductive management for my cattle (via veterinarians, para vets or government health camps, etc) and feed": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I can afford high quality feed, health care services, breeding services for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to quality feed and veterinary support": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to quality feed and veterinary support in close proximity (doorstep/ BMC/ in village/nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "4. Infertility": {"I know what is cattle infertility and know how it will affect my cattle production": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know infertility treatments and measures to improve the fertility of cattle": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "Herbal Remedies are available to me for infertility treatment": ["a. Completely Unavailable", "b. Unavailable", "c. Partially available", "d. Available", "e. Completely Available"], "I have 100% access to treat infertility for my cattle (via veterinarians, para vets or government health camps, dairy partner team etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I can afford infertility treatment for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to treatment and treat my cattle according to prescribed norms": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to treatment in close proximity (doorstep/BMC/in village/ nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "5. Artificial Insemination Services": {"I know what are Al services and how they will benefit my cattle's production": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know which type of AI straws are available as per breeding policy": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of credible semen sources and high-quality AI services to cattle production and want to access credible semen sources and high quality AI services for my cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to credible semen sources and high-quality AI services for my cattle (via veterinarians, para vets or government health camps, etc)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I can afford credible semen and high-quality AI services for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to credible semen source and high quality Al services": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to credible semen sources and high quality AI services in close proximity (doorstep/BMC/ in village/ nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "6. Pregnancy Management": {"I know what pregnancy management is and how it will benefit my cattle's production": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know caring for Pregnant animal by providing proper nutrition, health, stress-free environment and have reach out to Veterinarian for suggestions": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of pregnancy management to cattle production and want to access in all aspects like veterinary support, feed, health for my cattle": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have 100% access to veterinary support in pregnancy support for my cattle (via veterinarians, para vets or government health camps, etc) and feed": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I can afford high quality feed/ ration for 100% of my cattle": ["a. Strongly unaffordable", "b. Unaffordable", "c. Partially affordable", "d. Affordable", "e. Strongly unaffordable"], "I have 100% timely access to quality feed and veterinary support": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have 100% access to quality feed and veterinary support in close proximity (doorstep/ BMC/ in village/ nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}},
    "Women Empowerment": {"1. Community Gender Sensitization": {"I know about the role of women in dairy farming and how they contribute to the dairy sector": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know about gender roles in society and the importance of the role of women in dairy farming": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I am sensitized to gender roles and role of women in dairy farming and recognize their importance and want to empower them": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have access to resources to gain information and opportunity to learn about gender sensitivity": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. (Strongly accessible)"]}, "2. Know-how of dairy economics": {"I know what are dairy practices and dairy economics and why women's knowledge and contribution is important": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know best dairy practices, understand dairy economics and I am financially included": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know dairy practices and dairy economics and want to be actively included and build my knowledge and self- efficacy": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have access to resources and opportunity to learn and practice dairy practices and dairy economics": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"]}, "3. Status of Women Leadership": {"I know what is women leadership and how it benefits the development of women": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know women's leadership awareness camps, training programs, leadership development programs": ["a. Strongly uniformed/ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know about leadership awareness camps, training programs, leadership development programs etc and I want to actively participate in them": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have access to leadership awareness camps, training programs, leadership development programs (via government programs/ BMC camps/NGO workshops) etc": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have access leadership awareness programs, camps, training programs, leadership development programs in close proximity (doorstep/BMC/micro training centres/villages/ nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "4. Capability building of women": {"I know what are capability building workshops, seminars and training and how they will benefit women farmer's development": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know skill development and dairy entrepreneurship focused workshops, seminars and training programmes in my vicinity": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of participating in skill development and dairy entrepreneurship workshops, training programs and development programs on women development and want to actively participate in them": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have access to skill development and dairy entrepreneurship workshops, training programs and development program (via government programs/ BMC camps/NGO workshops) etc": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"], "I have access to skill development and dairy entrepreneurship workshops, training programs and development program in close proximity (doorstep/BMC/micro training centres/villages/ nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "5. Status of promotion of innovation": {"I know what is meant by innovations and how they can benefit dairy business as well as empower women": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know about innovative methods used in dairy and farm businesses globally": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of innovating in dairy and farm businesses and want to build my knowledge and innovate better ways of doing dairy and farm business": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have access to resources to get exposed to global innovations in dairy and farm businesses": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"]}, "6. Community Groups": {"I know what are SHG and JLG groups and how they empower women dairy farmers": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know how being part of SHGs/JLGs will help me supply milk and facilitate with credit linkages to improve my dairy farm": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know the benefits of being a part of SHG and JLG groups and want to be a part of these groups": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have access to SHG and JLG groups and participate in them": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"], "I have access to SHG and JLG groups in close proximity (doorstep/BMC/ micro training centres/villages/ nearby villages)": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly inaccessible"]}, "7. Farm Practices": {"I know what are dairy farming practices and how participating in them can empower women": ["a. Completely unaware", "b. Unaware", "c. Partially aware", "d. Aware", "e. Strongly aware"], "I know about the various labour, business and financial aspects of dairy farming": ["a. Strongly uniformed/ ill-informed", "b. Uniformed/ ill- informed", "c. Partially knowledgeable", "d. Knowledgeable", "e. Strongly knowledgeable"], "I know about the various labour, business and financial aspects of dairy farming and want to actively participate in them": ["a. Strongly disagree", "b. Disagree", "c. Partially agree", "d. Agree", "e. Strongly agree"], "I have access to resources and opportunity to learn and participate in the labour, business, and financial aspects of dairy farming": ["a. Strongly inaccessible", "b. Inaccessible", "c. Partially accessible", "d. Accessible", "e. Strongly accessible"]}},
    "Farmer Participation Questionnaire": {"1. Who regularly performs daily activities on your dairy farm? (Multiple Choices Possible)": {"options": ["Husband", "Wife", "Workers", "Male children", "Female children"], "activities": ["Cleaning animals", "Cleaning farm shed", "Cleaning farm and feeding equipment", "Cleaning dairy farm", "Feeding", "Making hay and silage", "Fetching water for cleaning", "Fetching water for drinking", "Milking (in the morning)", "Milking (in the afternoon)", "Milking (in the evening)", "Delivery of Milk Cans to BMCS", ]}, "2. Who performs activities on your dairy farm? (Multiple Choices Possible)": {"options": ["Husband", "Wife", "Workers", "Male children", "Female children"], "activities": ["Segregation of sick animals", "Isolation of sick animals", "Taking cows to veterinarian/arranging for veterinarian appointments", "Farm Maintenance", "Dipping", "Handling dairy economics/ finances", "Marketing", ]}},
}


# Session State Initialization
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "responses" not in st.session_state:
    st.session_state["responses"] = {}
if "section_keys" not in st.session_state:
    st.session_state["section_keys"] = list(QUESTIONS.keys())

responses = st.session_state["responses"]
section_keys = st.session_state["section_keys"]

# --- Helper Functions (Standard) ---

def get_default_index(options, saved_value):
    if saved_value is not None and saved_value in options:
        try:
            return options.index(saved_value)
        except ValueError:
            pass
    return 0

def generate_full_key(parent_key, label):
    return f"{parent_key} | {label}" if parent_key else label

def render_multi_input_rows(question_key, data, parent_key):
    st.markdown(f"**{question_key}**")
    num_rows = data.get("Number of Respondents", 1)
    fields = data.get("fields", [])
    st.markdown(f"*(Input details for up to {num_rows} respondents)*")
    columns = st.columns(len(fields))
    for i, field in enumerate(fields):
        with columns[i]:
            st.markdown(f"**{field['label']}**")
    for i in range(1, num_rows + 1):
        row_container = st.container(border=True)
        row_columns = row_container.columns(len(fields))
        for j, field in enumerate(fields):
            full_key = generate_full_key(parent_key, f"Respondent {i} - {field['label']}")
            with row_columns[j]:
                responses[full_key] = st.text_input(
                    field['label'],
                    value=responses.get(full_key, ""),
                    key=full_key + "-input",
                    label_visibility="collapsed"
                )

def render_nested_questions(questions_data, parent_key=""):
    for key, value in questions_data.items():
        full_key = generate_full_key(parent_key, key)
        if isinstance(value, dict):
            if "options" in value and "activities" in value:
                st.markdown(f"**{key}**")
                options = value['options']
                for activity in value['activities']:
                    activity_key = generate_full_key(full_key, activity)
                    responses[activity_key] = st.multiselect(
                        activity, options=options, default=responses.get(activity_key, []), key=activity_key)
                st.markdown("---")
            elif "Number of Respondents" in value and "fields" in value:
                 render_multi_input_rows(key, value, parent_key=full_key)
            else:
                st.markdown(f"**{key}**")
                render_nested_questions(value, parent_key=full_key)
        elif isinstance(value, list):
            if "Multiple Answers Possible" in key:
                responses[full_key] = st.multiselect(
                    key, value, default=responses.get(full_key, []), key=full_key)
            else:
                responses[full_key] = st.radio(
                    key, value, index=get_default_index(value, responses.get(full_key)), key=full_key)
            if "3. How did you acquire your dairy farm land?" in key and responses.get(full_key) == "d. Rented":
                 rent_key = generate_full_key(parent_key, "If Rented, what rent do you pay for your land (mention per month/per year)?")
                 responses[rent_key] = st.text_input(
                     "**Specify Rent (per month/year)**", value=responses.get(rent_key, ""), key=rent_key + "-text")
            remarks_key = generate_full_key(parent_key, f"Remarks for {key}")
            responses[remarks_key] = st.text_area(
                "Remarks (Optional)", value=responses.get(remarks_key, ""), key=remarks_key + "-text")
            st.markdown("---")
        elif value is None:
            responses[full_key] = st.text_input(
                key, value=responses.get(full_key, ""), key=full_key)
            st.markdown("---")


# --- Main Application Flow ---

# Step 1: Informed Consent
if st.session_state["step"] == 1:
    st.title("Project Ksheersagar – FGD for Farmers")
    st.header("Step 1: Informed Consent")
    st.markdown("""
        Namaste. My name is **[Your Name]**. I am working with TechnoServe, an NGO in partnership with ABBOTT to help farmers sustainably improve milk quality and quantity.

        We are conducting this focus group discussion (FGD) to collect information on current dairy farm practices, challenges, and opportunities.
        All answers will be **confidential**. Your participation is **voluntary**.
    """)

    with st.form("consent_form"):
        responses["Consent to fill the form"] = st.radio(
            "Do you agree to participate in the discussion, and give your permission for audio recording and photo documentation?",
            ["Yes", "No"],
            index=get_default_index(["Yes", "No"], responses.get("Consent to fill the form")),
            key="consent_radio"
        )

        if st.form_submit_button("Next"):
            if responses.get("Consent to fill the form") == "Yes":
                st.session_state["step"] = 2
                st.rerun()
            else:
                st.warning("Participation is required to proceed with the survey.")
                st.stop()

# Dynamic section display
elif st.session_state["step"] in range(2, len(section_keys) + 2):

    current_step_index = st.session_state["step"] - 2
    current_step_key = section_keys[current_step_index]

    st.title("Project Ksheersagar – FGD for Farmers")
    st.info(f"**Section {st.session_state['step'] - 1} of {len(section_keys)}:** {current_step_key}")

    questions_for_step = QUESTIONS[current_step_key]
    is_background_info = (current_step_key == "A. Background Information")

    # Render content without st.form wrapper (persistence fix)
    if is_background_info:
        background_data = questions_for_step.get(list(questions_for_step.keys())[0], {})
        render_multi_input_rows(list(questions_for_step.keys())[0], background_data, current_step_key)
    else:
        render_nested_questions(questions_for_step, parent_key=current_step_key)

    # --- Navigation Buttons (using st.button outside form) ---
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state["step"] > 2:
            if st.button("Back"):
                st.session_state["step"] -= 1
                st.rerun()
        elif st.session_state["step"] == 2:
            if st.button("Back to Consent"):
                st.session_state["step"] -= 1
                st.rerun()

    with col2:
        is_last_survey_step = st.session_state["step"] == len(section_keys) + 1
        next_button_text = "Review & Submit" if is_last_survey_step else "Save and Next"

        if st.button(next_button_text):
            st.session_state["step"] += 1
            st.rerun()

# Final Review and Submission Step
elif st.session_state["step"] == len(section_keys) + 2:
    st.header("Finalize and Submit")

    with st.form("final_submit_form"):
        st.subheader("Review your responses:")
        final_responses = st.session_state["responses"].copy()

        # Prepare data for final CSV saving and display
        display_data = {}
        for k, v in final_responses.items():
            if v is not None:
                if isinstance(v, list):
                    display_data[k] = "; ".join(v)
                elif isinstance(v, str) and v.strip() == "":
                    continue
                else:
                    display_data[k] = str(v)

        if display_data:
            df = pd.DataFrame([display_data]).T
            df.columns = ["Response"]
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No responses recorded.")

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Back to Form"):
                st.session_state["step"] = len(section_keys) + 1
                st.rerun()
        with col2:
            if st.form_submit_button("✅ Submit & Save Final"):

                # --- Submission Logic ---
                submission_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                submission_id = str(uuid.uuid4())

                # Update data with final metadata
                display_data["submission_id"] = submission_id
                display_data["submission_time"] = submission_time
                df_to_save = pd.DataFrame([display_data])

                if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
                    try:
                        existing_df = pd.read_csv(CSV_FILE)
                        df_to_save = pd.concat([existing_df, df_to_save], ignore_index=True)
                    except pd.errors.EmptyDataError:
                        st.warning("Existing CSV file was empty. Overwriting.")

                df_to_save.to_csv(CSV_FILE, index=False)
                
                # --- Store the latest response data for immediate download ---
                st.session_state['last_submission_data'] = pd.DataFrame([display_data])

                st.session_state["step"] = len(section_keys) + 3
                st.rerun()

# Confirmation page after submission
elif st.session_state["step"] == len(section_keys) + 3:
    st.header("Thank you! 🙏")
    st.success("Your responses have been successfully submitted and saved.")

    # Download button for the current submission
    if 'last_submission_data' in st.session_state and not st.session_state['last_submission_data'].empty:
        df_latest = st.session_state['last_submission_data']
        latest_csv = df_latest.to_csv(index=False).encode("utf-8")
        
        # Use a filename that includes unique ID and time for easy tracking
        filename_id = df_latest['submission_id'].iloc[0][:8]
        filename = f"FGD_Response_{filename_id}_{df_latest['submission_time'].iloc[0]}.csv"

        st.download_button(
            label="⬇️ Download This Response Only (CSV)",
            data=latest_csv,
            file_name=filename,
            mime="text/csv",
        )
        st.markdown("---")
        
    # Download button for the entire dataset
    if os.path.exists(CSV_FILE):
        saved_df = pd.read_csv(CSV_FILE)
        st.subheader("All Submitted Responses (Last 5 for Verification)")
        st.dataframe(saved_df.tail(5), use_container_width=True)

        csv_download = saved_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download ALL Responses (Master CSV)",
            data=csv_download,
            file_name=CSV_FILE,
            mime="text/csv",
        )

    st.balloons()
    if st.button("Start New Survey"):
        # Clear specific keys to allow a fresh start
        for key in ["step", "responses", "last_submission_data"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
