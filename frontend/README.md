# Entertainment App Frontend

React + TypeScript frontend for the LLM-powered entertainment app.

## Setup

```bash
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## Build

```bash
npm run build
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```
VITE_API_URL=http://localhost:8000
```

## Project Structure

- `/src/screens` - Application screens (ScenarioBuilder, SimulationView, etc.)
- `/src/components` - Reusable UI components
- `/src/services` - API service layer
- `/src/store` - Zustand state management
- `/src/types` - TypeScript type definitions

## Features

1. **Scenario Builder** - Create scenarios and select characters
2. **Live Simulation** - Watch characters interact with user-controlled turn order
3. **Chat with Character** - Talk to individual characters about the scenario
4. **Personality Editor** - Adjust character trait sliders
5. **Replay/What-If** - Re-run scenarios with different parameters
