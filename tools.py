from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

class CurrentDateTool(BaseTool):
    name: str = "Get Current Date"
    description: str = "Returns the current date in YYYY-MM-DD format. Useful for knowing 'today'."

    def _run(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

class WorkingDayCalculatorInput(BaseModel):
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    days_to_add: float = Field(..., description="Number of working days to add")

class WorkingDayCalculatorTool(BaseTool):
    name: str = "Working Day Calculator"
    description: str = "Calculates a future date by adding working days (skipping Sat/Sun) to a start date."
    args_schema: type[BaseModel] = WorkingDayCalculatorInput

    def _run(self, start_date: str, days_to_add: float) -> str:
        try:
            current_date = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            return "Error: Invalid date format. Please use YYYY-MM-DD."

        days_remaining = int(days_to_add)
        # Only add valid days
        if days_remaining <= 0 and days_to_add > 0:
             days_remaining = 1 # Minimum 1 day if fractional work exists

        while days_remaining > 0:
            current_date += timedelta(days=1)
            # 5=Saturday, 6=Sunday
            if current_date.weekday() >= 5:
                continue
            days_remaining -= 1
        
        return current_date.strftime("%Y-%m-%d")
