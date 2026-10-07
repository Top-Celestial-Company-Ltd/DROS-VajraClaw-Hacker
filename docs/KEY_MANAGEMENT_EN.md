# VajraClaw Hacker Edition - Key Management & Backup Guide (KEY_MANAGEMENT_EN.md)

This guide is designed for **individual developers and security researchers (Solo Developers / Hackers)**. In local and lightweight development environments, DROS / VajraClaw isolates policy signing from runtime verification to protect your system. To prevent accidental security lockouts or system meltdowns during policy updates, follow this guide to manage and back up your Ed25519 signing keys.

> [!CAUTION]
> **Core Security Declaration: No Backdoors & No Key Recovery Mechanism**
> * **No Vendor Assistance for Recovery**: DROS / VajraClaw strictly adheres to zero-trust security principles. **No master recovery keys or backdoors are built into the system**. If you lose your private key seed (Seed Hex), **the vendor (DROS) cannot recover it or sign new `policy.bin` files on your behalf**.
> * **Sole Recovery Path**: You must manually execute the "Trust Anchor Reconstruction" procedure (see Section 3, Scenario B). This requires administrative control (SSH/Root access) over your deployed servers to generate a new key pair and manually update the verification public key configuration on all execution nodes. If you lose both your private key and server access, the system will be permanently locked and cannot be upgraded.

---

## 1. Why Should Solo Developers Back Up Their Private Keys?

VajraClaw relies on asymmetric cryptography:
* **Signing Phase (Your Dev Machine)**: Holds the **Private Key Seed (Seed Hex)** to sign policy YAML and compile it into a binary `policy.bin`.
* **Execution Phase (AI Runtime / Proxy)**: Holds only the **Verification Public Key (PubKey Hex)** to check the integrity of `policy.bin`.

If you do not specify a `--key` during compilation, the compiler defaults to generating a random **Ephemeral Key**, which will render previous GuardVM configurations invalid upon the next compilation. To ensure stable policy updates, you **must use a static key**.

If you lose this static private key, you will not be able to upgrade your policies without modifying the public key stored on the server.

---

## 2. Key Generation & Backup in 3 Steps

### Step 1: Generate a Static Keypair
Run this Python snippet on your development machine to generate a permanent key pair:
```python
import nacl.signing
import binascii

# Generate a signing key seed
signing_key = nacl.signing.SigningKey.generate()
seed_hex = binascii.hexlify(signing_key.encode()).decode('utf-8')
pub_hex = binascii.hexlify(signing_key.verify_key.encode()).decode('utf-8')

print(f"Save this Private Key Seed (32-byte Seed Hex): {seed_hex}")
print(f"Deploy this Verification Public Key (PubKey Hex) : {pub_hex}")
```

### Step 2: Secure Backup (Recommended for Solo Developers)
* **Password Manager**: Copy the `Seed Hex` and save it inside your local password manager (e.g., KeePass, Bitwarden, 1Password) as a secure note.
* **Prevent Git Leaks**: Do not hardcode the key seed inside your public repository. Configure it via environment variables instead.

### Step 3: Compile with the Key
When building your safety contract, supply the key seed via the `--key` flag:
```bash
python cli.py build contracts/demo_policy.yaml -o policy.bin --key <YOUR_SEED_HEX>
```

---

## 3. Disaster Recovery SOP

When your development workstation fails but you need to release a policy update:

### Scenario A: Private Key Seed is Backed Up (Recommended)
1. Install Python and dependencies on the new build machine: `pip install pynacl pyyaml`.
2. Retrieve the `Seed Hex` from your password manager.
3. Re-run the compilation command using the `--key` flag.
4. Overwrite the old `policy.bin` on your execution side. The GuardVM will verify it successfully with no configuration changes required.

### Scenario B: Private Key Seed is Lost (Reconstruction)
1. Generate a new `NEW_SEED` and `NEW_PUBKEY` following Step 1.
2. Compile the policy YAML using `NEW_SEED`.
3. Log into your runtime server, and update the verification public key in your initialization script or config (e.g., `gemini_proxy.py`) with `NEW_PUBKEY`.
4. Securely store `NEW_SEED` in your password manager.
5. Restart your proxy/daemon to reload the new verification public key and policy.
