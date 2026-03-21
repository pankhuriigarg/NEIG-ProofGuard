// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EvidenceStorage {
    
    struct Evidence {
        string fileHash;
        string fileName;
        uint256 timestamp;
        address uploadedBy;
    }
    
    struct CustodyRecord {
        string fromCustodian;
        string toCustodian;
        uint256 timestamp;
        string remarks;
    }
    
    mapping(string => Evidence) private evidenceRecords;
    mapping(string => CustodyRecord[]) private custodyChain;
    mapping(string => bool) private caseExists;
    string[] private allCases;
    
    event EvidenceStored(string caseId, string fileHash, string fileName, uint256 timestamp);
    event CustodyTransferred(string caseId, string from, string to, uint256 timestamp);
    
    function storeEvidence(
        string memory caseId,
        string memory fileHash,
        string memory fileName,
        string memory investigatorName
    ) public {
        evidenceRecords[caseId] = Evidence(
            fileHash,
            fileName,
            block.timestamp,
            msg.sender
        );
        
        custodyChain[caseId].push(CustodyRecord(
            "Evidence Collected",
            investigatorName,
            block.timestamp,
            "Initial evidence collection"
        ));
        
        if (!caseExists[caseId]) {
            allCases.push(caseId);
            caseExists[caseId] = true;
        }
        
        emit EvidenceStored(caseId, fileHash, fileName, block.timestamp);
    }
    
    function transferCustody(
        string memory caseId,
        string memory fromCustodian,
        string memory toCustodian,
        string memory remarks
    ) public {
        custodyChain[caseId].push(CustodyRecord(
            fromCustodian,
            toCustodian,
            block.timestamp,
            remarks
        ));
        
        emit CustodyTransferred(caseId, fromCustodian, toCustodian, block.timestamp);
    }
    
    function verifyEvidence(
        string memory caseId,
        string memory fileHash
    ) public view returns (bool) {
        return keccak256(bytes(evidenceRecords[caseId].fileHash)) == 
               keccak256(bytes(fileHash));
    }
    
    function getEvidence(
        string memory caseId
    ) public view returns (string memory, string memory, uint256) {
        Evidence memory e = evidenceRecords[caseId];
        return (e.fileHash, e.fileName, e.timestamp);
    }
    
    function getCustodyCount(
        string memory caseId
    ) public view returns (uint256) {
        return custodyChain[caseId].length;
    }
    
    function getCustodyRecord(
        string memory caseId,
        uint256 index
    ) public view returns (string memory, string memory, uint256, string memory) {
        CustodyRecord memory c = custodyChain[caseId][index];
        return (c.fromCustodian, c.toCustodian, c.timestamp, c.remarks);
    }
    
    function getCaseCount() public view returns (uint256) {
        return allCases.length;
    }
    
    function getCaseId(uint256 index) public view returns (string memory) {
        return allCases[index];
    }
}