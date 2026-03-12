"""
Multi-agent example demonstrating tracking multiple agents
"""
import time
from aiops_guard import AIOpsGuard, get_global_tracker


class MarketAnalyst:
    """Market analysis agent"""
    
    @AIOpsGuard(agent_name="MarketAnalyst", model_name="gpt-4")
    def analyze_market(self, context: str) -> str:
        """Analyze market conditions"""
        time.sleep(0.2)
        return f"Market analysis for {context}: The market shows positive trends with moderate volatility. Key indicators suggest growth potential."
    
    @AIOpsGuard(agent_name="MarketAnalyst", model_name="gpt-4")
    def predict_trends(self, data: str) -> str:
        """Predict market trends"""
        time.sleep(0.15)
        return f"Trend prediction based on {data}: Upward trajectory expected in Q2 with potential consolidation in Q3."


class RiskManager:
    """Risk management agent"""
    
    @AIOpsGuard(agent_name="RiskManager", model_name="gpt-3.5-turbo")
    def assess_risk(self, scenario: str) -> str:
        """Assess risk level"""
        time.sleep(0.1)
        return f"Risk assessment for {scenario}: Medium risk level identified. Recommend diversification strategy."
    
    @AIOpsGuard(agent_name="RiskManager", model_name="gpt-3.5-turbo")
    def suggest_mitigation(self, risks: str) -> str:
        """Suggest risk mitigation strategies"""
        time.sleep(0.12)
        return f"Mitigation strategies for {risks}: Implement hedging, increase reserves, and monitor key metrics."


class DecisionMaker:
    """Decision making agent"""
    
    @AIOpsGuard(agent_name="DecisionMaker", model_name="gpt-4-turbo")
    def make_decision(self, inputs: str) -> str:
        """Make final decision"""
        time.sleep(0.25)
        return f"Decision based on {inputs}: Proceed with cautious optimism. Allocate 60% to growth, 40% to stability."


def main():
    """Run multi-agent simulation"""
    print("🤖 Multi-Agent Decision System\n")
    
    # Initialize agents
    market_analyst = MarketAnalyst()
    risk_manager = RiskManager()
    decision_maker = DecisionMaker()
    
    # Simulate decision-making workflow
    print("Step 1: Market Analysis...")
    market_analysis = market_analyst.analyze_market("Tech sector Q1 2024")
    market_trends = market_analyst.predict_trends("Historical data 2020-2024")
    
    print("Step 2: Risk Assessment...")
    risk_assessment = risk_manager.assess_risk("Tech investment portfolio")
    mitigation = risk_manager.suggest_mitigation("Market volatility and sector concentration")
    
    print("Step 3: Final Decision...")
    final_decision = decision_maker.make_decision("Market analysis + Risk assessment")
    
    print("\n✅ Decision workflow completed!\n")
    
    # Print comprehensive summary
    tracker = get_global_tracker()
    tracker.print_summary(show_agents=True, show_models=True)
    
    # Print agent-specific insights
    print("\n📊 Agent Performance Insights:")
    agent_summary = tracker.get_agent_summary()
    
    for agent_name, stats in agent_summary.items():
        efficiency = stats['total_tokens'] / stats['total_time_seconds']
        print(f"\n{agent_name}:")
        print(f"  - Efficiency: {efficiency:.0f} tokens/second")
        print(f"  - Cost per call: ${stats['avg_cost_per_call']:.4f}")
        print(f"  - Total cost: ${stats['total_cost_usd']:.4f}")


if __name__ == "__main__":
    main()
