const { expect } = require('chai');
const { ethers } = require('hardhat');
const { BigNumber } = require('bignumber.js');

// DEPOSIT, WITHDRAW, LIST, UNLIST, PAY, CONFIRM_RECEPTION
const DEPOSIT_EVENT = 0;
const WITHDRAW_EVENT = 1;
const LIST_EVENT = 2;
const UNLIST_EVENT = 3;
const PAY_EVENT = 4;
const CONFIRM_RECEPTION_EVENT = 5;

// Status Enum
const UNLISTED_STATUS = 0;
const LISTED_STATUS = 1;
const PAID_STATUS = 2;
const WITHDRAWN_STATUS = 3;

INITIAL_BUYER_BALANCE = 1000000;

describe('ONMarket', function () {
  let ONToken;
  let tokenON;
  let tokenONAddress;

  let Market;
  let market;
  let marketAddress;

  let NFTON;
  let nftON;
  let nftONAddress;

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

  // Normal behaviors
  it('Deploy: deployer fee percentage is 1%', async function () {
    let deployerFeePercentage = await market.getPercentageDeployerFee();
    deployerFeePercentage = deployerFeePercentage.toString();
    expect(deployerFeePercentage.toString()).to.equal('1');
  });

  it('Mint: mint NFT to seller account', async function () {
    const [deployer, seller, buyer] = await ethers.getSigners();
    await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0',
      seller.address,
      4,
    );

    const token1Owner = await nftON.ownerOf(1);
    expect(token1Owner.toString()).to.equal(seller.address.toString());
  });

  it('Complete Normal Transaction: deposit, list, pay, confirm, withdraw', async function () {
    // MINT
    const [deployer, seller, buyer] = await ethers.getSigners();
    await tokenON.transfer(buyer.address, INITIAL_BUYER_BALANCE);
    let createToken = await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0',
      seller.address,
      4,
    );
    let tx = await createToken.wait();
    let tokenId = tx.events[0].args[2].toNumber();

    // DEPOSIT
    await nftON.connect(seller).approve(marketAddress, tokenId);
    let deposit = await market.connect(seller).depositItem(nftONAddress, tokenId, seller.address);
    tx = await deposit.wait();
    let marketItemEvent = tx.events.find(
      element => element.hasOwnProperty('event') && element.event == 'MarketItemEvent',
    );
    const itemId = marketItemEvent.args.itemId;

    // check deposit event
    expect(marketItemEvent.args.eventType).to.equal(
      DEPOSIT_EVENT,
      'did not catch deposit event...',
    );

    // check token transfer to market place
    let tokenOwner = await nftON.ownerOf(tokenId);
    expect(tokenOwner.toString()).to.equal(
      marketAddress.toString(),
      'NFT not transfered to market...',
    );

    // LIST
    let listingPrice = 1000;
    let list = await market.connect(seller).listItem(itemId, listingPrice);
    tx = await list.wait();

    marketItemEvent = tx.events.find(
      element => element.hasOwnProperty('event') && element.event == 'MarketItemEvent',
    );

    // check list event
    const price = marketItemEvent.args.price;
    expect(marketItemEvent.args.eventType).to.equal(LIST_EVENT, 'did not catch list event...');

    // PAY
    await tokenON.connect(buyer).approve(marketAddress, price);
    let pay = await market.connect(buyer).payItem(itemId);
    tx = await pay.wait();

    marketItemEvent = tx.events.find(
      element => element.hasOwnProperty('event') && element.event == 'MarketItemEvent',
    );

    // check pay event
    expect(marketItemEvent.args.eventType).to.equal(PAY_EVENT, 'did not catch pay event...');

    // check money transfered to marketplace
    let marketBalance = await tokenON.balanceOf(marketAddress);
    let buyerBalance = await tokenON.balanceOf(buyer.address);
    let initDeployerBalance = await tokenON.balanceOf(deployer.address);

    expect(marketBalance.toNumber()).to.equal(price, 'market did not receive the price');
    expect(buyerBalance.toNumber()).to.equal(
      INITIAL_BUYER_BALANCE - price,
      'price was not reduced from buyer account...',
    );

    // // CONFIRM RECEPTION
    let confirm = await market.connect(buyer).confirmReceptionItem(itemId);
    tx = await confirm.wait();

    marketItemEvent = tx.events.find(
      element => element.hasOwnProperty('event') && element.event == 'MarketItemEvent',
    );

    // check confirmation event
    expect(marketItemEvent.args.eventType).to.equal(
      CONFIRM_RECEPTION_EVENT,
      'did not catch confirm reception event...',
    );
    expect(marketItemEvent.args.owner).to.equal(buyer.address, 'buyer is not the owner...');
    expect(marketItemEvent.args.minter.toString()).to.equal(
      deployer.address.toString(),
      'minter should be deployer',
    );
    expect(marketItemEvent.args.price).to.equal(0, 'price should be reset to 0...');
    expect(marketItemEvent.args.status).to.equal(UNLISTED_STATUS, 'status should be unlisted...');

    let marketPercentageFee = await market.getPercentageDeployerFee();
    let minterPercentageFee = marketItemEvent.args.percentageRoyalty;

    // check money transfered from marketplace to seller - fee
    marketBalance = await tokenON.balanceOf(marketAddress);
    let sellerBalance = await tokenON.balanceOf(seller.address);
    let finalDeployerBalance = await tokenON.balanceOf(deployer.address);
    let effectiveDeployerGains = BigNumber(finalDeployerBalance.toString()).minus(
      BigNumber(initDeployerBalance.toString()),
    );

    let expectedDeployerGains =
      ((marketPercentageFee.toNumber() + minterPercentageFee.toNumber()) / 100) * price.toNumber();

    expect(marketBalance.toNumber()).to.equal(0, 'market should not have money left...');
    expect(sellerBalance.toNumber()).to.equal(
      price.toNumber() - expectedDeployerGains,
      'seller should have initial 0.95 * initial price...',
    );
    expect(effectiveDeployerGains.toNumber()).to.equal(
      expectedDeployerGains,
      'deployer did not receive fee...',
    );

    // WITHDRAW
    let withdraw = await market.connect(buyer).withdrawItem(itemId);
    tx = await withdraw.wait();
    marketItemEvent = tx.events.find(
      element => element.hasOwnProperty('event') && element.event == 'MarketItemEvent',
    );

    // check deposit event
    expect(marketItemEvent.args.eventType).to.equal(
      WITHDRAW_EVENT,
      'did not catch withdraw event...',
    );
    expect(marketItemEvent.args.status).to.equal(WITHDRAWN_STATUS, 'status should be withdrawn...');

    // check token transfer to market place
    tokenOwner = await nftON.ownerOf(tokenId);
    expect(tokenOwner.toString()).to.equal(
      buyer.address.toString(),
      'NFT not transfered to owner...',
    );
  });

  it('Withdraw: deposit a withdrawn item should keep the same itemId', async function () {
    // MINT
    const [deployer, seller, buyer] = await ethers.getSigners();
    await tokenON.transfer(buyer.address, INITIAL_BUYER_BALANCE);
    let createToken = await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0',
      seller.address,
      4,
    );
    let tx = await createToken.wait();
    let tokenId = tx.events[0].args[2].toNumber();

    // DEPOSIT
    await nftON.connect(seller).approve(marketAddress, tokenId);
    let deposit = await market.connect(seller).depositItem(nftONAddress, tokenId, seller.address);
    tx = await deposit.wait();
    let marketItemEvent = tx.events.find(
      element => element.hasOwnProperty('event') && element.event == 'MarketItemEvent',
    );
    const previousItemId = marketItemEvent.args.itemId;

    // WITHDRAW
    let withdraw = await market.connect(seller).withdrawItem(previousItemId);
    tx = await withdraw.wait();
    marketItemEvent = tx.events.find(
      element => element.hasOwnProperty('event') && element.event == 'MarketItemEvent',
    );

    // check token transfer to market place
    tokenOwner = await nftON.ownerOf(tokenId);
    expect(tokenOwner.toString()).to.equal(
      seller.address.toString(),
      'NFT not transfered to owner...',
    );

    // // DEPOSIT
    await nftON.connect(seller).approve(marketAddress, tokenId);
    deposit = await market.connect(seller).depositItem(nftONAddress, tokenId, seller.address);
    tx = await deposit.wait();
    marketItemEvent = tx.events.find(
      element => element.hasOwnProperty('event') && element.event == 'MarketItemEvent',
    );
    const afterItemId = marketItemEvent.args.itemId;

    expect(previousItemId).to.equal(afterItemId, 'deposit Id changed after redepositing');
  });

  it('Pay: Pay listed item', async function () {
    // TODO
  });

  it('Unlist: unlist item', async function () {
    // TODO
  });

  it("Confirmation: buyer confirms item's reception", async function () {
    // TODO
  });

  it('Withdraw: withdraw token from the market', async function () {
    // TODO
  });

  // Edge Cases Deposit
  it('Deposit: fail to approve token not owned by sender', async function () {
    const [deployer, seller, buyer] = await ethers.getSigners();
    await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0',
      seller.address,
      4,
    );

    await expect(nftON.connect(buyer).approve(marketAddress, 1)).to.be.revertedWith(
      'ERC721: approve caller is not owner nor approved for all',
    );
  });

  it('Deposit: fail to deposit token not owned by sender', async function () {
    const [deployer, seller, buyer] = await ethers.getSigners();
    await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0',
      seller.address,
      4,
    );

    await nftON.connect(seller).approve(marketAddress, 1);

    await expect(
      market.connect(buyer).depositItem(nftONAddress, 1, buyer.address),
    ).to.be.revertedWith('ERC721: transfer of token that is not own');
  });

  // TODO: add deposit cases with new owner

  // Edge Cases List
  it('List: fail to list item not deposited', async function () {
    // TODO
  });

  it('List: fail to list item not owned', async function () {
    // TODO
  });

  it('List: fail to list with price == 0', async function () {
    // TODO
  });
  // Edge Cases Payment

  // Edge Cases Unlist

  // Edge Cases Confirmation

  // Edge Cases Withdraw

  // Get Market Data
  it('Market Data: get all items', async function () {
    // TODO
    const [deployer, seller, buyer] = await ethers.getSigners();
    await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0',
      seller.address,
      4,
    );
    await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/1',
      seller.address,
      4,
    );

    await nftON.connect(seller).approve(marketAddress, 1);
    await nftON.connect(seller).approve(marketAddress, 2);

    await market.connect(seller).depositItem(nftONAddress, 1, seller.address);
    await market.connect(seller).depositItem(nftONAddress, 2, seller.address);

    const allItems = await market.getItemsByStatus(0);
    expect(allItems[1]['owner'].toString()).to.equal(seller.address, 'owner is not correct...');
  });

  it('Market Data: get my items', async function () {
    // TODO
    const [deployer, seller, buyer] = await ethers.getSigners();
    await tokenON.transfer(buyer.address, INITIAL_BUYER_BALANCE);
    await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/0',
      seller.address,
      4,
    );
    await nftON.createToken(
      'ipfs://QmZvbEoE8HMqv1sufRQRDYjzKhm4VnuTyCPVzoHtnoJQqq/1',
      seller.address,
      4,
    );

    await nftON.connect(seller).approve(marketAddress, 1);
    await nftON.connect(seller).approve(marketAddress, 2);

    await market.connect(seller).depositItem(nftONAddress, 1, seller.address);
    await market.connect(seller).depositItem(nftONAddress, 2, seller.address);

    let allItems = await market.connect(seller).getMyItems();
    expect(allItems.length).to.equal(2, 'did not return the right number of items owned...');

    const price1 = 500;

    let list = await market.connect(seller).listItem(1, price1);
    tx = await list.wait();

    await tokenON.connect(buyer).approve(marketAddress, price1);
    let pay = await market.connect(buyer).payItem(1);
    tx = await pay.wait();

    allItems = await market.connect(buyer).getMyItems();
    expect(allItems.length).to.equal(1, 'did not return the right number of items owned...');
    console.log(allItems[0].owner);
  });
});
