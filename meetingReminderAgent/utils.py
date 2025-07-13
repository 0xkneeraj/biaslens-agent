from google.genai import types
import traceback

# Dummy display_state function (replace with actual implementation or import if available)
def display_state(session_service, session_id, user_id, label):
    print(f"{label}: session_id={session_id}, user_id={user_id}")

# Define Colors class for terminal formatting if not already defined elsewhere
class Colors:
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'
    BG_CYAN = '\033[46m'
    BG_RED = '\033[41m'
    FG_WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

async def process_agent_response(event):
    """ Process the agent's response event."""
    print(f"Event ID: {event.id}, Author: {event.author}")

    # check for specific parts first 
    has_specific_parts = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if  hasattr(part, 'executable_code') and part.executable_code:
                # Access the actual code string via .code 
                print(
                    f" DEBUG: Agent generated code: \n ```python\n{part.code_executable_code.CODE}\n```"
                )
                has_specific_parts = True
            elif hasattr(part, "code_excutable_result") and part.code_executable_result:
                # Access the actual code result string via .code_excutable_result
                print(
                    f" DEBUG: Agent generated code result: {part.code_excutable_result.outcome}"
                )
                has_specific_parts = True
            elif hasattr(part, "function_call") and part.function_call:
                print(f" DEBUG: Agent generated function call: {part.function_call}")
                
            elif hasattr(part, "tool-response") and part.tool_response:
                # print the tool response
                print(
                    f" DEBUG: Agent generated tool response: {part.tool_response.output}"
                )
            elif hasattr(part, "text") and part.text and not part.text.isspace():
                # print the text part
                print(f" DEBUG: Agent generated text: {part.text.strip()}")
    # check for final response after specific parts
    final_response = None
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
        ):
            final_response = event.content.parts[0].text.strip()
            # use colors for formatting ot make the final response stand out
            print(
                f"\n{Colors.BG_BLUE}{Colors.FG_WHITE}{Colors.BOLD}===== Agent Response====={Colors.END}"
            )
            print(
                f"\n{Colors.BG_CYAN}{Colors.FG_WHITE}Final Response: {final_response}{Colors.END}"
            )
        else:
            print(
                f"\n{Colors.BG_RED}{Colors.FG_WHITE}No final response text found.{Colors.END}"
            )
async def call_agent_async(runner, session_id, user_input, user_id):
    """ Call the agent asynchronously and process the response."""
    content = types.Content(role="user", parts=[types.Part(text=user_input)])

    print(
        f"\n{Colors.BG_GREEN}{Colors.FG_WHITE}User Input: {user_input}{Colors.END}"
    )
    final_response_text = None

    # Display state before processing
    display_state(
        runner.session_service,
        session_id,
        user_id,
        "STATE BEFORE PROCESSING",
    )

    try:
        async for event in runner.run_async(
            user_id = user_id, session_id=session_id, new_message=content
        ):
            # Process the event
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"Error during agent processing: {e}")
        traceback.print_exc()


    # Display state after processing
    display_state(
        runner.session_service,
        session_id,
        user_id,
        "STATE AFTER PROCESSING",
    )

    return final_response_text