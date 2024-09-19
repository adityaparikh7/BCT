// simple payment smart contract
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Payment {
    address public payer;
    address public payee;
    uint256 public amount;
    uint256 public paymentTime;
    uint256 public paymentDeadline;
    bool public isPaid;

    constructor(address _payer, address _payee, uint256 _amount, uint256 _paymentDeadline) {
        payer = _payer;
        payee = _payee;
        amount = _amount;
        paymentDeadline = _paymentDeadline;
    }

    function pay() public payable {
        require(msg.sender == payer, "Only payer can make payment");
        require(!isPaid, "Payment has been made already");
        require(block.timestamp <= paymentDeadline, "Payment deadline has passed");
        require(msg.value == amount, "Incorrect payment amount");

        isPaid = true;
        paymentTime = block.timestamp;
    }
}

