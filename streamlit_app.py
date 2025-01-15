
from crewai import Agent,Task,Crew, LLM # type: ignore
from crewai_tools import SerperDevTool # type: ignore
import streamlit as st
from dotenv import load_dotenv # type: ignore
load_dotenv ()
# Streamlit page config
st.set_page_config(page_title="Content Researcher and Writer", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
# Title and description 
st.title(" Content Researcher & Writer")
st.markdown ("Generate blog posts about any topic using AI agents.")

with st.sidebar:
    st. header ("Content Settings")
    # Make the text input take up more space
    topic = st.text_area("Enter your topic",
    height=100, 
    placeholder="Enter the topic"
    )

# Add more sidebar controls if needed
st.markdown ("### LLM Settings")
temperature = st.slider ("Temperature", 0.0, 1.0, 0.7)
# Add some spacing
st.markdown ("___")
# Make the generate button more prominent in the sidebar
generate_button = st.button("Generate Content", type="primary", use_container_width=True)
# Add some helpful information
with st.expander("How to use"):
    st.markdown("""
    1. Enter vour desired content topic\n
    2. Play with the temperature\n
    3. Click 'Generate Content' to start\n
    4. Wait for the AI to generate your article\n
    5. Download the result as a markdown file\n
    """)
def generate_content(topic):   
    llm = LLM(
        model="ollama/llama3.2",
        base_url="http://localhost:11434"
    )

    #Tool 2
    search_tool=SerperDevTool(n=10)

    research=Agent(
        role="Senior Research Analyst",
        goal=f"Identify the company’s key offerings and strategic focus areas (e.g., operations, supply chain, customer experience, etc.). A vision and product information on the industry should be fine as well.providing high-level insights, strategic recommendations, and data-driven intelligence on {topic} to support decision-making in an organization. In a broad sense, the role aims to leverage advanced research techniques, analytical skills, and industry knowledge to generate valuable insights for business growth, policy-making, product development, or market positioning.",
        backstory="you are a strategic thinker and problem solver at the heart of decision-making. You thrive on uncovering patterns, extracting valuable insights from complex data, and using them to shape impactful business strategies. You don’t just collect numbers; you interpret and transform them into actionable intelligence that drives informed decisions across the organization."
        "Your ability to connect the dots between data and business goals allows you to simplify complex findings and communicate them clearly to diverse stakeholders—from executives to technical teams. You’re not only focused on answering immediate questions but also on anticipating future opportunities and risks, ensuring the organization is prepared for what lies ahead."
        "Collaboration is key to your role. You work closely with various departments—product, marketing, finance—to ensure your insights align with broader business objectives. You challenge assumptions, ask the right questions, and think both tactically and strategically, balancing short-term needs with long-term vision."
        "Ultimately, your work drives the company forward. Whether optimizing operations, identifying new markets, or improving customer experiences, your data-driven recommendations help steer the organization toward smarter decisions and sustained growth. You’re not just analyzing data; you’re shaping the future through insights that guide the business toward success.",
        allow_delegation=False,

        tools=[search_tool],
        llm=llm
    )

    writer=Agent(
        role="Content Writer",
        goal=f"Based on the industry conducted, analyze industry trends and standards within the company’s sector related to AI, ML, and automation.Propose relevant use cases where the company can leverage GenAI, LLMs, and ML technologies to improve their processes, enhance customer satisfaction, and boost operational efficiency.Transform research finding into engaging blog posts while maintaining accuracy",
        backstory="You are a creative, curious, and adaptable individual with a knack for turning complex ideas into clear, engaging, and digestible content. At their core, they’re natural storytellers—able to weave compelling narratives that capture the audience’s attention and keep them coming back for more. They have a keen eye for detail and are deeply invested in understanding both their audience and the business goals behind every project."
        "With a strong blend of creativity and data-driven insight, a content writer thrives on research, using tools to extract valuable information that informs and elevates their writing. They excel at adapting their tone and style to fit different platforms and audiences, whether it’s an informative blog post, a persuasive landing page, or an engaging social media caption."
        "Content writers are highly collaborative, often working with marketing teams, designers, or subject matter experts to ensure their writing aligns with brand voice, SEO strategies, and business objectives. They’re also self-motivated, often juggling multiple projects and deadlines with efficiency, all while staying focused on delivering quality content that resonates with readers and drives action."
        "Ultimately, a content writer is a versatile communicator who understands the power of words to inform, inspire, and persuade, using their unique blend of creativity and strategy to make a meaningful impact.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    #research tasks
    research_tasks=Task(
        description=("""1. Conduct comprehensive research on {topic} including
                            - Recent developments and news
                            - Key industry trends and innovations
                            - Expert opinions and analyses
                            - Statistical data and market insights
                        2. Evaluate source credibility and fact-check all information
                        3. Organize findings into a structured research brief
                        4. Include all relevant citations and sources"""
        ),
        expected_output="""A detailed research report containing:
                            -Executive summary of key findingsh
                            - Comprehensive analysis of current trends and developments
                            - List of verified facts and statistics
                            - All citations and links to original sources
                            -Clear categorization of main themes and patterns
                            Please format with clear sections and bullet points for easy reference. """,
        agent=research
    )

    #writing_tasks
    writing_task=Task(
        description=("""
                    Using the research brief provided, create an engaging blog post that:

                    1. Transforms technical information into accessible content
                    2. Maintains all factual accuracy and citations from the research
                    3. Includes:
                    - Attention-grabbing introduction
                    - Well-structured body sections with clear headings
                    • Compelling conclusion
                    4. Preserves all source citations in [Source: URL] format
                    5. Includes a References section at the end
                    """),
        expected_output='''A polished blog post in markdown format that:
                    - Engages readers while maintaining accuracy
                    - Contains properly structured sections
                    - Includes Inline citations hyperlinked to the original source uri
                    - Presents information in an accessible yet informative way
                    - Follows proper markdown formatting, use H1 for the title and H3 for the sub-sections''',
        agent=writer
    )

    #crew
    crew=Crew(
        agents=[research,writer],
        tasks=[research_tasks,writing_task],
        verbose=True
    )

    return crew.kickoff(inputs={"topic":topic})

if generate_button:
    with st.spinner ('Generating content... This may take a moment.'):
        try:

            result = generate_content(topic)
            st.markdown("### Generated Content")
            st.markdown(result)

            # Add download button
            st.download_button(
                label="Download Content",
                data=result.raw,
                file_name=f"{topic.lower().replace(" " , '_')}article.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Footer
    st. markdown ("___")
    st.markdown ("Built with CrewAI, Streamlit and ChatGPT")