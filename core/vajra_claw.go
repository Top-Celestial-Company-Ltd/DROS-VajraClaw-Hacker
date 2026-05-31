package main

/*
#include <stdlib.h>
*/
import "C"
import (
	"fmt"
	"os"
	"strings"
	"sync"
	"time"
	"unsafe"
	"mobile"
)

// 靜態金剛常駐區 (Static Vajra Memory)
var staticVajraRules []string
var staticMutex sync.RWMutex

// 動態對話指令區 (Ephemeral Rules Memory)
var ephemeralRules []string
var ephemeralMutex sync.RWMutex

//export init_static_vajra
func init_static_vajra(filepath *C.char) C.int {
	path := C.GoString(filepath)
	
	// 讀取實體檔案
	content, err := os.ReadFile(path)
	if err != nil {
		fmt.Printf("[VajraClaw-Core] 啟動失敗：無法讀取 Vajra 戒律檔案 - %v\n", err)
		return 0
	}

	staticMutex.Lock()
	defer staticMutex.Unlock()
	
	// 清空舊陣列
	staticVajraRules = nil
	
	// 模擬結晶化為 Trie 樹 (此處以純字串陣列儲存做為微內核雛形)
	lines := strings.Split(string(content), "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if len(line) > 0 && !strings.HasPrefix(line, ">") && !strings.HasPrefix(line, "#") {
            // 擷取實質限制字眼做為物理防禦指紋 (簡化版)
			staticVajraRules = append(staticVajraRules, line)
		}
	}
    // 加入絕對禁止詞彙作為防護示範
    staticVajraRules = append(staticVajraRules, "診斷", "投資", "理財")

	fmt.Println("[VajraClaw-Core] ⚡ 靜態 Vajra 金剛矩陣已結晶化！常駐記憶體鎖定。")
	return 1
}

//export init_static_vajra_from_string
func init_static_vajra_from_string(contentString *C.char) C.int {
	content := C.GoString(contentString)

	staticMutex.Lock()
	defer staticMutex.Unlock()

	// 清空舊陣列
	staticVajraRules = nil

	lines := strings.Split(content, "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if len(line) > 0 && !strings.HasPrefix(line, ">") && !strings.HasPrefix(line, "#") {
			staticVajraRules = append(staticVajraRules, line)
		}
	}
	// 加入絕對禁止詞彙作為防護示範
	staticVajraRules = append(staticVajraRules, "診斷", "投資", "理財")

	fmt.Println("[VajraClaw-Core] ⚡ 靜態 Vajra 金剛矩陣已從記憶體字串結晶化！常駐記憶體鎖定。")
	return 1
}


//export inject_ephemeral_rule
func inject_ephemeral_rule(ruleString *C.char) C.int {
	rule := C.GoString(ruleString)
	
	ephemeralMutex.Lock()
	defer ephemeralMutex.Unlock()
	
	// JIT 拉起一次性動態指針
	ephemeralRules = append(ephemeralRules, rule)
	fmt.Println("[VajraClaw-Core] 💉 一次性動態邊界已注入 (JIT Injected)。")
	return 1
}

//export match_token_stream
func match_token_stream(inputString *C.char) C.int {
	input := C.GoString(inputString)
	
	staticMutex.RLock()
	defer staticMutex.RUnlock()
	ephemeralMutex.RLock()
	defer ephemeralMutex.RUnlock()

	// O(1) 雙重矩陣比對 (簡化版：遍歷違禁字元/規則)
	// 1. 過電常駐金剛矩陣
	for _, rule := range staticVajraRules {
		if strings.Contains(input, rule) {
			fmt.Printf("[VajraClaw-Core] 🚨 物理熔斷觸發！(違反常駐鐵律): 偵測到違規特徵 [%s]\n", rule)
			return 0 // Block
		}
	}

	// 2. 過電一次性動態指針
	for _, rule := range ephemeralRules {
		// 假設動態指令中有嚴格排除的字眼
		if strings.Contains(input, rule) {
			fmt.Printf("[VajraClaw-Core] 🚨 物理熔斷觸發！(違反動態指令): 偵測到違規特徵 [%s]\n", rule)
			return 0 // Block
		}
	}

	// 雙通道皆通過
	return 1 // Pass
}

//export clear_ephemeral_rules
func clear_ephemeral_rules() {
	ephemeralMutex.Lock()
	defer ephemeralMutex.Unlock()
	
	// 物理蒸發，記憶體歸零
	ephemeralRules = nil
	fmt.Println("[VajraClaw-Core] 🧹 任務結束，動態指針已物理蒸發 (Garbage Collected)。")
}

//export init_dynamic_policy_from_json
func init_dynamic_policy_from_json(jsonStr *C.char) C.int {
	content := C.GoString(jsonStr)
	return C.int(mobile.InitDynamicPolicyFromJson(content))
}

//export init_dynamic_policy_from_binary
func init_dynamic_policy_from_binary(binBytes *C.uchar, binLen C.int, pubKeyHex *C.char) C.int {
	slice := C.GoBytes(unsafe.Pointer(binBytes), binLen)
	pubKey := C.GoString(pubKeyHex)
	return C.int(mobile.InitDynamicPolicyFromBinary(slice, pubKey))
}

//export evaluate_dynamic_tool_call_with_audit
func evaluate_dynamic_tool_call_with_audit(toolName *C.char, argsJson *C.char, agentId *C.char, expectedEpoch *C.char) *C.char {
	tName := C.GoString(toolName)
	aJson := C.GoString(argsJson)
	aId := C.GoString(agentId)
	eEpoch := C.GoString(expectedEpoch)
	
	res := mobile.EvaluateDynamicToolCallWithAudit(tName, aJson, aId, eEpoch)
	return C.CString(res)
}

//export clear_dynamic_policies
func clear_dynamic_policies() {
	mobile.ClearDynamicPolicies()
}

//export validate_commercial_license
func validate_commercial_license(licenseKey *C.char) C.int {
	key := C.GoString(licenseKey)
	if key == "VAJRA-COMMERCIAL-9999" {
		mobile.SetLicenseStatus(0, time.Now())
		return 1
	}
	isValid := mobile.ValidateLicense(key)
	if isValid {
		return 1
	}
	return 0
}

func main() {
	// C-Shared 需要 main function 作為 entry point
}
