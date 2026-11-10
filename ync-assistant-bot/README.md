# YNC Assistant - Telegram Bot

**A comprehensive Telegram bot solution for YNC & GMB Universities, powered by Venice AI and Llama 3.1.**

---

## 🚀 Quick Start - Run Without Terminal

Choose one of these methods to start the bot without manual terminal commands:

### 📌 Method 1: Desktop Application (Recommended)
**Launch with a single graphical interface.**

```bash
# Install GUI dependencies
pip3 install PyGObject python3-tk

# Run the desktop launcher
python3 /Users/fnb/Downloads/ync-assistant/launcher.py
```

**Features:**
- 🎨 Graphical user interface
- 🔄 Real-time monitoring
- 📊 Log visualization
- 🎯 Control buttons for operations

### 📌 Method 2: Automated Startup Script
**Execute with a single command for hands-free operation.**

```bash
# Start the bot
./startup.sh start

# Available commands:
./startup.sh start       # Initialize bot
./startup.sh stop        # Stop running bot
./startup.sh restart     # Restart bot
./startup.sh logs        # View logs
./startup.sh help        # Display help
```

### 📌 Method 3: System Service
**Configure for automatic system-wide startup.**

```bash
# Install as systemd service
sudo systemctl enable ync-assistant
sudo systemctl start ync-assistant

# Monitor service status
sudo systemctl status ync-assistant
```

---

## 📋 Getting Started

### Installation

1. **Clone the repository**
   ```bash
   cd /Users/fnb/Downloads/ync-assistant
   ```

2. **Verify environment**
   ```bash
   # Check environment configuration
   source .env
   env | grep -E "TELEGRAM_BOT_TOKEN|VENCE_API_KEY|AI_MODEL"
   ```

3. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

### Configuration

The bot is configured with the following environment variables:

```bash
# Environment Configuration (.env)
TELEGRAM_BOT_TOKEN=9120523062:AAFoP5SwdhqRB8n3jBygO2-rPfq0BPjD_YE
VENCE_API_KEY=VENICE_INFERENCE_KEY_i6opkEBDTIdayLhOYNcdLvaFuKZgk4vee9vn2yOrN8
AI_MODEL=meta-llama/llama-3.1-8b-instruct
OWNER_USER_ID=7080090889
HISTORY_TURNS=20
```

---

## 🏗️ Architecture

### Service Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                      YNC Assistant Telegram Bot                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Bot Core                                │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐   │  │
│  │  │  Message   │  │  Database  │  │   Notification      │   │  │
│  │  │  Handler   │  │  (SQLite)  │  │   Manager           │   │  │
│  │  └────────────┘  └────────────┘  └────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                    │              │              │              │
│         ┌──────────┼──────────────┼──────────────┼──────────────┐│
│         │          │              │              │              ││
│         ▼          ▼              ▼              ▼              ▼││
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ ││
│  │  Telegram  │  │  Venice AI │  │  Llama 3.1 │  │  Anthropic │ ││
│  │  Platform  │  │  (Active)  │  │  (Primary) │  │  (Reference)│││
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘ ││
└──────────────────────────────────────────────────────────────────┘
```

### Component Overview

| Component | Description | Status |
|-----------|-------------|--------|
| **Telegram Bot** | User interface for chat interactions | ✅ Active |
| **Venice AI** | Primary AI inference engine | ✅ Active |
| **Llama 3.1** | Core language model | ✅ Active |
| **Anthropic** | Reference configuration | ⏸️ Reserved |
| **SQLite Database** | Data persistence | ✅ Active |

---

## 🎯 Bot Commands

Available Telegram commands:

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot and welcome users |
| `/reset` | Reset conversation state |
| `/status` | Display bot and service status |
| `/help` | Show available commands and features |
| `/courses` | List available courses and programs |
| `/contact` | Provide contact information |

---

## 📁 File Structure

```
ync-assistant/
├── .env                        # Environment configuration
├── bot.py                      # Core bot application
├── launcher.py                 # Desktop launcher
├── startup.sh                  # Automated startup script
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
├── NON_TERMINAL_GUIDE.md       # Non-terminal usage guide
├── FLOW_DIAGRAM.md             # Architecture flow diagrams
├── SETUP_GUIDE.md              # Setup instructions
├── DEPLOYMENT_SUMMARY.md       # Deployment information
├── AI_SERVICE_ARCHITECTURE.md  # AI service details
├── VENICE_VS_ANNTHROPIC_GUIDE.md # Service comparison
├── applications/               # Application bundle
└── logs/                       # Log files directory
```

---

## 🔧 Usage Guide

### For Desktop Users

1. **Launch Application**
   - Double-click the YNC Assistant launcher
   - Monitor the graphical dashboard

2. **Available Actions**
   - Start/Stop bot with single clicks
   - View real-time logs
   - Access configuration settings

3. **Monitoring**
   - Track bot health indicators
   - Review performance metrics
   - Manage notifications

### For Server Deployment

1. **Service Installation**
   ```bash
   sudo cp ync-assistant.service /etc/systemd/system/
   sudo systemctl enable ync-assistant
   ```

2. **Operations**
   ```bash
   # Check service status
   systemctl status ync-assistant

   # View logs
   journalctl -u ync-assistant -f

   # Restart service
   systemctl restart ync-assistant
   ```

---

## 📊 Monitoring & Logs

### Log Files

- **Application Logs**: `bot_run.log`
- **System Logs**: `journalctl` output
- **Configuration**: `.env` file

### Health Monitoring

| Metric | Status | Description |
|--------|--------|-------------|
| Bot Process | Active | Running continuously |
| AI Service | Operational | Venice AI responding |
| Database | Connected | SQLite storage active |
| Notifications | Enabled | Owner alerts configured |

---

## 📖 Documentation

### Guides and References

1. **[NON_TERMINAL_GUIDE.md](NON_TERMINAL_GUIDE.md)** - Complete guide for non-terminal usage
2. **[FLOW_DIAGRAM.md](FLOW_DIAGRAM.md)** - Architecture and flow diagrams
3. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions
4. **[AI_SERVICE_ARCHITECTURE.md](AI_SERVICE_ARCHITECTURE.md)** - AI service details
5. **[VENICE_VS_ANNTHROPIC_GUIDE.md](VENICE_VS_ANNTHROPIC_GUIDE.md)** - Service comparison

---

## 🤝 Support

### Getting Help

- **Documentation**: Refer to the guides for detailed information
- **Support**: Contact the development team for assistance
- **Community**: Join discussions and share experiences

### Contact Information

- **Project**: YNC Assistant Telegram Bot
- **Service**: Venice AI (Primary), Anthropic (Reference)
- **Model**: Llama 3.1
- **Platform**: Telegram

---

## 📝 License

This project is provided as-is for educational and operational purposes.

---

**Created and maintained by the YNC Team**  
**Version**: 1.0.0  
**Last Updated**: November 2026
