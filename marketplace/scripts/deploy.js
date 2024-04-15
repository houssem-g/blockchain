const hre = require('hardhat');
const keccak256 = require('keccak256');

const seller = '0x70997970C51812dc3A010C7d01b50e0d17dc79C8';
const buyer = '0x3c44cdddb6a900fa2b585dd299e03d12fa4293bc';
const brand = '0x90F79bf6EB2c4f870365E785982E1f101E93b906';

async function main() {
  const ONToken = await hre.ethers.getContractFactory('ONLimitedToken');
  const tokenON = await ONToken.deploy();
  await tokenON.deployed();

  const buyerMoney = ethers.utils.parseUnits('100000', 'ether');

  await tokenON.transfer(buyer, buyerMoney);

  console.log('ONLimitedToken deployed to:', tokenON.address);

  const tokenONAddress = tokenON.address;
  const ONMarket = await hre.ethers.getContractFactory('ONMarket');
  const onMarket = await ONMarket.deploy(tokenONAddress);
  await onMarket.deployed();

  console.log('ONMarket deployed to:', onMarket.address);

  const NFTON = await hre.ethers.getContractFactory('ONLimitedNFT');
  const nftON = await NFTON.deploy(onMarket.address);
  await nftON.deployed();

  // await nftON.grantRole(keccak256('MINTER_ROLE'), brand)
  await nftON.addMinter(brand, 'Brand Lux');

  console.log('NFTON deployed to:', nftON.address);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
