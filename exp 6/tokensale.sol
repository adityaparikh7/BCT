// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TokenSale {
    address public owner;
    uint256 public tokenPrice = 0.01 ether;
    mapping(address => uint256) public balances;

    constructor() {
        owner = msg.sender; // The deployer of the contract becomes the owner
    }

    // Function to buy tokens
    function buyTokens() public payable {
        require(msg.value > 0, "Send Ether to buy tokens");
        uint256 tokensToBuy = msg.value / tokenPrice;
        balances[msg.sender] += tokensToBuy;
    }

    // Function to withdraw Ether from the contract
    function withdraw() public {
        require(msg.sender == owner, "Only the owner can withdraw");
        payable(owner).transfer(address(this).balance);
    }

    // Function to check the balance of tokens for a specific address
    function tokenBalance(address account) public view returns (uint256) {
        return balances[account];
    }
}
