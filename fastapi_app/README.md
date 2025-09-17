# Auto-instrumentation FastAPI App

Show many ways to instrument your web app with FastAPI framework.

## Included files

1. `app.py` - just a simple app with one root (`/`) endpoint returns `{"message": "Hello World"}`
2. `app_with__traces.py` - the simple app with instrumented traces
3. `app_with__traces_logs.py` - app_with__traces + logs
4. `app_with__traces_logs_metrics.py` - app_with__traces_logs + metrics
5. `app_with__traces_logs_metrics_db.py - app_with__traces_logs_metrics app with endpoint to select users from DB and auto-instrumented sql-calling functions
