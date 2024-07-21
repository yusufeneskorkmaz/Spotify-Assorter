import gradio as gr
from main import classify_songs_and_create_playlists
import asyncio
import traceback

def format_playlist_info(playlists):
    return "\n".join([f"- {name}: {count} tracks" for name, count, _ in playlists])

async def create_playlists_ui(num_playlists, progress=gr.Progress()):
    try:
        result, playlists = await classify_songs_and_create_playlists(num_playlists)
        return result, format_playlist_info(playlists), [img for _, _, img in playlists]
    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return error_message, "", []

with gr.Blocks(theme=gr.themes.Soft()) as iface:
    gr.Markdown(
        """
        # 🎵 Spotify Genre Classifier and Playlist Creator

        This tool analyzes your liked songs on Spotify, classifies them by genre, and creates playlists based on the top genres.
        """
    )

    with gr.Row():
        num_playlists = gr.Slider(minimum=1, maximum=10, step=1, value=5, label="Number of Playlists to Create")
        create_button = gr.Button("Create Playlists", variant="primary")

    with gr.Row():
        output_text = gr.Textbox(label="Status", lines=2)
        playlist_info = gr.Textbox(label="Created Playlists", lines=5)

    gallery = gr.Gallery(label="Playlist Cover Images", show_label=True, elem_id="gallery")

    create_button.click(
        lambda num: asyncio.run(create_playlists_ui(num)),
        inputs=[num_playlists],
        outputs=[output_text, playlist_info, gallery]
    )

if __name__ == "__main__":
    iface.launch(server_port=8080)