"""
Call tracker for aggregating and reporting metrics
"""
from typing import List, Dict, Optional
from collections import defaultdict
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .models import CallMetrics


class CallTracker:
    """
    Tracks and aggregates LLM call metrics
    """
    
    def __init__(self):
        """Initialize the call tracker"""
        self.calls: List[CallMetrics] = []
        self.console = Console()
    
    def add_call(self, metrics: CallMetrics) -> None:
        """
        Add a call to the tracker
        
        Args:
            metrics: Call metrics to track
        """
        self.calls.append(metrics)
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics
        
        Returns:
            Dictionary with aggregated statistics
        """
        if not self.calls:
            return {
                "total_calls": 0,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "total_time_seconds": 0.0,
                "success_rate": 0.0,
            }
        
        total_calls = len(self.calls)
        successful_calls = sum(1 for call in self.calls if call.success)
        
        return {
            "total_calls": total_calls,
            "successful_calls": successful_calls,
            "failed_calls": total_calls - successful_calls,
            "success_rate": successful_calls / total_calls * 100,
            "total_tokens": sum(call.total_tokens for call in self.calls),
            "total_input_tokens": sum(call.input_tokens for call in self.calls),
            "total_output_tokens": sum(call.output_tokens for call in self.calls),
            "total_cost_usd": sum(call.total_cost_usd for call in self.calls),
            "total_input_cost_usd": sum(call.input_cost_usd for call in self.calls),
            "total_output_cost_usd": sum(call.output_cost_usd for call in self.calls),
            "total_time_seconds": sum(call.execution_time_seconds for call in self.calls),
            "avg_time_seconds": sum(call.execution_time_seconds for call in self.calls) / total_calls,
            "avg_tokens_per_call": sum(call.total_tokens for call in self.calls) / total_calls,
            "avg_cost_per_call": sum(call.total_cost_usd for call in self.calls) / total_calls,
        }
    
    def get_agent_summary(self) -> Dict[str, Dict]:
        """
        Get summary statistics grouped by agent
        
        Returns:
            Dictionary mapping agent names to their statistics
        """
        agent_calls = defaultdict(list)
        
        for call in self.calls:
            agent_calls[call.agent_name].append(call)
        
        summary = {}
        for agent_name, calls in agent_calls.items():
            total_calls = len(calls)
            successful_calls = sum(1 for call in calls if call.success)
            
            summary[agent_name] = {
                "total_calls": total_calls,
                "successful_calls": successful_calls,
                "success_rate": successful_calls / total_calls * 100,
                "total_tokens": sum(call.total_tokens for call in calls),
                "total_cost_usd": sum(call.total_cost_usd for call in calls),
                "total_time_seconds": sum(call.execution_time_seconds for call in calls),
                "avg_time_seconds": sum(call.execution_time_seconds for call in calls) / total_calls,
                "avg_cost_per_call": sum(call.total_cost_usd for call in calls) / total_calls,
            }
        
        return summary
    
    def get_model_summary(self) -> Dict[str, Dict]:
        """
        Get summary statistics grouped by model
        
        Returns:
            Dictionary mapping model names to their statistics
        """
        model_calls = defaultdict(list)
        
        for call in self.calls:
            model_calls[call.model_name].append(call)
        
        summary = {}
        for model_name, calls in model_calls.items():
            total_calls = len(calls)
            
            summary[model_name] = {
                "total_calls": total_calls,
                "total_tokens": sum(call.total_tokens for call in calls),
                "total_cost_usd": sum(call.total_cost_usd for call in calls),
                "avg_tokens_per_call": sum(call.total_tokens for call in calls) / total_calls,
                "avg_cost_per_call": sum(call.total_cost_usd for call in calls) / total_calls,
            }
        
        return summary
    
    def print_summary(self, show_agents: bool = True, show_models: bool = True) -> None:
        """
        Print a formatted summary table to the console
        
        Args:
            show_agents: Whether to show per-agent breakdown
            show_models: Whether to show per-model breakdown
        """
        if not self.calls:
            self.console.print("[yellow]No LLM calls tracked yet[/yellow]")
            return
        
        # Overall summary
        summary = self.get_summary()
        
        # Create header panel
        header = Text()
        header.append("🛡️  AIOpsGuard Summary Report\n", style="bold cyan")
        header.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", style="dim")
        
        self.console.print(Panel(header, border_style="cyan"))
        self.console.print()
        
        # Overall statistics table
        overall_table = Table(title="📊 Overall Statistics", show_header=True, header_style="bold magenta")
        overall_table.add_column("Metric", style="cyan", width=30)
        overall_table.add_column("Value", style="green", justify="right")
        
        overall_table.add_row("Total Calls", str(summary["total_calls"]))
        overall_table.add_row("Successful Calls", str(summary["successful_calls"]))
        overall_table.add_row("Failed Calls", str(summary["failed_calls"]))
        overall_table.add_row("Success Rate", f"{summary['success_rate']:.1f}%")
        overall_table.add_row("─" * 30, "─" * 20)
        overall_table.add_row("Total Tokens", f"{summary['total_tokens']:,}")
        overall_table.add_row("  ├─ Input Tokens", f"{summary['total_input_tokens']:,}")
        overall_table.add_row("  └─ Output Tokens", f"{summary['total_output_tokens']:,}")
        overall_table.add_row("Avg Tokens/Call", f"{summary['avg_tokens_per_call']:.0f}")
        overall_table.add_row("─" * 30, "─" * 20)
        overall_table.add_row("Total Cost", f"${summary['total_cost_usd']:.4f}")
        overall_table.add_row("  ├─ Input Cost", f"${summary['total_input_cost_usd']:.4f}")
        overall_table.add_row("  └─ Output Cost", f"${summary['total_output_cost_usd']:.4f}")
        overall_table.add_row("Avg Cost/Call", f"${summary['avg_cost_per_call']:.4f}")
        overall_table.add_row("─" * 30, "─" * 20)
        overall_table.add_row("Total Time", f"{summary['total_time_seconds']:.2f}s")
        overall_table.add_row("Avg Time/Call", f"{summary['avg_time_seconds']:.2f}s")
        
        self.console.print(overall_table)
        self.console.print()
        
        # Per-agent breakdown
        if show_agents:
            agent_summary = self.get_agent_summary()
            
            agent_table = Table(title="🤖 Per-Agent Breakdown", show_header=True, header_style="bold blue")
            agent_table.add_column("Agent", style="cyan")
            agent_table.add_column("Calls", justify="right")
            agent_table.add_column("Success Rate", justify="right")
            agent_table.add_column("Tokens", justify="right")
            agent_table.add_column("Cost (USD)", justify="right", style="green")
            agent_table.add_column("Time (s)", justify="right")
            agent_table.add_column("Avg Time", justify="right")
            
            for agent_name, stats in sorted(agent_summary.items()):
                agent_table.add_row(
                    agent_name,
                    str(stats["total_calls"]),
                    f"{stats['success_rate']:.1f}%",
                    f"{stats['total_tokens']:,}",
                    f"${stats['total_cost_usd']:.4f}",
                    f"{stats['total_time_seconds']:.2f}",
                    f"{stats['avg_time_seconds']:.2f}",
                )
            
            self.console.print(agent_table)
            self.console.print()
        
        # Per-model breakdown
        if show_models:
            model_summary = self.get_model_summary()
            
            model_table = Table(title="🔧 Per-Model Breakdown", show_header=True, header_style="bold yellow")
            model_table.add_column("Model", style="cyan")
            model_table.add_column("Calls", justify="right")
            model_table.add_column("Total Tokens", justify="right")
            model_table.add_column("Avg Tokens", justify="right")
            model_table.add_column("Total Cost", justify="right", style="green")
            model_table.add_column("Avg Cost", justify="right", style="green")
            
            for model_name, stats in sorted(model_summary.items()):
                model_table.add_row(
                    model_name,
                    str(stats["total_calls"]),
                    f"{stats['total_tokens']:,}",
                    f"{stats['avg_tokens_per_call']:.0f}",
                    f"${stats['total_cost_usd']:.4f}",
                    f"${stats['avg_cost_per_call']:.4f}",
                )
            
            self.console.print(model_table)
            self.console.print()
        
        # Cost projection
        if summary["total_calls"] > 0:
            daily_projection = summary["total_cost_usd"] * (86400 / summary["total_time_seconds"])
            monthly_projection = daily_projection * 30
            
            projection_table = Table(title="💰 Cost Projections", show_header=True, header_style="bold red")
            projection_table.add_column("Period", style="cyan")
            projection_table.add_column("Estimated Cost", justify="right", style="red")
            
            projection_table.add_row("Per Hour", f"${summary['total_cost_usd'] * (3600 / summary['total_time_seconds']):.2f}")
            projection_table.add_row("Per Day", f"${daily_projection:.2f}")
            projection_table.add_row("Per Month (30d)", f"${monthly_projection:.2f}")
            projection_table.add_row("Per Year (365d)", f"${daily_projection * 365:.2f}")
            
            self.console.print(projection_table)
            self.console.print()
    
    def export_to_dict(self) -> Dict:
        """
        Export all tracked calls to a dictionary
        
        Returns:
            Dictionary with all call metrics
        """
        return {
            "summary": self.get_summary(),
            "agent_summary": self.get_agent_summary(),
            "model_summary": self.get_model_summary(),
            "calls": [call.to_dict() for call in self.calls],
        }
    
    def clear(self) -> None:
        """Clear all tracked calls"""
        self.calls.clear()
