### LinageeNames related projects

### OGRunner.py LNR (.og) GlobalReg front runner

### LNRWrapper Free 0% ERC721A based wrapper for ".og" names
Features:  
  
ERC721A for cheaper bulk minting etc.  
Bulk minting.    
Bulk searching.  
Wrapping.  
Unwrapping - when a name is unwrapped its erc721 is non-transferable.  
Get Name by tokenId.  
Get TokenId by Name.  
Get NameHash (bytes32 hash) for a name.  

### LNRFront: React frontend for wrapping/minting erc721a versions of ".og" names
metadata for new mints is hosted on an EC2 currently.
metadata python script in metadata/


### The bad on LNR
No front running protection makes LNR vulnerable to hostage styled front running.  

Bytes32 type used in the Contract for _name means names cant be > 32bytes (no long emoji names).  

There is no extension associated with the project (such as .og). This is a major fault for a naming system.
This allows users to register existing TLD / extensions for impersonation, spams, squatting.
