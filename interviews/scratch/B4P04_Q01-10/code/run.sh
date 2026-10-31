export PATH=/tmp/claude-0/ven/v/bin:$PATH MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1
W=$(mktemp -d); cp "$1" $W/; cd $W; python3 -I "$(basename $1)" 2>&1 | grep -v -E 'Warning|warn|ARNING'
