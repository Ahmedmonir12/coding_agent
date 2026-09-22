from gradio.events import api
from agent import model_init,coder
import gradio as gr

WORKSPACE="workspace"
class ModelInterface:
    def __init__(self,api_key,base_url,model_name,reasoning="low") -> None:
        self.model=model_init(api_key,base_url)
        self.model_name=model_name
        self.reasoning=reasoning
    
    def message(self):
        sys_msg="""you are a coding agent.
        you modify the code according to the user request.
        before testing check if the required compiler is installed with run_command tool, if its not installed, you do not test it,
        and tell the user clearly that you changed the code but couldn't test it.
        if the compiler is installed you test after you modify the code with run command.
        if an error accures you inspect the error and fix it.
        you send the code that has been modified.
        keep your words simple and precise"""

        msg=[{"role":"system","content":sys_msg}]
        return msg 

    def chat(self,msg,history):
        history = [{"role": h["role"], "content": h["content"]} for h in history]
        messages=self.message()

        messages = messages + history + [{"role": "user", "content": msg}]
        response = coder(messages,self.model,self.model_name,self.reasoning)

        history.append({"role": "user", "content": msg})
        history.append({"role": "assistant", "content": response})

        return history

    def interface(self):
        

        with gr.Blocks() as app:

            with gr.Row():

                with gr.Column(scale=1):
                    gr.Markdown("Files")

                    files = gr.FileExplorer(
                        glob="**/*",
                        root_dir=WORKSPACE,
                        file_count="multiple",
                        label="Project"
                    )

                with gr.Column(scale=3):

                    chatbot = gr.Chatbot(
                        label="agent",
                        sanitize_html=False,
                        allow_tags=False,
                    )

                    message = gr.Textbox(
                        placeholder="type the file and the change you want in it"
                    )

                    send = gr.Button("send")

            send.click(
                self.chat,
                inputs=[message, chatbot],
                outputs=chatbot
            )

            message.submit(
                self.chat,
                inputs=[message, chatbot],
                outputs=chatbot
            )

        app.launch(inbrowser=True)

if __name__=="__main__":
    opj=ModelInterface(api_key="gmm",base_url="http://localhost:11434/v1",model_name="gemma4:e2b",reasoning="minimal")
    opj.interface()