import json
import os
from typing import Optional

import click
import requests
from pulp_glue.common.context import PulpContext

from pulpcore.cli.common.generic import (
    PulpCLIContext,
    pass_pulp_context,
)


def attach_chat_commands(console_group: click.Group) -> None:
    @console_group.group()
    @pass_pulp_context
    @click.pass_context
    def chat(ctx: click.Context, pulp_ctx: PulpContext, /) -> None:
        """ChatGPT integration commands."""
        pass

    @chat.command()
    @click.argument("question", type=str)
    @click.option(
        "--api-key",
        envvar="OPENAI_API_KEY",
        help="OpenAI API key (can also be set via OPENAI_API_KEY environment variable)",
    )
    @click.option(
        "--model",
        default="gpt-3.5-turbo",
        help="ChatGPT model to use (default: gpt-3.5-turbo)",
    )
    @click.option(
        "--max-tokens",
        type=int,
        default=150,
        help="Maximum number of tokens in the response (default: 150)",
    )
    @click.option(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for response randomness (0.0-2.0, default: 0.7)",
    )
    @click.option(
        "--format",
        "output_format",
        type=click.Choice(["json", "text"]),
        default="json",
        help="Output format: json (structured) or text (answer only, default: json)",
    )
    @pass_pulp_context
    def ask(
        pulp_ctx: PulpCLIContext,
        /,
        question: str,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 150,
        temperature: float = 0.7,
        output_format: str = "json",
    ) -> None:
        """Ask a question to ChatGPT and get a response."""
        
        if not api_key:
            raise click.ClickException(
                "OpenAI API key is required. Provide it via --api-key option or "
                "set the OPENAI_API_KEY environment variable."
            )
        
        # Validate parameters
        if not (0.0 <= temperature <= 2.0):
            raise click.ClickException("Temperature must be between 0.0 and 2.0")
        
        if max_tokens <= 0:
            raise click.ClickException("Max tokens must be a positive integer")
        
        # Prepare the API request
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        try:
            # Make the API call
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            
            # Extract the answer
            if "choices" in result and len(result["choices"]) > 0:
                answer = result["choices"][0]["message"]["content"].strip()
                
                if output_format == "text":
                    # Just print the answer directly with proper newlines
                    click.echo(answer)
                else:
                    # Prepare structured JSON output
                    output = {
                        "question": question,
                        "answer": answer,
                        "model": model,
                        "usage": result.get("usage", {}),
                    }
                    
                    pulp_ctx.output_result(output)
            else:
                raise click.ClickException("No response received from ChatGPT")
                
        except requests.exceptions.Timeout:
            raise click.ClickException("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"API request failed: {str(e)}")
        except json.JSONDecodeError:
            raise click.ClickException("Failed to parse API response")
        except KeyError as e:
            raise click.ClickException(f"Unexpected API response format: missing {str(e)}")

    @chat.command()
    @click.option(
        "--api-key",
        envvar="OPENAI_API_KEY",
        help="OpenAI API key (can also be set via OPENAI_API_KEY environment variable)",
    )
    @pass_pulp_context
    def models(
        pulp_ctx: PulpCLIContext,
        /,
        api_key: Optional[str] = None,
    ) -> None:
        """List available ChatGPT models."""
        
        if not api_key:
            raise click.ClickException(
                "OpenAI API key is required. Provide it via --api-key option or "
                "set the OPENAI_API_KEY environment variable."
            )
        
        # Prepare the API request
        url = "https://api.openai.com/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        try:
            # Make the API call
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            
            # Filter to only show GPT models (chat completion models)
            if "data" in result:
                gpt_models = [
                    model for model in result["data"] 
                    if "gpt" in model.get("id", "").lower()
                ]
                
                # Prepare output
                output = {
                    "available_models": [model["id"] for model in gpt_models],
                    "total_models": len(gpt_models),
                }
                
                pulp_ctx.output_result(output)
            else:
                raise click.ClickException("No models data received from API")
                
        except requests.exceptions.Timeout:
            raise click.ClickException("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise click.ClickException(f"API request failed: {str(e)}")
        except json.JSONDecodeError:
            raise click.ClickException("Failed to parse API response")
        except KeyError as e:
            raise click.ClickException(f"Unexpected API response format: missing {str(e)}")
