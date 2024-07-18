import gradio as gr
from main import classify_songs_and_create_playlists


def format_playlist_info(playlists):
    return "\n".join([f"- {name}: {count} tracks" for name, count, _ in playlists])


def create_playlists_ui(num_playlists, progress=gr.Progress()):
    try:
        result, playlists = classify_songs_and_create_playlists(num_playlists)
        return result, format_playlist_info(playlists), [img for _, _, img in playlists]
    except Exception as e:
        return f"An error occurred: {e}", "", []


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
        create_playlists_ui,
        inputs=[num_playlists],
        outputs=[output_text, playlist_info, gallery]
    )

if __name__ == "__main__":
    iface.launch()
