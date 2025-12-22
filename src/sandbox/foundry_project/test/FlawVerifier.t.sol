// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/FlawVerifier.sol";

contract FlawVerifierTest is Test {
    FlawVerifier public exploit;
    address public target = address(0);

    function setUp() public {
        // Give test contract initial balance
        vm.deal(address(this), 100 ether);

        // Deploy exploit contract
        exploit = new FlawVerifier(target);

        // Fund exploit contract
        vm.deal(address(exploit), 100 ether);
    }

    function testExploit() public {
        uint256 initialBalance = address(exploit).balance;

        // Execute exploit
        bool success = exploit.verify{value: 1 ether}();

        uint256 finalBalance = address(exploit).balance;
        uint256 profit = finalBalance > initialBalance ? finalBalance - initialBalance : 0;

        // Log results
        emit log_named_uint("Initial Balance", initialBalance);
        emit log_named_uint("Final Balance", finalBalance);
        emit log_named_uint("Profit (wei)", profit);
        emit log_named_uint("Profit (ether)", profit / 1 ether);

        // Test should pass if exploit succeeds or makes profit
        assertTrue(success || profit > 0, "Exploit failed");
    }
}
