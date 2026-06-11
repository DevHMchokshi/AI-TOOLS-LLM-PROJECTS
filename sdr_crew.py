import os
import json
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel
from typing import Optional

# Tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# We need an output model for the Qualifier Agent
class QualificationResult(BaseModel):
    score: int
    reasoning: str
    is_qualified: bool
    pain_points_found: list[str]
    company_size: Optional[str]
    tech_stack: list[str]

class SDRPipeline:
    def __init__(self, lead_data: dict, icp_data: dict):
        self.lead_data = lead_data
        self.icp_data = icp_data
        
    def get_researcher(self):
        return Agent(
            role='Lead Researcher',
            goal="Extract pain points, company size, tech stack, and growth signals from the lead's company website and recent news.",
            backstory="You are a master at OSINT and company research. You can find out exactly what a company does, what technologies they use, and what challenges they are likely facing right now. You are meticulous and detail-oriented.",
            tools=[search_tool, scrape_tool],
            verbose=True,
            memory=True
        )
        
    def get_qualifier(self):
        return Agent(
            role='Lead Qualifier',
            goal='Compare the researched lead against the defined ICP and output a qualification score (0-100) with detailed reasoning.',
            backstory='You are a strict and analytical Sales Operations manager. You understand exactly what makes a good customer for us based on our Ideal Customer Profile (ICP). You do not let bad leads pass through.',
            verbose=True,
            memory=True
        )

    def get_outreach(self):
        return Agent(
            role='Outreach Specialist',
            goal='Draft a hyper-personalized cold email referencing specific pain points found by the Researcher, aiming to book a meeting.',
            backstory="You are an elite SDR who writes cold emails that consistently get 80%+ open rates and 20%+ reply rates. You never use generic templates. Every email you write proves you know the prospect's business deeply.",
            verbose=True,
            memory=True
        )
        
    def create_crew(self):
        researcher = self.get_researcher()
        qualifier = self.get_qualifier()
        outreach = self.get_outreach()
        
        research_task = Task(
            description=f'''
            Conduct comprehensive research on the following lead:
            Name: {self.lead_data.get("name")}
            Role: {self.lead_data.get("role")}
            Company: {self.lead_data.get("company")}
            Website/LinkedIn: {self.lead_data.get("website", "")} {self.lead_data.get("linkedin", "")}
            
            Find out:
            1. What the company does.
            2. Estimated company size.
            3. Technologies they use.
            4. Recent news or growth signals.
            5. Potential pain points related to our value proposition.
            ''',
            expected_output='A comprehensive research report detailing company size, tech stack, recent news, and potential pain points.',
            agent=researcher
        )
        
        qualify_task = Task(
            description=f'''
            Review the research report from the Researcher and compare it against our ICP:
            {json.dumps(self.icp_data, indent=2)}
            
            Evaluate if this lead is a good fit. Output a score from 0-100.
            Set is_qualified to true if the score is >= {self.icp_data.get("minimum_qualification_score", 70)}.
            ''',
            expected_output='A JSON object matching the QualificationResult schema containing the score, reasoning, and whether the lead is qualified.',
            agent=qualifier,
            output_json=QualificationResult
        )
        
        outreach_task = Task(
            description='''
            Review the qualification result. If the lead is qualified (is_qualified=true), write a hyper-personalized cold email.
            The email must reference specific pain points and recent news found in the research.
            Include a clear Call to Action (CTA) to book a meeting, and actively include a Calendly link (e.g. "https://calendly.com/sdr-team/15min") in the CTA.
            Keep it under 150 words. Be conversational, not overly formal.
            If the lead is NOT qualified, output: "LEAD DISQUALIFIED - No email drafted."
            ''',
            expected_output='The final draft of the hyper-personalized cold email, or a disqualification message.',
            agent=outreach
        )
        
        return Crew(
            agents=[researcher, qualifier, outreach],
            tasks=[research_task, qualify_task, outreach_task],
            process=Process.sequential,
            memory=True, # Enables Short-term and Long-term memory (ChromaDB)
            verbose=True
        )
        
    def run(self):
        crew = self.create_crew()
        result = crew.kickoff()
        return result
