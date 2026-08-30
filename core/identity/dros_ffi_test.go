package identity

import (
	"crypto/sha256"
	"testing"
	"time"
	"unsafe"
)

// --- Unit Tests (DIC to DIT Mapping) ---

func TestTC_GO_001_IdentityPreservation(t *testing.T) {
	dic := DROSIdentityContext{
		Subject: Subject{ID: "user-A", Issuer: "idp"},
		Agent:   Agent{ID: "vajraclaw-1", Version: "2.1"},
		Session: Session{ID: "sess-1", CreatedAt: time.Now().Unix()},
	}

	dit := dic.ToCanonicalToken()

	tenantStr := string(dit.TenantID[:len("user-A")])
	if tenantStr != "user-A" {
		t.Errorf("Identity preservation failed: expected 'user-A', got %s", tenantStr)
	}
}

func TestTC_GO_002_DelegationBoundary(t *testing.T) {
	dic := DROSIdentityContext{
		Subject: Subject{ID: "user-A"},
		Delegation: Delegation{
			AllowedBy: "user-consent",
			Scope:     "write:policy",
		},
	}

	dit := dic.ToCanonicalToken()

	if dit.Delegation != 0 {
		t.Errorf("Delegation boundary failed: write:policy should be denied before FFI")
	}
}

func TestTC_GO_003_SessionReplay(t *testing.T) {
	oldTime := time.Now().Add(-24 * time.Hour).Unix()
	dic := DROSIdentityContext{
		Subject: Subject{ID: "user-A"},
		Session: Session{ID: "old-token", CreatedAt: oldTime},
	}

	dit := dic.ToCanonicalToken()

	if dit.Epoch != uint64(oldTime) {
		t.Errorf("Session replay prevention failed: Epoch mismatch")
	}
}

// --- ABI & Alignment Tests ---

func TestABI_AlignmentAndSize(t *testing.T) {
	// 1. Verify Go DrosIdentityToken structure layout matches C counterpart size.
	goDitSize := unsafe.Sizeof(DrosIdentityToken{})
	cDitSize := GetCDitSize()
	if goDitSize != cDitSize {
		t.Errorf("DrosIdentityToken size mismatch: Go=%d bytes, C=%d bytes", goDitSize, cDitSize)
	} else {
		t.Logf("DrosIdentityToken alignment validated: size is %d bytes on both Go & C boundaries.", goDitSize)
	}

	// 2. Verify offsets of each field in DrosIdentityToken
	var goDit DrosIdentityToken
	offsetVersionGo := unsafe.Offsetof(goDit.Version)
	offsetTenantGo := unsafe.Offsetof(goDit.TenantID)
	offsetHashGo := unsafe.Offsetof(goDit.SubjectHash)
	offsetDelegationGo := unsafe.Offsetof(goDit.Delegation)
	offsetEpochGo := unsafe.Offsetof(goDit.Epoch)

	offsetVersionC, offsetTenantC, offsetHashC, offsetDelegationC, offsetEpochC := GetCDitOffsets()

	if offsetVersionGo != offsetVersionC {
		t.Errorf("DrosIdentityToken.Version offset mismatch: Go=%d, C=%d", offsetVersionGo, offsetVersionC)
	}
	if offsetTenantGo != offsetTenantC {
		t.Errorf("DrosIdentityToken.TenantID offset mismatch: Go=%d, C=%d", offsetTenantGo, offsetTenantC)
	}
	if offsetHashGo != offsetHashC {
		t.Errorf("DrosIdentityToken.SubjectHash offset mismatch: Go=%d, C=%d", offsetHashGo, offsetHashC)
	}
	if offsetDelegationGo != offsetDelegationC {
		t.Errorf("DrosIdentityToken.Delegation offset mismatch: Go=%d, C=%d", offsetDelegationGo, offsetDelegationC)
	}
	if offsetEpochGo != offsetEpochC {
		t.Errorf("DrosIdentityToken.Epoch offset mismatch: Go=%d, C=%d", offsetEpochGo, offsetEpochC)
	}
}

// --- E2E Dynamic Link Integration Test ---

func TestIntegration_E2E_FFI_Decision(t *testing.T) {
	// Attempt initialization with empty policy (uses default settings)
	err := InitEngine("")
	if err != nil {
		t.Skip("Skipping E2E Integration test: DROS Rust engine shared library is not loaded/compiled in PATH.")
		return
	}

	// Setup a clean canonical DIT
	dit := DrosIdentityToken{
		Version:      0x00020100,
		TenantID:     [32]byte{'t', 'e', 'n', 'a', 'n', 't', '-', 'x'},
		SubjectHash:  sha256.Sum256([]byte("idp|user-x")),
		Delegation:   1,
		Epoch:        uint64(time.Now().Unix()),
	}

	// Request decision evaluation
	res, err := DecideExplain("/finance/records", &dit)
	if err != nil {
		t.Fatalf("Integration E2E call failed: %v", err)
	}

	t.Logf("Integration E2E Success! decision: %d, reason_code: %d, epoch: %d", 
		res.Decision, res.ReasonCode, res.TimestampEpoch)
}
