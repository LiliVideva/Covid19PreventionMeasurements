import wikipedia
import wikipediaapi
import os
import timeit

from google.colab import drive
from datetime import date, timedelta

wiki = wikipediaapi.Wikipedia()

all_countries = ["Afghanistan" ,"Albania" ,"Algeria" ,"Andorra" ,"Angola" ,"Antigua and Barbuda" ,"Argentina" ,"Armenia" ,"Australia" ,"Austria" ,"Azerbaijan" ,"Bahamas" ,"Bahrain" ,"Bangladesh" ,"Barbados" ,"Belarus" ,"Belgium" ,"Belize" ,"Benin" ,"Bhutan" ,"Bolivia" ,"Bosnia and Herzegovina" ,"Botswana" ,"Brazil" ,"Brunei" ,"Bulgaria" ,"Burkina Faso" ,"Burundi" ,"Ivory Coast" ,"Cabo Verde" ,"Cambodia" ,"Cameroon" ,"Canada" ,"Central African Republic" ,"Chad" ,"Chile" ,"China" ,"Colombia" ,"Comoros" ,"Congo-Brazzaville" ,"Costa Rica" ,"Croatia" ,"Cuba" ,"Cyprus" ,"Czech Republic" ,"Democratic Republic of the Congo" ,"Denmark" ,"Djibouti" ,"Dominica" ,"Dominican Republic" ,"Ecuador" ,"Egypt" ,"El Salvador" ,"Equatorial Guinea" ,"Eritrea" ,"Estonia" ,"Eswatini" ,"Ethiopia" ,"Fiji" ,"Finland" ,"France" ,"Gabon" ,"Gambia" ,"Georgia" ,"Germany" ,"Ghana" ,"Greece" ,"Grenada" ,"Guatemala" ,"Guinea" ,"Guinea-Bissau" ,"Guyana" ,"Haiti" ,"Holy See" ,"Honduras" ,"Hungary" ,"Iceland" ,"India" ,"Indonesia" ,"Iran" ,"Iraq" ,"Ireland" ,"Israel" ,"Italy" ,"Jamaica" ,"Japan" ,"Jordan" ,"Kazakhstan" ,"Kenya" ,"Kiribati" ,"Kuwait" ,"Kyrgyzstan" ,"Laos" ,"Latvia" ,"Lebanon" ,"Lesotho" ,"Liberia" ,"Libya" ,"Liechtenstein" ,"Lithuania" ,"Luxembourg" ,"Madagascar" ,"Malawi" ,"Malaysia" ,"Maldives" ,"Mali" ,"Malta" ,"Marshall Islands" ,"Mauritania" ,"Mauritius" ,"Mexico" ,"Micronesia" ,"Moldova" ,"Monaco" ,"Mongolia" ,"Montenegro" ,"Morocco" ,"Mozambique" ,"Myanmar" ,"Namibia" ,"Nauru" ,"Nepal" ,"Netherlands" ,"New Zealand" ,"Nicaragua" ,"Niger" ,"Nigeria" ,"North Korea" ,"North Macedonia" ,"Norway" ,"Oman" ,"Pakistan" ,"Palau" ,"Palestine State" ,"Panama" ,"Papua New Guinea" ,"Paraguay" ,"Peru" ,"Philippines" ,"Poland" ,"Portugal" ,"Qatar" ,"Romania" ,"Russia" ,"Rwanda" ,"Saint Kitts and Nevis" ,"Saint Lucia" ,"Saint Vincent and the Grenadines" ,"Samoa" ,"San Marino" ,"Sao Tome and Principe" ,"Saudi Arabia" ,"Senegal" ,"Serbia" ,"Seychelles" ,"Sierra Leone" ,"Singapore" ,"Slovakia" ,"Slovenia" ,"Solomon Islands" ,"Somalia" ,"South Africa" ,"South Korea" ,"South Sudan" ,"Spain" ,"Sri Lanka" ,"Sudan" ,"Suriname" ,"Sweden" ,"Switzerland" ,"Syria" ,"Tajikistan" ,"Tanzania" ,"Thailand" ,"Timor-Leste" ,"Togo" ,"Tonga" ,"Trinidad and Tobago" ,"Tunisia" ,"Turkey" ,"Turkmenistan" ,"Tuvalu" ,"Uganda" ,"Ukraine" ,"United Arab Emirates" ,"United Kingdom" ,"United States of America" ,"Uruguay" ,"Uzbekistan" ,"Vanuatu" ,"Venezuela" ,"Vietnam" ,"Yemen" ,"Zambia" ,"Zimbabwe"]
all_section_titles = {'Additional information on cases', 'Aid', 'Alert level', 'Alert level system', 'Alternative estimates', 'Antivirals', 'Assistance to other countries', 'Assists', 'Authorities actions on reporting', 'Background', 'Background and prevention', 'Background prior confirmation', 'Basic reproduction number', 'COVID-19 pandemic', 'Cancellations, suspensions, and closings', 'Case details', 'Case estimates', 'Case summary', 'Case-related events', 'Cases', 'Cases by province or territory', 'Cases by region', 'Cases timeline', 'Cases traced to travel from Egypt', 'Censorship of medical personnel', 'Charges of censorship', 'Charts', 'Charts based on daily reports', 'Closure of cities with high rates of infection', 'Confirmed Cases', 'Confirmed cases', 'Confirmed cases by country and territory', 'Containment', 'Controversies', 'Controversy', 'Cooperation with neighbouring states', 'Crisis Management', 'Crisis Management Staff', 'Criticism', 'Criticisms and reactions', 'Current number of cases by provinces', 'Data', 'Data Charts', 'Debate', 'Detailed case counts', 'Development', 'Diagrams', 'Early reaction controversy', 'Economic Impact', 'Economic consequences', 'Economic impact', 'Economic measures', 'Effects', 'Effects on civilian life', 'Epidemic controls', 'Epidemic curve', 'Epidemiological overview', 'Epidemiology', 'Evacuation of citizens', 'Exit strategy', 'External links', 'False reports and rumours', 'Festivals and contests', 'First cases', 'Footnotes', 'Forecasting', 'Foreign cases linked to Italy', 'Funds and aid on the pandemic', 'Further reading', 'Gallery', 'Government Response', 'Government measures', 'Government policy', 'Government reactions', 'Government response', 'Government response and impacts', 'Government responses', 'Graph', 'Graph of Active Cases (as of April 11, 2020)', 'Graphs', 'Health in The Gambia', 'Healthcare system', 'Help', 'History', 'Hospitals for COVID-19', 'Humanitarian aid', 'Humanitarian assistance', 'Hydroxychloroquine controversy', 'Impact', 'Impact and response', 'Impact on society', 'Impact on sport', 'Impacts', 'Impacts and incidents', 'Impacts and reactions', 'Implications', 'Infected Iranian officials', 'Infections in Hungary', 'Information', 'International assistance', 'International spread', 'International travel restrictions', 'Interpersonal solidarity', 'List of measures', 'Location of cases', 'Lockdown areas', 'Major events after confirmation', 'Management', 'Mauritians infected abroad', 'Measures', 'Measures taken by the government', 'Medical testing', 'Misinformation', 'Misinformation and criticism', 'Municipalities and Cantons affected', 'National Pandemic Plan', 'National lockdown', 'National state of emergency', 'Nile River cruise ship', 'Nomenclature', 'Non-government estimates', 'Notable people', 'Notes', 'Notes and references', 'Number of confirmed cases by hospital districts', 'Other cases', 'Other international reactions', 'Other responses', 'Pandemic by country', 'People', 'Phases', 'Policies to fight the contagion', 'Politicization', 'Possible spread to other countries', 'Preparations', 'Prevention', 'Prevention Measures', 'Prevention efforts', 'Prevention in other countries', 'Prevention in other countries and territories', 'Prevention measures', 'Prevention measures and Response', 'Prevention measures and response', 'Preventive Measures', 'Preventive measures', 'Preventive measures by government', 'Prison riots', 'Private sector reactions', 'Quarantine and isolation', 'Raiwind Hotspot', 'Reactions', 'Reactions abroad', 'References', 'Regional distribution of cases', 'Regional infection development', 'Relations with neighbouring countries and territories', 'Repatriation of citizens, residents, and travellers', 'Research', 'Response', 'Response by sector', 'Response from the public healthcare system', 'Response measures', 'Responses', 'See also', 'Shortage of masks controversy', 'Simulation statistics', 'Situation', 'Social impact', 'Social impacts', 'Socio-economic impact', 'Solidarity with other countries', 'Spread of SARS-CoV-2 within and around Poland', 'Spread to other countries and territories', 'State of emergency and other restrictions', 'Statistics', 'Stimulus policy', 'Summary', 'Summary of COVID-19 Medical Cases in Bhutan', 'Summary of Cases', 'Suspected cases', 'Technology', 'Testing', 'Testing and countermeasures', 'Testing and surveillance', 'Testing, treatment and preventive measures', 'Timeline', 'Timeline by state', 'Timeline of cases', 'Travel restrictions'}
relevant_section_titles = ["timeline", "background and prevention", "containment", "controversy", "covid-19 pandemic", "criticisms and reactions", "development", "economic impact", "economic measures", "effects on civilian life", "epidemic controls", "government measures", "government policy", "government reactions", "government response and impacts", "government response", "government responses", "impact", "impact and response", "impacts and reactions", "list of measures", "management", "measures taken by the government", "measures", "national lockdown", "national state of emergency", "prevention efforts", "prevention measures and response", "prevention measures", "prevention", "preventive measures by government", "preventive measures", "reactions abroad", "response by sector", "response from the public healthcare system", "response measures", "response", "responses", "social impact", "social impacts", "state of emergency and other restrictions", "testing, treatment and preventive measures", "travel restrictions"]

today = date.today()
yesterday = date.today() - timedelta(days=1)

# dynamic_titles = {f'Graph of Active Cases (as of {today.strftime("%B %d, %Y")})'}
# dynamic title replace
# if there are more than one dynamic title it could be extended in function

# all_section_titles.remove(f'Graph of Active Cases (as of {yesterday.strftime("%B %d, %Y")})')
all_section_titles.remove('Graph of Active Cases (as of April 11, 2020)')
all_section_titles.add(f'Graph of Active Cases (as of {today.strftime("%B %d, %Y")})')


titles = {}

def get_all_section_titles():
  for c in all_countries:
    sect = wiki.page(f'2020 coronavirus pandemic in {c}').sections
    for s in sect:
      titles[s.title] = c
  return titles

def check_for_new_section_titles():
  new_sections= {}
  for c in all_countries:
    sect = wiki.page(f'2020 coronavirus pandemic in {c}').sections
    for s in sect:
      if s.title not in all_section_titles:
        new_sections[s.title] = c
  return new_sections

# TODO add function add_to_relevant_titles

new_sects = check_for_new_section_titles()
for section,country in new_sects.items():
  print(f'There is new section title: "{section}" for 2020 coronavirus pandemic in {country}')

all_section_titles.update(set(new_sects.keys()))
print(len(all_section_titles))

drive.mount('/content/drive')
!ls "/content/drive/My Drive/COVID-19-Reasearch"
# MANDATORY: right click on the shared "COVID-19-Reasearch" folder and then click "Add shortcut to Drive"
for c in all_countries:
    sect = wiki.page(f'2020 coronavirus pandemic in {c}').sections
    for s in sect:
        if s.title.lower() in relevant_section_titles:
            with open(f'/content/drive/My Drive/COVID-19-Reasearch/{c}.txt', 'a') as f:
              f.write(s.full_text())