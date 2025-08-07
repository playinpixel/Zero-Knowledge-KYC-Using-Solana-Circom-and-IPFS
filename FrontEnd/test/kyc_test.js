const KYCContract = artifacts.require("KYCContract");

contract("KYCContract", (accounts) => {
  let kycInstance;
  const [owner, user] = accounts;

  before(async () => {
    kycInstance = await KYCContract.deployed();
  });

  it("should set owner correctly", async () => {
    assert.equal(await kycInstance.owner(), owner);
  });

  it("should store and verify KYC data", async () => {
    const ipfsHash = "QmXYZ...";
    const age = 25;
    
    await kycInstance.storeKYC(user, ipfsHash, age, { from: owner });
    const isVerified = await kycInstance.verifyAge(user);
    
    assert.isTrue(isVerified);
  });
});