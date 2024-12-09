import gradio as gr
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline

# Initialize the object detection pipeline
object_detector = pipeline("object-detection",
                         model="facebook/detr-resnet-50")

def draw_bounding_boxes(image, detections, font_size=20):
    """
    Draws bounding boxes on the given image based on the detections.
    """
    # Make a copy of the image to draw on
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)

    # Use default font since custom font paths might not be available
    font = ImageFont.load_default()

    for detection in detections:
        box = detection['box']
        xmin = int(box['xmin'])
        ymin = int(box['ymin'])
        xmax = int(box['xmax'])
        ymax = int(box['ymax'])

        # Draw the bounding box
        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=3)

        # Create label with score
        label = detection['label']
        score = detection['score']
        text = f"{label} {score:.2f}"

        # Draw text with background rectangle for visibility
        text_bbox = draw.textbbox((xmin, ymin), text, font=font)
        draw.rectangle([
            (text_bbox[0], text_bbox[1]),
            (text_bbox[2], text_bbox[3])
        ], fill="red")
        draw.text((xmin, ymin), text, fill="white", font=font)

    return draw_image

def detect_object(image):
    if image is None:
        return None
    
    try:
        # Detect objects
        output = object_detector(image)
        
        # Draw bounding boxes
        processed_image = draw_bounding_boxes(image, output)
        return processed_image
    except Exception as e:
        print(f"Error during object detection: {str(e)}")
        return None

# Create the Gradio interface
demo = gr.Interface(
    fn=detect_object,
    inputs=[
        gr.Image(label="Upload Image", type="pil")
    ],
    outputs=[
        gr.Image(label="Detected Objects")
    ],
    title="Object Detection using image",
    description="Upload an image to detect and identify objects within it. The application will draw bounding boxes around detected objects and show their labels with confidence scores."
)

if __name__ == "__main__":
    demo.launch()
