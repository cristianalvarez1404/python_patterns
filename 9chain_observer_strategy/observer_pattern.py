import asyncio
from dataclasses import dataclass
from typing import Optional,Protocol

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

load_dotenv()

#Dependencies and output schema

@dataclass
class TravelDeps:
  user_name: str
  origin_city: str

class TravelResponse(BaseModel):
  destination: str
  message: str

#Observer interface

class AgentCallObserver(Protocol):
  def notify(
      self,
      agent_name:str,
      prompt: str,
      deps: TravelDeps,
      output: BaseModel,
      duration: float,
  ) -> None: ...

class ConsoleLogger:
  def notify(
      self,
      agent_name:str,
      prompt: str,
      deps: TravelDeps,
      output: BaseModel,
      duration: float,
  ) -> None: 
    print("\n Agent Call Log")
    print(f"Agent: {agent_name}")
    print(f"Prompt: {prompt}")
    print(f"User: {deps.user_name}, Origin: {deps.origin_city}")
    print(f"Output: {output.model_dump()}")
    print(f"Duration: {duration:.2f}s")

async def run_with_observer(
  *,
  agent: Agent[TravelDeps, TravelResponse],
  prompt: str,
  deps: TravelDeps,
  observers: list[AgentCallObserver],
) -> TravelResponse:
  start = time.perf_counter()
  result = await agent.run(prompt, deps = deps)
  end = time.perf_counter()
  duration = end - start

  for observer in observers:
    observer.notify(
      agent_name = agent.name or "Unnamed Agent",
      prompt = prompt,
      deps = deps,
      output=result.output,
      duration=duration
    )
  
  return result.output

class DestinationOutput(BaseModel):
  destination: str

destination_agent = Agent(
  "openai:gpt-4o",
  deps_type = TravelDeps,
  output_type = DestinationOutput,
  system_prompt = "You help users select an ideal travel destination based on their preferences"
)

async def main():
  deps = TravelDeps(user_name="Nina", origin_city="Copenhagen")

  prompt = "I want to escape to a cozy place in the mountains for the weekend."
  output = await run_with_observer(
    agent=travel_agent,
    prompt=prompt,
    deps=deps,
    observers=[ConsoleLogger()]
  )

  print(f"\nTravel Agent says: {output.message}")
  print(f"\nDestination Suggested: {output.destination}")