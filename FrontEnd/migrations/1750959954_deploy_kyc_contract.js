// SPDX-License-Identifier: MIT
const KYCContract = artifacts.require("KYCContract");

module.exports = function(deployer) {
  deployer.deploy(KYCContract);
};
