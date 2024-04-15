require("@nomiclabs/hardhat-waffle");
const fs = require("fs")
const privateKey = fs.readFileSync(".secret").toString()
const onlimitedId = "aa6e004788dc4529a1a9527bcffb4d10"

module.exports = {
  networks: {
    hardhat: {
      chainId: 1337,
    },
    mumbai: {
      url: `https://polygon-mumbai.infura.io/v3/${onlimitedId}`,
      accounts: [privateKey]
    },
    mainnet: {
      url: `https://polygon-mainnet.infura.io/v3/${onlimitedId}`,
      accounts: [privateKey]
    },
  },
  solidity: "0.8.9",
};
