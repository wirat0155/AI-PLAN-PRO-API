from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import PlanAgents
from tasks import PlanTasks
from api_schema import PlanRequest
from models import ProjectPlan

load_dotenv()

app = FastAPI(title="AI-PLAN-PRO-API", version="1.0")

@app.post("/plan", response_model=ProjectPlan)
def generate_project_plan(request: PlanRequest):
    # 1. Construct team composition string
    # Format: "Role X1 (Name), Role X1 (Name)"
    team_parts = []
    for member in request.team_composition:
        # Assuming X1 for each individual input
        team_parts.append(f"{member.role} X1 ({member.name})")
    
    team_composition_str = ", ".join(team_parts)
    print(f"Generated Team Composition String: {team_composition_str}")

    # 2. Setup Crew
    agents = PlanAgents()
    tasks = PlanTasks()

    architect_agent = agents.project_architect()
    scheduler_agent = agents.scheduling_analyst()

    decomposition_task = tasks.task_decomposition(architect_agent, request.project_name)
    estimation_task = tasks.timeline_estimation(scheduler_agent, request.project_name, team_composition_str, request.description)

    crew = Crew(
        agents=[architect_agent, scheduler_agent],
        tasks=[decomposition_task, estimation_task],
        process=Process.sequential,
        verbose=True
    )

    # 3. Kickoff
    # result will be the output of the last task, which is a Pydantic model ProjectPlan
    try:
        result = crew.kickoff()
        
        # CrewAI 0.x return raw string or whatever. 
        # CrewAI 1.x with output_json usually returns the object or result.pydantic
        
        # We need to extract the ProjectPlan object
        if hasattr(result, 'pydantic') and result.pydantic:
            return result.pydantic
        elif hasattr(result, 'json_dict') and result.json_dict:
            return result.json_dict
        
        # Fallback if it returns raw json string?
        # But we defined output_json=ProjectPlan in tasks.py so it should be structured.
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
