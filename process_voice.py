import torch
import argparse
import os
import sys
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

def process_voice(input_voice, output_dir='outputs_v2', device="cpu"):
    """
    Process a voice file and extract voice features
    
    Args:
        input_voice (str): Path to the input voice file
        output_dir (str): Directory to save the output
        device (str): Device to use for processing (cpu/cuda)
    """
    try:
        # Constants
        ckpt_converter = 'checkpoints_v2/converter'
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if input file exists
        if not os.path.exists(input_voice):
            raise FileNotFoundError(f"Input file not found: {input_voice}")
        
        print(f"Processing voice file: {input_voice}")
        print(f"Using device: {device}")
        
        # Load models
        print("Loading tone color converter...")
        tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
        tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')
        
        # Extract voice features
        print("Extracting voice features...")
        reference_speaker = input_voice 
        target_se, _ = se_extractor.get_se(reference_speaker, tone_color_converter, vad=True)
        
        # Save the voice features
        output_path = os.path.join(output_dir, 'voice.pt')
        torch.save(target_se, output_path)
        print(f"Successfully saved voice features to: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"Error processing voice: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Process voice file and extract voice features')
    parser.add_argument('input_voice', help='Path to the input voice file (MP3)')
    parser.add_argument('--output-dir', default='outputs_v2', help='Output directory (default: outputs_v2)')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'], help='Device to use (default: cpu)')
    
    args = parser.parse_args()
    
    # Use CUDA if available and requested
    if args.device == 'cuda' and torch.cuda.is_available():
        device = "cuda:0"
    else:
        device = "cpu"
    
    output_path = process_voice(args.input_voice, args.output_dir, device)
    print(f"Processing complete. Output saved to: {output_path}")

if __name__ == "__main__":
    main()