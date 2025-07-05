#!/bin/bash

# OpenVoice Docker Runner Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "OpenVoice Docker Runner"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  build          Build the Docker image"
    echo "  start          Start the API server"
    echo "  stop           Stop the API server"
    echo "  restart        Restart the API server"
    echo "  process FILE   Process a single voice file"
    echo "  process-url URL Process a voice file from URL"
    echo "  shell          Open a shell in the container"
    echo "  logs           Show container logs"
    echo "  clean          Clean up containers and images"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 start"
    echo "  $0 process inputs/my_voice.mp3"
    echo "  $0 process-url https://example.com/voice.mp3"
    echo ""
}

# Function to create directories
create_directories() {
    print_status "Creating input/output directories..."
    mkdir -p inputs outputs
}

# Function to build the image
build_image() {
    print_status "Building OpenVoice Docker image..."
    docker compose build
    print_status "Build completed successfully!"
}

# Function to start the API server
start_server() {
    print_status "Starting OpenVoice API server..."
    create_directories
    docker compose up -d
    print_status "API server started on http://localhost:8000"
    print_status "Use '$0 logs' to view logs"
}

# Function to stop the server
stop_server() {
    print_status "Stopping OpenVoice API server..."
    docker compose down
    print_status "Server stopped"
}

# Function to restart the server
restart_server() {
    stop_server
    start_server
}

# Function to process a file
process_file() {
    if [ -z "$1" ]; then
        print_error "No file specified"
        echo "Usage: $0 process <file>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "File not found: $1"
        exit 1
    fi
    
    create_directories
    
    # Copy file to inputs directory
    filename=$(basename "$1")
    cp "$1" "inputs/$filename"
    
    print_status "Processing file: $filename"
    docker compose --profile cli run --rm openvoice-cli python process_voice.py "inputs/$filename" --output-dir outputs
    
    if [ -f "outputs/voice.pt" ]; then
        print_status "Processing completed! Output saved to: outputs/voice.pt"
    else
        print_error "Processing failed - no output file generated"
        exit 1
    fi
}

# Function to process from URL
process_url() {
    if [ -z "$1" ]; then
        print_error "No URL specified"
        echo "Usage: $0 process-url <url>"
        exit 1
    fi
    
    print_status "Processing voice from URL: $1"
    
    # Check if server is running
    if ! docker compose ps | grep -q "openvoice-container.*Up"; then
        print_warning "API server not running. Starting it..."
        start_server
        sleep 5
    fi
    
    # Process the URL
    response=$(curl -s -X POST "http://localhost:8000/process-voice-url" \
        -H "Content-Type: application/json" \
        -d "{\"url\": \"$1\"}" \
        --output "outputs/voice.pt" \
        --write-out "%{http_code}")
    
    if [ "$response" = "200" ]; then
        print_status "Processing completed! Output saved to: outputs/voice.pt"
    else
        print_error "Processing failed with HTTP code: $response"
        exit 1
    fi
}

# Function to open shell
open_shell() {
    print_status "Opening shell in OpenVoice container..."
    docker compose --profile cli run --rm openvoice-cli /bin/bash
}

# Function to show logs
show_logs() {
    print_status "Showing container logs..."
    docker compose logs -f
}

# Function to clean up
clean_up() {
    print_warning "This will remove all containers and images. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "Cleaning up..."
        docker compose down --rmi all --volumes --remove-orphans
        docker system prune -f
        print_status "Cleanup completed"
    else
        print_status "Cleanup cancelled"
    fi
}

# Main script logic
case "${1:-}" in
    build)
        build_image
        ;;
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    process)
        process_file "$2"
        ;;
    process-url)
        process_url "$2"
        ;;
    shell)
        open_shell
        ;;
    logs)
        show_logs
        ;;
    clean)
        clean_up
        ;;
    *)
        show_usage
        exit 1
        ;;
esac 