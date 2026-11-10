#!/bin/bash
# ============================================================================
# YNC Assistant - Automated Startup Script
# This script automatically starts the YNC Telegram Bot with no terminal input required.
# ============================================================================

set -e

# Configuration
PROJECT_DIR="/Users/fnb/Downloads/ync-assistant"
LOG_FILE="${PROJECT_DIR}/bot_run.log"
ENV_FILE="${PROJECT_DIR}/.env"
PID_FILE="${PROJECT_DIR}/bot.pid"
PROMPT_FILE="${PROJECT_DIR}/start_prompt.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

log_action() {
    echo -e "${BLUE}→${NC} $1"
}

# Check environment configuration
check_environment() {
    log_action "Checking environment configuration..."
    
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file not found: $ENV_FILE"
        return 1
    fi
    
    # Source environment variables
    source "$ENV_FILE"
    
    # Validate required variables
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        log_error "TELEGRAM_BOT_TOKEN not configured"
        return 1
    fi
    
    if [ -z "$VENCE_API_KEY" ]; then
        log_error "VENCE_API_KEY not configured"
        return 1
    fi
    
    log_info "Environment configuration validated successfully"
    return 0
}

# Check Python installation
check_python() {
    log_action "Verifying Python installation..."
    
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    log_info "Python version: $PYTHON_VERSION"
    
    # Check required modules
    if python3 -c "import telegram, requests, dotenv" 2>/dev/null; then
        log_info "All required Python modules are installed"
        return 0
    else
        log_warning "Some Python modules may need installation"
        return 0
    fi
}

# Install dependencies
install_dependencies() {
    log_action "Installing Python dependencies..."
    
    pip3 install -q telegram-bot anthropic requests dotenv
    log_info "Dependencies installed successfully"
}

# Start the bot
start_bot() {
    log_action "Starting YNC Assistant Bot..."
    
    cd "$PROJECT_DIR"
    
    # Check if bot is already running
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if ps -p "$OLD_PID" > /dev/null 2>&1; then
            log_info "Bot is already running (PID: $OLD_PID)"
            return 0
        fi
    fi
    
    # Start the bot in background
    nohup python3 "$PROJECT_DIR/bot.py" > "$LOG_FILE" 2>&1 &
    BOT_PID=$!
    
    # Save PID
    echo "$BOT_PID" > "$PID_FILE"
    
    log_info "Bot started with PID: $BOT_PID"
    
    # Wait for bot initialization
    sleep 3
    
    # Verify bot is running
    if ps -p "$BOT_PID" > /dev/null 2>&1; then
        log_info "Bot is running successfully"
        
        # Display bot status
        log_info "Bot Configuration:"
        echo "  - Environment File: $ENV_FILE"
        echo "  - Log File: $LOG_FILE"
        echo "  - Database: $PROJECT_DIR/assistant.db"
        echo "  - Model: $(grep AI_MODEL $ENV_FILE | cut -d'=' -f2)"
    else
        log_error "Bot failed to start"
        return 1
    fi
    
    return 0
}

# Stop the bot
stop_bot() {
    log_action "Stopping YNC Assistant Bot..."
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        
        if ps -p "$PID" > /dev/null 2>&1; then
            log_info "Stopping bot (PID: $PID)..."
            kill "$PID"
            sleep 2
            
            if ! ps -p "$PID" > /dev/null 2>&1; then
                log_info "Bot stopped successfully"
                rm -f "$PID_FILE"
                return 0
            fi
        fi
    fi
    
    log_info "Bot was not running"
    return 0
}

# Restart the bot
restart_bot() {
    log_action "Restarting YNC Assistant Bot..."
    
    stop_bot
    sleep 2
    start_bot
}

# Display bot logs
view_logs() {
    log_action "Viewing bot logs..."
    
    if [ -f "$LOG_FILE" ]; then
        log_info "Recent bot activity:"
        tail -n 20 "$LOG_FILE" | while read line; do
            echo "  $line"
        done
    else
        log_warning "No log file available"
    fi
}

# Create startup prompt
create_startup_prompt() {
    cat > "$PROMPT_FILE" << 'PROMPT'
=============================================================================
                    YNC ASSISTANT - AUTOMATED STARTUP
=============================================================================

🤖 The YNC Assistant Telegram Bot has been started successfully!

Status: Running (No Terminal Input Required)

Bot Features:
  • Automated customer support for YNC & GMB Universities
  • Real-time chat responses powered by Venice AI
  • Conversation history tracking
  • Owner notifications for important events

Available Actions:
  1. View Logs:      $ tail -f /Users/fnb/Downloads/ync-assistant/bot_run.log
  2. Check Status:  $ ps aux | grep bot.py
  3. Restart Bot:   $ /Users/fnb/Downloads/ync-assistant/startup.sh restart
  4. Stop Bot:      $ /Users/fnb/Downloads/ync-assistant/startup.sh stop

Application Files:
  📁 Environment:  .env
  📁 Bot Script:   bot.py
  📁 Logger:       bot_run.log
  📁 Database:     assistant.db

=============================================================================
No further action is required. The bot will continue running in the background.
=============================================================================
PROMPT

    log_info "Startup instructions saved to: $PROMPT_FILE"
}

# Main execution
main() {
    echo ""
    echo "=============================================================================="
    echo "          YNC Assistant - Automated Startup"
    echo "=============================================================================="
    echo ""
    
    check_environment
    check_python
    install_dependencies
    start_bot
    view_logs
    create_startup_prompt
    
    echo ""
    echo "=============================================================================="
    echo "          ✅ Startup Complete"
    echo "=============================================================================="
    echo ""
    echo "The YNC Assistant is now running without terminal intervention."
    echo "You can now close this window or use the startup instructions below."
    echo ""
    echo "📍 Location: $PROJECT_DIR"
    echo ""
}

# Parse command line arguments
case "${1:-start}" in
    start)
        main
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    logs)
        view_logs
        ;;
    help)
        echo "Usage: $0 {start|stop|restart|logs|help}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the YNC Assistant bot"
        echo "  stop    - Stop the running bot"
        echo "  restart - Restart the bot"
        echo "  logs    - View bot logs"
        echo "  help    - Show this help message"
        ;;
    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac
