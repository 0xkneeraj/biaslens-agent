from google.genai import types
from datetime import datetime

# Dummy display_state function (replace with actual implementation or import if available)
def display_state(
    session_service, app_name, user_id, session_id, label="Current State"
):
    """Display the current session state in a formatted way."""
    try:
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        # Format the output with clear sections
        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # Handle the user name
        user_name = session.state.get("user_name", "Unknown")
        print(f"👤 User: {user_name}")

        # Handle purchased courses
        purchased_history = session.state.get("purchased_history", [])
        if purchased_history and any(purchased_history):
            print("📚 Courses:")
            for course in purchased_history:
                if isinstance(course, dict):
                    course_id = course.get("id", "Unknown")
                    purchase_date = course.get("purchase_date", "Unknown date")
                    print(f"  - {course_id} (purchased on {purchase_date})")
                elif course:  # Handle string format for backward compatibility
                    print(f"  - {course}")
        else:
            print("📚 Courses: None")

        # Handle interaction history in a more readable way
        interaction_history = session.state.get("interaction_history", [])
        if interaction_history:
            print("📝 Interaction History:")
            for idx, interaction in enumerate(interaction_history, 1):
                # Pretty format dict entries, or just show strings
                if isinstance(interaction, dict):
                    action = interaction.get("action", "interaction")
                    timestamp = interaction.get("timestamp", "unknown time")

                    if action == "user_query":
                        query = interaction.get("query", "")
                        print(f'  {idx}. User query at {timestamp}: "{query}"')
                    elif action == "agent_response":
                        agent = interaction.get("agent", "unknown")
                        response = interaction.get("response", "")
                        # Truncate very long responses for display
                        if len(response) > 100:
                            response = response[:97] + "..."
                        print(f'  {idx}. {agent} response at {timestamp}: "{response}"')
                    else:
                        details = ", ".join(
                            f"{k}: {v}"
                            for k, v in interaction.items()
                            if k not in ["action", "timestamp"]
                        )
                        print(
                            f"  {idx}. {action} at {timestamp}"
                            + (f" ({details})" if details else "")
                        )
                else:
                    print(f"  {idx}. {interaction}")
        else:
            print("📝 Interaction History: None")

        # Show any additional state keys that might exist
        other_keys = [
            k
            for k in session.state.keys()
            if k not in ["user_name", "purchased_history", "interaction_history"]
        ]
        if other_keys:
            print("🔑 Additional State:")
            for key in other_keys:
                print(f"  {key}: {session.state[key]}")

        print("-" * (22 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")
   

class Colors:
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'
    BG_CYAN = '\033[46m'
    BG_RED = '\033[41m'
    FG_WHITE = '\033[97m'
    RESET = "\033[0m"
    YELLOW = "\033[33m",
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = '\033[0m'


def interaction_history(session_service, app_name, session_id, user_id, entry):
    """
        Adds a user query to the conversation history.

        Args:
            history (list): The conversation history.
            user_query (str): The user query to add.

        Returns:
            list: Updated conversation history with the user query added.
    """
    try:
        session = session_service.get_session(
            app_name=app_name, session_id=session_id, user_id=user_id
        )

        interaction_history = session.state.get("interaction_history", [])

        # Add timestamp if not already present
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # add entry to interaction_history
        interaction_history.append(entry)

        # create udpate state
        updated_state = session.state.copy()
        updated_state["interaction_history"] = interaction_history

        # create a new session with update state
        session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=updated_state
        )

    except Exception as e:
        print(f"Error updating interaction history: {e}")

def add_user_query_to_history(session_service, app_name, session_id, user_id, user_input):
   
    """Add a user query to the interaction history."""
    interaction_history(session_service, 
                        app_name, 
                        session_id, 
                        user_id,
                        entry = {
                            "action": "user_query",
                            "query": user_input,
                        } )

def add_agent_response_to_history(
    session_service, app_name, user_id, session_id, agent_name, response
):
    """Add an agent response to the interaction history."""
    interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "agent_response",
            "agent": agent_name,
            "response": response,
        },
    )


async def process_agent_response(event):
    # process and display agent response events
    print(f"Event id : {event.id}, Author : {event.author}")

    has_specific_part = False 
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f" Text: '{part.text.strip()}'")

    # check for final response after specific parts
    final_response = None
    if not has_specific_part and event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response  = event.content.parts[0].text.strip()

            # use colors and formatting to make the final response stand out
            print(
                f"\n{Colors.BG_BLUE}{Colors.FG_WHITE}{Colors.BOLD}================== AGENT RESPONSE===================="
            )
            print(
                f"\n{Colors.BG_CYAN}{Colors.BOLD}{final_response}{Colors.END}"
            )

            print(
                f"{Colors.BG_BLUE}{Colors.FG_WHITE}{Colors.BOLD}==========================================================="
            )
        else:
            print(
                f"\n {Colors.BG_RED}{Colors.FG_WHITE}{Colors.BOLD} ===> Final Agent Response: [No text content in final event]"
            )
        return final_response

async def call_agent_async(runner, user_id, session_id, user_input):
    
    # Call the agent asynchronously with the user input and session details.
    cotent = types.Content(
        role="user", parts=[types.Part(text=user_input)]
    )
    print(
        f"\n{Colors.BG_BLUE}{Colors.FG_WHITE}{Colors.BOLD}===== User Input====={Colors.END}"
    )

    final_response_text=None
    agent_name = None

    # display state before processing
    display_state(
        runner.session_service,
        runner.app_name,
        session_id,
        user_id,
        "STATE BEFORE PROCESSING",
    )
    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=cotent
        ):
            if event.author:
                agent_name = event.author
            response = await process_agent_response(event)
            if response:
                final_response_text = response

    except Exception as e:
        print(
            f"{Colors.BG_RED}{Colors.FG_WHITE}Error during agent run: {e}{Colors.BG_RED}"
        )
    # add the agent response to interaction history if we got a final response

    if final_response_text and agent_name:
        add_agent_response_to_history(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            agent_name,
            final_response_text,
        )

    # Display state after processing the message
    display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State AFTER processing",
    )

    print(f"{Colors.YELLOW}{'-' * 30}{Colors.RESET}")
    return final_response_text