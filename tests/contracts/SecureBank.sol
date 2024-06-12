// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title SecureBank
 * @notice A secure implementation of a bank contract with proper security measures
 * @dev Demonstrates best practices for smart contract security
 */
contract SecureBank is ReentrancyGuard, Ownable {
    mapping(address => uint256) public balances;

    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    event OwnershipTransferInitiated(address indexed previousOwner, address indexed newOwner);

    /**
     * @notice Deposit ether into the bank
     */
    function deposit() external payable nonReentrant {
        require(msg.value > 0, "Must deposit non-zero amount");

        balances[msg.sender] += msg.value;

        emit Deposit(msg.sender, msg.value);
    }

    /**
     * @notice Withdraw ether from the bank
     * @param amount Amount to withdraw
     */
    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(amount > 0, "Must withdraw non-zero amount");

        // Checks-Effects-Interactions pattern
        balances[msg.sender] -= amount;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        emit Withdrawal(msg.sender, amount);
    }

    /**
     * @notice Emergency withdrawal by owner only
     * @param recipient Address to receive funds
     * @param amount Amount to withdraw
     */
    function emergencyWithdraw(address payable recipient, uint256 amount) external onlyOwner {
        require(recipient != address(0), "Invalid recipient");
        require(amount <= address(this).balance, "Insufficient contract balance");

        recipient.transfer(amount);
    }

    /**
     * @notice Update user balance (owner only, for administrative purposes)
     * @param user User address
     * @param newBalance New balance to set
     */
    function updateBalance(address user, uint256 newBalance) external onlyOwner {
        require(user != address(0), "Invalid user address");

        uint256 oldBalance = balances[user];
        balances[user] = newBalance;

        emit Deposit(user, newBalance > oldBalance ? newBalance - oldBalance : 0);
    }

    /**
     * @notice Get contract balance
     */
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }

    /**
     * @notice Receive function to accept direct transfers
     */
    receive() external payable {
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }
}
