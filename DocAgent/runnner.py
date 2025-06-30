from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types
from uuid import uuid4
from dotenv import load_dotenv
from agent import docAgent
import asyncio


load_dotenv()
# Create a session service
session_service = InMemorySessionService()

APP_NAME = 'Doctor Bot'
USER_ID = 'anitkumar'
SESSION_ID = str(uuid4())

initial_state = {
    "user_name": "Anit Kumar",
    "user_preference": "doctor, health, medical advice. I want to provide accurate and helpful medical information to users.",
}

async def main():
    session: Session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
        session_id=SESSION_ID,
    )

    print("Session created with ID:", SESSION_ID)
    runner = Runner(
        agent=docAgent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    new_message = types.Content(
        role="user", parts=[
            types.Part(
                text="What are the best treatments for severe eczema and how should I handle a critical allergic reaction for someone with sensitive skin?"
            )
        ]
    )

    # Create a runner
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,

    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print("Final response:", event.content.parts[0].text)


    print("Runner finished.")
    print("==== Session Event Exploration ====")
    session_events = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("=== Final Session State ===")
    for key, value in session_events.state.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())