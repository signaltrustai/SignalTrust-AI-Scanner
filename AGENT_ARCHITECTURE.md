# 🧠 SignalTrust AI — Multi‑Agent Architecture

## Overview
SignalTrust AI uses a distributed multi‑agent system to analyze markets, detect patterns, track whales, evaluate sentiment, and generate predictions.

## Core Agents
- Coordinator (8000)
- Crypto Agent (8001)
- Stock Agent (8002)
- Whale Agent (8003)
- News Agent (8004)

## Advanced Agents
- Social Sentiment (8005)
- On‑Chain Data (8006)
- Macro Economics (8007)
- Portfolio Optimizer (8008)

## Supervisor
Auto‑GPT‑based supervisor that:
- monitors agents
- restarts failing agents
- optimizes workflows
- ensures consistency

## Data Flow
User → Coordinator → Agents → Coordinator → API → Web App

## Technologies
- Python
- Flask
- CrewAI
- OpenAI / Claude / Local models
- Docker
- Redis
- Render

## Goals
- Scalability
- Reliability
- Real‑time intelligence
- Modular expansion
