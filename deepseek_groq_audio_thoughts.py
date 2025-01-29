import os
import asyncio
import queue
import threading
import re
from termcolor import cprint
from groq import Groq
from openai import OpenAI
import pygame
import signal
import tempfile
from pathlib import Path
import sys

# Constants
MODEL_NAME = "deepseek-r1-distill-llama-70b"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOICE_MODEL = "tts-1"
VOICE_NAME = "onyx"
PROMPT = "why is the sky blue?"
CONTINUOUS = True  # Enable continuous deeper thinking
MAX_ITERATIONS = 3  # Maximum number of thinking iterations

# Simple system message
SYSTEM_MESSAGE = """You are a helpful and fun assistant."""

# Continuous thinking prompt template
DEEPER_THINKING_PROMPT = """Based on your previous thoughts about {original_prompt}, let's explore some fascinating tangents and unexpected connections.

Feel free to:
- Draw surprising parallels to other fields or phenomena
- Consider metaphysical or philosophical implications
- Make creative analogies or metaphors
- Connect this to art, music, literature, or culture
- Explore historical or futuristic perspectives
- Think about how this relates to human psychology or behavior
- Consider paradoxes or counterintuitive aspects

Your previous thoughts were: {previous_thinking}

Now, take us on an interesting tangent or make an unexpected connection..."""

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize pygame mixer
pygame.mixer.init()

# Create a queue for audio files
audio_queue = queue.Queue()
should_stop = threading.Event()

def signal_handler(signum, frame):
    """Handle Ctrl+C"""
    cprint("\n⚠️ Stopping audio playback and cleanup...", "yellow")
    should_stop.set()
    pygame.mixer.quit()
    os._exit(0)  # Force exit the process

def generate_tts(text: str) -> Path:
    """Generate TTS audio file from text"""
    try:
        temp_dir = Path(tempfile.gettempdir())
        output_path = temp_dir / f"thought_{hash(text)}.mp3"
        
        if not output_path.exists():
            response = openai_client.audio.speech.create(
                model=VOICE_MODEL,
                voice=VOICE_NAME,
                input=text
            )
            # Fix for streaming warning - write bytes directly
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
        return output_path
    except Exception as e:
        cprint(f"\n⚠️ TTS Error: {str(e)}", "red")
        return None

def play_audio_worker():
    """Worker thread to play audio files from queue"""
    while not should_stop.is_set():
        try:
            audio_file = audio_queue.get(timeout=1)
            if audio_file and audio_file.exists():
                pygame.mixer.music.load(str(audio_file))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() and not should_stop.is_set():
                    pygame.time.Clock().tick(10)
            audio_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            cprint(f"\n⚠️ Audio Playback Error: {str(e)}", "red")

async def process_thinking(text: str):
    """Process thinking text and generate audio"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sentence in sentences:
        if sentence.strip() and not should_stop.is_set():
            audio_path = generate_tts(sentence)
            if audio_path:
                audio_queue.put(audio_path)

async def call_groq_with_audio(prompt: str, iteration: int = 1):
    """
    Calls the Groq API and generates audio for thinking process
    """
    audio_thread = None
    try:
        cprint(f"\n[{iteration}/{MAX_ITERATIONS if CONTINUOUS else 1}] 🔄 Calling Groq API... (Streaming with Audio)", "cyan")

        # Start audio player thread
        audio_thread = threading.Thread(target=play_audio_worker, daemon=True)
        audio_thread.start()

        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)

        # Print headers
        print("\n" + "-"*50)
        cprint(f"🤔 Thinking Process - Iteration {iteration}:", "yellow", attrs=['bold'])
        print("-"*50 + "\n")

        current_thinking = ""
        full_thinking = ""
        in_thinking_block = False

        # Make the API call with system message
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        for chunk in completion:
            if should_stop.is_set():
                break

            chunk_content = chunk.choices[0].delta.content or ""
            
            if "<think>" in chunk_content:
                in_thinking_block = True
                chunk_content = chunk_content.replace("<think>", "")
            elif "</think>" in chunk_content:
                in_thinking_block = False
                # Process any remaining thinking text
                if current_thinking:
                    await process_thinking(current_thinking)
                    full_thinking += current_thinking
                break  # Stop processing after thinking ends

            if in_thinking_block:
                cprint(chunk_content, 'yellow', end="", flush=True)
                current_thinking += chunk_content
                
                # Process complete sentences
                if any(punct in chunk_content for punct in '.!?'):
                    sentences = re.split(r'(?<=[.!?])\s+', current_thinking)
                    # Keep the last incomplete sentence
                    current_thinking = sentences[-1]
                    # Process complete sentences
                    for sentence in sentences[:-1]:
                        if sentence.strip():
                            await process_thinking(sentence)
                            full_thinking += sentence + " "

        # Wait for audio queue to be empty
        audio_queue.join()
        
        if CONTINUOUS and iteration < MAX_ITERATIONS and not should_stop.is_set():
            cprint("\n\n🔄 Preparing for deeper analysis...", "cyan")
            # Create prompt for deeper thinking
            deeper_prompt = DEEPER_THINKING_PROMPT.format(
                original_prompt=PROMPT,
                previous_thinking=full_thinking[-500:]  # Use last 500 chars as context
            )
            await call_groq_with_audio(deeper_prompt, iteration + 1)
        else:
            cprint("\n\n✅ Thinking process complete!", "green", attrs=['bold'])
            print("-"*50 + "\n")

    except Exception as e:
        cprint(f"\n⚠️ Error: {str(e)}", "red")
    finally:
        if iteration == MAX_ITERATIONS or not CONTINUOUS:
            should_stop.set()
            pygame.mixer.quit()
            if audio_thread and audio_thread.is_alive():
                audio_thread.join(timeout=1.0)
            # Force cleanup of any remaining temporary files
            try:
                temp_dir = Path(tempfile.gettempdir())
                for file in temp_dir.glob("thought_*.mp3"):
                    try:
                        file.unlink()
                    except:
                        pass
            except:
                pass

def main():
    """Main entry point with proper signal handling"""
    try:
        asyncio.run(test())
    except KeyboardInterrupt:
        cprint("\n\n⚠️ Interrupted by user. Cleaning up...", "yellow")
        should_stop.set()
        pygame.mixer.quit()
        os._exit(0)  # Force exit the process
    except Exception as e:
        cprint(f"\n⚠️ Unexpected error: {str(e)}", "red")
        os._exit(1)

if __name__ == "__main__":
    # Define the user prompt at the top for easy modification

    async def test():
        try:
            await call_groq_with_audio(PROMPT) # Use the PROMPT variable
        finally:
            # Ensure cleanup happens
            should_stop.set()
            pygame.mixer.quit()

    # Set up signal handlers before running
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    main() 
