pragma circom 2.0.0;

template HashCheck() {
    // Private input — actual hash value
    signal input hash;
    
    // Public input — expected hash
    signal input expectedHash;
    
    // Constraint — hash equal hona chahiye
    hash === expectedHash;
}

component main {public [expectedHash]} = HashCheck();