// SPDX-License-Identifier: UNLICENSEDn
pragma solidity ^0.8.0;

contract KYCContract {
    struct User {
        string ipfsHash;
        uint age;
        bool verified;
    }

    mapping(address => User) public users;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // Store user KYC data (callable by owner)
    function storeKYC(address _user, string memory _ipfsHash, uint _age) public {
        require(msg.sender == owner, "Only owner can add KYC");
        users[_user] = User(_ipfsHash, _age, false);
    }

    // Verify age 
    function verifyAge(address _user) public view returns (bool) {
        return users[_user].age >= 18; // Returns true if age >= 18
    }
}
