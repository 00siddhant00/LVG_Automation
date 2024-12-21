from moviepy.editor import VideoClip
import numpy as np
from PIL import Image
from PIL.Image import Resampling


class BackgroundAnimator:
    def __init__(self, image_path):
        """Initialize with path to background image."""
        # Load the image using PIL
        self.pil_image = Image.open(image_path).convert("RGBA")  # Ensure RGBA mode
        self.original_size = self.pil_image.size

    def animate_background(self, duration, amplitude=0.1, frequency=0.08):
        """Create a breathing animation effect matching audio duration."""
        w, h = self.original_size
        base_img = self.pil_image

        def make_frame(t):
            # Calculate scale factor using sine wave
            scale = 1 + amplitude * 0.5 * (1 + np.sin(2 * np.pi * frequency * t))

            # Calculate new dimensions
            new_w = int(w * scale)
            new_h = int(h * scale)

            # Resize using LANCZOS
            resized = base_img.resize((new_w, new_h), Resampling.LANCZOS)

            # Create a new image with original size and paste resized image in center
            result = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            x = (w - new_w) // 2
            y = (h - new_h) // 2
            result.paste(resized, (x, y))

            # Convert to numpy array and remove alpha channel (RGBA to RGB)
            frame = np.array(result)
            frame_rgb = frame[:, :, :3]  # Keep only RGB channels
            return frame_rgb

        # Use VideoClip for dynamic frame generation
        clip = VideoClip(make_frame, duration=duration)

        return clip