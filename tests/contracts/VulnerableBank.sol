// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;

/**
 * @title VulnerableBank
 * @notice This contract contains INTENTIONAL vulnerabilities for testing purposes
 * DO NOT deploy to production!
 */
contract VulnerableBank {
    mapping(address => uint256) public balances;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // VULNERABILITY: Missing zero address check
    function setOwner(address newOwner) public {
        require(msg.sender == owner, "Not owner");
        owner = newOwner;
    }

    // VULNERABILITY: Reentrancy attack possible
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");

        // External call before state update - classic reentrancy
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        // State update after external call - WRONG!
        balances[msg.sender] -= amount;
    }

    // VULNERABILITY: Unprotected ether withdrawal
    function emergencyWithdraw(address payable recipient, uint256 amount) public {
        recipient.transfer(amount);
    }

    // VULNERABILITY: tx.origin authentication
    function withdrawToOrigin(uint256 amount) public {
        require(tx.origin == owner, "Not original owner");
        balances[tx.origin] -= amount;
        payable(tx.origin).transfer(amount);
    }

    // VULNERABILITY: Integer overflow (Solidity 0.7.x)
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // VULNERABILITY: Unchecked low-level call
    function executeCall(address target, bytes memory data) public returns (bool) {
        (bool success, ) = target.call(data);
        return success; // Return value checked but no revert
    }

    // VULNERABILITY: Block timestamp dependence
    function timeLock(uint256 amount) public {
        require(block.timestamp > 1234567890, "Too early");
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    // VULNERABILITY: Unprotected selfdestruct
    function destroy() public {
        selfdestruct(payable(owner));
    }

    // VULNERABILITY: Dangerous delegatecall
    function delegateExecute(address target, bytes memory data) public returns (bytes memory) {
        (bool success, bytes memory result) = target.delegatecall(data);
        require(success, "Delegatecall failed");
        return result;
    }

    // Missing event emission for critical state change
    function updateBalance(address user, uint256 newBalance) public {
        require(msg.sender == owner, "Not owner");
        balances[user] = newBalance;
        // No event emitted!
    }

    receive() external payable {
        balances[msg.sender] += msg.value;
    }
}
