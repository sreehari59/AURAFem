import streamlit as st
from crewai import Agent, Crew, Process, Task, LLM
import os
from openai import OpenAI

st.set_page_config(page_title="AURAFem", page_icon="🤖")
st.markdown("""
    <div style='text-align: center;'>
        <h1> Welcome to AURAFem </h1>
    </div>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:  
    st.session_state.messages =  [{"role": "assistant", "content": "Hello!"}]
    st.session_state.app = None
    st.session_state.chat_active = True
    

keys = "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"
openai_key = keys

client = OpenAI(api_key=keys)
st.session_state["openai_model"] = "gpt-4o-mini"

def crew_agent(openai_key):
    llm=LLM(model="gpt-4o-mini", api_key=openai_key)

    symptoms_agent = Agent(
                role="Find the symptoms",
                goal="Should ask for the relevant symptoms for given the disease",
                allow_delegation=False,
                verbose=True,
                llm=llm,
                backstory=(
                    """
                    The symptoms agent is worlds best doctor and has excellent knowledge about the SYMPTOMS associated with
                    diseases like endometriosis,
                    PCOS, cervical cancer, endometrial cancer and ovarian cancer. 
                    """
                ),
                tools=[],
                )
    
    symptoms_task = Task(
        description=(
            """
            We have a patient SHE is suffering from a disease. Ask her more into about the SYMPTOMS based on the
            patient disease:
            {patient_disease}
            """
        ),
        expected_output="""
            Start being a positive and telling stay positive. 
            Detail the disease mentioned by the patient and also ask about more about the symptoms
            """,
        tools=[],
        agent=symptoms_agent,
    )

    treatment_agent = Agent(
                role="Provide a possible treatment",
                goal="Should suggest the possible treatment given the disease",
                allow_delegation=False,
                verbose=True,
                llm=llm,
                backstory=(
                    """
                    The treatment agent is worlds best doctor and has excellent knowledge about the diseases like endometriosis,
                    PCOS, cervical cancer, endometrial cancer and ovarian cancer. 
                    """
                ),
                tools=[],
                )

    treatment_task = Task(
        description=(
            """
            We have a patient SHE is suffering from a disease. Provide a detailed treatment based on the
            patient disease:
            {patient_disease}
            """
        ),
        expected_output="""
            Start with the heading "TREATMENT"
            Detailed treatment explanation
            """,
        tools=[],
        agent=treatment_agent,
    )

    manager = Agent(
        role="Master Agent",
        goal="Oversee the patients response and manage the specialized agents to deliver a positive and helping hand for the patient.",
        backstory="""Experienced, meticulous MEDICAL manager coordinating the efforts of agents across different domains like symptom identifying, treatment suggestion.
        The MEDICAL manager should always start asking SYMPTOMS before moving into treatment""",
        allow_delegation=True,
        cache=True,
        verbose=True,
        # llm=llm,
        )   

    crew = Crew(
                agents=[symptoms_agent, treatment_agent],
                tasks=[symptoms_task, treatment_task],
                manager_agent=manager,
                process=Process.hierarchical
                )
    
    return crew

def initialize_agents():
    os.environ["OPENAI_API_KEY"] = openai_key
    crew = crew_agent(openai_key)
    return crew

app = initialize_agents()
def generate_response(patient_disease):
    return app.kickoff(
            inputs={"patient_disease": patient_disease}
            )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if patient_disease:= st.chat_input(placeholder="Ask a question"):
    st.chat_message("user").markdown(patient_disease)

    st.session_state.messages.append({"role": "user", "content": patient_disease})
    with st.spinner("Thinking..."):
        if "cancer" in patient_disease:
            print("SUCESS")
            response = generate_response(patient_disease)
        else:
            st.session_state["openai_model"] = "gpt-3.5-turbo"
            response = ""

    with st.chat_message("assistant"):
        if "" in response:
            stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        else:
            st.markdown(response.raw)
            st.session_state.messages.append({"role": "assistant", "content": response.raw})
            
        