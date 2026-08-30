package identity

import (
    "crypto/sha256"
)

// DrosIdentityToken (DIT) must match Rust struct exactly.
// This is the Layer B Runtime Identity Token.
type DrosIdentityToken struct {
    Version      uint32
    TenantID     [32]byte
    SubjectHash  [32]byte
    Delegation   uint64
    Epoch        uint64
}

// ToCanonicalToken transforms the complex DIC into the flat binary DIT for the microkernel.
func (dic *DROSIdentityContext) ToCanonicalToken() DrosIdentityToken {
    var dit DrosIdentityToken
    dit.Version = 0x00020100

    // tenant_id: Map Subject ID or Tenant directly into [32]byte
    copy(dit.TenantID[:], []byte(dic.Subject.ID))

    // subject_hash: Hash of (issuer + id)
    subData := []byte(dic.Subject.Issuer + "|" + dic.Subject.ID)
    dit.SubjectHash = sha256.Sum256(subData)

    // delegation: Encode simple scope rules. 
    // In TC-GO-002, trying to "write:policy" is denied early by Adapter or marked as invalid delegation.
    if dic.Delegation.Scope == "write:policy" {
        dit.Delegation = 0 // Denied scope
    } else {
        dit.Delegation = 1 // Read/other allowed scope
    }

    // epoch: Session creation time, used for replay protection
    dit.Epoch = uint64(dic.Session.CreatedAt)

    return dit
}
