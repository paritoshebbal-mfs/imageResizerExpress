import streamlit as st
from PIL import Image
import io
import base64

# Function to resize the image
def resize_image(image, size):
    return image.resize(size)

# Function to generate a downloadable link for the image
def get_image_download_link(image, filename, text):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")  # Save as PNG to support RGBA mode
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Streamlit app
def main():
    st.title("Image Resizer App")

    # Upload image through drag and drop
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Display the uploaded image
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        # Get user input for new size
        new_width = st.number_input("Enter the new width:", min_value=1)
        new_height = st.number_input("Enter the new height:", min_value=1)

        if st.button("Resize"):
            # Resize the image
            img = Image.open(uploaded_image)
            resized_image = resize_image(img, (new_width, new_height))

            # Display the resized image
            st.image(resized_image, caption="Resized Image", use_column_width=True, clamp=True)

            # Generate download link
            download_link = get_image_download_link(resized_image, "resized_image.png", "Download Resized Image")
            st.markdown(download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
