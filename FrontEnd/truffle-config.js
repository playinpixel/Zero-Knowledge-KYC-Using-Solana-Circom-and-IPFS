// SPDX-License-Identifier: MIT
/**
 * Truffle Configuration File
 * This file configures the networks, compiler, and other options for your Truffle project.
 */

const path = require("path");

module.exports = {
  // Default build directory for compiled contracts
  contracts_build_directory: path.join(__dirname, "build/contracts"),

  networks: {
    // Configuration for a local Ganache blockchain instance
    development: {
      host: "127.0.0.1",    // Localhost
      port: 7545,            // Ganache default port
      network_id: "5777", 
      gas: 6721975,    // Match any network id
    },
  },

  // Configure your compilers
  compilers: {
    solc: {
      version: "0.8.20",      // Match the version your contracts use
      settings: {
        optimizer: {
          enabled: true,
          runs: 200
        },
        // ADDED THIS LINE to fix the "invalid opcode" error
        evmVersion: "london"
      }
    }
  },
};