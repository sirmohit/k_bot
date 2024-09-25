import streamlit as st
from chat import extract_text_from_pdf, get_text_chunks_and_metadata, get_vector_store, get_answer, load_chat_history, save_chat_history,clear_chat_history
import base64

# Streamlit chatbot UI
def main():
    clear_chat_history()  # Clear the chat history at the start of each session
    
    hardcoded_file_path = "Gen_Q.pdf"
    
    # Extract text from PDF and create vector store
    all_texts = extract_text_from_pdf(hardcoded_file_path)
    chunks_metadata = get_text_chunks_and_metadata(all_texts)
    get_vector_store(chunks_metadata)

# Initialize session state
if 'session_chat' not in st.session_state:
    st.session_state.session_chat = []

if 'user_question' not in st.session_state:
    st.session_state.user_question = ""

if 'welcome_message_shown' not in st.session_state:
    st.session_state.welcome_message_shown = False

# Handle user input and generate chatbot response
def user_input():
    user_question = st.session_state.user_question
    answer_text = get_answer(user_question)

    chat_entry = {
        "question": user_question,
        "answer": answer_text
    }

    st.session_state.session_chat.append(chat_entry)
    st.session_state.user_question = ""

    save_chat_history(st.session_state.session_chat)

    # Hide the welcome message once the user asks a question
    st.session_state.welcome_message_shown = True

# Helper function to get the base64 encoding of the image
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Use the image file
image_base64 = get_base64_image("genilogo.jpg")

st.markdown(f"""
    <style>
    .chat-message {{ margin-bottom: 10px; padding: 10px; border-radius: 10px; background-color: #e0e0e0; clear: both; max-width: 80%; display: flex; align-items: center; }}
    .chat-message.question {{ align-self: flex-end; background-color: #1d3557; color: white; float: right; text-align: right; margin-left: auto; }}
    .chat-message.answer {{ align-self: flex-start; background-color: #262730; color: white; float: left; text-align: left; margin-right: auto; display: flex; align-items: center; }}
    .container {{ display: flex; flex-direction: column-reverse; }}
    .stTextInput {{ position: fixed; bottom: 0.1rem; padding: 0px; border-radius: 0px; max-width: 902px; right: 40%; left: 26%; }}
    
    /* Fix the bot name and logo */
    .fixed-header-container {{
        position: fixed;
        top: 60px;
        left: 400px;
        z-index: 1000;
        width: 1000px; 
        height: 70px; 
        background-color: black;
    }}
    
    .fixed-header {{
        position: absolute;
        top: -10px;
        left: 85px;
        color: white;
    }}
    .fixed-logo {{
        position: absolute;
        top: 10px;
        left: 0px;
        width: 70px;
        height: 60px;
    }}

    /* Style for inline logo in responses */
    .inline-logo {{
        margin-right: 10px;
        width: 40px;
        height: 40px;
    }}
    .chat-container, .welcome-message {{
        margin-top: 100px;  
    }}
    </style>
    
    <!-- Bot name and logo container -->
    <div class="fixed-header-container">
        <img src="data:image/jpeg;base64,{image_base64}" class="fixed-logo">
        <h1 class="fixed-header">GENIBOT</h1>
    </div>
    """, unsafe_allow_html=True)

# Display the welcome message
if not st.session_state.welcome_message_shown:
     st.markdown("<div class='chat-message answer welcome-message'>🎉🎉 Hi, welcome to Genillect Assistant. How can I help you 🎉🎉</div>", unsafe_allow_html=True)

# Add margin to the chat container to avoid overlap
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Display chat history with logo before each answer
    for chat in st.session_state.session_chat:
        st.markdown(f'<div class="chat-message question">{chat["question"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-message answer"><img src="data:image/jpeg;base64,{image_base64}" class="inline-logo">{chat["answer"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# User input field
st.text_input(" ", key="user_question", on_change=user_input, placeholder="Ask your question here...")

if __name__ == "__main__":
    main()






# def main():
    
#     #st.set_page_config(page_title="GENIBOT", page_icon="genilogo.jpg", layout="centered")

#     hardcoded_file_path = "Gen_Q.pdf"
    
#     # Extract text from PDF and create vector store
#     all_texts = extract_text_from_pdf(hardcoded_file_path)
#     chunks_metadata = get_text_chunks_and_metadata(all_texts)
#     get_vector_store(chunks_metadata)

# CHAT_HISTORY_FILE = "chat_history.json"

# #Initialize session state for chat
# if 'session_chat' not in st.session_state:
#     st.session_state.session_chat = load_chat_history()

# if 'user_question' not in st.session_state:
#     st.session_state.user_question = ""

# # if 'welcome_message_shown' not in st.session_state:
# #     st.session_state.welcome_message_shown = False


# #Handle user input and generate chatbot response
# def user_input():
#     user_question = st.session_state.user_question
#     answer_text = get_answer(user_question)

#     chat_entry = {
#         "question": user_question,
#         "answer": answer_text
#     }
    
#     st.session_state.session_chat.append(chat_entry)
#     save_chat_history(st.session_state.session_chat)  # Save chat history
#     st.session_state.user_question = ""  # Reset input after response
    
#     # Check if the system was unable to provide an answer
#     # if not answer_text or "Sorry, I don't have the information you're looking for. Please contact our team for further assistance via phone at +91 9263283565 or email at Genillect@gmail.com." in answer_text:
#     #     answer_text = "Sorry, I don't have the information you're looking for. Please contact our team for further assistance via phone at +91 9263283565 or email at Genillect@gmail.com."
        
#     # chat_entry = {
#     #     "question": user_question,
#     #     "answer": answer_text
#     # }
#     # st.session_state.session_chat.append(chat_entry)
#     # st.session_state.user_question = "" 


# st.markdown("""
#     <style>
#     .chat-message { margin-bottom: 10px; padding: 10px; border-radius: 10px; background-color: #e0e0e0; clear: both; max-width: 80%; }
#     .chat-message.question { align-self: flex-end; background-color: #1d3557; color: white; float: right; text-align: right; margin-left: auto; }
#     .chat-message.answer { align-self: flex-start; background-color: #262730; color: white; float: left; text-align: left; margin-right: auto; }
#     .container { display: flex; flex-direction: column-reverse; }
#     .stTextInput {position: fixed;bottom: 1rem;padding: 0px;border-radius: 0px; max-width: 902px;  right: 40%; left: 26%; }  
#     </style>
#     <h1 style='text-align: left; margin-top: 10px; margin-left: 65px; color: white;'>GENIBOT</h1>
#     """, unsafe_allow_html=True)

#     # Function to load base64 logo
# def get_base64_image(genilogo):
#         with open('genilogo.jpg', "rb") as img_file:
#             return base64.b64encode(img_file.read()).decode()

# image_base64 = get_base64_image("genilogo.jpg")
# st.markdown(f'''
#     <style>
#         .logo {{
#             position:absolute;
#             margin-top: -55px;
#             margin-left: -15px;
#             width: 70px;
#             height: 60px;
#         }}
#     </style>
#     <img src="data:image/jpeg;base64,{image_base64}" class="logo">
#     ''', unsafe_allow_html=True)

# # Display chat history
# chat_container = st.container()
# for chat in st.session_state.session_chat:
#         with chat_container:
#             st.markdown(f'<div class="chat-message question">{chat["question"]}</div>', unsafe_allow_html=True)
#             st.markdown(f'<div class="chat-message answer">{chat["answer"]}</div>', unsafe_allow_html=True)

# #User input 
# st.text_input(" ", key="user_question",on_change=user_input, placeholder="Welcome to Genillect")

# if __name__ == "__main__":
#     main()











