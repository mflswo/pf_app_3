import math
import random

# Constants
TOTAL_ETH = 1000  # Total ETH available
BASE_FEE_MAX_CHANGE = 8
TARGET_GAS = 15000000
initial_base_fee = 10  # in gwei
gas_used = 30000000  # Full block usage in gas

# Initialize list of base fees starting with the initial base fee
base_fees = [initial_base_fee]
base_fee = initial_base_fee

# Calculate base fees for each of the next 10 blocks
for i in range(1, 11):
    base_fee_next = base_fee + base_fee * ((gas_used - TARGET_GAS) / (TARGET_GAS * BASE_FEE_MAX_CHANGE))
    base_fees.append(base_fee_next)
    base_fee = base_fee_next

# Calculate the total cost in gwei and convert to ETH
total_cost = sum(fee * gas_used / 1e9 for fee in base_fees)  # Now includes the initial base fee

# Calculate available profit
available_profit = TOTAL_ETH - total_cost - 1  # Subtract 1 ETH for interacting with contract

giveup_profit = 0.9 * available_profit
# net_profit = 0.1 * available_profit

# Distribute the remaining profit exponentially
profits = []
# Use a sharp base for exponential increase
base = 1.05
sum_exponential_factors = sum([base**i for i in range(10)])

# Calculate each block's profit with little randomization to confuse people
random_factors = [random.uniform(0.99, 1.01) for _ in range(10)]

for i in range(10):
    profit = (base**i / sum_exponential_factors) * giveup_profit * random_factors[i]
    profits.append((profit, profit * 1e9 / gas_used))

# Print base fees and profits for each block
print("Block distributions (in ETH):")
for index, (fee, (profit, priority_fee)) in enumerate(zip(base_fees, profits), start=0):
    print(f"Block {index}: Base Fee: {fee:.2f} gwei, Profit: {profit:.6f} ETH, Priority Fee: {priority_fee:.6f} gwei")

# Report
total_distributed_profit = sum(p[0] for p in profits)
print(f"\nTotal distributed profit: {total_distributed_profit:.6f} ETH")
print(f"Total cost for 10 blocks: {total_cost:.6f} ETH")
print(f"Net profit: {(available_profit - total_distributed_profit):.6f} ETH")
