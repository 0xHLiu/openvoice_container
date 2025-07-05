import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

## Constants
ckpt_converter = 'checkpoints_v2/converter'
device = "cpu" #"cuda:0" if torch.cuda.is_available() else "cpu"
output_dir = 'outputs_v2'

## Inputs
input_voice = 'example/example_reference.mp3' # This is the voice you want to clone

## Load models
tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

reference_speaker = input_voice 
target_se, _ = se_extractor.get_se(reference_speaker, tone_color_converter, vad=True)

torch.save(target_se, f'{output_dir}/voice.pt')
print("Successfully saved voice features")