# OpenVoice Docker Container

This Docker container provides an easy way to use OpenVoice for voice processing and feature extraction.

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and start the API server:**
   ```bash
   docker compose up --build
   ```

2. **Create input/output directories:**
   ```bash
   mkdir -p inputs outputs
   ```

3. **Place your MP3 file in the inputs directory:**
   ```bash
   cp your_voice_file.mp3 inputs/
   ```

4. **Use the CLI to process the file:**
   ```bash
   docker compose --profile cli run --rm openvoice-cli python process_voice.py inputs/your_voice_file.mp3 --output-dir outputs
   ```

5. **Find your output file:**
   ```bash
   ls outputs/
   # You should see voice.pt
   ```

### Option 2: Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t openvoice .
   ```

2. **Run with volume mounts:**
   ```bash
   docker run -v $(pwd)/inputs:/app/inputs -v $(pwd)/outputs:/app/outputs openvoice inputs/your_voice_file.mp3 --output-dir outputs
   ```

## API Usage

The container also provides a REST API for processing voice files:

### Start the API server:
```bash
docker compose up --build
```

### API Endpoints:

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Process voice file from URL:**
   ```bash
   curl -X POST "http://localhost:8000/process-voice-url" \
        -H "Content-Type: application/json" \
        -d '{"url": "https://example.com/voice.mp3"}' \
        --output voice.pt
   ```

3. **Upload and process voice file:**
   ```bash
   curl -X POST "http://localhost:8000/process-voice" \
        -F "file=@your_voice_file.mp3" \
        --output voice.pt
   ```

## Examples

### Process a local file:
```bash
# Copy your file to inputs directory
cp /path/to/your/voice.mp3 inputs/

# Process it
docker compose --profile cli run --rm openvoice-cli python process_voice.py inputs/voice.mp3 --output-dir outputs

# Check the result
ls -la outputs/voice.pt
```

### Process a file from URL:
```bash
# Using the API
curl -X POST "http://localhost:8000/process-voice-url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/sample.mp3"}' \
     --output voice.pt
```

### Use CUDA (if available):
```bash
docker run --gpus all -v $(pwd)/inputs:/app/inputs -v $(pwd)/outputs:/app/outputs openvoice inputs/voice.mp3 --output-dir outputs --device cuda
```

## File Structure

```
.
├── inputs/          # Place your input MP3 files here
├── outputs/         # Processed voice.pt files will appear here
├── Dockerfile       # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt # Python dependencies
├── process_voice.py # Main processing script
└── api.py          # REST API wrapper
```

## Requirements

- Docker
- Docker Compose (for easier usage)
- At least 4GB RAM
- MP3 audio files as input

## Troubleshooting

### Common Issues:

1. **Out of memory errors:**
   - Increase Docker memory limit
   - Use CPU-only mode: `--device cpu`

2. **File not found errors:**
   - Ensure your input file is in the `inputs/` directory
   - Check file permissions

3. **Model loading errors:**
   - Ensure all checkpoint files are present in `checkpoints_v2/`
   - Check that the container has access to all required files

### Debug Mode:
```bash
# Run with interactive shell for debugging
docker-compose --profile cli run --rm openvoice-cli /bin/bash
```

## Advanced Usage

### Custom Output Directory:
```bash
docker run -v $(pwd)/inputs:/app/inputs -v $(pwd)/custom_output:/app/custom_output openvoice inputs/voice.mp3 --output-dir custom_output
```

### Batch Processing:
```bash
# Process multiple files
for file in inputs/*.mp3; do
    docker-compose --profile cli run --rm openvoice-cli python process_voice.py "$file" --output-dir outputs
done
```

### GPU Support:
To use GPU acceleration, ensure you have NVIDIA Docker runtime installed:
```bash
docker run --gpus all -v $(pwd)/inputs:/app/inputs -v $(pwd)/outputs:/app/outputs openvoice inputs/voice.mp3 --output-dir outputs --device cuda
```

## License

This project is based on OpenVoice, which is MIT licensed. See the main README.md for more details. 