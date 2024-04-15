const { expect } = require('chai');
const { ethers } = require('hardhat');
const keccak256 = require('keccak256');

describe('ONLimitedNFT', function () {
  let ONToken;
  let tokenON;
  let tokenONAddress;

  let Market;
  let market;
  let marketAddress;

  let NFTON;
  let nftON;
  let nftONAddress;

  const adminRoleBytes = '0x0000000000000000000000000000000000000000000000000000000000000000';

  beforeEach(async function () {
    ONToken = await ethers.getContractFactory('ONLimitedToken');
    tokenON = await ONToken.deploy();
    await tokenON.deployed();
    tokenONAddress = tokenON.address;

    Market = await ethers.getContractFactory('ONMarket');
    market = await Market.deploy(tokenONAddress);
    await market.deployed();
    marketAddress = market.address;

    NFTON = await ethers.getContractFactory('ONLimitedNFT');
    nftON = await NFTON.deploy(marketAddress);
    await nftON.deployed();
    nftONAddress = nftON.address;
  });

  it('Mint: mint NFT from admin to seller account', async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();
    await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0',
      seller.address,
      4,
    );

    const token1Owner = await nftON.ownerOf(1);
    const tokenMinter = await nftON.tokenMinterAddress(1);
    const tokenPercentageRoyalty = await nftON.tokenPercentageRoyalty(1);

    expect(token1Owner.toString()).to.equal(seller.address.toString());
    expect(tokenMinter.toString()).to.equal(deployer.address.toString());
    expect(tokenPercentageRoyalty).to.equal(4);
  });

  it('Mint: fail to mint if not minter role', async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();

    await expect(
      nftON
        .connect(seller)
        .createToken('ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0', seller.address, 4),
    ).to.be.revertedWith('Caller is not a minter');
  });

  it('Grant Minter Role: fail grand minter role if not admin', async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();

    await expect(
      nftON.connect(seller).grantRole(keccak256('MINTER_ROLE'), seller.address),
    ).to.be.revertedWith(
      'AccessControl: account ' +
        seller.address.toLowerCase() +
        ' is missing role ' +
        adminRoleBytes,
    );

    await expect(
      nftON
        .connect(seller)
        .createToken('ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0', seller.address, 4),
    ).to.be.revertedWith('Caller is not a minter');
  });

  it('Grant Minter Role: grant minter role to brand then mint NFT to seller account', async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();
    await nftON.connect(deployer).grantRole(keccak256('MINTER_ROLE'), brand.address);
    await nftON
      .connect(brand)
      .createToken('ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0', seller.address, 4);

    const token1Owner = await nftON.ownerOf(1);
    expect(token1Owner.toString()).to.equal(seller.address.toString());
  });

  it('Grant Minter Role: minter account fails to grant minter role to other account', async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();
    await nftON.connect(deployer).grantRole(keccak256('MINTER_ROLE'), brand.address);

    await expect(
      nftON.connect(brand).grantRole(keccak256('MINTER_ROLE'), seller.address),
    ).to.be.revertedWith(
      'AccessControl: account ' +
        brand.address.toLowerCase() +
        ' is missing role ' +
        adminRoleBytes,
    );
  });

  it("Revoke Minter Role: Account can't mint anymore after minter role is revoked", async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();
    await nftON.connect(deployer).grantRole(keccak256('MINTER_ROLE'), brand.address);
    await nftON
      .connect(brand)
      .createToken('ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0', seller.address, 4);

    await nftON.connect(deployer).revokeRole(keccak256('MINTER_ROLE'), brand.address);

    await expect(
      nftON
        .connect(brand)
        .createToken('ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/1', seller.address, 4),
    ).to.be.revertedWith('Caller is not a minter');
  });

  it('Revoke Minter Role: Only admin can revoke minter role', async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();
    await nftON.connect(deployer).grantRole(keccak256('MINTER_ROLE'), brand.address);

    await expect(
      nftON.connect(seller).revokeRole(keccak256('MINTER_ROLE'), brand.address),
    ).to.be.revertedWith(
      'AccessControl: account ' +
        seller.address.toLowerCase() +
        ' is missing role ' +
        adminRoleBytes,
    );
  });

  it('Revoke Minter Role: minter can renounce his role', async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();
    await nftON.connect(deployer).grantRole(keccak256('MINTER_ROLE'), brand.address);

    await nftON.connect(brand).renounceRole(keccak256('MINTER_ROLE'), brand.address);

    await expect(
      nftON
        .connect(brand)
        .createToken('ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/1', seller.address, 4),
    ).to.be.revertedWith('Caller is not a minter');
  });

  it('Revoke Minter Role: only minter can renounce his role', async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();
    await nftON.connect(deployer).grantRole(keccak256('MINTER_ROLE'), brand.address);

    await expect(
      nftON.connect(seller).renounceRole(keccak256('MINTER_ROLE'), brand.address),
    ).to.be.revertedWith('AccessControl: can only renounce roles for self');

    await nftON
      .connect(brand)
      .createToken('ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/1', seller.address, 4);
  });

  it('Check Role: get if account is admin, minter or user', async function () {
    const [deployer, brand, seller, buyer] = await ethers.getSigners();
    await nftON.connect(deployer).grantRole(keccak256('MINTER_ROLE'), brand.address);

    const deployerIsAdmin = await nftON.connect(buyer).hasRole(adminRoleBytes, deployer.address);
    const deployerIsMinter = await nftON
      .connect(buyer)
      .hasRole(keccak256('MINTER_ROLE'), deployer.address);

    const brandIsAdmin = await nftON.connect(buyer).hasRole(adminRoleBytes, brand.address);
    const brandIsMinter = await nftON
      .connect(buyer)
      .hasRole(keccak256('MINTER_ROLE'), brand.address);

    const sellerIsAdmin = await nftON.connect(buyer).hasRole(adminRoleBytes, seller.address);
    const sellerIsMinter = await nftON
      .connect(buyer)
      .hasRole(keccak256('MINTER_ROLE'), seller.address);

    await expect(deployerIsAdmin && deployerIsMinter && brandIsMinter).true;
    await expect(brandIsAdmin && sellerIsAdmin && sellerIsMinter).false;
  });
});
