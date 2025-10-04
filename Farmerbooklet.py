import streamlit as st
import pandas as pd
from datetime import datetime, date
import uuid
import os
import io

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Project Ksheersagar – Farmer Interview Booklet", layout="wide")

# --- Persistent storage file ---
CSV_FILE = "farmer_interview.csv"

# --- Helper Likert scales ---
awareness_scale = ["Completely unaware", "Unaware", "Partially aware", "Aware", "Strongly aware"]
knowledge_scale = ["Strongly uninformed/ill-informed", "Uninformed/ill-informed", "Partially knowledgeable", "Knowledgeable", "Strongly knowledgeable"]
agreement_scale = ["Strongly disagree", "Disagree", "Partially agree", "d. Agree", "Strongly agree"]
access_scale = ["Strongly inaccessible", "Inaccessible", "Partially accessible", "Accessible", "Strongly accessible"]
affordability_scale = ["Strongly unaffordable", "Unaffordable", "Partially affordable", "Affordable", "Strongly affordable"]
availability_scale = ["Completely Unavailable", "Unavailable", "Partially available", "Available", "Completely Available"]
person_responsible_options = ["Husband", "Wife", "Workers", "Male children", "Female children"]
economic_activities_options = ["Agriculture", "Dairy Farming", "Livestock Rearing", "Fisheries", "Daily Labor", "Private sector employment", "Government employment", "Trade/Shopkeeper", "Other"]
breed_options = ["Local", "Cross breeds", "Pure breeds"]
cow_breeds_options = ["Holstein Friesian (HF)", "Gir", "Jersey", "Red Sindhi", "Sahiwal", "Other"]

# --- Document Questions and Structure ---
QUESTIONS = {
    "Background Information": {
        "Individual Details": {
            "Name": {"type": "text_input", "options": None},
            "Age": {"type": "text_input", "options": None},
            "Highest level of education": {"type": "text_input", "options": None},
            "Number of years working as a dairy farmer": {"type": "text_input", "options": None}
        }
    },
    "Basic Household Information": {
        "What are the primary economic activities that you are involved in? (Multiple Answers Possible)": {"type": "multiselect", "options": economic_activities_options},
        "Approximately, what percentage of households in this area have dairy farming as their primary source of income?": {"type": "radio", "options": ["5-20%", "20-50%", "50-70%", "70-90%", "More than 90%"]},
        "How did you acquire your dairy farm land?": {"type": "radio", "options": ["Given by Parents", "Given by Government", "Given by Relatives", "Rented", "Purchased"]},
        "What livestock are raised within the area? Please mention their composition as well. (Multiple Answers Possible)": {"type": "multiselect", "options": ["Cows", "Buffaloes", "Hens", "Goats", "Other"]},
        "What are the animals mainly used for?": {"type": "radio", "options": ["Economic purpose", "Household consumption", "Other"]},
        "Who are the major clients of the dairy in this area?": {"type": "text_input", "options": None},
        "What do they purchase? (Multiple Answers Possible)": {"type": "multiselect", "options": ["Raw Milk", "Milk products like cheese, curd paneer etc", "Milk Powder", "Other"]},
        "What type of breeds do you have in your dairy farm? (Multiple Answers Possible)": {"type": "multiselect", "options": breed_options},
        "Which breeds of cows do you have? Please mention composition as well. (Multiple Answers Possible)": {"type": "multiselect", "options": cow_breeds_options},
        "What are the difficulties in procuring higher quality breed cows? (Multiple Answers Possible)": {"type": "multiselect", "options": ["Buying cost", "Maintenance Cost", "Difficulty in Maintaining", "Lack of Space", "Lack of access to higher quality breeds"]},
        "Where do you buy your cows from?": {"type": "text_input", "options": None},
        "What is your source of money to conduct dairy farming activities?": {"type": "radio", "options": ["Personal Finances", "Borrowing from relatives/ friends", "Bank Loans", "Government funds", "Other"]}
    },
    "Animal Care": {
        "Vaccination": {"I know what vaccinations are and how they will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know yearly vaccination schedule for atleast 6 vaccines, and whom to approach for vaccinating my cattle": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of vaccinations to cattle health and want to vaccinate my cattle as per prescribed schedule": {"options": agreement_scale, "type": "radio"}, "I have 100% access to atleast 3 vaccination dosages for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford vaccination dosages for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to vaccination and vaccinate my cattle according to prescribed vaccination schedule": {"options": access_scale, "type": "radio"}, "I have 100% access to vaccination in close proximity (doorstep/BMC/ in village/ nearby villages) and vaccinate my cattle according to prescribed vaccination schedule": {"options": access_scale, "type": "radio"}},
        "Deworming": {"I know what deworming is and how it will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know yearly deworming schedule, and whom to approach for deworming my cattle": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of deworming to cattle health and want to deworm my cattle as per prescribed schedule": {"options": agreement_scale, "type": "radio"}, "I have 100% access to deworming tablets for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford deworming services for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to deworming and deworm my cattle according to prescribed deworming schedule": {"options": access_scale, "type": "radio"}, "I have 100% access to deworming in close proximity (doorstep/BMC/ in village/ nearby villages) and deworm my cattle according to prescribed deworming schedule": {"options": access_scale, "type": "radio"}},
        "Tick Control": {"I know what tick control is and how it will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know deticking methods and how to detick my cattle": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of deticking to cattle health and want to detick my cattle": {"options": agreement_scale, "type": "radio"}, "I have 100% access to deticking services for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford deticking services for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to deticking services and detick my cattle": {"options": access_scale, "type": "radio"}, "I have 100% access to deticking services in close proximity (doorstep/BMC/in village/ nearby villages) and detick my cattle": {"options": access_scale, "type": "radio"}},
        "Preventive Check-ups": {"I know what preventive check ups are and how they will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know yearly preventive check up schedule, and whom to approach for checking my cattle": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of preventive check ups to cattle health and want to check my cattle as per prescribed schedule": {"options": agreement_scale, "type": "radio"}, "I have 100% access to preventive checkups for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford preventive check ups for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to preventive check ups and conduct checkups for my cattle according to prescribed schedule": {"options": access_scale, "type": "radio"}, "I have 100% access to check ups in close proximity (doorstep/BMC/in village/ nearby villages) and check my cattle according to prescribed schedule": {"options": access_scale, "type": "radio"}},
        "Sick Animal Segregation": {"I know what is segregation of sick animals and how it will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know segregation protocols and methods": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of segregating sick animals for cattle health and want to segregate sick animals from healthy cattle": {"options": agreement_scale, "type": "radio"}, "I have space available to segregate sick animals from healthy cattle": {"options": availability_scale, "type": "radio"}, "I have 100% access to space for segregating sick animals from healthy cattle": {"options": access_scale, "type": "radio"}, "I can afford segregation of sick animals from healthy animals for 100% of my cattle": {"options": affordability_scale, "type": "radio"}},
        "New Cattle Introduction and Testing": {"I know what is testing of new cattle before introducing them into the herd and how it will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know testing protocols and methods": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of testing new cattle before introducing them into the herd for cattle health and want to test new cattle": {"options": agreement_scale, "type": "radio"}, "I have 100% access to space for quarantine and testing new animals before introducing them into the herd": {"options": access_scale, "type": "radio"}, "I can afford quarantining and testing of new cattle before introducing them into the herd for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% access to quarantine and test new cattle before introducing them in the herd in close proximity (doorstep/BMC/in village/ nearby villages) and quarantine and test my cattle accordingly": {"options": access_scale, "type": "radio"}},
        "Feeding of Colostrum": {"I know what is feeding of colostrum to newborn calves and how it will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know how feeding milk replacers to calf will benefit them": {"options": awareness_scale, "type": "radio"}, "I know protocols and methodology for feeding colustrum& Milk replacers to newborn calves": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of feeding colostrum & Milk replacers to new born calves and want to feed the newborn calves with milk replacers": {"options": agreement_scale, "type": "radio"}, "I have milk replacers available to use for calves": {"options": availability_scale, "type": "radio"}, "I have 100% access to Milk replacers (via DP/ Paravert at door step)": {"options": access_scale, "type": "radio"}, "I can afford feeding colostrum to 100% of the new born calves on my farm": {"options": affordability_scale, "type": "radio"}, "I feed colostrum in a timely manner as per prescribed norms, to 100% of the new born calves on my farm": {"options": access_scale, "type": "radio"}},
        "Use of Herbal Remedies": {"I know what herbal remedies are and know how they will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know herbal remedies for most common preventive diseases": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of herbal remedies for my cattle and want to use herbal remedies to prevent diseases for my cattle": {"options": agreement_scale, "type": "radio"}, "Herbal remedies are available to me (via home preparation/ herbal gardens in village/ nearby villages)": {"options": availability_scale, "type": "radio"}, "I have 100% access to herbal remedies (via herbal gardens, in villages, nearby villages, micro training centres etc)": {"options": access_scale, "type": "radio"}, "I can afford getting herbal raw materials/ ready to use herbal medicines and herbal remedies for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have timely access to herbal remedies and use it to prevent diseases that maybe harmful for 100% of my catle": {"options": access_scale, "type": "radio"}, "I have 100% access to herbal remedies in close proximity (doorstep/BMC/in village/ nearby villages) and use them to prevent diseases for my cattle": {"options": access_scale, "type": "radio"}},
        "Post Dipping": {"I know what is post dipping and how it will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know post dipping solution application methods/types (Spray/cups)": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of post-dipping to cattle health and want to perform post-dipping my cattle as per the prescribed norms": {"options": agreement_scale, "type": "radio"}, "I have dipping solution and dip cups available to me": {"options": availability_scale, "type": "radio"}, "I have 100% access to post-dipping solutions for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford post-dipping chemicals for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to post-dipping chemicals and apply them to my cattle according to the prescribed norms": {"options": access_scale, "type": "radio"}, "I have 100% access to post-dipping chemicals in close proximity (doorstep/BMC/in village/ nearby villages) and apply them to my cattle according to the prescribed norms": {"options": access_scale, "type": "radio"}},
        "Assessing Healthy and Sick Animals (Body Scoring)": {"I know what is body scoring and how it will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know assessing of healthy and sick animals for 5 criteria based on body scoring": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of body scoring to cattle health and want to perform body scoring my cattle as per the prescribed norms": {"options": agreement_scale, "type": "radio"}},
        "Mastitis Testing and Prevention": {"I know what is mastitis and how its testing and prevention will benefit my cattle's health": {"options": awareness_scale, "type": "radio"}, "I know the symptoms of mastitis and its prevention using California Mastitis Test (CMT) results": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of the California Mastitis Test (CMT) to cattle health and want to perform California Mastitis Test (CMT) for my cattle as per the prescribed norms": {"options": agreement_scale, "type": "radio"}, "I have CMT solution available to me": {"options": availability_scale, "type": "radio"}, "I have 100% access to post-dipping solutions for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford California Mastitis Test (CMT) chemicals for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to California Mastitis Test (CMT) chemicals and perform California Mastitis Test (CMT) to my cattle according to the prescribed norms": {"options": access_scale, "type": "radio"}, "I have 100% access to California Mastitis Test (CMT) chemicals in close proximity (doorstep/BMC/ in village/ nearby villages) and apply them to my cattle according to the prescribed norms": {"options": access_scale, "type": "radio"}},
        "Access to Diagnostic Services": {"I know what diagnostic services are and how it will benefit my cattle's health": {"options": awareness_scale, "type": "radio"}, "I know the actions to be taken up immediately post-diagnosis like getting in touch with a Veterinarian and starting appropriate treatment protocol, taking the animal to a diagnostic facility etc": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of diagnostic facilities to cattle health and want to access diagnostic services for my cattle": {"options": agreement_scale, "type": "radio"}, "I have 100% access to diagnostic services for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford diagnostic services for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to diagnostic facilities": {"options": access_scale, "type": "radio"}, "I have 100% access to diagnostic facilities in close proximity (doorstep/BMC/ in village/ nearby villages)": {"options": access_scale, "type": "radio"}},
        "Veterinarian Services": {"I know what are veterinary services and how they will benefit my cattle's health": {"options": awareness_scale, "type": "radio"}, "I know what the services provided by para-vet and qualified veterinary doctor": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of veterinary services to cattle health and want to access veterinary services for my cattle": {"options": agreement_scale, "type": "radio"}, "Doorstep services and Veterinary Hospitals are available": {"options": availability_scale, "type": "radio"}, "I have 100% access to veterinary services for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford veterinary services for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to veterinary services": {"options": access_scale, "type": "radio"}, "I have 100% access to veterinary services in close proximity (doorstep/BMC/ in village/ nearby villages)": {"options": access_scale, "type": "radio"}},
        "Accessibility to medicines": {"I know what medicines are and how it will benefit my cattle's health": {"options": awareness_scale, "type": "radio"}, "I know the standardized treatment protocols and medicines to be used to treat the general diseases (Fever, cough/respiratory problems, lameness etc.)": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of high-quality medicines to cattle health and want to access high-quality medicines for my cattle": {"options": agreement_scale, "type": "radio"}, "I have 100% access to high-quality medicines for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford high-quality medicines for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to high-quality medicines": {"options": access_scale, "type": "radio"}, "I have 100% access to high-quality medicines in close proximity (doorstep/BMC/ in village/ nearby villages)": {"options": access_scale, "type": "radio"}},
        "Isolation of sick animals": {"I know what is isolation of sick animals and how it will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know isolation protocols and methods": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of isolating sick animals for cattle health and want to isolate sick animals from healthy cattle": {"options": agreement_scale, "type": "radio"}, "There is space available for me to isolate my sick animals from healthy cattle": {"options": availability_scale, "type": "radio"}, "I have 100% access to space for isolating sick animals from healthy cattle": {"options": access_scale, "type": "radio"}, "I can afford isolation of sick animals from healthy animals for 100% of my cattle": {"options": affordability_scale, "type": "radio"}},
        "Ethno veterinary medicine (RTU (Ready To Use) EVM)": {"I know what RTU EVM are and know how they will benefit my cattle": {"options": awareness_scale, "type": "radio"}, "I know RTU EVM for most common diseases": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of RTU EVM for my cattle and want to use RTU EVM to cure diseases for my cattle": {"options": agreement_scale, "type": "radio"}, "Herbal remedies are available to me (via home preparation/ herbal gardens in village/ nearby villages)": {"options": availability_scale, "type": "radio"}, "I have 100% access to RTU EVM (via herbal gardens, in villages, nearby villages, micro training centers etc)": {"options": access_scale, "type": "radio"}, "I can afford to get RTU EVM for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have timely access to RTU EVM and use them to cure diseases for 100% of my cattle": {"options": access_scale, "type": "radio"}, "I have 100% access to RTU EVM in close proximity (doorstep/BMC/in village/ nearby villages) and use them to cure diseases for my cattle": {"options": access_scale, "type": "radio"}},
    },
    "Cattle Breeding": {
        "Cattle Breed and Identification": {"I know how to identify different cattle breeds": {"options": awareness_scale, "type": "radio"}, "I know that different cattle breeds' production capacities, diseases resistance, and which breed is suitable for my locality": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of different cattle breeds and want to introduce new cattle in the herd": {"options": agreement_scale, "type": "radio"}, "There are various types of breeds available in my area to procure": {"options": availability_scale, "type": "radio"}, "I have 100% access to new cattle breeds (via veterinarians, para vets, government cattle schemes or DP team etc)": {"options": access_scale, "type": "radio"}, "I can afford new cattle breed introduction and its management in the herd": {"options": affordability_scale, "type": "radio"}},
        "Disease Prevention": {"I know what difficulties are faced by cattle during calving and how they will affect my cattle": {"options": awareness_scale, "type": "radio"}, "I know difficulties are faced by cattle during calving, and whom to approach for preventing": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of preventing difficulties faced by cattle during calving and want to vaccinate my cattle as per prescribed schedule": {"options": agreement_scale, "type": "radio"}, "I have 100% access to prevent/treat difficulties faced by cattle during calving for my cattle (via veterinarians, para vets or government health camps etc)": {"options": access_scale, "type": "radio"}, "I can afford to prevent difficulties are faced by cattle during calving for 100% of my cattle": {"options": affordability_scale, "type": "radio"}},
        "Reproductive Management Practices": {"I know what reproductive management practices and how it will benefit my cattle's production": {"options": awareness_scale, "type": "radio"}, "I know how to maintain a successful reproductive cycle of my cattle": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of reproductive management to cattle production and want to access in all aspects like veterinary support, feed, health for my cattle": {"options": agreement_scale, "type": "radio"}, "I have 100% access to veterinary support in reproductive management for my cattle (via veterinarians, para vets or government health camps, etc) and feed": {"options": access_scale, "type": "radio"}, "I can afford high quality feed, health care services, breeding services for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to quality feed and veterinary support": {"options": access_scale, "type": "radio"}, "I have 100% access to quality feed and veterinary support in close proximity (doorstep/ BMC/ in village/nearby villages)": {"options": access_scale, "type": "radio"}},
        "Infertility": {"I know what is cattle infertility and know how it will affect my cattle production": {"options": awareness_scale, "type": "radio"}, "I know infertility treatments and measures to improve the fertility of cattle": {"options": knowledge_scale, "type": "radio"}, "Herbal Remedies are available to me for infertility treatment": {"options": availability_scale, "type": "radio"}, "I have 100% access to treat infertility for my cattle (via veterinarians, para vets or government health camps, dairy partner team etc)": {"options": access_scale, "type": "radio"}, "I can afford infertility treatment for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to treatment and treat my cattle according to prescribed norms": {"options": access_scale, "type": "radio"}, "I have 100% access to treatment in close proximity (doorstep/BMC/in village/ nearby villages)": {"options": access_scale, "type": "radio"}},
        "Artificial Insemination Services": {"I know what are Al services and how they will benefit my cattle's production": {"options": awareness_scale, "type": "radio"}, "I know which type of AI straws are available as per breeding policy": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of credible semen sources and high-quality AI services to cattle production and want to access credible semen sources and high quality AI services for my cattle": {"options": agreement_scale, "type": "radio"}, "I have 100% access to credible semen sources and high-quality AI services for my cattle (via veterinarians, para vets or government health camps, etc)": {"options": access_scale, "type": "radio"}, "I can afford credible semen and high-quality AI services for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to credible semen source and high quality Al services": {"options": access_scale, "type": "radio"}, "I have 100% access to credible semen sources and high quality AI services in close proximity (doorstep/BMC/ in village/ nearby villages)": {"options": access_scale, "type": "radio"}},
        "Pregnancy Management": {"I know what pregnancy management is and how it will benefit my cattle's production": {"options": awareness_scale, "type": "radio"}, "I know caring for Pregnant animal by providing proper nutrition, health, stress-free environment and have reach out to Veterinarian for suggestions": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of pregnancy management to cattle production and want to access in all aspects like veterinary support, feed, health for my cattle": {"options": "agreement_scale", "type": "radio"}, "I have 100% access to veterinary support in pregnancy support for my cattle (via veterinarians, para vets or government health camps, etc) and feed": {"options": access_scale, "type": "radio"}, "I can afford high quality feed/ ration for 100% of my cattle": {"options": affordability_scale, "type": "radio"}, "I have 100% timely access to quality feed and veterinary support": {"options": access_scale, "type": "radio"}, "I have 100% access to quality feed and veterinary support in close proximity (doorstep/ BMC/ in village/ nearby villages)": {"options": access_scale, "type": "radio"}},
    },
    "Women Empowerment": {
        "Community Gender Sensitization": {"I know about the role of women in dairy farming and how they contribute to the dairy sector": {"options": awareness_scale, "type": "radio"}, "I know about gender roles in society and the importance of the role of women in dairy farming": {"options": knowledge_scale, "type": "radio"}, "I am sensitized to gender roles and role of women in dairy farming and recognize their importance and want to empower them": {"options": agreement_scale, "type": "radio"}, "I have access to resources to gain information and opportunity to learn about gender sensitivity": {"options": access_scale, "type": "radio"}},
        "Know-how of dairy economics": {"I know what are dairy practices and dairy economics and why women's knowledge and contribution is important": {"options": awareness_scale, "type": "radio"}, "I know best dairy practices, understand dairy economics and I am financially included": {"options": knowledge_scale, "type": "radio"}, "I know dairy practices and dairy economics and want to be actively included and build my knowledge and self- efficacy": {"options": agreement_scale, "type": "radio"}, "I have access to resources and opportunity to learn and practice dairy practices and dairy economics": {"options": access_scale, "type": "radio"}},
        "Status of Women Leadership": {"I know what is women leadership and how it benefits the development of women": {"options": awareness_scale, "type": "radio"}, "I know women's leadership awareness camps, training programs, leadership development programs": {"options": knowledge_scale, "type": "radio"}, "I know about leadership awareness camps, training programs, leadership development programs etc and I want to actively participate in them": {"options": agreement_scale, "type": "radio"}, "I have access to leadership awareness camps, training programs, leadership development programs (via government programs/ BMC camps/NGO workshops) etc": {"options": access_scale, "type": "radio"}, "I have access leadership awareness programs, camps, training programs, leadership development programs in close proximity (BMC/micro training centres/villages/ nearby villages)": {"options": access_scale, "type": "radio"}},
        "Capability building of women": {"I know what are capability building workshops, seminars and training and how they will benefit women farmer's development": {"options": awareness_scale, "type": "radio"}, "I know skill development and dairy entrepreneurship focused workshops, seminars and training programmes in my vicinity": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of participating in skill development and dairy entrepreneurship workshops, training programs and development programs on women development and want to actively participate in them": {"options": agreement_scale, "type": "radio"}, "I have access to skill development and dairy entrepreneurship workshops, training programs and development program (via government programs/ BMC camps/NGO workshops) etc": {"options": access_scale, "type": "radio"}, "I have access to skill development and dairy entrepreneurship workshops, training programs and development program in close proximity (BMC/micro training centres/villages/ nearby villages)": {"options": access_scale, "type": "radio"}},
        "Status of promotion of innovation": {"I know what is meant by innovations and how they can benefit dairy business as well as empower women": {"options": awareness_scale, "type": "radio"}, "I know about innovative methods used in dairy and farm businesses globally": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of innovating in dairy and farm businesses and want to build my knowledge and innovate better ways of doing dairy and farm business": {"options": agreement_scale, "type": "radio"}, "I have access to resources to get exposed to global innovations in dairy and farm businesses": {"options": access_scale, "type": "radio"}},
        "Community Groups": {"I know what are SHG and JLG groups and how they empower women dairy farmers": {"options": awareness_scale, "type": "radio"}, "I know how being part of SHGs/JLGs will help me supply milk and facilitate with credit linkages to improve my dairy farm": {"options": knowledge_scale, "type": "radio"}, "I know the benefits of being a part of SHG and JLG groups and want to be a part of these groups": {"options": agreement_scale, "type": "radio"}, "I have access to SHG and JLG groups and participate in them": {"options": access_scale, "type": "radio"}, "I have access to SHG and JLG groups in close proximity (BMC/ micro training centres/villages/ nearby villages)": {"options": access_scale, "type": "radio"}},
        "Farm Practices": {"I know what are dairy farming practices and how participating in them can empower women": {"options": awareness_scale, "type": "radio"}, "I know about the various labour, business and financial aspects of dairy farming": {"options": knowledge_scale, "type": "radio"}, "I know about the various labour, business and financial aspects of dairy farming and want to actively participate in them": {"options": agreement_scale, "type": "radio"}, "I have access to resources and opportunity to learn and participate in the labour, business, and financial aspects of dairy farming": {"options": access_scale, "type": "radio"}},
    },
    "Farmer Participation Questionnaire": {
        "1. Who regularly performs daily activities on your dairy farm? (Multiple Choices Possible)": {
            "type": "multiselect_list",
            "options": person_responsible_options,
            "list": ["Cleaning animals", "Cleaning farm shed", "Cleaning farm and feeding equipment", "Cleaning dairy farm", "Feeding", "Making hay and silage", "Fetching water for cleaning", "Fetching water for drinking", "Milking (in the morning)", "Milking (in the afternoon)", "Milking (in the evening)", "Delivery of Milk Cans to BMCS"]
        },
        "2. Who performs activities on your dairy farm? (Multiple Choices Possible)": {
            "type": "multiselect_list",
            "options": person_responsible_options,
            "list": ["Segregation of sick animals", "Isolation of sick animals", "Taking cows to veterinarian/arranging for veterinarian appointments", "Farm Maintenance", "Dipping", "Handling dairy economics/ finances", "Marketing"]
        }
    },
    "Farm Observation": {
        "1. Hazard and Contamination": {"type": "text_area", "list": ["Check if there are secure boundaries from adjoining neighbours"]},
        "2. Treatment Protocols": {"type": "text_area", "list": ["Observe for written treatment process/protocols / investigating forms if he has any"]},
        "3. Antibiotic Withdrawal Chart": {"type": "text_area", "list": ["Observe for the display of any antibiotic withdrawal limits chart"]},
        "4. Access to clean drinking water": {"type": "text_area", "list": ["Observe for unlimited drinking water throughout the day for cattle", "Observe the cleanliness of water trough/tank"]},
        "5. Access to quality and palatable feed": {"type": "text_area", "list": ["Observe the Nutrient composition of feed", "Check if palatable feed is available on the farm"]},
        "6. Knowledge of alternate feeds and their access": {"type": "text_area", "list": ["Alternate feeds available on farm"]},
        "7. Carbon Sequestration": {"type": "text_area", "list": ["Observe green fodder on farm", "Observe moringa and other high quality seeds on farm"]},
        "8. Segregation of feed and equipment's": {"type": "text_area", "list": ["Feed and chemical handling equipment segregated on the farm", "Feed and chemical handling equipment stored properly and separate from each other"]},
        "9. Feed protection": {"type": "text_area", "list": ["Feed well protected on farm", "Feed properly packed to secure from physical and chemical damages"]},
        "10. Documentation and maintenance of Feed records": {"type": "text_area", "list": ["Check for records", "Records for cattle feed, ration and nutrition", "Observe the source of availability for purchase of cattle feed"]},
        "11. Testing of water and feed": {"type": "text_area", "list": ["Observe for water and feed testing reports"]},
        "12. Knowledge of and access to quality hay and silage": {"type": "text_area", "list": ["Observe for hay and silage usage", "Observe for hay and silage making facilities & process", "Observe for crops used and its harvesting age for hay and silage preparation"]},
        "13. Usage of toxin binder in cattle feed": {"type": "text_area", "list": ["Observe the practice of using toxin binders in feed", "Observe for a percentage of toxin binder on the feed pack", "Observe for rodents infestation"]},
        "14. Availability of Compliant Cattle Feed": {"type": "text_area", "list": ["Observe the cattle feed brands used in farm", "Observe the storage area for moisture and elevation, fodder coverage", "Observe for pest incidences & mould/fungal growth"]},
        "15. Dry fodder protection": {"type": "text_area", "list": ["Observe for fouls smell, colour change, fungus growth, rancidity of dry fodder", "Observe the storage area for moisture and elevation, fodder coverage", "Observe for rodents infestation", "Observe for stacking", "Observe materials used for fodder coverage"]},
        "16. Liver Detoxification": {"type": "text_area", "list": ["Observe cattle skin and eyes for yellowish tinges jaundice, and color change in urine", "Observe for liver tonics availability in shed"]},
        "17. Acidosis": {"type": "text_area", "list": ["Observe for the usage of eating soda during feeding"]},
        "18. Protection of feed": {"type": "text_area", "list": ["Observe for fouls smell, color change, fungus growth, rancidity of cattle feed", "Observe the storage area for moisture and elevation, fodder coverage", "Observe for rodents infestation", "Observe for lumps/ hard mass presence in feed"]},
        "19. Clean feed manger and water": {"type": "text_area", "list": ["Observe the feed manger and water trough/ vessels for their cleanliness", "Observe for the algae/fungal growth/slimy underlining in water storage structures", "Observe for water transparency", "Observe for feed residues/wastage in water storage structures", "Observe for prevalence of flies", "Observe for height of feed manger and water trough from ground level"]},
        "20. Cleaning and disinfection": {"type": "text_area", "list": ["Observe for chemicals/ solutions used for cleaning and disinfection"]},
        "21. Assessment of cleanliness": {"type": "text_area", "list": ["Observe for the cleanliness of floor, stall, bedding", "Observe for floor dryness"]},
        "22. Access to water": {"type": "text_area", "list": ["Observe for adequate water source availability"]},
        "23. Provision for drainage and waste disposal (only for commercial farms)": {"type": "text_area", "list": ["Observe for drainage facility", "Observe for dung, urine & water stagnation", "Observe for a distance of the dumping yard from the farm shed"]},
        "24. Manure Management": {"type": "text_area", "list": ["Observe for the presence of a dumping pit"]},
        "25. Biogas Installation": {"type": "text_area", "list": ["Observe for presence of bio-gas installation and utilization"]},
        "26. Water Conservation Management": {"type": "text_area", "list": ["Observe for waste water storage", "Observe for waste water re-utilization"]},
        "27. Farm Shed Design": {"type": "text_area", "list": ["Observe the type of farm shed (basic/normal, modern)", "Observe the farm shed roof (closed /open)", "Observe for farm having customized cattle shed for calf, heifers, bulls and milking cows.", "Observe for proper drainage, ventilation, aeration", "Observe for cleaning and disinfection solutions"]},
        "28. Protection from climate extremes": {"type": "text_area", "list": ["Observe well-ventilated, protected from extremes of weather, have optimal space for animals and clean drinking water, loud noises", "Check if there is proper ventilation in cattle shed", "Check if there is shed protection/ shade", "Check if the shed has concrete flooring with proper provisions for waste handling and drainage", "Check if floors, feeding trough and farm shed are cleaned regularly"]},
        "29. Safe surfaces": {"type": "text_area", "list": ["Check if cattle shed flooring is skid free, soil/dirt free, dry and comfortable to move and rest"]},
        "30. Comfort of cattle": {"type": "text_area", "list": ["Check if cattle has enough space to move and rest", "Check if well protected loose housing system with well-defined boundary is established on farm"]},
        "31. Space in shed": {"type": "text_area", "list": ["Check if cattle if optimal space to move and rest", "Check if there is availability of clean drinking water", "Check is the surfaces are safe, to minimize discomfort and injuries"]},
        "32. Waste handling and disposal": {"type": "text_area", "list": ["Check if cattle has enough space to move and rest", "Check if well protected loose housing system with well-defined boundary is established on farm"]}
    },
    "Animal Observation": {
        "Hygiene Score": {"type": "radio", "options": ["1", "2", "3", "4"]},
        "Locomotion Score": {"type": "radio", "options": ["1", "2", "3"]},
        "Body Conditioning Score": {"type": "radio", "options": ["1", "2", "3", "4", "5"]},
        "Hock Lesion Score (for Hock)": {"type": "radio", "options": ["1", "2", "3", "4", "5"]},
        "Hock Lesion Score (for Knee)": {"type": "radio", "options": ["1", "2", "3"]},
        "Udder Score (Udder Suspension)": {"type": "radio", "options": ["1", "2", "3", "4", "5"]},
        "Udder Score (Teat Size)": {"type": "radio", "options": ["1", "2", "3", "4", "5"]},
        "Documentation and Maintenance of Cattle Records": {"type": "text_area_list", "list": ["Check for records", "Records for cattle treatment"]},
        "Animal Grooming": {"type": "text_area_list", "list": ["Observe for tick infestation", "Observe for dung and soil adherence on cow skin coat", "Observe for loose hair", "Observe for grooming materials like brushes etc", "Observe for ears, tails, and lower side of hip joints for cleanliness"]},
        "Hoof Hygiene": {"type": "text_area_list", "list": ["Observe for lameness, hoof injuries", "Observe for foot baths, hoof mats, and foaming systems", "Observe for hoof cleaning solutions", "Observe for hoof trimming materials", "Observe for floor smooth & slipper or hard and firm"]},
        "Udder hygiene": {"type": "text_area_list", "list": ["Observe for dirt/dung splashes/particle adherence on udder and teat surfaces and hip joint", "Observe for swollen and reddening of teats", "Observe for udder and teat injuries", "Observe for soil, dust and animal wastages on the floor cleanness", "Observe milkers hands for nails", "Observe for teat dippers usage and availability", "Observe for udder disinfecting solutions"]},
        "Life Cycle Records": {"type": "text_area_list", "list": ["Check for records", "Check for records of cattle life cycle (age, lactations, calf mortality etc.)", "Check if there are digital records"]},
        "Breeding Records": {"type": "text_area_list", "list": ["Check for records", "Check for records of dates of heat, service and parturition", "Check if there are digital records"]}
    }
}


# --- Session State Initialization and Data Loading ---
if 'farmer_interview_data' not in st.session_state:
    if os.path.exists(CSV_FILE):
        try:
            st.session_state.farmer_interview_data = pd.read_csv(CSV_FILE).to_dict('records')
        except (pd.errors.EmptyDataError, TypeError):
            st.session_state.farmer_interview_data = []
    else:
        st.session_state.farmer_interview_data = []

if 'current_entry' not in st.session_state:
    st.session_state['current_entry'] = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

entry = st.session_state['current_entry']

def get_default_value(key, default_value=None):
    """Safely retrieves a value from the current entry, initializing if missing."""
    # Ensure default for multiselect is an empty list if None is provided
    if default_value is None and 'multiselect' in key.lower():
        default_value = []
    return entry.setdefault(key, default_value)

# --- App Title ---
st.title("Project Ksheersagar – Farmer Interview Booklet")

# --- Main App Logic ---
# --- Start/Reset Buttons ---
col1, col2, _ = st.columns([1, 1, 3])
with col1:
    if st.button("🔄 Start New Interview", key="start_new_btn_top"):
        for key in ['current_entry', 'last_submission_data']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
with col2:
    if st.button("🗑️ Clear and Reset Current Form", key="reset_top_button"):
        if 'current_entry' in st.session_state:
            del st.session_state['current_entry']
        st.info("Form has been reset. Rerunning...")
        st.rerun()
st.markdown("---")

# --- Informed Consent ---
st.header("Informed Consent")
st.markdown("Namaste. My name is **[Your Name]**. We are conducting this discussion to collect information on the current dairy farm structure, practices, challenges, and opportunities. Your participation is **voluntary** and your answers will be **confidential**.")
consent_key = "initial_consent"
consent_options = ["Yes", "No"]
default_consent = get_default_value(consent_key, "No")
consent_index = consent_options.index(default_consent) if default_consent in consent_options else 1
entry[consent_key] = st.radio(
    "Do you agree to participate in the discussion, and give your permission for audio recording and photo documentation?",
    consent_options,
    index=consent_index,
    key="consent_radio"
)

# --- Main Form ---
if entry.get("initial_consent") == "Yes":

    # --- Identification Section (Live entry, outside the main form) ---
    st.header("1. Identification")
    st.info("This section saves as you type.")
    col1, col2 = st.columns(2)
    with col1:
        entry["dairy_partner"] = st.text_input("Name of Dairy Partner", value=get_default_value("dairy_partner", ""), key="dp_name_input")
        entry["bmc_name"] = st.text_input("Name of BMC", value=get_default_value("bmc_name", ""), key="bmc_name_input")
        entry["state"] = st.text_input("State", value=get_default_value("state", ""), key="state_input")
    with col2:
        entry["district"] = st.text_input("District", value=get_default_value("district", ""), key="district_input")
        entry["village"] = st.text_input("Village", value=get_default_value("village", ""), key="village_input")
        entry["interviewer"] = st.text_input("Name of Interviewer", value=get_default_value("interviewer", ""), key="interviewer_input")
        default_date_val = get_default_value("date", datetime.now().date())
        if isinstance(default_date_val, str):
            try:
                # Handle conversion from string (from CSV) to date object for st.date_input
                default_date_val = datetime.strptime(default_date_val, "%Y-%m-%d").date()
            except ValueError:
                default_date_val = datetime.now().date()
        entry["date"] = st.date_input("Date", value=default_date_val, key="date_input")
    st.markdown("---")

    # --- Survey Questions Form ---
    st.header("2. Survey Questionnaire")
    st.warning("Your progress in this section is **NOT** saved live. Please click the **'💾 Save Progress'** button below to save your inputs.", icon="⚠️")
    
    # List to store all the keys we expect to be updated by the form widgets
    # This helps in the final step of pulling data from st.session_state
    form_widget_keys = []
    
    with st.form(key='survey_form', clear_on_submit=False):
        for section_title, subsections in QUESTIONS.items():
            with st.expander(f"Section: {section_title}", expanded=False):
                if section_title == "Background Information":
                    st.markdown("Tell me a little bit about your background information such as age, education, experience as a dairy farmer.")
                    respondent_fields = ["Name", "Age", "Highest level of education", "Number of years working as a dairy farmer"]
                    for i in range(1, 11):
                        st.markdown(f"**Respondent {i}**")
                        cols = st.columns(len(respondent_fields))
                        for j, field_name in enumerate(respondent_fields):
                            response_key = f"respondent_{i}_{field_name.replace(' ', '_').lower()}"
                            form_widget_keys.append(response_key) # Track key
                            with cols[j]:
                                # Use the response_key as the widget key
                                entry[response_key] = st.text_input(
                                    field_name,
                                    value=get_default_value(response_key, ""),
                                    key=response_key, # Use the response_key here
                                    label_visibility="collapsed" if i > 1 else "visible"
                                )
                        st.markdown("---")
                elif section_title == "Basic Household Information":
                    st.markdown("I would like to know a few pieces of information about the dairy farm structure size and types of breeds commonly used by the dairy farming community here.")
                    for question_text, question_details in subsections.items():
                        q_type = question_details["type"]
                        q_options = question_details.get("options")
                        response_key = question_text.replace(' ', '_').replace('?', '').replace('(Multiple_Answers_Possible)', '').replace(',', '').replace('/', '').lower()
                        form_widget_keys.append(response_key) # Track key

                        if q_type == "radio":
                            default_val = get_default_value(question_text, q_options[0])
                            default_idx = q_options.index(default_val) if default_val in q_options else 0
                            # Use the response_key as the widget key and rely on the return value
                            st.session_state[response_key] = st.radio(question_text, options=q_options, index=default_idx, key=response_key)
                        elif q_type == "multiselect":
                            # Default for multiselect needs to be an empty list if not set
                            default_multiselect = get_default_value(question_text, [])
                            # Default for st.multiselect must be a list of selected options
                            st.session_state[response_key] = st.multiselect(question_text, options=q_options, default=default_multiselect, key=response_key)
                        elif q_type == "text_input":
                            st.session_state[response_key] = st.text_input(question_text, value=get_default_value(question_text, ""), key=response_key)

                        # Special case for 'Rented'
                        if question_text == "How did you acquire your dairy farm land?" and st.session_state.get(response_key) == "Rented":
                            rent_key = "If Rented, what rent do you pay for your land (mention per month/per year)?"
                            form_widget_keys.append(rent_key) # Track special key
                            st.session_state[rent_key] = st.text_input(rent_key, value=get_default_value(rent_key, ""), key=rent_key)
                        st.markdown("---")
                        
                elif section_title in ["Animal Care", "Cattle Breeding", "Women Empowerment"]:
                    for subsection_title, questions in subsections.items():
                        st.markdown(f"#### {subsection_title}")
                        for question_text, question_details in questions.items():
                            q_options = question_details.get("options")
                            response_key = f"{section_title}-{subsection_title}-{question_text}"
                            form_widget_keys.append(response_key) # Track key
                            
                            default_val = get_default_value(response_key, q_options[0])
                            default_idx = q_options.index(default_val) if default_val in q_options else 0
                            
                            # Use the response_key as the widget key
                            st.session_state[response_key] = st.radio(question_text, options=q_options, index=default_idx, key=response_key)
                            
                            remarks_key = f"Remarks for {response_key}"
                            form_widget_keys.append(remarks_key) # Track remarks key
                            # Use the remarks_key as the widget key
                            st.session_state[remarks_key] = st.text_area(f"Remarks for **{question_text}** (Optional)", value=get_default_value(remarks_key, ""), key=remarks_key)
                            st.markdown("---")
                            
                elif section_title == "Farmer Participation Questionnaire":
                    for subsection_title, question_details in subsections.items():
                        st.markdown(f"#### {subsection_title}")
                        if question_details["type"] == "multiselect_list":
                            st.write(subsection_title)
                            for activity in question_details["list"]:
                                response_key = f"Who performs: {activity}"
                                form_widget_keys.append(response_key) # Track key
                                # Use the response_key as the widget key
                                st.session_state[response_key] = st.multiselect(activity, options=question_details["options"], default=get_default_value(response_key, []), key=response_key)
                                st.markdown("---")
                                
                elif section_title in ["Farm Observation", "Animal Observation"]:
                    for subsection_title, question_details in subsections.items():
                        st.markdown(f"#### {subsection_title}")
                        if question_details["type"] == "radio":
                            response_key = f"Score: {subsection_title}"
                            form_widget_keys.append(response_key) # Track key
                            q_options = question_details["options"]
                            default_val = get_default_value(response_key, q_options[0])
                            default_idx = q_options.index(default_val) if default_val in q_options else 0
                            # Use the response_key as the widget key
                            st.session_state[response_key] = st.radio("Score", options=q_options, index=default_idx, key=response_key)
                            
                            remarks_key = f"Remarks for Score: {subsection_title}"
                            form_widget_keys.append(remarks_key) # Track remarks key
                            # Use the remarks_key as the widget key
                            st.session_state[remarks_key] = st.text_area("Remarks", value=get_default_value(remarks_key, ""), key=remarks_key)
                            
                        elif question_details["type"] in ["text_area", "text_area_list"]:
                            for item in question_details["list"]:
                                response_key = f"Observation: {subsection_title} - {item}"
                                form_widget_keys.append(response_key) # Track key
                                # Use the response_key as the widget key
                                st.session_state[response_key] = st.text_area(item, value=get_default_value(response_key, ""), key=response_key)
                                
                        st.markdown("---")

        submitted = st.form_submit_button("💾 Save Progress")
        
        # --- FIX APPLIED HERE ---
        if submitted:
            # Iterate through all the response keys we generated and update the 'entry' dict
            for key in form_widget_keys:
                if key in st.session_state:
                    # Update the entry dictionary with the new value from the form widget
                    entry[key] = st.session_state[key]
            
            # Special case for the land acquisition follow-up, check if it was rendered and update
            rent_key = "If Rented, what rent do you pay for your land (mention per month/per year)?"
            if st.session_state.get('basic_household_information_how_did_you_acquire_your_dairy_farm_land') == "Rented":
                if rent_key in st.session_state:
                    entry[rent_key] = st.session_state[rent_key]
            else:
                 # Clear the key if the 'Rented' option is no longer selected
                if rent_key in entry:
                    del entry[rent_key]
            
            # Update the entire session state entry to force Streamlit to recognize the change
            st.session_state['current_entry'] = entry
            
            st.success("Progress saved! You can continue editing or finalize the submission below.")

    st.header("3. Final Submission")
    st.markdown("---")
    if st.button("✅ Finalize and Submit Interview", key="final_submit_btn"):
        # The FIX ensures 'entry' is up-to-date from the last Save Progress click.
        # However, if the user fills the form and clicks 'Finalize' *without* clicking 'Save Progress',
        # the latest inputs are still stored in st.session_state. We need to pull them one last time.
        
        # --- RE-APPLY THE FIX FOR FINAL SUBMISSION ---
        for key in form_widget_keys:
             if key in st.session_state:
                 entry[key] = st.session_state[key]

        rent_key = "If Rented, what rent do you pay for your land (mention per month/per year)?"
        if st.session_state.get('basic_household_information_how_did_you_acquire_your_dairy_farm_land') == "Rented":
            if rent_key in st.session_state:
                entry[rent_key] = st.session_state[rent_key]
        else:
             if rent_key in entry:
                 del entry[rent_key]
        # --- END OF RE-APPLY ---

        required_fields = ["dairy_partner", "interviewer", "initial_consent"]
        if not all(entry.get(f) for f in required_fields):
            st.error("Please ensure the Identification section (Dairy Partner and Interviewer Name) and Consent are completed.")
        else:
            entry["submission_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry["submission_id"] = str(uuid.uuid4())
            st.session_state.farmer_interview_data.append(entry.copy())
            df_all = pd.DataFrame(st.session_state.farmer_interview_data)
            df_all.to_csv(CSV_FILE, index=False)
            st.session_state['last_submission_data'] = pd.DataFrame([entry])
            st.success("Interview submitted successfully! 🎉 The form has been reset for the next interview.")
            del st.session_state['current_entry']
            st.rerun()

elif entry.get("initial_consent") == "No" and st.session_state.get('consent_radio') == "No":
    st.warning("Participation consent is required to proceed with the survey.")

if 'last_submission_data' in st.session_state and not st.session_state.get('last_submission_data', pd.DataFrame()).empty:
    st.header("Submission Complete & Download Options")
    df_latest = st.session_state['last_submission_data']
    latest_csv = df_latest.to_csv(index=False).encode("utf-8")
    submission_id_short = df_latest['id'].iloc[0][:8]
    # Check if 'submission_timestamp' exists before accessing it
    timestamp_str = df_latest['submission_timestamp'].iloc[0].replace(' ', '_').replace(':', '-') if 'submission_timestamp' in df_latest.columns and not df_latest['submission_timestamp'].empty else datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"FIB_Response_{submission_id_short}_{timestamp_str}.csv"
    st.download_button(
        label="⬇️ Download This Response Only (CSV)",
        data=latest_csv,
        file_name=filename,
        mime="text/csv",
    )
    st.markdown("---")

st.header("Previously Submitted Responses")
if st.session_state.farmer_interview_data:
    df_all = pd.DataFrame(st.session_state.farmer_interview_data)
    display_cols = [col for col in df_all.columns if not col.startswith(('Observation:', 'Remarks for'))]
    st.dataframe(df_all[display_cols].tail(10), use_container_width=True)
    csv_download_all = df_all.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download All Submissions (Master CSV)",
        csv_download_all,
        file_name="farmer_interview_all.csv",
        mime="text/csv"
    )
else:
    st.info("No responses yet.")
