import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import uuid

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Project Ksheersagar – TNS Self-Assessment", layout="wide")

# --- Global Configuration and State Initialization ---
CSV_FILE = "self_assessment_TNS_responses.csv"

if "step" not in st.session_state:
    st.session_state.step = 0  # Start at Step 0 (Consent)
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --- Data Loading ---
@st.cache_data
def get_questions():
    """
    Loads the entire survey questions dictionary.
    """
    return {
        "Respondent and Location Details": {
            "Name of the Dairy Partner": ["Parag", "Sunfresh Lactalis", "Govind", "Schreiber"],
            "Name of the respondent": None,
            "Respondent Email ID": None,
            "Respondent Contact Number": None,
            "Designation": ["Route Incharge", "Facilitator", "Manager", "Supervisor", "Entrepreneur", "Other"],
            "Department": ["Procurement", "Dairy Extension", "Quality", "Other"],
            "Milk chilling and collection center": ["BMC", "MCC"],
            "BMC/ MCC Name": None,
            "BMC/ MCC code": None,
            "Route Number": None,
            "Route Details": None,
            "Location (Village, Taluka, District)": None,
            "Date of response": None,
            # These fields are handled in the consent step but kept here for structure
            "Consent to fill the form": ["Yes", "No"],
            "Signature of the respondent": None,
            "Reviewed and confirmed by Route Incharge": ["Yes", "No"],
            "Signature of Route In charge": None,
            "Reviewed and confirmed by Ksheersagar SPOC": ["Yes", "No"],
            "Signature of SPOC": None,
        },
        "1. Animal Care": {
            "1.1 Cattle Health": {
                "1.1.1 Preventive Care": {
                    "1.1.1.1 Vaccination, deworming, tick control and preventive checks ups": ["a. 100% of dairy farmers are aware and have sufficient knowledge of recommended vaccinations (6), deworming, and tick control schedules", "b. 100% of dairy farmers can access vaccines (3) and as per vaccination services provided by government and/ or private, deworming and tick medicines, and preventive checkups timely as per recommended schedule", "c. Timely doorstep services ensured for all cattle for vaccinations (3), deworming, tick and preventive checkups as per recommended schedule at an affordable price", "d. Timely affordable doorstep services ensured for all cattle for vaccinations (6), deworming, and preventive checkups as per recommended schedule.", "e. 100% cattle vaccinated (8 recommended vaccines, stock as provided by government from time to time), dewormed, checked periodically based on prescribed schedule customized to different physiological stages of the cattle cycle", "f. None of the above", "g. Not aware"],
                    "1.1.1.2 Documentation and maintenance of records": ["a. Written records of all cattle and their treatments are maintained and available for further investigation by 40% of farmers", "b. Written records of all cattle and their treatments are maintained and available for further investigation by 60% of farmers", "c. Written records of all cattle and their treatments are maintained and available for further investigation by 80% of farmers", "d. Written records of all cattle and their treatments are maintained and available for further investigation by 100% of dairy farmers", "e. Digital records of all cattle and their treatments are maintained and available for further investigation for all dairy farmers", "f. None of the above", "g. Not aware"],
                    "1.1.1.3 Sick animal segregation": ["a. Segregation of healthy cattle from the sick is practiced by 60% of dairy farmers", "b. Segregation of healthy cattle from the sick is practiced by 80% of dairy farmers", "c. Segregation of healthy cattle from the sick is practiced by 100% farmers and a designated space available for segregation", "d. Segregation of 100% of sick animals is practiced", "e. Segregation of healthy cattle from the 100% sick animals is practiced by 100% dairy farmers", "f. None of the above", "g. Not aware"],
                    "1.1.1.4 New cattle introduction and testing": ["a. 100% of dairy farmers are aware and have preliminary knowledge of the criteria for selection of healthy animal/s before introducing them into the herd", "b. Health status of animals sourced is known to 100% of dairy farmers", "c. Health status of animals sourced is known to 100% of dairy farmers and their introduction is controlled into the herd through quarantine. Testing of these animals at an affordable price is ensured.", "d. Health status of animals sourced is known to 100% of dairy farmers through testing that is available at an affordable price and 100% of cattle introduced are quarantined.", "e. Health status of 100% animals sourced is known through in house testing infrastructure and their introduction into the herd is 100% controlled through quarantine", "f. None of the above", "g. Not aware"],
                    "1.1.1.5 Feeding of colostrum": ["a. Colostrum fed to newborn calves by 100% dairy farmers", "b. Colostrum fed to newborn calves for 3 days by 100% of dairy farmers", "c. Colostrum fed at least 2 LPD of fresh colostrum over 3 days to newborn calves by 100% of dairy farmers", "d. Colostrum fed to newborn calves (2 L in first 2 hours and 1-2 LPD for next 2-3 days) by all dairy farmers", "e. Colostrum fed to newborn calves (2 L in first 2 hours and 2 LPD of fresh colostrum in a day over 3-4 times for next 5-7 days)", "f. None of the above", "g. Not aware"],
                    "1.1.1.6 Use of herbal remedies": ["a. 100 % of dairy farmers are aware of Herbal remedies for most common preventive diseases", "b. Herbal remedies are adopted and practiced by 100% of dairy farmers", "c. Herbal raw materials or ready to use herbal medicines are made easily available and herbal remedies are practiced by 100% dairy farmers", "d. Herbal remedies are adopted and practiced on 100% cattle with highest level of self-efficacy and diseases are prevented.", "e. Herbal gardens are promoted widely and herbal remedies and ready to use medicines are easily accessible to 100% of dairy farmers who are practicing herbal remedies on regular", "f. None of the above", "g. Not aware"],
                    "1.1.1.7 Hazard and contamination": ["a. 100% of dairy farmers are aware and have knowledge of potential hazards caused by bio contaminants", "b. 100% of dairy farmers monitor farms from potential hazards and secure boundaries from adjoining neighbors", "c. 100% of dairy farmers are aware and have knowledge of inter-herd and intra- herd practices to reduce bio contamination", "d. Biosecurity is enhanced and bio contamination reduced through the adoption of inter-herd and intra-herd practice by 80% dairy farmers", "e. Biosecurity is enhanced and bio contamination reduced through the adoption of inter-herd and intra-herd practice by 100% dairy farmers", "f. None of the above", "g. Not aware"],
                    "1.1.1.8 Post dipping": ["a. 100% of dairy farmers are aware of post dipping with prescribed chemicals to prevent mastitis", "b. 100% of dairy farmers are adopting post dipping with prescribed dosages of chemicals to prevent mastitis", "c. 100% of dairy farmers are having access to chemicals for post dipping and are adopting on 100% of their milch cattle", "d. 100% of dairy farmers have access to chemicals for post dipping at an affordable price at their doorstep and practice post dipping on 100% of their cattle immediate post milking", "e. Post dipping done mandatorily as practice on 100% of cattle in herd immediately post milking using globally approved prescribed chemicals", "f. None of the above", "g. Not aware"]
                },
                "1.1.2 Disease Diagnosis": {
                    "1.1.2.1 Body scoring (assessing healthy and sick animals)": ["a. 100 % of dairy farmers are aware and have sufficient knowledge of body scoring i.e. assessing healthy (for at least 5 criteria) and sick animals (at least 5 parameters). 60 % of dairy farmers apply body scoring knowledge as part of the daily animal care regime", "b. 100% of dairy farmers are aware and have sufficient knowledge of body scoring i.e. assessing healthy (at least 8 criteria) and sick animals (at least 20 parameters). 80% dairy farmers apply body scoring knowledge as part of the daily animal care regime", "c. 100% dairy farmers do body scoring of all animals as part of the daily animal care regime and 80% of dairy farmers segregate healthy animals from diseased", "d. 100% dairy farmers do body scoring of 100% of animals as part of the daily animal care regime", "e. Body Scoring of 100% cattle done based on a prescribed checklist which is used periodically to assess signs of healthy animals (13 criteria) and signs of disease (20 parameters)", "f. None of the above", "g. Not aware"],
                    "1.1.2.2 Mastitis testing and prevention": ["a. 60 % of dairy farmers are aware of symptoms of mastitis and care to be taken to contain this disease at the individual animal level", "b. 60% dairy farmers have an ability to diagnose early stage of mastitis and the 40% of larger farms (herd size > 10) perform the California Mastitis Test (CMT)", "c. 100% dairy farmers can diagnose mastitis and the of them 80% of large farms (herd size>10) perform the California Mastitis Test (CMT)", "d. 100% large dairy farmers (herd size >10) have access to affordable testing of CMT across all cattle on a day to day basis", "e. California Mastitis Test (CMT) done for 100% cattle for 100% milk produced every day", "f. None of the above", "g. Not aware"],
                    "1.1.2.3 Access to diagnostic services": ["a. 40% of dairy farmers are aware of actions to be taken up immediately post-diagnosis like getting in touch with a Veterinarian and starting appropriate treatment protocol, taking the animal to a diagnostic facility etc.", "b. 60% dairy farmers can access timely and affordable diagnostic facilities and services for further disease diagnosis and commence appropriate treatment protocol", "c. 100% dairy farmers can access timely and affordable doorstep diagnostic facilities and services for further disease diagnosis and commence appropriate treatment protocol", "d. 100% dairy farmers can access timely and affordable doorstep (mobile) diagnostic facilities and services for further disease diagnosis and are timely advised on the appropriate treatment protocol. Government programs and budgets are leveraged to strengthen these services", "e. In-house diagnostic facilities and services available to diagnose further and to commence appropriate treatment protocol immediately for 100% cattle", "f. None of the above", "g. Not aware"]
                },
                "1.1.3 Disease Treatment": {
                    "1.1.3.1 Veterinarian services": ["a. Veterinarian or paravet service on call available to treat 80% of sick animal’s post disease diagnosis", "b. Veterinarian parapet service available at the village level to treat 100% sick animals immediately post disease diagnosis", "c. Affordable and timely veterinarian services available doorstep to treat 100% sick animals immediately post", "d. Affordable and timely dedicated veterinarian services available at the doorstep to treat 100% sick cattle", "e. In-house dedicated veterinarian or team of veterinarians treat 100% of sick animals immediately post disease diagnosis", "f. None of the above", "g. Not aware"],
                    "1.1.3.2 Treatment protocols": ["a. 100% of dairy farmers are aware of standardized investigation forms and treatment protocols at farm level", "b. Standardized investigation forms and written treatment protocols are available at farm level with 80% of dairy farmers", "c. Standardized investigation forms and written treatment protocols ensured for the 80% of sick animals", "d. Standardized investigation forms and digitized treatment protocols are ensured for 100% sick animals", "e. Centralized investigation forms and digitized treatment protocols are ensured for 100% sick animals.", "f. None of the above", "g. Not aware"],
                    "1.1.3.3 Accessibility to Medicines": ["a. 100% of dairy farmers are aware of standardized treatment protocols and medicines to be used to treat the critical and important diseases", "b. 80% dairy farmers have access to affordable high quality medicines and they treat sick animals with the prescribed dosage", "c. 100% of dairy farmers have access to affordable high-quality medicines at their doorstep and they treat 100% sick animals with prescribed dosages", "d. 100% dairy farmers have access to affordable and high-quality medicines at their doorstep and they treat 100% sick animals with prescribed dosages linked to their growth stage", "e. Best in class treatment provided to all sick animals in line with prescribed disease treatment protocols (balanced nutrition, stress management)", "f. None of the above", "g. Not aware"],
                    "1.1.3.4 Isolation of sick animals": ["a. 100% dairy farmers have awareness and knowledge regarding isolation of sick animals to prevent disease and fast-track treatment of sick animals.60% of farmers practice isolation of 50% of sick animals from healthy animals immediately post diagnosis of disease", "b. 80% dairy farmers practice isolation of 50% of sick animals from healthy animals immediately post diagnosis of disease and for the entire duration of treatment", "c. 100% of dairy farmers practice isolation of 100% of sick animals from healthy animals immediately post diagnosis of disease and for the entire duration of treatment", "d. 100% of dairy farmers practice isolation of 100% of sick animals from healthy animals immediately post diagnosis of disease and for the entire duration of treatment", "e. Provision for immediate Isolation of 100% of sick animals in a designated shed that are designed for better care and recovery of animals", "f. None of the above", "g. Not aware"],
                    "1.1.3.5 Knowledge of pharmacological data and requirements": ["a. Paraveterinarian have acceptable knowledge of requirements associated with antimicrobial use, permitable residual levels", "b. Practicing Paraveterinarian have adequate knowledge of requirements associated with antimicrobial use, permitable residual levels", "c. Practicing veterinarians understanding of pharmacological data and requirements associated with antimicrobial use, permitable residual levels", "d. Practicing Paraveterinarian or veterinarians have thorough knowledge of pharmacological data and requirements associated with antimicrobial use, permitable residual levels", "e. Practicing paraveterinarians or Veterinarians have expertise and a deep understanding of pharmacological data and requirements associated with antimicrobial use, permitable residual levels", "f. None of the above", "g. Not aware"],
                    "1.1.3.6 Herbal Remedies": ["a. 80% of dairy farmers have awareness and having knowledge of herbal remedies and are treating at least 5 diseases using herbal remedies", "b. 80% dairy farmers are treating at least 10 diseases using herbal remedies and source raw materials from their farm or a nearby herbal garden or same village", "c. 80% of dairy farmers have the ability to treat at least 15 diseases using herbal remedies and source raw materials in their village or from a nearby herbal garden from same village", "d. 100% farmers have the ability to treat at least 15 diseases using herbal remedies and grow raw materials on their farm or have access to raw materials in the same village", "e. 100% farmers have the ability to treat at least 20 diseases using herbal remedies and grow raw materials on their farm", "f. None of the above", "g. Not aware"],
                    "1.1.3.7 Ethno veterinary medicine": ["a. 100% of dairy farmers are aware and have knowledge of ready to use EVM Medicines", "b. 80% of dairy farmers have access to ready to use EVM Medicines and herbal gardens", "c. 100% of dairy farmers have access to ready to use EVM Medicines and herbal gardens", "d. 100% of dairy farmers have access to ready to use EVM Medicines at an affordable price. Government programs and budgets are leveraged to strengthen these services", "e. 100% of the herd is provided with ready to use EVM medicines, when it is required", "f. None of the above", "g. Not aware"],
                    "1.1.3.8 Antibiotic withdrawal chart": ["a. 100% of dairy farmers are aware and having knowledge of antibiotic withdrawal limits and timelines", "b. 100% of dairy farmers have a chart in their dairy shed depicting all antibiotics and their withdrawal limits", "c. 100% of dairy farmers have a chart and use the same to assess antibiotic withdrawal limit and to decide on pouring milk in the collection centre", "d. 100% of dairy farmers are supplying milk after considering the antibiotic withdrawal limits for 100% of milch cattle all through the year", "e. 100% of Milking and supply of milk is linked to antibiotic withdrawal limits to 100% of cattle", "f. None of the above", "g. Not aware"],
                }
            },
            "1.2 Nutrition": {
                "1.2.1 Cattle Feed and Fodder": {
                    "1.2.1.1 Ration balancing of cattle": ["a. 60% of the dairy farmers are aware and have sufficient knowledge of Ration balancing of cattle based on their needs (growth/maintenance/milk production) and physiological stage", "b. 80% of dairy farmers provide ration balanced feed to all cattle based on their stage and need", "c. 100% dairy farmers provide ration balanced feed to all cattle based on their stage and need", "d. 100% dairy farmers provide ration balanced feed to all cattle based on their stage and need", "e. 100% of herd provided with ration balanced feed based on their physiological stage and linked to the specific need", "f. None of the above", "g. Not aware"],
                    "1.2.1.2 Access to clean drinking water": ["a. 100% of dairy farmers are aware of the need to provide unlimited water to the cattle throughout the day", "b. 60% of dairy farmers are able to provide clean drinking water throughout the day", "c. 80% of dairy farmers have made provision to provide clean drinking water through the day", "d. 100% dairy farmers provide unlimited water to the cattle throughout the day", "e. 100% of the herd provided with clean drinking water ad. libitum that is tested periodically and adheres to prescribed standards", "f. None of the above", "g. Not aware"],
                    "1.2.1.3 Access to quality and palatable feed": ["a. 100% of farmers are aware of the importance of quality and palatable feed and nutrient requirements during extreme climate events and 40% of farmers are providing quality and palatable feed", "b. 60% of dairy farmers are able to timely access quality and palatable feed at village level", "c. 80% dairy farmers can access affordable, high quality and palatable feed on the doorstep", "d. 100% farmers can access affordable, high quality and palatable feed on the doorstep", "e. 100% herd is provided with best in class feed based on their physiological stage (calf, heifer, adult cow) linked to their specific need", "f. None of the above", "g. Not aware"],
                    "1.2.1.4 Knowledge of alternate feeds and their access": ["a. 100% of dairy farmers are aware and have knowledge of the provision of alternative feeds customized to climate extremes", "b. 60% of dairy farmers provide alternative feeds customized to climate extremes", "c. 80% dairy farmers can access affordable alternative feeds customized to climate extremes", "d. 100% dairy farmers can access affordable alternative feeds customized to climate extremes. Government programs and budgets are leveraged to strengthen these services", "e. 100% herd is provided with nutrient enhanced alternative feeds customized to climate extremes", "f. None of the above", "g. Not aware"],
                    "1.2.1.5 Green fodder and carbon sequestration": ["a. 80% of dairy farmers are aware and have knowledge of green fodder like Moringa and its benefits to carbon sequestration", "b. 100% of dairy farmers are aware and have knowledge about carbon sequestration and quality seeds to grow green fodder having benefits of carbon sequestration. 60% of dairy farmers have access to high quality seeds.", "c. 60% of dairy farmers have access to high quality seeds of Moringa. 60% of dairy farmers follow green fodder cultivation practices timely according to recommended agricultural practices", "d. 80% of dairy farmers follow green fodder cultivation practices timely according to recommended agricultural practices. They have Moringa plantations for high quality all year round green fodder", "e. 100% of dairy farms practice best in class green fodder (Moringa, etc) production practices according to recommended agricultural practices", "f. None of the above", "g. Not aware"],
                    "1.2.1.6 Soil management practices": ["a. 80% of dairy farmers are aware and have knowledge of soil sampling and testing", "b. 100% of dairy farmers are aware and have knowledge of soil sampling and testing. 40% of dairy farmers conduct soil sampling and testing for high quality growth rates and healthy fodder.", "c. 60% of dairy farmers conduct soil sampling and testing for high quality growth rates and healthy fodder. 80% of dairy farmers apply fertilizers based on the soil testing information to improve the soil health.", "d. 80% of dairy farmers apply fertilizers based on the soil testing information to improve soil health. They practice soil management practices to reduce soil plugging, erosion and compaction.", "e. 100% of dairy farms apply fertilizers to improve soil health. They practice soil management practices to reduce soil plugging, erosion and compaction.", "f. None of the above", "g. Not aware"]
                },
                "1.2.2 Cattle Feed Management": {
                    "1.2.2.1 Segregation of feed and equipment’s": ["a. 100% of dairy farmers are aware of the importance of segregation of feed and chemical handling equipment", "b. 60% of dairy farmers adopt segregation of feed and chemical handling equipment", "c. 80% dairy farmers segregate feed and chemicals handling equipment.", "d. 100% dairy farmers segregate feed, milking, and chemical handling equipment’s", "e. 100% equipment’s and tools are segregated from feed in the dairy farm and 100% disinfected/ sanitized to avoid any contamination with feed", "f. None of the above", "g. Not aware"],
                    "1.2.2.2 Feed protection and discarding": ["a. 60% of dairy farmers are aware and protect feed to reduce spoilage or contamination. 60% of dairy farmers discard the feed parts found with moulds or other contaminants immediately", "b. 80% of dairy farmers are aware and protect feed to reduce spoilage or contamination. 80% of dairy farmers discard the feed parts found with moulds or other contaminants immediately", "c. 100% dairy farmers are aware to protect feed to reduce spoilage or contamination. 100% of dairy farmers discard the feed parts found with moulds or other contaminants immediately.", "d. 100% dairy farmers have provision to protect feed and ensure feed spoilage or contamination. 100% dairy farmers immediately discard the feed with moulds /contaminants as per prescribed standards", "e. 100% feed properly packed and well protected from physical and chemical damages. 100% moulded and contaminated Feed immediately discarded as per prescribed safe disposal standards.", "f. None of the above", "g. Not aware"],
                    "1.2.2.3 Documentation and record keeping": ["a. 100% of dairy farmers are aware of documentation and record keeping .40% of dairy farmers maintain written records for cattle feed, ration, and nutrition", "b. 60% of dairy farmers maintain written records for cattle feed, ration, and nutrition", "c. 80% of dairy farmers maintain written records for cattle feed, ration, and nutrition", "d. 100% dairy farmers access and maintain digital records for cattle feed, ration, and nutrition", "e. 100% digital records maintained for feed, ration, and nutrition details of entire herd", "f. None of the above", "g. Not aware"],
                    "1.2.2.4 Testing of water and feed": ["a. 100% of people in the village are aware and have knowledge of testing water and feed as per prescribed norms", "b. 60% of dairy farmers test the water regularly as per prescribed norms to avoid health problems", "c. 80% of dairy farmers test the water regularly as per prescribed norms to avoid health problems", "d. 100% of dairy farmers in milk shed test the water regularly as per prescribed norms", "e. 100% Water and feed tested regularly as per prescribed norms", "f. None of the above", "g. Not aware"],
                    "1.2.2.5 Knowledge of and access to quality hay and silage": ["a. 100% of dairy farmers have awareness of best harvesting techniques for fodder cutting and making hay and silage. 40% of dairy farmers adopt fodder cutting and make good quality hay & silage.", "b. 60% of dairy farmers adopt the best harvesting techniques for fodder cutting and make good quality hay & silage.", "c. 80% of dairy farmers adopt the best harvesting techniques for fodder cutting and make good quality hay & silage.", "d. 100% dairy farmers adopt the best harvesting techniques for fodder cutting and make good quality hay & silage.", "e. Best quality hay & silage produced and maintained on the farm all through the year", "f. None of the above", "g. Not aware"],
                    "1.2.2.6 Usage of toxin binder in cattle feed": ["a. 100% dairy farmers have awareness and knowledge of toxin binder in feed to reduce aflatoxins", "b. 100% dairy farmers provide feed with toxin binder as per prescribed standards (0.5%, 50g/animal per day)", "c. 100% of dairy farmers have timely access to affordable feed with toxin binder as per prescribed standards", "d. 100% of dairy farmers have timely doorstep access to feed with toxin binder in prescribed dosages", "e. All feed provided to the cattle in herd have toxin binders in prescribed dosages as recommended globally (10 grams of toxin binder per kg)", "f. None of the above", "g. Not aware"],
                    "1.2.2.7 Availability of compliant cattle feed": ["a. 100% dairy farmers are aware about compliant cattle feed.", "b. 50% dairy farmers have access to compliant cattle feed.", "c. 65% dairy farmers have access to compliant cattle feed.", "d. 75% dairy farmers have access to complaint cattle feed.", "e. 100% dairy farmers have access to compliant cattle feed.", "f. None of the above", "g. Not aware"],
                    "1.2.2.8 Dry fodder protection": ["a. 100% of dairy farmers are aware of dry fodder coverage to avoid mould and infestation", "b. 100% of dairy farmers practice dry fodder coverage and prevent mould and infestation", "c. 100% of dairy farmers have access to materials at an affordable price to cover the dry fodder and protect it from any fungal infestations that cause aflatoxins", "d. 100% of dairy farmers adopt dry fodder coverage using best in class materials, tools and techniques made available as service and product at dairy farmers’ doorstep", "e. Dry cattle feed is well protected in warehouses that are covered and disinfected frequently", "f. None of the above", "g. Not aware"],
                    "1.2.2.9 Liver detoxification": ["a. 100% of dairy farmers are aware and having knowledge about liver detoxification and its impact on reduced aflatoxin in milk", "b. 100% of dairy farmers use liver detoxification medicines like Liv 52 syrup or equivalent medicines daily to prevent effects of aflatoxins on 100% of their cattle", "c. 100% of dairy farmers have access to Liv 52 or equivalent at an affordable price at their doorstep and are using the same on 100% of their milching cattle everyday", "d. 100% of dairy farmers have access to affordable liver detoxification medicines at their doorstep and use the same on 100% of their cattle every day", "e. 100% of cattle in the herd are provided with prescribed dosages of liver detoxification medicines all the year at all the physiological stages of the animal", "f. None of the above", "g. Not aware"],
                    "1.2.2.10 Acidosis": ["a. 100% of dairy farmers are aware and have knowledge regarding acidosis in the animals and resulting increase in aflatoxin contamination", "b. 100% of dairy farmers add buffer to the feed like eating soda @ 40-50 grams per cattle every day to maintain rumen PH", "c. 100% of dairy farmers have access to soda and provide prescribed dosage of eating soda / buffer to the feed every day to milching cattle", "d. 100% of dairy farmers have timely access to affordable buffer/eating soda at the doorstep and they provide prescribed dosage of buffer /eating soda to 100% of their cattle", "e. All cattle in the herd are provided feed with buffer as per the global standards soil every day for all the feeds provided through the day", "f. None of the above", "g. Not aware"],
                    "1.2.2.11 Protection of feed": ["a. 100% of dairy farmers are aware of feed storage and protection guidelines (raised platform and away from the walls) to avoid humidity and resultant mould infestation", "b. 100% of dairy farmers store feed as per the prescribed guidelines (above raised platform, away from walls) and ensure they protect feed from infestation arising from humidity", "c. 100% of dairy farmers have a dedicated storage area for feed that is designed using all prescribed norms that prevent any mould infestation arising due to humid conditions", "d. 100% of dairy farmers have access to finance at an affordable rate of interest and expertise to build feed storage spaces that are in line with prescribed guidelines to avoid an mould infestations", "e. All feed is stored in well ventilated warehouses protected from humidity and other externalities to avoid any future mould infestations", "f. None of the above", "g. Not aware"],
                    "1.2.2.12 Clean feed manger and water": ["a. 100% of dairy farmers are aware of cleaning feeding and water spaces after every feed to avoid any future fungal infestations", "b. 100% of dairy farmers adopt cleaning practices every day to clean all feed and water spaces", "c. 100% of dairy farmers clean all their feeding and water spaces after every feed", "d. 100% of dairy farmers clean entire cattle sheds e specially feeding and water spaces after feed with clean water", "e. All feeding and water spaces in the dairy shed are cleaned, and scrubbed with tested water post every feed with prescribed chemicals", "f. None of the above", "g. Not aware"]
                }
            },
            "1.3 Dairy Farm Hygiene": {
                "1.3.1 Hygiene Management": {
                    "1.3.1.1 Cleaning and disinfection": ["a. 80% of the dairy farmers are aware of cleaning of floor of milkshed, feed storage and water spaces and all milking equipment’s, feeding utensils using approved non-corrosive detergent and disinfectant as per the industry standards", "b. 100% of dairy farmers have access to approved non-corrosive detergent and disinfectant for cleaning of floor, feed and water spaces and all milking equipment’s as per the industry standards", "c. 100% dairy farmers practice milk shed hygiene and have access to affordable approved chemicals and disinfectants", "d. 100% dairy farms floor, feed and water spaces and all milking equipment’s are cleaned using approved non-corrosive detergent and disinfectant as per the industry standards", "e. Dairy farm, equipment’s, pathways, feed spaces and waterways are cleaned at least twice a day as per schedule using industry standard chemicals", "f. None of the above", "g. Not aware"],
                    "1.3.1.2 Assessment of cleanliness": ["a. 80% of the dairy farmers are aware of assessment of cleanliness of farm done regularly as per industry standards", "b. 100% of dairy farmers assess cleanliness of farm regularly as per industry standards", "c. 100% dairy farmers assess and monitor cleanliness of dairy farm and milking equipment’s regularly as per industry standards", "d. 100% of dairy farms and milking equipment’s are assessed and monitored for cleanliness regularly as per industry standards", "e. Dairy farms and milking equipment’s are audited regularly for cleanliness as per industry standards", "f. None of the above", "g. Not aware"],
                    "1.3.1.3 Access to water": ["a. 100% dairy farms are aware of importance of access to adequate water through the day for cleaning", "b. 80% dairy farms have access to adequate water through the day for cleaning", "c. 100% dairy farms have access to adequate water through the day for cleaning", "d. 100% dairy farms have affordable access to adequate water through the day for cleaning", "e. Clean and tested water available through the day for cleaning and maintaining milk shed hygiene", "f. None of the above", "g. Not aware"],
                    "1.3.1.4 Provision for drainage and waste disposal (only for commercial farms)": ["a. 40% of the dairy farmers are aware of practices for drainage and waste water as per the approved standards", "b. 60% of dairy farmers are aware and practice drainage and waste water as per the approved standards", "c. 80% dairy farmers are aware and practice drainage and waste water treatment (recycle, reuse) as per the approved standards", "d. 100% dairy farms have well planned and managed drainage and waste water as per the approved standards", "e. Dairy farms are designed best in class to manage and drainage and waste water as per approved standards", "f. None of the above", "g. Not aware"],
                    "1.3.1.5 Farmer /Staff personal hygiene": ["a. 100% of farmers/ staff have full awareness of personal hygiene practices.50% of farmers practice personal hygiene practices on the dairy farms (handwashing, clean clothing, masking, etc.)", "b. 60% dairy farmers follow personal hygiene practices as per industry norms (handwashing, clean clothing, masking, etc.)", "c. 80% dairy farmers follow personal hygiene practices as per industry norms (handwashing, clean clothing, masking, etc.)", "d. 100% dairy farmers /staff practice Personal hygiene on the dairy farms as per industry norms (handwashing, clean clothing, masking, etc.)", "e. 100% staff practice personal hygiene as per industry norms (handwashing, clean clothing, masking, PPE etc.)", "f. None of the above", "g. Not aware"],
                    "1.3.1.6. Animal Grooming": ["a. 80% of dairy farmers are aware of animal grooming practices .40% of the farmers adopt animal grooming practices and segregation of all animal personal hygiene material materials and separate disposal", "b. 100% of dairy farmers are aware of animal grooming practices. 60% dairy farmers practice animal grooming practices regularly and all animal personal hygiene materials are segregated and disposed separately", "c. 80% dairy farmers practice animal grooming practices regularly", "d. 100% of animals are groomed regularly and all animal personal hygiene material materials are segregated and disposed separately", "e. 100% herd is groomed regularly and their personal hygiene material materials are segregated and disposed of separately as per prescribed standards", "f. None of the above", "g. Not aware"],
                    "1.3.1.7 Hoof hygiene": ["a. 100% of dairy farmers are aware and have knowledge of hoof hygiene", "b. 80% dairy farms adopt and ensure animal hoof hygiene measures like foot baths, hoof mats and foaming systems", "c. 100% dairy farms adopt and have access to animal hoof hygiene measures like foot baths, hoof mats and foaming systems", "d. 100% dairy farms adopt and have affordable access to and ensure animal hoof hygiene measures like foot baths, hoof mats and foaming systems", "e. Hoof hygiene measures are best ensured in 100% cattle in the herd", "f. None of the above", "g. Not aware"],
                    "1.3.1.8 Udder hygiene": ["a. 100% of dairy farmers are aware of udder hygiene practices. 50% Majority of the farmers practice udder hygiene practices as per Indian prescribed norms before milking", "b. 70% dairy farmers follow udder hygiene practices as per Indian prescribed norms before milking 100% of their milching cattle", "c. 80% dairy farmers follow udder hygiene practices as per Indian prescribed norms before milking for 100% of their milching cattle", "d. 100% dairy farmers adopt and practice udder hygiene as per Indian prescribed norms followed before milking for 100% of their milching cattle", "e. Udder hygiene practices adopted as per Indian prescribed norms across 100% of cattle in the herd", "f. None of the above", "g. Not aware"],
                    "1.3.1.9 Manure Management": ["a. 80% of dairy farmers are aware and have knowledge of manure management practices (such as composting system, crushing, screening, mixing, granulating, drying and cooling and packaging)", "b. 100% of dairy farmers are aware and have knowledge of manure management practices. 80% of dairy farmers have access to manure management equipment", "c. 100% of dairy farmers have access to manure management equipment and infrastructure. 80% dairy farmers adopt manure management practices", "d. 100% of dairy farmers adopt manure management practices", "e. 100% of dairy farms practice best in class manure management practices.", "f. None of the above", "g. Not aware"],
                    "1.3.1.10 Biogas Installation": ["a. 80% of dairy farmers are aware and have knowledge of biogas and their benefits", "b. 100% of dairy farmers are aware and have knowledge of biogas. 60% of dairy farmers have access to biogas loans and subsidies", "c. 80 % of dairy farmers are able to access loans/ subsidies to install biogas plants and 60% of eligible farmers have biogas unit on the farm", "d. 100% of dairy farmers have access to biogas loans and subsidies and 80% of eligible farmers have biogas unit on farm. Solid waste is used as manure in 80% of farms", "e. 100% of dairy farmers have access to biogas loans and subsidies and 100% of eligible farmers have biogas unit on farm. Solid waste is used as manure in 100% of farms", "f. None of the above", "g. Not aware"],
                    "1.3.1.11 Water Conservation Management": ["a. 80% of dairy farmers are aware of water conservation practices such as water harvesting, reusing and recycling water", "b. 100% of dairy farmers are aware of water conservation practices such as water harvesting, reusing and recycling water. 40% of dairy farmers practice reusing and recycling water and water storage", "c. 60% of dairy farmers practice rainwater harvesting, reusing and recycling water and water storage.", "d. 80% of dairy farmers practice rainwater harvesting, reusing and recycling water and water storage.", "e. 100% of dairy farms practice best in class practices to conserve water and use sustainable dairy and agricultural practices on the farms.", "f. None of the above", "g. Not aware"]
                }
            },
            "1.4 Stress in Cattle": {
                "1.4.1 Stress management": {
                    "1.4.1.1 Farm shed Design": ["a. 100% of dairy farmer have awareness and knowledge of farm shed design that reduced stress of cattle. 60% of dairy farmers have access to loans/ subsidies to construct some improved cattle shed as per prescribed norms", "b. 80% dairy farmers have access to loans/ subsidies to construct improved cattle shed as per prescribed norms", "c. 80% of cattle sheds and their roof are designed to suit to the local climatic conditions", "d. 100% of cattle sheds and their roof are designed to suit to the local climatic conditions", "e. Dairy farms have customized cattle shed for calf, heifers, bulls and milching cows", "f. None of the above", "g. Not aware"],
                    "1.4.1.2 Protection from climate extremes": ["a. 100% of dairy farmers are awareness of the protection of cattle shed from climate extremes. 60% of cattle sheds are well- ventilated, protected from extremes of weather, have optimal space for animals and clean drinking water", "b. 80% Majority of cattle shed are fully ventilated, dampness free with complete protection from extremes of weather events (wind, solar radiation etc.) and loud noises", "c. 100% cattle shed are fully ventilated, dampness free with complete protection from extremes of weather events (wind, solar radiation etc.), loud noises and protected by boundary / fence", "d. 100% cattle shed are fully ventilated (with coolers and exhausts), dampness free with complete protection from extremes of weather events (wind, solar radiation etc.) and loud noises", "e. Dairy farms have provision for water sprays, exhausts and coolers to manage heat and other climate induced stress", "f. None of the above", "g. Not aware"],
                    "1.4.1.3 Safe surfaces": ["a. 100% of dairy farmers are aware and have sufficient knowledge on factors that affect cattle milk productivity like stress induced due to improper ventilation in cattle shed, no protection or shade, inconvenient floor surface and inadequate space for resting, movement and feeding", "b. 80% of cattle shed have skid free, soil/dirt free, dry and comfortable flooring to move and rest", "c. 100% of cattle shed have skid free, soil/dirt free, dry and comfortable flooring to move and rest", "d. 80% cattle sheds have concrete floors with proper provision for drainage and waste handling. Floors are cleaned regularly and comfortable to rest", "e. 100% cattle sheds have concrete floors with proper provision for drainage and waste handling. Floors are cleaned regularly and comfortable to rest", "f. None of the above", "g. Not aware"],
                    "1.4.1.4 Comfort of cattle": ["a. 100% of dairy farmers are aware and have sufficient knowledge on factors that affect cattle milk productivity due to lack of space for free movement", "b. 100% of dairy farmers have awareness of loose housing", "c. 60% of dairy farmers adopt well protected loose housing system with well-defined boundary", "d. 80% of dairy farmers adopt well protected loose housing system with well-defined boundary", "e. 100% dairy farms have well protected loose housing system with a well-defined boundary", "f. None of the above", "g. Not aware"],
                    "1.4.1.5 Space in shed": ["a. 100% of dairy farmers are aware and have sufficient knowledge on factors that affect cattle milk productivity due to insufficient space to move and rest.", "b. 100% dairy farmers are aware and have knowledge of importance of space in shed for cattle to move and rest", "c. 80% cattle sheds have optimal space for animals to move and clean drinking water", "d. 100% cattle sheds have optimal space for animals to move and clean drinking water", "e. All cattle sheds in dairy farms are designed to provide ample space as per industry norms and safe surfaces to minimize injuries and discomfort", "f. None of the above", "g. Not aware"],
                    "1.4.1.6 Waste handling and disposal": ["a. 100% of dairy farmers are aware and have knowledge of waste handling and disposal", "b. 80% dairy farms have provision for ETP plant to treat wastewater", "c. 100% Dairy farms have provision for ETP plant to treat wastewater", "d. 80% dairy farms have provision of biogas for solid waste management and reduce methane emissions", "e. 100% dairy farms have provision of biogas for solid waste management and reduce methane emissions", "f. None of the above", "g. Not aware"]
                }
            },
            "1.5 Cattle Breeding": {
                "1.5.1 Breed management": {
                    "1.5.1.1 Cattle breed and identification": ["a. 80% of dairy farmers are aware about different cattle breeds, their productivity and their identification.", "b. 100% dairy farmers are aware about different cattle breeds and their breed identification.", "c. 60% dairy farmers are introducing new breeds in their herd", "d. 80% dairy farmers introducing new breeds into their herd", "e. Dairy farms adopt strategic plans to introduce new breeds and cattle in the herd", "f. None of the above", "g. Not aware"],
                    "1.5.1.2 Reproductive management": {
                        "1.5.1.2.1 Disease prevention": ["a. 40% of dairy farmers are aware of diseases or difficulties faced during previous calving. They follow programs of disease tests/prevention.", "b. 60% of dairy farmers are aware of diseases or difficulties faced during previous calving. They follow programs of disease tests/prevention.", "c. 80% of dairy farmers are aware of diseases or difficulties faced during previous calving. They follow programs of disease tests/prevention.", "d. 100% of dairy farmers are aware of diseases or difficulties faced during previous calving. They follow programs of disease tests/prevention.", "e. 100% dairy farms have access to and follow programs of disease tests/ prevention relevant to reproductive management", "f. None of the above", "g. Not aware"],
                        "1.5.1.2.2 Reproductive Management practices": ["a. 40% of dairy farmers have awareness and knowledge of reproductive management practices", "b. 60% of dairy farmers have awareness and knowledge of reproductive management practices", "c. 80% of dairy farmers have awareness and knowledge of reproductive management practices (such as heat management, nutrition management and stress free environment)", "d. 100% of dairy farmers have access to reproductive management practices (such as heat management, parturition management sire monitoring, nutrition management and stress free environment)", "e. 100% of Dairy farms practice best in class reproductive management practices", "f. None of the above", "g. Not aware"]
                    },
                    "1.5.1.3 Documentation and maintenance of records": {
                        "1.5.1.3.1 Life Cycle Records": ["a. 100% of dairy farmers have awareness of maintenance of lifecycle records.60% of farmers maintain written records of cattle life cycle (age, lactations, calf mortality etc.).", "b. 80% dairy farmers maintain written records of cattle life cycle (age, lactations, calf mortality etc.)", "c. 100% dairy farmers maintain written records of cattle life cycle (age, lactations, calf mortality etc.)", "d. 100% dairy farmers maintain digital records of cattle life cycle (age, lactations, calf mortality etc.)", "e. Dairy farms have digital records of 100% herd lifecycle (age, lactations, calf mortality etc.) are maintained", "f. None of the above", "g. Not aware"],
                        "1.5.1.3.2 Breeding Records": ["a. 100% of dairy farmers are aware of maintenance of breeding records. 60% of farmers keep accurate written breeding records of dates of heat, service and parturition.", "b. 80% of farmers keep accurate written breeding records of dates of heat, service and parturition.", "c. 100% of dairy farmers keep accurate written breeding records of dates of heat, service and parturition.", "d. 80% of dairy farmers keep accurate digital breeding records of dates of heat, service and parturition. They use these records in predicting the dates of heat and observe the females carefully for heat.", "e. 100% dairy farmers keep accurate digital breeding records of dates of heat, service and parturition. They use these records in predicting the dates of heat and observe the females carefully for heat.", "f. None of the above", "g. Not aware"]
                    },
                    "1.5.1.4 Infertility": ["a. 60% of dairy farmers are aware of infertility treatments and are aware of measures to improve fertility of cattle", "b. 80% of dairy farmers are aware of infertility treatments and 50% farmers are adopting of measures to improve fertility of cattle", "c. 80% of dairy farmers are aware of infertility treatments and 70% farmers are adopting of measures to improve fertility of cattle", "d. 100% dairy farmers are aware of infertility treatments and 80 % of dairy farmers are adopting measures to improve fertility of cattle. Government programs and budgets are leveraged to strengthen these services", "e. 100% dairy farmers are aware of infertility treatments and 100 % of dairy farmers are adopting measures to improve fertility of cattle.", "f. None of the above", "g. Not aware"],
                    "1.5.1.5 AI services": ["a. 100% of dairy farmers are aware of AI in cattle.40% of farmers are aware of resources for credible semen sources and high quality AI services.", "b. 60% of dairy farmers have access to resources for credible semen source and high quality AI services.", "c. 80% dairy farmers have timely access to resources for credible semen source and high quality AI services.", "d. 100% dairy farmers have timely access to resources for credible semen source and high quality AI services.", "e. Dairy farm has in-house semen bank and full fledged AI expertise", "f. None of the above", "g. Not aware"],
                    "1.5.1.6 Pregnancy Management": ["a. 100% of dairy farmers are aware that they have to reach out to Para veterinarian or veterinarians for pregnancy management.50% of dairy farmers manage pregnancy with inputs from at least a paravet through on-call support.", "b. 70% of dairy farmers manage pregnancy with inputs from a qualified veterinarian/ paravet through on-call support.", "c. 90% of dairy farmers manage pregnancy with inputs from a qualified veterinarian/ paravet. The veterinarian service is also used to examine cows periodically.", "d. 100% dairy farmers manage pregnancy with inputs from a qualified veterinarian.", "e. Dairy farm has in-house experts team of veterinarians to timely treat infertility, pregnancy related complications etc.", "f. None of the above", "g. Not aware"]
                }
            }
        },
        "2. Dairy Extension Services": {
            "2.1 Services": {
                "2.1.1 Team structure and size": ["a. 100% dedicated field extension team", "b. 100% Dedicated and qualified field extension team for building capability of dairy farmers", "c. 100% Dedicated, experienced and qualified dairy and veterinary extension teams available for capability building of dairy farmers", "d. 100% Dedicated, qualified, and experienced dairy extension teams (Diploma/Degree in agriculture, livestock, dairy, veterinary) to build the capability of dairy farmers", "e. 100% Dedicated, qualified, and experienced dairy extension teams (Diploma/Degree in agriculture, livestock, dairy, veterinary / Minimum 3 years' experience) to build the capability of dairy farmers", "f. None of the above", "g. Not aware"],
                "2.1.2 Functional dairy extension department": ["a. 100% Dedicated and qualified Field extension team", "b. 100% Dedicated Field extension team is single point of contact for 100% extension and procurement related communication with farmers", "c. 100% Dedicated department available for planning, implementation, and monitoring of dairy extension activities", "d. 100% Dedicated IT-enabled dairy extension department that works closely with the procurement department on the field to ensure both quality dairy extension services and quality milk procurement", "e. 100% Dedicated departments (procurement, veterinary) to offer extension services", "f. None of the above", "g. Not aware"],
                "2.1.3 Monitoring of extension services": ["a. Procurement department is accountable for 100% dairy extension activities", "b. Regular monitoring of extension services, training materials, and training delivery is ensured", "c. Regular monitoring of extension services, training materials, and training delivery is ensured using digital records and a monitoring system", "d. Dairy Extension policy framework is in place", "e. Five Year Dairy Extension Policy Framework / Vision Document is in place", "f. None of the above", "g. Not aware"],
                "2.1.4 Convergence of funds from the Government": ["a. 60% of funds for dairy extension are from 100% dairy extension team is aware of government schemes and subsidies available for dairy extension services", "b. convergence with government services for knowledge and skill building on dairy extension", "c. 80% of funds for dairy extension are from convergence with government schemes for dairy extension services", "d. 100% of funds for dairy extension are from convergence with government schemes and subsidies for dairy extension services", "e. All extension activities are done in partnership with government schemes and funds.", "f. None of the above", "g. Not aware"],
                "2.1.5 Budget allocation for extension activities": ["a. 100% Dedicated Budget available for hiring of dedicated dairy extension team", "b. 100% Dedicated Budget available for dedicated dairy extension activities (workshop, travel, awareness camps, etc.)", "c. 100% Dedicated budgets for exposure visits, demonstration plots, training, and awareness camps.", "d. 100% Dedicated budgets allocated for all dairy extension activities including but not limited to a trainer of trainer program, creation of communication material, development of training modules, dedicated training center, etc.", "e. 100% Dedicated budgets allocated to all dairy extension activities including training and capability of the dairy extension teams", "f. None of the above", "g. Not aware"],
                "2.1.6 Communication with dairy farmers": ["a. Periodic communication with dairy farmers, as and when needed", "b. Regular communication with dairy farmers", "c. 100% Dedicated Communication channels which can also be used for 2-way communication (between the Beneficiary and Extension Department)", "d. 100% Dedicated Communication channels (for example, radio and television broadcasts and face-to-face communication) which can also be used for 2-way communication (between the beneficiary and Extension Department", "e. 100% Dedicated Communication channels (for example, Farmer camps, mobile APPs, Website, Call Centre, Toll-Free, Social Media Pages) which can also be used for 2-way communication (between the beneficiary and Extension Department", "f. None of the above", "g. Not aware"]
            },
            "2.2 Training": {
                "2.2.1 Capability building of team and trainer of trainers": ["a. 100% of the field extension team are aware of training sessions and these sessions are conducted at least once a year", "b. 80% field extension team have access to trainings for trainer programs conducted regularly to build a cadre of trained extension resources", "c. 100% field extension team have access to trainings for trainer programs conducted regularly to build a cadre of trained extension resources", "d. 100% field extension team have timely access to training for trainer programs customized to the region based on the prevalent situations", "e. All Dairy farms have in-house trained resources who have expertise to disseminate best practices to teams in a timely manner", "f. None of the above", "g. Not aware"],
                "2.2.2 Training materials": ["a. 100% of the training modules/topics are decided based on standard dairy extension topics (for example, Hygiene, Animal care, EVMs, etc.). These modules are not need-based or on current issues/problem areas", "b. 80% field extension team have access to holistic training materials", "c. 100% field extension team have access to holistic training materials covering all aspects of animal care, milking and pouring", "d. 100% field extension team have access to holistic training materials covering all aspects of animal care, milking and pouring, and marketing along with reference to the latest developments / new practices in dairy from leading research institutes", "e. 100% of Dairy farms have Holistic training materials covering all aspects of animal care, milking and pouring, and marketing along with reference to the latest developments / new practices in dairy from leading research institutes", "f. None of the above", "g. Not aware"],
                "2.2.3 Exposure visits": ["a. 100% of the field extension team are aware of and have access to classroom training (traditional methods)", "b. 40% field extension team have access to gaining real-time experiences through exposure visits to demonstration farms and progressive farmers that practice good dairy practices", "c. 60% field extension team have access to gaining real-time experiences through exposure visits to demonstration farms and progressive farmers that practice good dairy practices", "d. 80% field extension team have access to gaining real-time experiences through exposure visits to demonstration farms and progressive farmers that practice good dairy practices", "e. 100% dairy extension teams access to gaining real-time experiences through exposure visits to demonstration farms and progressive farmers that practice good dairy practices is ensured.", "f. None of the above", "g. Not aware"],
                "2.2.4 Upskilling": ["a. 60% field extension team have access to versatile trainings and training modules that are available both offline and online in their regional/ local language", "b. 80% field extension team have access to versatile trainings and training modules that are available both offline and online in their regional/ local language", "c. 100% field extension team have timely access to affordable and versatile training and training modules that are available both offline and online in their regional/ local language", "d. Dairy farms have versatile training and training modules that are available both offline and online in their regional/ local language", "e. Upskilling of 100% dairy extension teams with timely access to the latest scientific advancements in animal healthcare, dairy farming, milk procurement, and milk marketing is ensured", "f. None of the above", "g. Not aware"],
                "2.2.5 Field Situation": ["a. 20% field extension team have access to streamlined follow ups to get first handed information on field situations", "b. 40% field extension team have access to streamlined follow ups to get first handed information on field situations", "c. 60% field extension team have access to streamlined follow ups to get first handed information on field situations", "d. 80% field extension team have access to streamlined follow ups to get first handed information on field situations", "e. 100% field extension team have timely access to streamlined follow ups to get first-handed information on field situations", "f. None of the above", "g. Not aware"]
            },
            "2.3 Research": {
                "2.3.1 Dairy farm level documentation and record-keeping": ["a. 100% of dairy extension team is aware of demonstration pilots.", "b. 100% of dairy demonstration farm units are monitored on regular basis", "c. 100% dairy demonstration farm units are monitored regularly and farm situation data written records are maintained", "d. 100% of dairy demonstration farm units is monitored on day to day basis and farm situation date is digitally maintained", "e. 100% of dairy demonstration farm units are linked to central database through ERP and all data is reviewed on real time basis", "f. None of the above", "g. Not aware"],
                "2.3.2 Dairy farm analysis and management": ["a. 100% of dairy extension field team are aware and have sufficient knowledge to observe dairy demonstration units and collect farm situation data.", "b. 100% dairy extension field teams are well equipped to understand how farm analysis results can be incorporated in the farm day to day decision making and farm management", "c. 80% dairy farmers are aware and have sufficient knowledge of farm management. 80% dairy farmers can identify and explain farm management functions and management areas.", "d. 100% dairy farmers are aware and have sufficient knowledge of farm management. 100% dairy farmers can identify and explain farm management functions and management areas.", "e. 100% Dairy Farms ensure farm management practices are carried out efficiently. Dairy Farms ensure farm management functions are carried out smoothly and management areas are checked periodically and improved upon regularly", "f. None of the above", "g. Not aware"],
                "2.3.3 Farm assessment and improvement": ["a. 80% field supervisors have sufficient knowledge and understanding of how farm analysis results can be incorporated into the farm day to day decision making and farm management", "b. 80% dairy farmers are skilled on farm assessment and preparing farm improvement plans", "c. 100% dairy farmers are skilled on-farm assessment and preparing farm improvement plans", "d. 100% dairy farmers are skilled in on-farm assessment and preparing farm improvement plans. Government programs and budgets are leveraged to strengthen these skills and improve farm situations", "e. Dairy Farms are assessed regularly and farm improvement plans are carried out periodically", "f. None of the above", "g. Not aware"]
            }
        },
        "3. Procurement and Milk Quality": {
            "3.1 Milk Procurement": {
                "3.1.1 Model of procurement of milk": ["a. Milk procured in two shifts directly from dairy farmers or aggregators at village level milk collection centers (30-50 dairy farmers,200-300 LPD milk procured, average 6 liters per day per dairy farmer)", "b. Milk procured in two shifts directly from dairy farmers at village level milk collection centers (50-100 dairy farmers, 500-800 LPD milk procured, average 8-10 liters per day per dairy farmer)", "c. Milk procured in two shifts directly from dairy farmers through company owned or managed milk collection centers at village level (100-150 dairy farmers, 1000 LPD milk procured, average 8-10 liters per day per dairy farmer)", "d. 100% milk is directly procured from company owned herd size> 1000) or large farmer managed dairy farms (herd size > 300) with yield per cattle greater than 20 LPD", "e. 100% the milk is directly procured from well managed dairy farms (herd size >1000) with yield per animal more than 40 LPD", "f. None of the above", "g. Not aware"],
                "3.1.2 Milk Pricing": ["a. Milk pricing is based fat and SNF (double axis) (Total solids minimum 11.5% (Fat: SNF 3.2/8.3) as per FSSAI) and determined manually", "b. Milk pricing is based fat and SNF (double axis) (Average solids minimum 12% (Fat: SNF 3.5/8.5 as per FSSAI))) and determined digitally", "c. Milk pricing is based on fat, SNF and determined digitally which is linked automatic rate management system", "d. Milk pricing is based on fat, SNF and proteins linked to automatic rate management system", "e. Milk pricing is based on fat, SNF and proteins and additional incentives linked to superior quality (no residues of aflatoxins, antibiotics)", "f. None of the above", "g. Not aware"],
                "3.1.3 Milk handling through stainless steel": ["a. 100% of dairy farmers are aware of use of stainless steel containers for milking, storage and pouring.60% of dairy farmers use stainless steel containers for milking and pouring", "b. 80% of dairy farmers use stainless steel containers for milking 100% of VLCs use stainless steel cans for milk handling", "c. 100% of dairy farmers use stainless steel containers for milking and pouring and 100% milk handling equipment at BMCs, VLCs are made of stainless steel", "d. 100% Milk from VLCs transported to BMCs through closed stainless steel GPS enabled tankers", "e. 100% of milk is handled in stainless steel containers from farm to dock with 100% norms adopted for their maintenance", "f. None of the above", "g. Not aware"],
                "3.1.4 Milk logistics": ["a. 100% of Milk from VLCs to be transported to BMCs through closed roof vehicles", "b. 100% of Bulk Milk Chillers / MCC are set up within 4 hours and milk logistics is optimized through route mapping and time management", "c. 100% BMCs/ MCCs are set up within 4 hours and milk logistics is optimized through GPS monitored route mapping and time management", "d. 100% of Milk transportation is carried in company owned vehicles, maintain complete hygiene and follow best practices", "e. 100% Milk transportation is carried in company owned GPS enabled vehicles adhering to global milk standards", "f. None of the above", "g. Not aware"],
                "3.1.5 Data Processing": ["a. 80% of village collection centers have DPUs", "b. 100% village collection centers have DPUs", "c. 100% village collection centers have dairy farmer records linked to company ERP", "d. 100% of village collection centers and BMC have AMCS with centralized repository of individual records linked to ERP and the same is used to make payments to farmers directly to their bank accounts", "e. 100% of DPUS VLCs and BMCs are linked to company and data is used to trace early signals to evade milk contamination", "f. None of the above", "g. Not aware"],
                "3.1.6 Farmer Payments": ["a. Direct payment to dairy farmers on monthly basis", "b. Direct payment to dairy farmers on fortnightly basis", "c. Direct bank payment to dairy farmers through 10-day payment cycle", "d. Direct bank payment to dairy farmers through weekly payment cycle", "e. Direct payment to dairy farmers through a daily payment cycle", "f. None of the above", "g. Not aware"]
            },
            "3.2 Milk Quality": {
                "3.2.1 Adherence to standard operating procedures (Pick multiple options)": [
                    "BMC/MCC equipped to test Fat, SNF, Adulteration (salt, sugar, urea) MBRT, Protein (for MCC), Acidity",
                    "BMC / MCC have experienced people for OT (Olfactory test)",
                    "BMC/MCC have equipment's to calibrate and reset the weighing scales",
                    "BMC/CC display SOPs and Do's and Don'ts",
                    "BMC/CC follow all SOPs at all times",
                    "All SOPs are in line with quality standards (FSSAI) and norms (Shop Act, Fire Safety compliant) as prescribed by the Government from time to time",
                    "MCC do qualitative test (microbial, antibiotics etc.) as per standard lab protocol on testing milk samples for quality and safety",
                    "MCC are equipped to test (physical, chemical, microbial, antibiotics etc.) as per standard lab protocol on testing milk samples for quality and safety",
                    "BMC/CC have chambers to segregate milk",
                    "Dairy farm adheres to global dairy quality standards like HACCP",
                    "None of the above",
                    "Not aware"
                ],
                "3.2.2 Quality of milk defined through Methylene Blue Dye Reduction Test": ["a. MBRT < 1 hour", "b. MBRT 1-2 hours", "c. MBRT 2-3 hours", "d. MBRT 3-4 hours", "e. MBRT > 5 hours", "f. None of the above", "g. Not aware"],
                "3.2.3 Aflatoxin": ["a. Volume of milk rejected due to aflatoxin is 20%", "b. Volume of milk rejected due to aflatoxin is 15-20%", "c. Volume of milk rejected due to aflatoxin is 10-15%", "d. Volume of milk rejected due to aflatoxin is 5-10%", "e. Volume of milk rejected due to aflatoxin is 0-5%", "f. None of the above", "g. Not aware"],
                "3.2.4 Antibiotic- B lactam": ["a. Volume of milk rejected due to B lactam antibiotic contamination is 20%", "b. Volume of milk rejected due to B lactam antibiotic contamination is 15-20%", "c. Volume of milk rejected due to B lactam antibiotic contamination is 10-15%", "d. Volume of milk rejected due to B lactam antibiotic contamination is 5-10%", "e. Volume of milk rejected due to B lactam antibiotic contamination is 0-5%", "f. None of the above", "g. Not aware"],
                "3.2.5 Antibiotic- Sulphanomide": ["a. Volume of milk rejected due to sulphanomide antibiotic contamination is 20%", "b. Volume of milk rejected due to sulphanomide antibiotic contamination is 15-20%", "c. Volume of milk rejected due to sulphanomide antibiotic contamination is 10-15%", "d. Volume of milk rejected due to sulphanomide antibiotic contamination is 5-10%", "e. Volume of milk rejected due to sulphanomide antibiotic contamination is 0-5%", "f. None of the above", "g. Not aware"],
                "3.2.6 Antibiotic- Chloramphenicol": ["a. Volume of milk rejected due to chloramphenicol antibiotic contamination is 20%", "b. Volume of milk rejected due to chloramphenicol antibiotic contamination is 15-20%", "c. Volume of milk rejected due to chloramphenicol antibiotic contamination is 10-15%", "d. Volume of milk rejected due to chloramphenicol antibiotic contamination is 5-10%", "e. Volume of milk rejected due to chloramphenicol antibiotic contamination is 0-5%", "f. None of the above", "g. Not aware"],
                "3.2.7 Antibiotic- Tetracycline": ["a. Volume of milk rejected due to Tetracycline antibiotic contamination is 20%", "b. Volume of milk rejected due to Tetracycline antibiotic contamination is 15-20%", "c. Volume of milk rejected due to Tetracycline antibiotic contamination is 10-15%", "d. Volume of milk rejected due to Tetracycline antibiotic contamination is 5-10%", "e. Volume of milk rejected due to Tetracycline antibiotic contamination is 0-5%", "f. None of the above", "g. Not aware"]
            }
        },
        "4. Women Empowerment -Participation and Entrepreneurship": {
            "4.1 Community gender sensitization": ["a. 40% of the community is aware of the role of women in dairy farming", "b. 50% community is sensitized to gender roles and the role of women in dairy farming", "c. 60% community is sensitized to gender roles and the role of women in dairy farming", "d. 80% community is sensitized to gender roles and the role of women in dairy farming", "e. 100% of the community in the dairy milk shed is sensitized to gender roles and the role of women in dairy farming", "f. None of the above", "g. Not aware"],
            "4.2 Know-how of dairy economics": ["a. 50% of the women dairy farmers are aware of dairy practices, dairy economics and are financially literate", "b. 70% women dairy farmers’ knowledge and built self-efficacy around dairy best practices, understand dairy economics and are financially included", "c. 80% women dairy farmers with sound knowledge of dairy economics and are connected to financial institutions", "d. 100% women dairy farmers have sound knowledge of dairy economics and are connected to financial institutions", "e. 100% women dairy farmers are empowered to use digitally solutions to improve financial inclusion", "f. None of the above", "g. Not aware"],
            "4.3 Status of women leadership": ["a. 30% Women have access to periodic awareness camps, training programs, leadership development etc. focused on developing women led enterprises", "b. 50% Women have access to periodic awareness camps, training programs, leadership development etc. focused on developing women led enterprises", "c. 100% women farmer led dairy value chain and businesses encouraged (Women lead milk producer company).", "d. Dedicated dairy entrepreneurship program promoted with a focus on women entrepreneurs", "e. 100% of dairy extension teams are run, managed and supervised by all women team", "f. None of the above", "g. Not aware"],
            "4.4 Capability building of women": ["a. 30% women access workshops, seminars and training programmes focused on skill development and dairy entrepreneurship", "b. 50% of women dairy farmers access workshops, seminars and training programmes focused on skill development and dairy entrepreneurship", "c. 80% women dairy farmers access workshops, seminars and training programmes focused on skill development and dairy entrepreneurship. Special incentives provided to women dairy farmers in order to increase participation in dairy training programs.", "d. 100% women dairy farmers access workshops, seminars and training programmes focused on skill development and dairy entrepreneurship. Special incentives provided to women dairy farmers in order to increase participation in dairy training programs", "e. 100% women farmer led dairy value chain and businesses encouraged (Women led milk producer company)", "f. None of the above", "g. Not aware"],
            "4.5 Status of promotion of Innovation": ["a. 40% woman are encouraged to innovate better ways of doing dairy and farm businesses and are regularly exposed to innovations globally", "b. 60% women are encouraged to innovate better ways of doing dairy and farm businesses and are regularly exposed to innovations globally", "c. 80% women are encouraged to innovate better ways of doing dairy and farm businesses and are regularly exposed to innovations globally", "d. 100% women are encouraged to innovate better ways of doing dairy and farm businesses and are regularly exposed to innovations globally. Government programs and schemes are leveraged for wider access", "e. Dairy farms use best in class trainings and programs for encouraging women to innovate better ways of doing dairy and farm businesses and regularly expose them to innovations globally.", "f. None of the above", "g. Not aware"],
            "4.6 Community Groups": ["a. 30% of milk suppliers are women SHG / JLG groups", "b. 50% of milk suppliers are women SHG / JLG groups", "c. 70% Women dairy farmers part of SHGs/JLG groups are encouraged to supply milk and are facilitated with credit linkages to improve their dairy farm", "d. 90% Women dairy farmers part of SHGs/JLG groups are encouraged to supply milk and are facilitated with credit linkages to improve their dairy farm", "e. 100% Women dairy farmers part of SHGs/JLG groups are encouraged to supply milk and are facilitated with credit linkages to improve their dairy farm", "f. None of the above", "g. Not aware"],
            "4.7 Farm Practices": ["a. 80% Women actively participate in dairy farming practices on the farm", "b. 100% of Women actively participate in all dairy farming practices on the farm and 50% involved in marketing of the milk", "c. 100% of Women actively participate in all dairy farming practices on the farm and 100% involved in marketing of the milk", "d. 80% women dairy farmers actively participate in all labour, business and financial aspects of dairy farming", "e. 100% women dairy farmers actively participate in all labour, business and financial aspects of dairy farming", "f. None of the above", "g. Not aware"]
        },
        "5. Strengthening Traceability – Across all Levels": {
            "5.1 Documentation and record keeping till animal level": ["a. 100% Dairy farmer details, their herd size and basic profile of their cattle maintained by dairy partner (at least hard copy)", "b. 100% Dairy farmer details, their herd size and basic profile of their cattle maintained digitally", "c. Dairy partner has digital records of entire dairy value chain (cattle, farmers, agents, dairy company)", "d. Dairy partner's value chain is digitized (cattle, farmers, agents, dairy company) and data stored in cloud and is accessible on a real time basis.", "e. 100% cattle in the herd are tagged and their complete records (on nutrition, breeding, treatments etc.) linked to digitized records", "f. None of the above", "g. Not aware"],
            "5.2 Best Practices and exposure visits": ["a. Dairy partner teams have 100% knowledge on early warning system protocols", "b. Dairy partner teams have 100% knowledge on early warning system protocols and their capability is built via knowledge building and training material", "c. Dairy partner teams have 100% knowledge on early warning system protocols and their capability is built periodically through trainings, exposure visits, workshops, best practices, innovations etc.", "d. Dairy partner teams are provided with timely advanced training about best practices and innovation in early warning system protocols", "e. 100% milk produced in the dairy farm is traceable till the animal level", "f. None of the above", "g. Not aware"],
            "5.3 Early warning system protocols": ["a. 100% dairy partner team are aware and have sufficient knowledge around early warning system protocols", "b. 100% of Early warnings communicated within 12 hours to farmers, agents and dairy extension team at least verbally to prevent possible contamination of milk (through feed or diseases", "c. All early warnings communicated in real time basis, using mobile/ digital applications, to farmers, agents and dairy extension team to prevent possible contamination of milk (through feed or disease)", "d. Dairy partner invested in IT enabled early warnings system (right from the VLC level) and communicates to farmers, agents and dairy extension team on real time basis to prevent possible contamination of milk", "e. Dairy partner has block chain enabled technology based early warning systems that have inbuilt capability to communicate immediately to farmers, agents and dairy extension team on potential deterrents to milk quality", "f. Dairy farm has an in-house robust early warning systems that use advanced statistical models to predict quality deterrents way ahead of the potential deterioration of milk", "g. None of the above", "h. Not aware"],
            "5.4 Testing of milk": ["a. Dairy partner is outsourcing testing", "b. Dairy partner has well defined SOPs, mechanisms and in-house capability to diagnose root cause of issues and action to resolve the issues.", "c. Dairy partner has in-house experienced and qualified team to diagnose issue and respond within 48 hours", "d. Dairy partner has in-house best in class testing equipment’s that test for all the parameters that ascertain quality milk", "e. Dairy partner has made provision for doorstep testing facility at an affordable price to 80% of farmers to test quality of the milk at farm level", "f. Dairy farm has in-house latest testing equipment for testing all parameters that ascertains milk quality. Testing of milk and samples can be tracked down till individual animal level in a herd", "g. None of the above", "h. Not aware"],
            "5.5 Root Cause Diagnosis": ["a. Dairy partners have mechanisms to diagnose the root cause of issues", "b. Dairy partners have mechanisms and standard operating processes in place to diagnose the root cause of issues and detailed action plans to resolve the issues.", "c. Dairy partners have access to outside facilities to test for factors affecting milk quality", "d. Dairy partner has in-house testing facility that test for parameters that ascertains milk quality", "e. Dairy partner has in-house testing facility that test for parameters that ascertains milk quality and implement detailed action plans to resolve the issues", "f. None of the above", "g. Not aware"]
        }
    }

QUESTIONS = get_questions()

if "section_keys" not in st.session_state:
    st.session_state.section_keys = list(QUESTIONS.keys())

# --- Helper Functions ---
def get_full_key(parent_key, question_label):
    return f"{parent_key}|{question_label}"

def get_default_index(options, saved_value):
    if saved_value in options:
        try:
            return options.index(saved_value)
        except ValueError:
            return 0
    return 0

def render_nested_questions(questions_data, parent_key=""):
    responses = st.session_state.responses
    excluded_keys = [
        "Consent to fill the form", "Signature of the respondent",
        "Reviewed and confirmed by Route Incharge", "Signature of Route In charge",
        "Reviewed and confirmed by Ksheersagar SPOC", "Signature of SPOC"
    ]

    for label, value in questions_data.items():
        if label in excluded_keys:
            continue

        full_key = get_full_key(parent_key, label)

        if isinstance(value, dict):
            st.markdown(f"#### {label}")
            render_nested_questions(value, parent_key=full_key)
            st.markdown("---")
        else:
            if isinstance(value, list):
                if "multiple options" in label:
                    responses[full_key] = st.multiselect(
                        label, value, default=responses.get(full_key, []), key=full_key
                    )
                else:
                    responses[full_key] = st.radio(
                        label, value, index=get_default_index(value, responses.get(full_key)), key=full_key
                    )
            elif value is None:
                if "Date" in label:
                    default_date = responses.get(full_key, date.today())
                    if not isinstance(default_date, (datetime, date)):
                        default_date = date.today()
                    responses[full_key] = st.date_input(label, value=default_date, key=full_key)
                else:
                    responses[full_key] = st.text_input(label, value=responses.get(full_key, ""), key=full_key)
            
            remarks_key = f"{full_key}|Remarks"
            responses[remarks_key] = st.text_area(f"Remarks for **{label}**", value=responses.get(remarks_key, ""), key=remarks_key)
            st.markdown("<br>", unsafe_allow_html=True)

def show_questions_for_block(block_name, questions_data):
    st.header(block_name)
    with st.form(key=f"form-{block_name}"):
        render_nested_questions(questions_data, parent_key=block_name)
        
        st.markdown("---")
        col1, _, col2 = st.columns([1, 3, 1])
        
        with col1:
            if st.session_state.step > 0:
                if st.form_submit_button("⬅️ Back"):
                    st.session_state.step -= 1
                    st.rerun()
        
        with col2:
            is_last_step = st.session_state.step == len(st.session_state.section_keys)
            button_text = "Review & Submit ➡️" if is_last_step else "Save and Next ➡️"
            if st.form_submit_button(button_text):
                st.session_state.step += 1
                st.rerun()

# --- Application Flow ---
N = len(st.session_state.section_keys) # Total number of survey sections

# Step 0: Consent Form
if st.session_state.step == 0:
    st.title("Project Ksheersagar – TNS Associate Self-Assessment")
    st.header("Step 0: Informed Consent & Authorization")
    
    with st.form("consent_form"):
        responses = st.session_state.responses
        consent_options = ["Yes", "No"]
        
        # Consent and signature inputs
        responses["Consent to fill the form"] = st.radio("Consent to fill the form", consent_options, index=0, key="consent-radio")
        responses["Signature of the respondent"] = st.text_input("Signature of the respondent", value=responses.get("Signature of the respondent", ""), key="signature-respondent")
        st.markdown("---")
        responses["Reviewed and confirmed by Route Incharge"] = st.radio("Reviewed and confirmed by Route Incharge", consent_options, index=0, key="confirmed-route-incharge")
        responses["Signature of Route In charge"] = st.text_input("Signature of Route In charge", value=responses.get("Signature of Route In charge", ""), key="signature-route-incharge")
        st.markdown("---")
        responses["Reviewed and confirmed by Ksheersagar SPOC"] = st.radio("Reviewed and confirmed by Ksheersagar SPOC", consent_options, index=0, key="confirmed-spoc")
        responses["Signature of SPOC"] = st.text_input("Signature of SPOC", value=responses.get("Signature of SPOC", ""), key="signature-spoc")

        if st.form_submit_button("Start Survey"):
            if responses["Consent to fill the form"] == "Yes" and responses.get("Signature of the respondent", "").strip():
                st.session_state.step = 1
                st.rerun()
            else:
                st.error("Consent and Respondent's signature are required to start the survey.")

# Steps 1 through N: Survey Sections
elif 1 <= st.session_state.step <= N:
    current_step_index = st.session_state.step - 1
    current_key = st.session_state.section_keys[current_step_index]
    st.title("TNS Self-Assessment")
    st.markdown(f"**Part {st.session_state.step} of {N}: {current_key}**")
    show_questions_for_block(current_key, QUESTIONS[current_key])

# Final Step: Review and Submit (Step N + 1)
elif st.session_state.step == N + 1: 
    st.title("Final Review and Submission")
    
    status_message = st.empty()
    
    with st.form("final_submit_form"):
        st.subheader("Review Your Responses")
        
        # Prepare data for review display and final submission
        final_data = {
            k: ("; ".join(map(str, v)) if isinstance(v, list) else str(v))
            for k, v in st.session_state.responses.items() if v not in [None, "", []]
        }

        if not final_data:
            st.warning("No complete responses were recorded. Please go back and fill out the form.")
            can_submit = False
        else:
            # Display responses in a readable table (excluding remarks for cleaner main table)
            review_data = {
                "Question": [k.split("|")[-1] for k in final_data.keys() if "|Remarks" not in k],
                "Response": [v for k, v in final_data.items() if "|Remarks" not in k]
            }
            review_df = pd.DataFrame(review_data)
            st.dataframe(review_df, use_container_width=True, hide_index=True)
            can_submit = True


        st.markdown("---")
        c1, _, c2 = st.columns([1, 2, 1])
        
        with c1:
            if st.form_submit_button("⬅️ Back to Edit"):
                # Go back to the last section for editing (Step N)
                st.session_state.step = N
                st.rerun()
        
        with c2:
            if st.form_submit_button("✅ Submit Final"):
                if not can_submit:
                    status_message.error("Cannot submit an empty form.")
                else:
                    # Show temporary status while saving
                    with st.spinner('💾 Saving and submitting responses...'):
                        
                        # Append submission details to the final data package
                        final_data["submission_id"] = str(uuid.uuid4())
                        final_data["submission_timestamp"] = datetime.now().isoformat()
                        df_to_save = pd.DataFrame([final_data])
                        
                        try:
                            # Save to CSV
                            header = not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0
                            df_to_save.to_csv(CSV_FILE, mode='a', header=header, index=False)
                            
                            # CRITICAL FIX: Save the exact final data structure for display on the confirmation page
                            st.session_state.submitted_options = final_data
                            
                            st.session_state.step = N + 2 # Move to the confirmation page
                            st.rerun()
                            
                        except Exception as e:
                            status_message.error(f"❌ Error saving file: {e}")
                            st.rerun() 

# Confirmation Page (Submitted Options & Download) (Step N + 2)
elif st.session_state.step == N + 2:
    st.balloons()
    st.success("🎉 Thank you! Your responses have been submitted successfully.")
    st.markdown("---")
    
    st.subheader("Submitted Options")

    # Display the final, recorded submission data using the dedicated session key
    submitted_data = st.session_state.get("submitted_options", {})
    if submitted_data:
        # Create a DataFrame to display the submitted values, similar to the review table
        display_data = {
            "Question": [k.split("|")[-1] for k in submitted_data.keys() if "|Remarks" not in k],
            "Response": [v for k, v in submitted_data.items() if "|Remarks" not in k]
        }
        st.dataframe(pd.DataFrame(display_data), use_container_width=True, hide_index=True)
    else:
        st.info("The detailed options are not available in this session, but the data was successfully saved to the CSV file.")
    
    st.markdown("---")

    # The code to make the CSV downloadable
    try:
        # Read the file content for download
        with open(CSV_FILE, "r") as f:
            csv_content = f.read()
            st.download_button(
                label="⬇️ Download All Responses (CSV)",
                data=csv_content,
                file_name=CSV_FILE,
                mime="text/csv",
                key="download_submitted_data"
            )
    except FileNotFoundError:
        st.warning("The responses file is not yet available. It will appear after the first submission.")
    except Exception as e:
        st.error(f"Could not read the CSV file for download: {e}")

    st.markdown("---")
    
    if st.button("Start New Survey"):
        # Clear state to begin a new survey
        for key in list(st.session_state.keys()):
            # Only delete survey-specific data, keep configuration keys
            if key not in ["section_keys"]: 
                del st.session_state[key]
        st.rerun()
        
# Fallback for unexpected state (resets the app for safety)
else:
    # This catches any unexpected step value other than 0 (which is handled above)
    if st.session_state.step != 0:
        st.error("🚨 Application in an unexpected state. Restarting survey from the beginning.")
        for key in list(st.session_state.keys()):
            if key not in ["section_keys"]:
                del st.session_state[key]
        st.rerun()
