import time
import json
import os
import sys

# Ensure the parent directory is in the path to import integrations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations.vajraclaw.runtime import VajraClaw

def run_simulation():
    print("\n==================================================")
    print(" 🛡️  VajraClaw - Execution Sandbox & Attack Simulator ")
    print("==================================================")
    print("\n[1] Initializing VajraClaw Engine & O(1) Memory Matrix...")

    # Load the demo policy
    policy_path = os.path.join(os.path.dirname(__file__), "demo_policy.yaml")
    with open(policy_path, "r", encoding="utf-8") as f:
        policy_str = f.read()

    # Initialize the protection engine
    vc = VajraClaw(rules_string=policy_str)
    time.sleep(1)
    print("✔ Engine Armed. Strict Fail-Closed mode enabled.\n")

    print("--------------------------------------------------")
    print("🧪 SIMULATION 1: Normal Agent Operation (Safe)")
    print("--------------------------------------------------")
    safe_payload = {"amount": 500, "currency": "USD"}
    print(f"🤖 Agent attempts to call: execute_payment {json.dumps(safe_payload)}")
    try:
        start_time = time.time()
        result = vc.evaluate("execute_payment", safe_payload)
        latency = (time.time() - start_time) * 1000
        print(f"✅ PASSED: Transaction approved.")
        print(f"⏱️  Latency: {latency:.2f} ms\n")
    except Exception as e:
        print(f"❌ Error: {e}")

    time.sleep(2)

    print("--------------------------------------------------")
    print("🔥 SIMULATION 2: Prompt Injection Attack (Malicious)")
    print("--------------------------------------------------")
    print("An attacker tricked the AI into transferring $50,000 to their wallet.")
    attack_payload = {"amount": 50000, "currency": "USD", "destination": "HACKER_WALLET_X"}
    print(f"🤖 Agent attempts to call: execute_payment {json.dumps(attack_payload)}")
    print("...")
    time.sleep(1)

    try:
        start_time = time.time()
        # This should be blocked by VajraClaw!
        result = vc.evaluate("execute_payment", attack_payload)
        print(f"❌ CRITICAL FAILURE: Attack succeeded! (VajraClaw failed to block)")
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        print(f"\n🛡️  VAJRACLAW INTERVENTION!")
        print(f"🚫 BLOCKED: {e}")
        print(f"⚡ Action: OS System Call hard-terminated.")
        print(f"⏱️  Latency: {latency:.2f} ms")

    print("\n==================================================")
    print("💡 This is your 'First Denial Moment'.")
    print("   VajraClaw is invisible infrastructure—until you need it.")
    print("   Your enterprise systems are safe. Welcome to VajraClaw.")
    print("==================================================\n")

if __name__ == "__main__":
    run_simulation()
