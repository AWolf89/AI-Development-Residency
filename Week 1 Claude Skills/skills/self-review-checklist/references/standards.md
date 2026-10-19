# Error handling and logging standards

## Error handling
1. Never swallow errors silently: every except/catch handles the error or re-raises it.
2. Catch specific errors (ValueError, not except Exception), except at the top level.
3. Users see a friendly message; details go to logs. Never show stack traces publicly.
4. Validate input at the boundary (forms, API requests, files) and reject bad input
   early with a clear reason.
5. Calls to external services set a timeout and handle failure.

## Logging
1. Use a logging library (Python logging, a Node logger), not print or console.log.
2. Use levels: DEBUG detail, INFO normal events, WARNING unexpected but handled,
   ERROR failures.
3. Use structured logs (key-value or JSON) so they can be searched.
4. Never log secrets, passwords, tokens, or personal data.
5. Each log line says what happened and includes useful context (such as a request ID).

Analogy: error handling is the car's airbags; logging is the black box.
