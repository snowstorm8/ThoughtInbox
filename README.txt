# ThoughtInbox

A lightweight desktop application for capturing, organizing, searching, and managing thoughts.

ThoughtInbox is a Python desktop application built around a SQLite database, with support for tags, favorites, reminders, autosaving, preferences, and multiple export formats. It was developed as a personal software project with an emphasis on persistence, modularity, testing, and reliable behavior outside the development environment.

## Features

### Thought Management

* Create, edit, and delete thoughts
* Undo deleted thoughts
* Automatically persist thoughts using SQLite
* View thoughts in a card-based interface

### Organization

* Mark thoughts as favorites
* Assign multiple tags to thoughts
* Search thoughts by their content
* Search and filter by tags and favorites

### Reminders

* Create reminders for individual thoughts
* Persist reminders across application restarts
* Automatically check for due reminders
* Use Windows Task Scheduler so reminders can trigger even when the application is closed

### Autosave

* Automatically save unfinished text from the input panel
* Configurable autosave delay
* Restore or discard saved drafts when reopening the application

### Preferences

* Persistent application settings
* Theme selection
* Window size and position persistence
* Configurable autosave behavior and delay

### Export

Thoughts can be exported in multiple formats:

* `.txt`
* Markdown
* JSON

Exports preserve relevant metadata such as dates, favorites, and tags.

## Tech Stack

* **Python**
* **CustomTkinter** for the graphical user interface
* **SQLite** for persistent application data
* **JSON** for application settings and structured exports
* **Windows Task Scheduler** for persistent reminders
* **PyInstaller** for creating a standalone Windows executable
* **unittest** for automated testing

## Project Structure

```text
ThoughtInbox/
│
├── main.py                 # Application entry point
├── app.py                  # Main application logic
├── database.py             # SQLite database operations
├── settings.py             # Persistent application settings
├── ui.py                   # UI components
├── exporter.py             # TXT, Markdown, and JSON exports
│
├── dialogs/                # Dialog windows
├── reminders/              # Reminder scheduling and notification logic
├── utils/                  # Shared utilities and application paths
├── widgets/                # Reusable UI widgets
├── assets/                 # Application assets and icons
│
├── tests/                  # Automated test suite
│
└── README.md
```

## Data Storage

Application data is stored separately from the application executable.

On Windows, ThoughtInbox uses the user's application data directory:

```text
%APPDATA%\ThoughtInbox\
├── thoughts.db
├── settings.json
└── drafts.txt
```

This separation allows the executable to be moved or packaged without coupling persistent user data to the installation directory.

## Testing

ThoughtInbox includes an automated test suite covering the application's database and persistence functionality.

The test suite currently contains **79 automated tests** covering areas such as:

* Thought creation
* Thought retrieval
* Thought updates
* Thought deletion
* Favorites
* Tags
* Search
* Reminders
* Reminder updates and deletion
* Database persistence
* Database reopening
* Export functionality
* Settings persistence
* Draft persistence

Run the tests with:

```bash
python -m unittest discover -s tests -v
```

The project also underwent manual smoke testing of the packaged application, including:

* Application startup
* Window sizing and persistence
* Creating and saving thoughts
* Editing thoughts
* Deleting and restoring thoughts
* Tags and favorites
* Search
* Autosave
* Draft restoration
* Preferences
* Export
* Reminders
* Running the packaged executable independently of the development environment

## Running From Source

Clone the repository and install the required dependencies.

```bash
pip install customtkinter pillow
```

Then run:

```bash
python main.py
```

## Building the Windows Executable

ThoughtInbox can be packaged into a standalone Windows application using PyInstaller.

```bash
pyinstaller --onedir --windowed --name ThoughtInbox --add-data "assets;assets" --icon "assets/inbox.ico" main.py
```

The executable will be generated under:

```text
dist/ThoughtInbox/ThoughtInbox.exe
```

The packaged application uses the same application-data directory as the development version, allowing reminders and persistent data to work independently of the source-code directory.

## Architecture

The application separates responsibilities across several components:

```text
                    ┌─────────────────┐
                    │     main.py     │
                    │ Entry Point     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     app.py      │
                    │ Application     │
                    │ Logic / State   │
                    └───────┬─────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌────────────┐
        │ database │  │    UI    │  │ reminders  │
        │   .py    │  │          │  │            │
        └────┬─────┘  └──────────┘  └─────┬──────┘
             │                            │
             ▼                            ▼
        ┌──────────┐              ┌──────────────┐
        │ SQLite   │              │ Task         │
        │ Database │              │ Scheduler    │
        └──────────┘              └──────────────┘
```

The packaged reminder system launches the application executable with a dedicated reminder mode rather than relying on a separate Python interpreter. This allows the same packaged application to handle both the normal GUI and scheduled reminder execution.

## Design Considerations

A few implementation decisions were made specifically to improve reliability:

### Persistent User Data

User data is stored outside the executable so that rebuilding or moving the application does not overwrite the database, settings, or drafts.

### Dependency Management

Application resources such as icons are explicitly included in the PyInstaller build, while Python modules are resolved through normal imports.

### Testable Database Layer

The database class accepts an optional database path, allowing tests to operate on temporary SQLite databases without modifying the user's real application data.

### Reminder Persistence

Reminders are stored in SQLite rather than only in application memory. Windows Task Scheduler periodically launches the packaged application in reminder mode, allowing reminders to be processed even when the main GUI is closed.

Current Status

ThoughtInbox is a complete and functional Windows desktop application for its intended scope.

The application includes persistent SQLite storage, tags, favorites, search, autosave and draft restoration, configurable preferences, multi-format export, persistent reminders, automated testing, and a standalone Windows executable.

The project is considered complete for the foreseeable future. Further development, if undertaken, would focus on optional refinements such as UI/UX improvements, architectural refactoring, or additional features rather than completing the core application.

## License

This project is currently for personal use.
