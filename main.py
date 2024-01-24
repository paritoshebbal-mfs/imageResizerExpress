import streamlit as st
from PIL import Image
import io
import base64
from datetime import datetime

# Function to resize the image to a fixed height
def resize_image(image, target_height):
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height
    new_width = int(aspect_ratio * target_height)
    resized_image = image.resize((new_width, target_height))
    return resized_image, (original_width, original_height), (new_width, target_height)

# Function to generate a downloadable link for the image
def get_image_download_link(image, original_filename, text):
    date_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{original_filename}_resized_for_viva_{date_suffix}.png"

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    href = f'<a href="data:image/png;base64,{img_str}" download="{new_filename}">{text}</a>'
    return href

# Streamlit app
def main():
    st.title("Image Resizer App")

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        # Set the target height
        target_height = 390

        if st.button("Resize"):
            img = Image.open(uploaded_image)
            resized_image, original_size, new_size = resize_image(img, target_height)
            st.image(resized_image, caption="Resized Image", use_column_width=True, clamp=True)

            original_filename = uploaded_image.name.split(".")[0]
            download_link = get_image_download_link(resized_image, original_filename, "Download Resized Image")
            st.markdown(download_link, unsafe_allow_html=True)

            # Print sizes
            st.write(f"Original Image Size: {original_size}")
            st.write(f"Resized Image Size: {new_size}")

if __name__ == "__main__":
    main()
