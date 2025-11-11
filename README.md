# Legrand AI - 3D AI Assistant

A complete MVP of an interactive 3D AI Assistant powered by OpenAI's GPT technology and Three.js for 3D visualization.

## Features

- 🎨 **3D Avatar**: Interactive 3D character with animations and expressions
- 💬 **Chat Interface**: Modern, responsive chat UI for text-based interaction
- 🎤 **Voice Input**: Speech-to-text using Web Speech API
- 🔊 **Text-to-Speech**: AI responses can be spoken aloud
- 🤖 **AI Integration**: Powered by OpenAI's GPT-3.5-turbo for intelligent conversations
- ⚙️ **Customizable Settings**: Configurable API key, voice, and animation settings
- 🔒 **Privacy First**: API key stored locally in browser, never sent to our servers
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, or Edge)
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. Clone this repository or download the files:
   ```bash
   git clone https://github.com/MartynLegrand/Legrand_AI.git
   cd Legrand_AI
   ```

2. Open `index.html` in your web browser:
   - Double-click the file, or
   - Use a local server (recommended):
     ```bash
     # Python 3
     python -m http.server 8000
     
     # Node.js (with http-server)
     npx http-server
     ```

3. Visit `http://localhost:8000` in your browser

### Configuration

1. Click the settings icon (⚙️) in the bottom-right corner
2. Enter your OpenAI API key
3. Configure your preferences:
   - Enable/disable voice interaction
   - Enable/disable avatar animations

## Usage

### Text Chat
1. Type your message in the input field at the bottom of the chat
2. Press Enter or click the send button (➤)
3. The AI will respond with helpful information

### Voice Input
1. Click the microphone icon (🎤) in the chat header
2. Speak your message
3. The system will transcribe and send your message automatically

### Clear Chat
- Click the trash icon (🗑️) to clear the conversation history

## Project Structure

```
Legrand_AI/
├── index.html          # Main HTML file
├── styles.css          # Styling and animations
├── app.js             # Core application logic
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Technologies Used

- **Three.js**: 3D graphics and avatar rendering
- **OpenAI API**: GPT-3.5-turbo for conversational AI
- **Web Speech API**: Voice recognition and synthesis
- **Vanilla JavaScript**: No framework dependencies
- **CSS3**: Modern styling with gradients and animations

## Browser Compatibility

- ✅ Chrome/Edge (recommended) - Full support including voice features
- ✅ Firefox - Full support (voice features may vary)
- ✅ Safari - Full support (voice features may vary)
- ⚠️ Mobile browsers - Limited voice support

## Security & Privacy

- Your OpenAI API key is stored locally in your browser's localStorage
- No data is sent to any server except OpenAI's API
- Conversation history is kept in memory and cleared on page reload
- Open source and transparent - review the code yourself
- See [SECURITY.md](SECURITY.md) for detailed security information and best practices

## API Usage & Costs

This application uses the OpenAI API, which has associated costs:
- GPT-3.5-turbo is used by default (cost-effective)
- Typical conversation: ~$0.001-0.002 per message
- You control your spending by managing your API key usage

## Development

### Making Changes

1. Edit the files directly in your text editor
2. Refresh the browser to see changes
3. Use browser DevTools for debugging

### Customization Ideas

- Change avatar colors in `app.js` (search for color values like `0x7c3aed`)
- Modify the AI personality by editing the system prompt in `getAIResponse()`
- Adjust animation speeds in the `animate()` function
- Add new 3D elements to the avatar in `createAvatar()`

## Troubleshooting

### "API request failed" error
- Check that your API key is valid and has credits
- Verify your internet connection
- Check the browser console for detailed error messages

### Voice features not working
- Use Chrome or Edge for best voice support
- Check browser permissions for microphone access
- Ensure you're using HTTPS or localhost

### Avatar not displaying
- Check that Three.js loaded correctly (check browser console)
- Try refreshing the page
- Ensure JavaScript is enabled in your browser

## Future Enhancements

- [ ] Multiple avatar styles and customization options
- [ ] Export conversation history
- [ ] Context-aware responses based on user profile
- [ ] Integration with additional AI models
- [ ] Advanced gesture recognition
- [ ] Multi-language support
- [ ] Voice cloning for personalized responses

## Contributing

Contributions are welcome! Feel free to:
- Report bugs by opening an issue
- Suggest new features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Credits

Created by MartynLegrand
- Three.js for 3D graphics
- OpenAI for AI capabilities
- Web Speech API for voice features

## Support

For questions or issues:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the code comments for detailed explanations

---

**Note**: This is an MVP (Minimum Viable Product). It includes core functionality and can be extended with additional features based on user feedback and requirements.
