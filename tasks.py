from crewai import Task
from models import ProjectPlan

class PlanTasks:
    def task_decomposition(self, agent, project_name):
        return Task(
            description=(
                f"Analyze the request '{project_name}'. "
                "Decompose it into 3-7 distinct sub-tasks logicially sorted from start to finish. "
                "For each sub-task, provide:\n"
                "1. A clear Title\n"
                "2. A detailed Description (what needs to be done)\n"
                "3. Complexity (Low, Medium, or High)\n"
                "**Critical**: Ensure the order makes logical sense. (e.g., 'Build Foundation' must come before 'Build Roof'). "
                "The breakdown should be appropriate for the domain of the request (e.g. Software, Event Planning, Construction, etc)."
            ),
            expected_output="A list of sub-tasks with title, description, and complexity, sorted chronologically.",
            agent=agent
        )

    def timeline_estimation(self, agent, project_name, team_composition, description):
        description_text = f"Constraint/Description: '{description}'" if description else "Constraint: None"
        return Task(
            description=(
                f"Take the sub-tasks identified for '{project_name}' and apply timeline estimation. "
                "1. First, get the current date using the 'Get Current Date' tool. "
                f"2. Analyze the Team Composition: '{team_composition}'.\n"
                f"3. Analyze the {description_text}. \n"
                "   - **Start Date Interpretation**: If the description mentions a start time (e.g. 'start next month', 'begin on Friday'), calculate the absolute start date relative to the Current Date. If not specified, use Current Date. \n"
                "   - **Constraints**: If a deadline or duration limit is specified (e.g. 'Finish by end of month', '7 days max'), you MUST plan accordingly. Increase parallelism if needed to meet the date.\n"
                "4. For each task:\n"
                "   - Assign 'estimated_days' based on Complexity: Low = 0.5-1 day (use 1), Medium = 2-3 days, High = 5+ days.\n"
                "   - Calculate 'start_date' and 'due_date' using the 'Working Day Calculator'. Use the project's calculated start date for the first task.\n"
                "   - **Sequential vs Parallel**: \n"
                "       - Single Resource -> Sequential.\n"
                "       - Multiple Resources -> Parallel allowed.\n"
                "       - **Logical Dependencies**: Even with multiple resources, you MUST respect logical dependencies. \n"
                "           - Example: You cannot start 'Deploy' before 'Testing' is finished. \n"
                "           - Example: You cannot start 'Roof' before 'Walls' are done.\n"
                "           - If Task B intelligently depends on Task A, enforce: Task B Start Date >= Task A Due Date (or Task A Due Date + 1 day).\n"
                "       - **Override**: If the 'Constraint' requires faster delivery, maximize parallelism ONLY for tasks that correspond to independent efforts (e.g. 'Develop Frontend' and 'Develop Backend' can be parallel, but 'Build Foundation' and 'Build Roof' cannot).\n"
                "   - **Task Assignment**: Assign strictly 1 person per task.\n"
                "5. Sum up for 'total_estimated_duration' (Total calendar duration from first start date to last due date).\n"
                "6. Return the final fully populated JSON matching the ProjectPlan schema."
            ),
            expected_output="A JSON object containing project_name, total_estimated_duration, and detailed sub_tasks with start_date and due_date.",
            agent=agent,
            output_json=ProjectPlan
        )
