# AI Thinking Process Narrator

A unique tool that combines Groq's LLM capabilities with OpenAI's Text-to-Speech to create an audible, stream-of-consciousness experience of an AI's thinking process, complete with creative tangents and unexpected connections. The tool specifically focuses on narrating the AI's thought process, intentionally ignoring the final response to maintain the stream-of-consciousness experience.

## Features

- 🎭 **Styled Thinking**: Customizable thinking styles (e.g., jovial, analytical, stuttering)
- 🌀 **Creative Tangents**: Explores unexpected connections and parallel concepts
- 🗣️ **Real-time Audio Narration**: Converts thoughts to speech as they're generated
- 📝 **Streaming Text Output**: Visual representation of thoughts in real-time
- 🔄 **Continuous Exploration**: Multiple iterations of increasingly creative connections
- 🎯 **Process-Focused**: Only narrates the thinking process, not the final answer
- ⌨️ **Interrupt Handling**: Clean exit with Ctrl+C
- 🧹 **Automatic Cleanup**: Temporary audio files are removed after execution

## ❤️ Join my AI community & Get 400+ AI Projects

This is one of 400+ fascinating projects in my collection! [Support me on Patreon](https://www.patreon.com/c/echohive42/membership) to get:

- 🎯 Access to 400+ AI projects (and growing daily!)
  - Including advanced projects like [2 Agent Real-time voice template with turn taking](https://www.patreon.com/posts/2-agent-real-you-118330397)
- 📥 Full source code & detailed explanations
- 📚 1000x Cursor Course
- 🎓 Live coding sessions & AMAs
- 💬 1-on-1 consultations (higher tiers)
- 🎁 Exclusive discounts on AI tools & platforms (up to $180 value)

## Requirements

```plaintext
groq
openai
pygame
termcolor
```

## Environment Variables

The following environment variables need to be set:
- `GROQ_API_KEY`: Your Groq API key
- `OPENAI_API_KEY`: Your OpenAI API key

## Configuration

Key parameters at the top of the script:
```python
PROMPT = "Explain why the sky is blue, but think very short about it."
STYLE_OF_THINKING = "very jovial and fun and daydreaming like"
CONTINUOUS = True  # Enable creative tangent exploration
MAX_ITERATIONS = 3  # Maximum number of thinking iterations
VOICE_MODEL = "tts-1"
VOICE_NAME = "onyx"
```

## How It Works

1. **Initial Thinking**:
   - Processes the initial prompt with specified thinking style
   - Converts thoughts to speech in real-time
   - Only processes content between `<think>` tags
   - Stops processing when thinking ends (at `</think>` tag)

2. **Creative Tangents**:
   - Each iteration explores new connections like:
     - Metaphysical implications
     - Historical perspectives
     - Cultural connections
     - Scientific parallels
     - Artistic analogies
     - Psychological aspects
     - Philosophical considerations

3. **Audio Generation**:
   - Completed sentences trigger TTS conversion
   - Audio plays sequentially while new thoughts generate
   - Only thinking process is converted to speech
   - Final conclusions are shown but not narrated

4. **Continuous Exploration**:
   - Uses previous thoughts as springboards
   - Discovers unexpected connections
   - Maintains consistent thinking style
   - Each iteration only processes new thinking, not conclusions

## Important Note

This tool is designed to focus exclusively on the AI's thinking process. While the model will generate both thoughts and a final answer, only the content within the `<think>` tags is processed and narrated. This design choice emphasizes the stream-of-consciousness nature of the tool and allows users to focus on the journey rather than the destination.

## Example Tangents

Starting with "Why is the sky blue?", the AI might explore:
- Connection to human perception and color psychology
- Cultural significance of the color blue across civilizations
- Parallel with ocean depths and spatial perception
- Musical analogies about frequency and wavelength
- Philosophical implications about reality vs. perception

## Usage

1. Set up environment variables:
```bash
export GROQ_API_KEY='your-groq-key'
export OPENAI_API_KEY='your-openai-key'
```

2. Run the script:
```bash
python deepseek_groq_audio_thoughts.py
```

3. Listen as the AI explores your prompt through multiple creative angles!

## Customization

- Modify `STYLE_OF_THINKING` for different thinking personalities
- Adjust `MAX_ITERATIONS` for more or fewer tangents
- Change `VOICE_NAME` to alter the narrator's voice
- Edit `PROMPT` to explore different topics

## Error Handling

- Graceful handling of API errors
- Clean termination with Ctrl+C
- Automatic cleanup of temporary files
- Informative error messages with color coding

## Notes

- Audio files are temporarily stored in system temp directory
- All files are cleaned up after execution
- The system uses streaming for both text and audio
- Memory efficient with queue-based audio processing
- Each iteration builds creatively on previous thoughts

## Dependencies

- Groq: For LLM capabilities
- OpenAI: For text-to-speech conversion
- Pygame: For audio playback
- Termcolor: For colored terminal output

## License

MIT License 
