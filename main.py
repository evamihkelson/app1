import streamlit as st
from langchain import PromptTemplate
#from langchain.llms import OpenAI #so vananenud rida ning asendatud allolevaga
from langchain_community.llms import OpenAI
import os


template = """
 You are a personal trainer with 20 years of experience. You analyze the client's training goals to create a personalized training plan that only this client will receive;
    PRODUCT input text: {content};
    CUSTOMER age group (y): {agegroup};
    CUSTOMER main training goals: {training goals};
    TASK: Create a training plan that suits the client's age group and fitness goals.;
    FORMAT: Present the result in the following order: (WEEKLY PLAN), (EXERCISES PLAN);
    PRODUCT DESCRIPTION: describe the training exercises in 5 sentences;
    BENEFITS: describe in 3 sentences why this training plan is perfect considering customers age group and training plan goal;
    USE CASE: Write a gym workout plan with 6 exercises, determine how many times a week one should train in the gym based on their training goals {traininggoal} and age {agegroup}. Assign each individual their own workout plan."


"""


prompt = PromptTemplate(
    input_variables=["agegroup", "traininggoal", "content"],
    template=template,
)


def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=.7, openai_api_key=openai_api_key)
    return llm


st.set_page_config(page_title="Customer tailored content", page_icon=":robot:")
st.header("Personaliseeritud turundusteksti konverter")


col1, col2 = st.columns(2)


with col1:
    st.markdown("Otstarve:; Veebilehel kuvatavate treeningkavade personaliseerimine igale kliendile või kliendigruppidele; väljundtekst on kohandatud kliendi a) vanuserühmaga ja b) treeningkava eesmärgiga; sisendtekstiks on neutraalses vormis treeningkava.\
    \n\n Kasutusjuhend: Kasutaja: 1) valmistab ette treeningkava (sisendteksti);
2) määrab segemendid lähtuvalt vanuserühma ja treeningkava eesmärgist;
3) sisestab ükshaaval segmentide lõikes eeltoodud info äpi kasutajaliideses, saadab ära;
4) kopeerib ükshaaval segmentide lõikes äpi väljundteksti kõnealusetreeningkavale.\
    4) kopeeri ükshaaval treeningkavade lõikes äpi treeningkava kõnealuse treenija juuurde.")


with col2:
    st.image(image='companylogo.jpg', caption='Natural and healthy shirts for everybody')


st.markdown("## Enter Your Content To Convert")


def get_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return openai_api_key
    # If OPENAI_API_KEY environment variable is not set, prompt user for input
    input_text = streamlit.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text


openai_api_key = get_api_key()


col1, col2 = st.columns(2)
with col1:
    option_agegroup = st.selectbox(
        'Which age group would you like your content to target?',
        ('9-15', '16-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-100'))
    
def get_traininggoal():
    input_text = st.text_input(label="Customers main training goal", key="traininggoal_input")
    return input_text


hobby_input = get_traininggoal()


def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="Your content...", key="content_input")
    return input_text


content_input = get_text()


if len(content_input.split(" ")) > 700:
    st.write("Please enter a shorter content. The maximum length is 700 words.")
    st.stop()


def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "t shirts, all clolors, cotton, responsible manufacturing"


st.button("*GENERATE TEXT*", type='secondary', help="Click to see an example of the content you will be converting.", on_click=update_text_with_example)


st.markdown("### Your customer tailored content:")


if content_input:
#    if not openai_api_key:
#        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
#        st.stop()


    llm = load_LLM(openai_api_key=openai_api_key)


    prompt_with_content = prompt.format(agegroup=option_agegroup, hobby=hobby_input, content=content_input)


    formatted_content = llm(prompt_with_content)


    st.write(formatted_content)

