from pydantic import BaseModel, Field
from typing import List, Optional

class SubTask(BaseModel):
    sequenceno: int = Field(..., description="Unique identifier for the sub-task")
    title: str = Field(..., description="Title of the sub-task")
    description: str = Field(..., description="Short technical description of the sub-task")
    complexity: str = Field(..., description="Complexity level: Low, Medium, or High")
    estimated_days: float = Field(..., description="Estimated effort in days")
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    due_date: str = Field(..., description="Estimated due date in YYYY-MM-DD format")
    assignee: str = Field(..., description="Name of the person assigned to this task")

class ProjectPlan(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    total_estimated_duration: str = Field(..., description="Total estimated duration string (e.g., '14 Days')")
    sub_tasks: List[SubTask] = Field(..., description="List of sub-tasks")
