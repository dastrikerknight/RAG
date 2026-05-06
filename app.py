import gradio as gr
from rag import ask

def chat_fn(message, history):
    answer, docs = ask(message)

    sources = "\n\n---\n**Sources:**\n"
    for i, d in enumerate(docs):
        sources += f"\n{i+1}. {d[:200]}..."

    return answer + sources

demo = gr.ChatInterface(
    fn=chat_fn,
    title="Gemini RAG Chat",
    description="Ask questions based on custom documents",
)

demo.launch()