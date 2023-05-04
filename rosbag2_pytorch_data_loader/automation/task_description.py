from dataclasses import dataclass, field
from dataclass_wizard import YAMLWizard
from rosbag2_pytorch_data_loader.exception import TaskDescriptionError
from enum import Enum


class ClipModelType(Enum):
    RN50 = "RN50"
    RN101 = "RN101"
    RN50x4 = "RN50x4"
    RN50x16 = "RN50x16"
    RN50x64 = "RN50x64"
    ViT_B_32 = "ViT-B/32"
    ViT_B_16 = "ViT-B/16"
    ViT_L_14 = "ViT-L/14"
    ViT_L_14_at_336px = "ViT-L/14@336px"


@dataclass
class TargetObjectsConfig(YAMLWizard):  # type: ignore
    label: str = ""
    threshold: float = 0.5
    positive_prompt_prefix = "A photo of "
    negative_prompt_prefix = "Not a photo of"


@dataclass
class ClipImageFilterConfig(YAMLWizard):  # type: ignore
    dataset_type: str = "clip_image_filter"
    clip_model_type: ClipModelType = "ViT-B/32"  # type: ignore
    target_objects: list[TargetObjectsConfig] = field(default_factory=list)

    def get_prompts(self) -> list[tuple[str, str]]:
        prompts = []
        for target_object in self.target_objects:
            prompts.append(
                (
                    target_object.positive_prompt_prefix + target_object.label,
                    target_object.negative_prompt_prefix + target_object.label,
                )
            )
        return prompts
