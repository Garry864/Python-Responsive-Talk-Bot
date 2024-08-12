from Gemini_ivoker import *
from Voice_Initiator import *
from Text_parser import *

KEY = os.getenv('GOOGLE_API_KEY')

intro_1 = "Role: your name is Utkarsh. Your are a Examiner and ask verbal questions about the Subject. ask one question at a time and give honest and critical feedback to his answers . tell user to repeat if answer is unsatifactory or imcomplete"

intro_2 = "Hello I am Utkarsh Tell me your Name and subject"

bot = ChatBot(model="gemini-1.5-flash", temperature=0.3, google_api_key=KEY)

sys = bot.add_system_message(intro_1)
AI = bot.add_ai_message(intro_2)

print(AI)
talk(AI)
while True:
    prompt = receive_voice()

    if prompt:
        print("Voice input: " + prompt)
        bot.add_human_message(prompt)
        print('\n')

        if "end" in prompt or "bye" in prompt or "finish" in prompt:
            # print("Ending the program.")
            convo = bot.get_response()
            words = clean_text(convo)
            print("\nChatbot:\n" + convo + "\n")
            talk(words)
            sys.exit()

        response = bot.get_response()
        print("\nChatbot:\n" + response + "\n")
        words = clean_text(response)
        talk(words)