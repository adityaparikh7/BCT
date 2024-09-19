// simple escrow payment contract
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Escrow {
    address public payer;
    address public payee;
    address public escrowAgent; // The address that deploys the contract is the escrow agent
    uint256 public amount;

    constructor(address _payer, address _payee, uint256 _amount) {
        payer = _payer;
        payee = _payee;
        escrowAgent = msg.sender;
        amount = _amount;
    }

    function deposit() public payable {
        require(msg.sender == payer, "Only the payer can deposit.");
        require(msg.value == amount, "Incorrect deposit amount.");
    }

    function release() public {
        require(msg.sender == escrowAgent, "Only the escrow agent can release the funds.");
        payable(payee).transfer(address(this).balance);
    }

    function refund() public {
        require(msg.sender == escrowAgent, "Only the escrow agent can refund the funds.");
        payable(payer).transfer(address(this).balance);
    }
}
