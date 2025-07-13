import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService, Session
from google.genai import types
from agent import meetingReminder
from memory_agent import memory_agent
from utils import call_agent_async


load_dotenv()

# Database URL for session storage
# You can change this to your preferred database, e.g., PostgreSQL, MySQL, etc.
# For SQLite, the file will be created in the current directory.
db_url = "sqlite:///./agent_sessions.db"
session_service = DatabaseSessionService(db_url=db_url)


# Application and user details
initial_state = {
    "user_name": "Anil Kumar",
    "reminders": [],
}

async def main():
    # setup contants
    APP_NAME = 'Meeting Reminder Agent'
    USER_ID = 'anilkumar'

    # check for existing session
    exiting_session = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # if there's an existing session, use it, otherwise create a new one
    if exiting_session and len(exiting_session.sessions) > 0:
        # use recent session
        session = exiting_session.sessions[0]
        print("Using existing session with ID:", session.id)
    else:
        # create a new session
        session : Session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )

        print("Session created with ID:", session.id)

    # create a runner
    runner= Runner(
        agent = memory_agent, #2  meetingReminder,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # interactive conversation loop
    print("You can start asking about meeting reminders. Type 'exit' to quit.")

    while True:
        # get user input
        user_input = input("You: ")

        # check if user wants to exit
        if user_input:
            if user_input.lower() == 'exit':
                print("Exiting the meeting reminder agent. Goodbye!")
                break

            # call the agent asynchronously
            try:
                await call_agent_async(
                    runner=runner,
                    session_id=session.id,
                    user_input=user_input,
                    user_id=USER_ID
                )
            except Exception as e:
                print(f"Error during agent : {e}")
    

if __name__ == "__main__":
    asyncio.run(main())