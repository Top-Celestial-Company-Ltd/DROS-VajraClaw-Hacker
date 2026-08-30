package identity

/*
#cgo linux LDFLAGS: -L/opt/dros_build -ldros_core_rs -ldl -lpthread -lm
#cgo windows LDFLAGS: -LE:/dev_tools/dros_build -ldros_core_rs -lws2_32 -luserenv -lbcrypt -lntdll
#include <stdint.h>
#include <stdlib.h>

struct DrosIdentityToken {
    uint32_t version;
    uint8_t tenant_id[32];
    uint8_t subject_hash[32];
    uint64_t delegation;
    uint64_t epoch;
} __attribute__((aligned(8)));

struct DrosDecisionResult {
    uint32_t abi_version;
    uint32_t decision;
    uint64_t rule_id;
    uint32_t reason_code;
    uint32_t policy_version;
    uint8_t trace_id[16];
    uint64_t timestamp_epoch;
    uint8_t reserved[16];
} __attribute__((aligned(8)));

int dros_v2_init(const char* policy_path);
int dros_v2_decide_explain(const char* resource_uri, const struct DrosIdentityToken* dit, struct DrosDecisionResult* out_result);
*/
import "C"
import (
	"errors"
	"unsafe"
)

// DrosDecisionResult maps to the C.struct_DrosDecisionResult but is Go-native,
// avoiding CGO import limitations in test files.
type DrosDecisionResult struct {
	ABIVersion     uint32
	Decision       uint32
	RuleID         uint64
	ReasonCode     uint32
	PolicyVersion  uint32
	TraceID        [16]byte
	TimestampEpoch uint64
	Reserved       [16]byte
}

// InitEngine initializes the Rust DROS engine.
func InitEngine(policyPath string) error {
	var cPath *C.char
	if policyPath != "" {
		cPath = C.CString(policyPath)
		defer C.free(unsafe.Pointer(cPath))
	}

	res := C.dros_v2_init(cPath)
	if res < 0 && res != -4 { // -4 is ALREADY_INIT
		return errors.New("failed to initialize DROS engine")
	}
	return nil
}

// DecideExplain routes the canonical DIT token to the Rust microkernel.
func DecideExplain(resourceURI string, dit *DrosIdentityToken) (*DrosDecisionResult, error) {
	cURI := C.CString(resourceURI)
	defer C.free(unsafe.Pointer(cURI))

	var cDit C.struct_DrosIdentityToken
	cDit.version = C.uint32_t(dit.Version)
	for i := 0; i < 32; i++ {
		cDit.tenant_id[i] = C.uint8_t(dit.TenantID[i])
		cDit.subject_hash[i] = C.uint8_t(dit.SubjectHash[i])
	}
	cDit.delegation = C.uint64_t(dit.Delegation)
	cDit.epoch = C.uint64_t(dit.Epoch)

	var outResult C.struct_DrosDecisionResult

	res := C.dros_v2_decide_explain(cURI, &cDit, &outResult)
	if res < 0 {
		return nil, errors.New("DROS FFI execution failed")
	}

	return &DrosDecisionResult{
		ABIVersion:     uint32(outResult.abi_version),
		Decision:       uint32(outResult.decision),
		RuleID:         uint64(outResult.rule_id),
		ReasonCode:     uint32(outResult.reason_code),
		PolicyVersion:  uint32(outResult.policy_version),
		TraceID:        *(*[16]byte)(unsafe.Pointer(&outResult.trace_id)),
		TimestampEpoch: uint64(outResult.timestamp_epoch),
		Reserved:       *(*[16]byte)(unsafe.Pointer(&outResult.reserved)),
	}, nil
}

// GetCDitSize returns the size of C.struct_DrosIdentityToken.
func GetCDitSize() uintptr {
	return unsafe.Sizeof(C.struct_DrosIdentityToken{})
}

// GetCDecResultSize returns the size of C.struct_DrosDecisionResult.
func GetCDecResultSize() uintptr {
	return unsafe.Sizeof(C.struct_DrosDecisionResult{})
}

// GetCDitOffsets returns the offsets of C.struct_DrosIdentityToken fields.
func GetCDitOffsets() (uintptr, uintptr, uintptr, uintptr, uintptr) {
	var cDit C.struct_DrosIdentityToken
	return unsafe.Offsetof(cDit.version),
		unsafe.Offsetof(cDit.tenant_id),
		unsafe.Offsetof(cDit.subject_hash),
		unsafe.Offsetof(cDit.delegation),
		unsafe.Offsetof(cDit.epoch)
}
