import os
from typing import Optional, Tuple

import gradio as gr
import pickle
from query_data import get_chain
from threading import Lock
from elevenlabs import set_api_key
import openai
import whisper

set_api_key('Enter your ElevenLabs API Key: ')
openai.api_key = "Your_API_KEY_HERE"



model = whisper.load_model("base")
from typing import Optional


class Chat:

    def __init__(self, system: Optional[str] = None):
        self.system = system
        self.messages = []
        
        if system is not None:
            self.messages.append({
                "role": "system",
                "content": system
            })

    def prompt(self, content: str) -> str:
          self.messages.append({
              "role": "user",
              "content": content
          })
          response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=self.messages
          )
          response_content = response["choices"][0]["message"]["content"]
          self.messages.append({
              "role": "assistant",
              "content": response_content
          })
          return response_content
from elevenlabs import generate, play


chat = Chat(system="You have to take Interview for the rust programming language ask questions one by one." )


def run_text_prompt(message, chat_history):
    bot_message = chat.prompt(content=message)

    audio = generate(
        text=bot_message,
        voice="Bella"
    )

    play(audio, notebook=True)

    chat_history.append((message, bot_message))
    return "", chat_history


def run_audio_prompt(audio, chat_history):
    if audio is None:
        return None, chat_history

    message_transcription = model.transcribe(audio)["text"]
    _, chat_history = run_text_prompt(message_transcription, chat_history)
    return None, chat_history


with gr.Blocks() as app2:
    chatbot = gr.Chatbot()

    msg = gr.Textbox()
    msg.submit(run_text_prompt, [msg, chatbot], [msg, chatbot])

    with gr.Row():
        audio = gr.Audio(source="microphone", type="filepath")

        send_audio_button = gr.Button("Send Audio", interactive=True)
        send_audio_button.click(run_audio_prompt, [audio, chatbot], [audio, chatbot])

with open("vectorstore.pkl", "rb") as f:
    vectorstore = pickle.load(f)


def set_openai_api_key(api_key: str):
    """Set the api key and return chain.
    If no api_key, then None is returned.
    """
    if api_key:
        os.environ["OPENAI_API_KEY"] = "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"
        chain = get_chain(vectorstore)
        os.environ["OPENAI_API_KEY"] = "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"
        return chain

class ChatWrapper:


    def __init__(self, system: Optional[str] = None):
        self.system = system
        self.messages = []
        if system is not None:
            self.messages.append({
                "role": "system",
                "content": system
            })
        self.lock = Lock()
    def prompt(self, content: str) -> str:
          self.messages.append({
              "role": "user",
              "content": content
          })
          response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=self.messages
          )
          response_content = response["choices"][0]["message"]["content"]
          self.messages.append({
              "role": "assistant",
              "content": response_content
          })
          return response_content
    def __call__(
        self, api_key: str, inp: str, history: Optional[Tuple[str, str]], chain
    ):
        """Execute the chat functionality."""
        self.lock.acquire()
        try:
            history = history or []
            # If chain is None, that is because no API key was provided.
            if chain is None:
                history.append((inp, "Please paste your OpenAI key to use"))
                return history, history
            # Set OpenAI key
            import openai
            openai.api_key = api_key
            # Run chain and append input.
            output = chain({"question": inp, "chat_history": history})["answer"]
            history.append((inp, output))
        except Exception as e:
            raise e
        finally:
            self.lock.release()
        return history, history

chat = ChatWrapper()

block = gr.Blocks(css=".gradio-container {background-color: lightgray}")

with block as app1:
    with gr.Row():
        gr.Markdown("<h3><center>Get List of PHD Titles</center></h3>")
        openai_api_key_textbox = gr.Textbox(
            placeholder="Paste your OpenAI API key (sk-...)",
            show_label=False,
            lines=1,
            type="password",
        )

    chatbot = gr.Chatbot()

    with gr.Row():
        message = gr.Textbox(
            label="What's your question?",
            placeholder="List your question here",
            lines=1,
        )
        submit = gr.Button(value="Send", variant="secondary").style(full_width=False)

    gr.Examples(
        examples=[
        ],
        inputs=message,
    )
    state = gr.State()
    agent_state = gr.State()

    submit.click(chat, inputs=[openai_api_key_textbox, message, state, agent_state], outputs=[chatbot, state])
    message.submit(chat, inputs=[openai_api_key_textbox, message, state, agent_state], outputs=[chatbot, state])

    openai_api_key_textbox.change(
        set_openai_api_key,
        inputs=[openai_api_key_textbox],
        outputs=[agent_state],
    )

# block.launch(debug=True)

demo = gr.TabbedInterface([app1,app2], ["Welcome","Chatbot"])

demo.launch()
