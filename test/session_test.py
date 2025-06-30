from google.adk.sessions import Session, InMemorySessionService

# create a session service
session_service = InMemorySessionService()
# create a session
session: Session = session_service.create_session(
    app_name='farmAGent',
    user_id='user123',
    state={
        'intial_key': 'initial_value',
    }
)

print("............ Examining session properties ............")
# print(f"Session ID: {session.id}")
print(f"App Name: {session.app_name}")
print(f"User ID: {session.user_id}")
print(f"State: {session.state}")
print(f"Events: {session.events}")
print(f"Last updated: {session.last_update.timestamp()}")