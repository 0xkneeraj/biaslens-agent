from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def add_reminder(reminder:str, tool_context: ToolContext) -> dict:
    """
    Adds a reminder to the user's reminder list.

    Args:
        reminder (str): The reminder text to be added.
        tool_context (ToolContext): The context in which the tool is executed.

    Returns:
        dict: A dictionary containing the updated state with the new reminder.
    """
    # Get the current state from the tool context
    reminders = tool_context.state.get("reminders", [])

    # Add the new reminder to the reminders list
    reminders.append(reminder)

    # Update the state in the tool context
    tool_context.state["reminders"] = reminders


    return {"status": "success", "message": f"Reminder added successfully. : {reminder}"}


def view_reminders(tool_context: ToolContext) -> dict:
    """
    Retrieves the list of reminders from the user's reminder list.

    Args:
        tool_context (ToolContext): The context in which the tool is executed.

    Returns:
        dict: A dictionary containing the list of reminders.
    """
    # Get the current state from the tool context
    reminders = tool_context.state.get("reminders", [])

    return {"status": "success", "reminders": reminders}


def update_reminder(reminder_index: int, new_reminder: str, tool_context: ToolContext) -> dict:
    """
    Updates an existing reminder in the user's reminder list.

    Args:
        reminder_index (int): The index of the reminder to be updated.
        new_reminder (str): The new reminder text.
        tool_context (ToolContext): The context in which the tool is executed.

    Returns:
        dict: A dictionary containing the updated state with the modified reminder.
    """
    # Get the current state from the tool context
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if 0 <= reminder_index < len(reminders):
        reminders[reminder_index] = new_reminder
        tool_context.state["reminders"] = reminders
        return {"status": "success", "message": f"Reminder updated successfully. : {new_reminder}"}
    else:
        return {"status": "error", "message": "Invalid reminder index."}
    

def delete_reminder(reminder_index: int, tool_context: ToolContext) -> dict:
    """
    Deletes a reminder from the user's reminder list.

    Args:
        reminder_index (int): The index of the reminder to be deleted.
        tool_context (ToolContext): The context in which the tool is executed.

    Returns:
        dict: A dictionary containing the updated state with the reminder removed.
    """
    # Get the current state from the tool context
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if 0 <= reminder_index < len(reminders):
        reminders.pop(reminder_index)
        tool_context.state["reminders"] = reminders
        return {"status": "success", "message": f"Reminder deleted successfully."}
    else:
        return {"status": "error", "message": "Invalid reminder index."}
    

def update_user_name(new_name: str, tool_context: ToolContext) -> dict:
    """
    Updates the user's name in the state.

    Args:
        new_name (str): The new name to be set.
        tool_context (ToolContext): The context in which the tool is executed.

    Returns:
        dict: A dictionary containing the updated state with the new user name.
    """
    # Update the user's name in the state
    tool_context.state["user_name"] = new_name

    return {"status": "success", "message": f"User name updated successfully. : {new_name}"}


memory_agent = Agent(
    name = "memory_agent",
    model = 'gemini-2.0-flash-001',
    description="A smart agent with persistent memory that can store and retrieve information.",
    instruction="""
        You are a friendly reminder assistant. Your task is to help users manage their meeting schedules and reminders effectively.
        The user's information is store in state, which is persistent across sessions.

        - User's name : {user_name}
        - Reminders: {reminders}

        You can help user manage their reminders with the following capabilities:
        1. Add new reminders.
        2. View existing reminders.
        3. Update existing reminders.
        4. Delete reminders.
        5. Update the user's name.
        Always respond in a friendly and professional manner. If you encounter any issues, inform the user politely and offer assistance.

        ** REMINDER MANAGEMENT GUIDELINES **
        1. When the user asks to add a reminder, ensure you capture all necessary details such as date, time, and description.
        2. For viewing reminders, provide a clear list of all existing reminders.
        3. When updating a reminder, confirm the changes with the user before finalizing.   
        4. If the user requests to delete a reminder, confirm which reminder they want to remove. if they mention a specific reminder, delete that one. If they do not specify, delete the most recent one. if they 
           mention reminder ( e.g " delete my meeting reminder for tomorrow at 10 AM"), look through the reminder to find a match , use that index and delete the close match.
        5. when user methiion a number or posittion : 
            - Use that as the index ( e.g. "delete reminder 2" means index = 2 delete that).
            - Remember that the index is 1-based, so the first reminder is at index 1.
        6. For relative positions:
            - "first" means index 1.
            - "last" means the last reminder in the list.
            - "next" means the next reminder in the list (if applicable).
            - "previous" means the previous reminder in the list (if applicable).
        7. For addition:
            - If the user mentions a specific date and time, add that reminder.
            - If they just mention a meeting without specifics, ask for the details before adding.
            - Extract the actual reminder text from the user's input.
        8. Always confirm with the user before making any changes to their reminders.
        9. If the user asks to update their name, confirm the new name before updating.
        10. If the user asks to view their reminders, provide a clear and concise list of all reminders.
            
        
    """,
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name
    ],

)