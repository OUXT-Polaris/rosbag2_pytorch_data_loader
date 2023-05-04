import torch
import clip
from PIL import Image
from rosbag2_pytorch_data_loader.automation.automation import Automation
from typing import Any
from rosbag2_pytorch_data_loader.dataset.rosbag2_pytorch_dataset import Rosbag2Dataset
from rosbag2_pytorch_data_loader.automation.task_description import (
    ClipImageFilterConfig,
)
import torchvision.transforms as transforms
from torch.utils.data import DataLoader


class ClipImageFilter(Automation):  # type: ignore
    def __init__(self, yaml_path: str) -> None:
        self.config = ClipImageFilterConfig.from_yaml_file(yaml_path)
        print(self.config)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(
            self.config.clip_model_type, device=self.device
        )
        self.transform = transforms.ToPILImage()

    def inference(self, dataset: Rosbag2Dataset) -> Any:
        for index, image in enumerate(dataset):
            image = self.preprocess(self.transform(image)).unsqueeze(0).to(self.device)
            for object_index, prompt in enumerate(self.config.get_prompts()):
                text = clip.tokenize([prompt[0], prompt[1]]).to(self.device)
                with torch.no_grad():
                    image_features = self.model.encode_image(image)
                    text_features = self.model.encode_text(text)
                    logits_per_image, logits_per_text = self.model(image, text)
                    probs = logits_per_image.softmax(dim=-1).cpu().numpy()
                if probs[0][0] >= self.config.target_objects[object_index].threshold:
                    print("Index : " + str(index) + " , Score : " + str(probs[0][0]))
