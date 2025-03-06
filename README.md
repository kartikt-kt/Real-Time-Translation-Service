# Real-Time Translation Service

A modern web application that provides real-time translation services across multiple languages. Built with Python (FastAPI) backend and a responsive HTML/JavaScript frontend, this application offers a seamless translation experience with a clean, user-friendly interface.

## Features

### Core Functionality
- Real-time translation to multiple languages simultaneously
- Support for 9 major languages including Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, and Chinese
- Progress tracking for translation tasks
- Translation history and status checking

### User Interface
- Clean, modern interface with Bootstrap styling
- Dark/Light theme toggle with persistent preference
- Responsive design that works on both desktop and mobile devices
- Interactive language selection with multi-select capability
- Real-time progress indicators for translations

### User Experience
- Copy-to-clipboard functionality for translated text
- Share translations directly from the interface
- Select all/deselect all languages option
- Clear all inputs with a single click
- Convenient keyboard shortcuts:
  - Ctrl/Cmd + Enter: Translate
  - Esc: Clear All
  - Ctrl/Cmd + D: Toggle Dark Mode

### Translation Management
- Task ID system for tracking translations
- Status checking for translation tasks
- Detailed view of translation content
- Progress tracking with percentage completion

## Technical Stack

### Frontend
- HTML5
- CSS3 with custom properties for theming
- JavaScript (ES6+)
- Bootstrap 4.5.2
- Font Awesome 5.15.4
- Axios for HTTP requests
- Select2 for enhanced dropdowns

### Backend
- Python
- FastAPI framework
- Translation API integration

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/real-time-translation-service.git
   cd real-time-translation-service
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

4. Open `app/templates/index.html` in your web browser or serve it using a local server.

## Usage

1. Enter the text you want to translate in the input field
2. Select one or more target languages from the dropdown menu
3. Click the "Translate" button or use Ctrl/Cmd + Enter
4. Watch the real-time progress of your translation
5. Copy or share the translated text as needed

## API Endpoints

- `POST /translate`: Submit text for translation
- `GET /translate/{task_id}`: Check translation status and results

## Future Enhancements

- Speech-to-text input capability (requires stable internet connection)
- Additional language support
- Translation memory for frequently translated phrases
- API key management for third-party translation services
- Offline mode for basic translations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap for the responsive design framework
- Font Awesome for the icons
- Select2 for the enhanced dropdown functionality
- Translation service providers for API access 