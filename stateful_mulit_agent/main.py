import asyncio

from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from customer_service_agent.agent import customer_service_agent
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

# Initialize session service
session_service = InMemorySessionService()

# define initial state

initial_state = {
    "user_name" : "Anil Kumar",
    "purchased_history": [],
    "interaction_history": []
}

# main function to run the agent
async def main():
    # setup content
    APP_NAME = "Customer Service Agent"
    USER_ID = "anil_kumar_123"

    # session creation
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )

    SESSION_ID = new_session.id
    print(f"Session created with ID: {SESSION_ID}")

    # Agent Runner setup

    runner = Runner(
        agent=customer_service_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # interactive conversation loop

    print("Welcome to the Customer Service Agent. Type 'exit' to end the conversation.")

    while True:
        # get user input
        user_input = input("You: ")
        # check if user wants to exit
        if user_input.lower() == 'exit' or "exit" in user_input.lower():
            print("Ending conversation. Goodbye!")
            break

        # add user query to history
        add_user_query_to_history(
            session_service, APP_NAME, SESSION_ID, USER_ID, user_input
        )

        # process the user input through the agent

        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    
    # state examination
    # show final session state
    final_session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    print("Final session state:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    """Entry point for the application."""
    asyncio.run(main())