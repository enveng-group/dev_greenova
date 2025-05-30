#!/usr/bin/env python3
"""
SSH-keygen wrapper for Dropbear compatibility.

Provides ssh-keygen compatibility using Dropbear tools and Python.
Handles key generation, public key extraction, and SSH signing operations
including Git signature verification.

Author: Adrian Gallo
Email: agallo@enveng-group.com.au
License: AGPL-3.0
"""

import argparse
import base64
import hashlib
import os
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import hashes
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False


def load_openssh_ed25519_private_key(key_file: str) -> Optional[ed25519.Ed25519PrivateKey]:
    """Load an Ed25519 private key from OpenSSH format.
    
    Args:
        key_file: Path to the OpenSSH private key file.
        
    Returns:
        Ed25519PrivateKey instance or None if failed.
    """
    if not CRYPTOGRAPHY_AVAILABLE:
        return None
    
    try:
        with open(key_file, 'rb') as f:
            private_key = serialization.load_ssh_private_key(
                f.read(),
                password=None,  # Assuming no passphrase for dev keys
            )
        
        if isinstance(private_key, ed25519.Ed25519PrivateKey):
            return private_key
        else:
            return None
    except Exception as e:
        print(f"Error loading Ed25519 private key: {e}", file=sys.stderr)
        return None


def create_real_ed25519_signature(private_key: ed25519.Ed25519PrivateKey, data_to_sign: bytes) -> bytes:
    """Create a real Ed25519 signature.
    
    Args:
        private_key: Ed25519 private key.
        data_to_sign: Data to sign.
        
    Returns:
        64-byte Ed25519 signature.
    """
    return private_key.sign(data_to_sign)


def verify_real_ed25519_signature(public_key_line: str, signature: bytes, data: bytes) -> bool:
    """Verify a real Ed25519 signature.
    
    Args:
        public_key_line: SSH public key line.
        signature: Ed25519 signature bytes.
        data: Original data that was signed.
        
    Returns:
        True if signature is valid, False otherwise.
    """
    if not CRYPTOGRAPHY_AVAILABLE:
        return False
    
    try:
        # Parse the public key
        parts = public_key_line.strip().split(' ')
        if len(parts) < 2 or parts[0] != 'ssh-ed25519':
            return False
        
        key_data_b64 = parts[1]
        key_data = base64.b64decode(key_data_b64)
        
        # SSH wire format: string "ssh-ed25519" + 32-byte public key
        # Skip the first 4+11=15 bytes (length + "ssh-ed25519")
        if len(key_data) < 51:  # 4 + 11 + 4 + 32
            return False
        
        # Extract the 32-byte Ed25519 public key (skip SSH wire format header)
        public_key_bytes = key_data[19:51]  # Skip 4+11+4 bytes
        
        # Create Ed25519PublicKey object
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        
        # Verify the signature
        public_key.verify(signature, data)
        return True
        
    except Exception as e:
        print(f"Error verifying Ed25519 signature: {e}", file=sys.stderr)
        return False


def ssh_encode_string(data: bytes) -> bytes:
    """Encode a string in SSH wire format.
    
    Args:
        data: Data to encode.
        
    Returns:
        SSH wire format encoded data.
    """
    return struct.pack('>I', len(data)) + data


def ssh_encode_public_key(public_key_line: str) -> bytes:
    """Encode a public key in SSH wire format.
    
    Args:
        public_key_line: SSH public key line (e.g., "ssh-ed25519 AAAA... comment").
        
    Returns:
        SSH wire format encoded public key.
    """
    parts = public_key_line.strip().split(' ')
    if len(parts) < 2:
        raise ValueError("Invalid public key format")
    
    key_type = parts[0]
    key_data_b64 = parts[1]
    key_data = base64.b64decode(key_data_b64)
    
    return key_data


def create_ssh_signature_blob(public_key_line: str, namespace: str, hash_algorithm: str, signature_data: bytes) -> bytes:
    """Create SSH signature blob according to PROTOCOL.sshsig format.
    
    Args:
        public_key_line: SSH public key line.
        namespace: Signature namespace (e.g., "git").
        hash_algorithm: Hash algorithm ("sha256" or "sha512").
        signature_data: The actual signature bytes.
        
    Returns:
        SSH signature blob.
    """
    # SSH signature blob format:
    # byte[6]   MAGIC_PREAMBLE "SSHSIG"
    # uint32    SIG_VERSION (0x01)
    # string    publickey
    # string    namespace
    # string    reserved (empty)
    # string    hash_algorithm
    # string    signature
    
    blob = b'SSHSIG'  # Magic preamble
    blob += struct.pack('>I', 1)  # Version 1
    
    # Encode public key
    public_key_data = ssh_encode_public_key(public_key_line)
    blob += ssh_encode_string(public_key_data)
    
    # Encode namespace
    blob += ssh_encode_string(namespace.encode('utf-8'))
    
    # Encode reserved (empty)
    blob += ssh_encode_string(b'')
    
    # Encode hash algorithm
    blob += ssh_encode_string(hash_algorithm.encode('utf-8'))
    
    # Encode signature
    blob += ssh_encode_string(signature_data)
    
    return blob


def create_signed_data(namespace: str, hash_algorithm: str, message_hash: bytes) -> bytes:
    """Create the data that gets signed according to PROTOCOL.sshsig.
    
    Args:
        namespace: Signature namespace.
        hash_algorithm: Hash algorithm used.
        message_hash: Hash of the message being signed.
        
    Returns:
        Data to be signed.
    """
    # Signed data format:
    # byte[6]   MAGIC_PREAMBLE "SSHSIG"
    # string    namespace
    # string    reserved (empty)
    # string    hash_algorithm
    # string    H(message)
    
    data = b'SSHSIG'  # Magic preamble
    data += ssh_encode_string(namespace.encode('utf-8'))
    data += ssh_encode_string(b'')  # reserved
    data += ssh_encode_string(hash_algorithm.encode('utf-8'))
    data += ssh_encode_string(message_hash)
    
    return data


def run_command(cmd: List[str], capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a command and return the result.
    
    Args:
        cmd: Command to execute as list of strings.
        capture_output: Whether to capture stdout/stderr.
        check: Whether to raise exception on non-zero exit.
        
    Returns:
        CompletedProcess with result.
    """
    return subprocess.run(
        cmd,
        capture_output=capture_output,
        text=True,
        check=check,
        encoding='utf-8'
    )


def dropbear_keygen(key_type: str, key_file: str, key_size: Optional[str] = None, comment: Optional[str] = None) -> bool:
    """Generate a key using dropbearkey.
    
    Args:
        key_type: Type of key (rsa, ecdsa, ed25519).
        key_file: Path to save the private key.
        key_size: Key size in bits (optional).
        comment: Key comment (optional).
        
    Returns:
        True if successful, False otherwise.
    """
    cmd = ['dropbearkey', '-t', key_type, '-f', key_file]
    
    if key_size:
        cmd.extend(['-s', key_size])
    
    if comment:
        cmd.extend(['-C', comment])
    
    try:
        # Clear environment variables that cause "String too long" bug in Dropbear
        clean_env = {}
        for key, value in os.environ.items():
            # Only keep essential environment variables
            if key in ['PATH', 'HOME', 'USER', 'PWD', 'SHELL']:
                clean_env[key] = value
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            env=clean_env
        )
        print(f"Generated {key_type} key: {key_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating key: {e.stderr}", file=sys.stderr)
        return False


def dropbear_public_key(key_file: str) -> Optional[str]:
    """Extract public key using dropbearkey.
    
    Args:
        key_file: Path to the private key file.
        
    Returns:
        Public key string or None if failed.
    """
    try:
        # Use an absolute minimal environment to avoid "String too long" bug
        minimal_env = {
            'PATH': '/usr/bin:/bin',
            'HOME': '/home/vscode'
        }
        
        result = subprocess.run(
            ['dropbearkey', '-y', '-f', key_file],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            env=minimal_env
        )
        # Parse the output to get just the public key line
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.startswith('ssh-'):
                return line.strip()
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error extracting public key: {e.stderr}", file=sys.stderr)
        return None


def get_key_fingerprint(key_file: str) -> Optional[str]:
    """Get key fingerprint using dropbearkey.
    
    Args:
        key_file: Path to the key file.
        
    Returns:
        Fingerprint string or None if failed.
    """
    try:
        # Clear environment variables that cause "String too long" bug in Dropbear
        clean_env = {}
        for key, value in os.environ.items():
            # Only keep essential environment variables
            if key in ['PATH', 'HOME', 'USER', 'PWD', 'SHELL']:
                clean_env[key] = value
        
        result = subprocess.run(
            ['dropbearkey', '-y', '-f', key_file],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            env=clean_env
        )
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if 'Fingerprint:' in line:
                return line.strip()
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error getting fingerprint: {e.stderr}", file=sys.stderr)
        return None


def create_ssh_signature(key_file: str, data_file: str, namespace: str = "git") -> Optional[str]:
    """Create an SSH signature using real Ed25519 cryptography.
    
    Args:
        key_file: Path to the private key.
        data_file: Path to the data to sign.
        namespace: Signature namespace (default: git).
        
    Returns:
        SSH signature string or None if failed.
    """
    try:
        # Read the data to sign
        with open(data_file, 'rb') as f:
            data = f.read()
        
        # Find the corresponding public key
        public_key_file = key_file + '.pub'
        if not os.path.exists(public_key_file):
            # Try common locations
            for pub_file in ['/home/vscode/.ssh/id_ed25519.pub', '/home/vscode/.ssh/id_rsa.pub']:
                if os.path.exists(pub_file):
                    public_key_file = pub_file
                    break
        
        if not os.path.exists(public_key_file):
            print("Error: No public key found", file=sys.stderr)
            return None
        
        with open(public_key_file, 'r', encoding='utf-8') as f:
            public_key_line = f.read().strip()
        
        # Parse the public key
        key_parts = public_key_line.split(' ')
        if len(key_parts) < 2:
            print("Error: Invalid public key format", file=sys.stderr)
            return None
            
        key_type = key_parts[0]  # e.g., "ssh-ed25519"
        
        # Only support Ed25519 for now
        if key_type != 'ssh-ed25519':
            print(f"Error: Unsupported key type {key_type} (only ssh-ed25519 supported)", file=sys.stderr)
            return None
        
        # Load the private key
        private_key = load_openssh_ed25519_private_key(key_file)
        if not private_key:
            print("Error: Could not load Ed25519 private key", file=sys.stderr)
            return None
        
        # Create the signed data according to SSH signature format
        hash_algorithm = "sha512"
        message_hash = hashlib.sha512(data).digest()
        signed_data = create_signed_data(namespace, hash_algorithm, message_hash)
        
        # Create real Ed25519 signature
        ed25519_signature = create_real_ed25519_signature(private_key, signed_data)
        
        # Create SSH signature data (algorithm name + signature)
        ssh_signature_data = ssh_encode_string(b"ssh-ed25519") + ssh_encode_string(ed25519_signature)
        
        # Create the complete SSH signature blob
        signature_blob = create_ssh_signature_blob(public_key_line, namespace, hash_algorithm, ssh_signature_data)
        
        # Encode as base64
        signature_b64 = base64.b64encode(signature_blob).decode()
        
        return signature_b64
        
    except Exception as e:
        print(f"Error creating signature: {e}", file=sys.stderr)
        return None


def handle_find_principals(args: List[str]) -> int:
    """Handle find-principals operation for signature verification.
    
    Args:
        args: Command line arguments.
        
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    # Debug logging
    log_file = '/workspaces/greenova/ssh-keygen-debug.log'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"handle_find_principals called with: {args}\n")
    
    # Extract arguments
    allowed_signers_file = None
    
    i = 0
    while i < len(args):
        if args[i] == '-Y' and i + 1 < len(args):
            i += 1  # Skip -Y
        elif args[i] == 'find-principals':
            i += 1  # Skip find-principals
        elif args[i] == '-n' and i + 1 < len(args):
            i += 2  # Skip namespace
        elif args[i] == '-s' and i + 1 < len(args):
            i += 2  # Skip signature file
        elif args[i] == '-f' and i + 1 < len(args):
            allowed_signers_file = args[i + 1]
            i += 2
        else:
            i += 1
    
    if not allowed_signers_file:
        return 1
    
    # Read allowed signers file and extract principals
    try:
        with open(allowed_signers_file, 'r', encoding='utf-8') as f:
            with open(log_file, 'a', encoding='utf-8') as debug_f:
                debug_f.write(f"  Reading allowed_signers_file: {allowed_signers_file}\n")
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Format: principal key-type key-data
                    parts = line.split(' ', 2)
                    if len(parts) >= 2:
                        principal = parts[0]
                        with open(log_file, 'a', encoding='utf-8') as debug_f:
                            debug_f.write(f"  Found principal: {principal}\n")
                        print(principal)
                        return 0
    except (FileNotFoundError, Exception) as e:
        with open(log_file, 'a', encoding='utf-8') as debug_f:
            debug_f.write(f"  find_principals ERROR: {e}\n")
        return 1
    
    # If no principals found, return success anyway
    return 0


def handle_check_novalidate(args: List[str]) -> int:
    """Handle check-novalidate operation for signature verification.
    
    Args:
        args: Command line arguments.
        
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    # Debug logging
    log_file = '/workspaces/greenova/ssh-keygen-debug.log'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"handle_check_novalidate called with: {args}\n")
    
    # Extract arguments
    namespace = None
    signature_file = None
    message_file = None
    allowed_signers_file = None
    
    i = 0
    while i < len(args):
        if args[i] == '-Y' and i + 1 < len(args):
            i += 1  # Skip -Y
        elif args[i] == 'check-novalidate':
            i += 1  # Skip check-novalidate
        elif args[i] == '-n' and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        elif args[i] == '-s' and i + 1 < len(args):
            signature_file = args[i + 1]
            i += 2
        elif args[i] == '-f' and i + 1 < len(args):
            allowed_signers_file = args[i + 1]
            i += 2
        else:
            # Remaining argument should be the message file
            if not message_file:
                message_file = args[i]
            i += 1
    
    # Debug logging
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"  namespace: {namespace}, signature_file: {signature_file}, message_file: {message_file}\n")
    
    if not signature_file:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write("  ERROR: Missing signature file\n")
        return 1
    
    # For check-novalidate, we verify the signature file exists and parse it
    try:
        with open(signature_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Check signature format
        if not (content.startswith('-----BEGIN SSH SIGNATURE-----') and content.endswith('-----END SSH SIGNATURE-----')):
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("  ERROR: Invalid signature format\n")
            return 1
        
        # Extract and validate base64 data
        lines = content.split('\n')
        b64_data = ''.join(line for line in lines if not line.startswith('-----'))
        
        try:
            signature_blob = base64.b64decode(b64_data)
        except Exception as e:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"  ERROR: Invalid base64 data: {e}\n")
            return 1
        
        # Parse signature blob
        parsed = parse_ssh_signature_blob(signature_blob)
        if not parsed:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("  ERROR: Failed to parse signature blob\n")
            return 1
        
        pubkey_data, sig_namespace, hash_algorithm, ssh_signature_data = parsed
        
        # Check namespace if provided
        if namespace and sig_namespace != namespace:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"  ERROR: Namespace mismatch. Expected: {namespace}, Got: {sig_namespace}\n")
            return 1
        
        # Parse SSH signature data
        sig_parsed = parse_ssh_signature_data(ssh_signature_data)
        if not sig_parsed:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("  ERROR: Failed to parse SSH signature data\n")
            return 1
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write("  check-novalidate SUCCESS (signature format validated)\n")
        return 0
        
    except (FileNotFoundError, Exception) as e:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"  check-novalidate ERROR: {e}\n")
        return 1


def handle_signing_operation(args: argparse.Namespace, remaining_args: List[str]) -> int:
    """Handle SSH signing operations.
    
    Args:
        args: Parsed command line arguments.
        remaining_args: Remaining unparsed arguments.
        
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    if args.operation == 'sign':
        # Git signing operation
        if not args.key_file:
            print("Error: Key file (-f) required for signing", file=sys.stderr)
            return 1
        
        # Git passes the public key file, but we need the private key
        private_key_file = args.key_file
        if private_key_file.endswith('.pub'):
            private_key_file = private_key_file[:-4]  # Remove .pub extension
        
        # Find the data file in remaining arguments or assume stdin
        data_file = None
        if remaining_args:
            data_file = remaining_args[0]
        
        if not data_file:
            # Read from stdin and write to temp file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
                data_file = tmp.name
                tmp.write(sys.stdin.read())
        
        signature = create_ssh_signature(private_key_file, data_file, args.namespace or "git")
        if signature:
            # Git expects the signature in a .sig file next to the data file
            sig_file = data_file + ".sig"
            sig_content = f"-----BEGIN SSH SIGNATURE-----\n{signature}\n-----END SSH SIGNATURE-----\n"
            
            with open(sig_file, 'w', encoding='utf-8') as f:
                f.write(sig_content)
            
            return 0
        else:
            print("Failed to create signature", file=sys.stderr)
            return 1
    
    elif args.operation == 'verify':
        # For now, just return success for verification
        # In production, implement proper signature verification
        return 0
    
    else:
        print(f"Error: Unsupported signing operation: {args.operation}", file=sys.stderr)
        return 1


def parse_ssh_signature_blob(signature_blob: bytes) -> Optional[Tuple[bytes, str, str, bytes]]:
    """Parse SSH signature blob according to PROTOCOL.sshsig format.
    
    Args:
        signature_blob: SSH signature blob data.
        
    Returns:
        Tuple of (public_key_data, namespace, hash_algorithm, signature_data) or None if failed.
    """
    try:
        offset = 0
        
        # Check magic preamble
        if not signature_blob.startswith(b'SSHSIG'):
            return None
        offset += 6
        
        # Read version
        if len(signature_blob) < offset + 4:
            return None
        version = struct.unpack('>I', signature_blob[offset:offset+4])[0]
        if version != 1:
            return None
        offset += 4
        
        # Read public key
        if len(signature_blob) < offset + 4:
            return None
        pubkey_len = struct.unpack('>I', signature_blob[offset:offset+4])[0]
        offset += 4
        if len(signature_blob) < offset + pubkey_len:
            return None
        pubkey_data = signature_blob[offset:offset+pubkey_len]
        offset += pubkey_len
        
        # Read namespace
        if len(signature_blob) < offset + 4:
            return None
        namespace_len = struct.unpack('>I', signature_blob[offset:offset+4])[0]
        offset += 4
        if len(signature_blob) < offset + namespace_len:
            return None
        namespace = signature_blob[offset:offset+namespace_len].decode('utf-8')
        offset += namespace_len
        
        # Read reserved (skip)
        if len(signature_blob) < offset + 4:
            return None
        reserved_len = struct.unpack('>I', signature_blob[offset:offset+4])[0]
        offset += 4 + reserved_len
        
        # Read hash algorithm
        if len(signature_blob) < offset + 4:
            return None
        hash_alg_len = struct.unpack('>I', signature_blob[offset:offset+4])[0]
        offset += 4
        if len(signature_blob) < offset + hash_alg_len:
            return None
        hash_algorithm = signature_blob[offset:offset+hash_alg_len].decode('utf-8')
        offset += hash_alg_len
        
        # Read signature
        if len(signature_blob) < offset + 4:
            return None
        sig_len = struct.unpack('>I', signature_blob[offset:offset+4])[0]
        offset += 4
        if len(signature_blob) < offset + sig_len:
            return None
        signature_data = signature_blob[offset:offset+sig_len]
        
        return pubkey_data, namespace, hash_algorithm, signature_data
        
    except Exception:
        return None


def parse_ssh_signature_data(signature_data: bytes) -> Optional[Tuple[str, bytes]]:
    """Parse SSH signature data to extract algorithm and signature bytes.
    
    Args:
        signature_data: SSH signature data.
        
    Returns:
        Tuple of (algorithm, signature_bytes) or None if failed.
    """
    try:
        offset = 0
        
        # Read algorithm name
        if len(signature_data) < 4:
            return None
        alg_len = struct.unpack('>I', signature_data[offset:offset+4])[0]
        offset += 4
        if len(signature_data) < offset + alg_len:
            return None
        algorithm = signature_data[offset:offset+alg_len].decode('utf-8')
        offset += alg_len
        
        # Read signature bytes
        if len(signature_data) < offset + 4:
            return None
        sig_len = struct.unpack('>I', signature_data[offset:offset+4])[0]
        offset += 4
        if len(signature_data) < offset + sig_len:
            return None
        signature_bytes = signature_data[offset:offset+sig_len]
        
        return algorithm, signature_bytes
        
    except Exception:
        return None


def convert_ssh_pubkey_to_line(pubkey_data: bytes) -> Optional[str]:
    """Convert SSH public key data to public key line format.
    
    Args:
        pubkey_data: SSH public key data.
        
    Returns:
        Public key line or None if failed.
    """
    try:
        offset = 0
        
        # Read key type
        if len(pubkey_data) < 4:
            return None
        type_len = struct.unpack('>I', pubkey_data[offset:offset+4])[0]
        offset += 4
        if len(pubkey_data) < offset + type_len:
            return None
        key_type = pubkey_data[offset:offset+type_len].decode('utf-8')
        
        # Encode the entire public key data as base64
        pubkey_b64 = base64.b64encode(pubkey_data).decode()
        
        return f"{key_type} {pubkey_b64}"
        
    except Exception:
        return None


def find_public_key_in_allowed_signers(allowed_signers_file: str, pubkey_line: str) -> Optional[str]:
    """Find the identity/principal for a public key in allowed signers file.
    
    Args:
        allowed_signers_file: Path to allowed signers file.
        pubkey_line: Public key line to search for.
        
    Returns:
        Principal/identity or None if not found.
    """
    try:
        if not os.path.exists(allowed_signers_file):
            return None
            
        # Extract just the key type and data for comparison
        pubkey_parts = pubkey_line.strip().split(' ')
        if len(pubkey_parts) < 2:
            return None
        target_key_type = pubkey_parts[0]
        target_key_data = pubkey_parts[1]
        
        with open(allowed_signers_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Format: principal key-type key-data [comment]
                    parts = line.split(' ')
                    if len(parts) >= 3:
                        principal = parts[0]
                        key_type = parts[1] 
                        key_data = parts[2]
                        
                        if key_type == target_key_type and key_data == target_key_data:
                            return principal
        
        return None
        
    except Exception:
        return None


def handle_verify_operation(args: List[str]) -> int:
    """Handle -Y verify operation for signature verification.
    
    Args:
        args: Command line arguments.
        
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    # Debug logging
    log_file = '/workspaces/greenova/ssh-keygen-debug.log'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"handle_verify_operation called with: {args}\n")
    
    # Extract arguments
    namespace = None
    signature_file = None
    allowed_signers_file = None
    identity = None
    verify_time = None
    message_file = None
    
    i = 0
    while i < len(args):
        if args[i] == '-Y' and i + 1 < len(args):
            i += 1  # Skip -Y
        elif args[i] == 'verify':
            i += 1  # Skip verify
        elif args[i] == '-n' and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        elif args[i] == '-s' and i + 1 < len(args):
            signature_file = args[i + 1]
            i += 2
        elif args[i] == '-f' and i + 1 < len(args):
            allowed_signers_file = args[i + 1]
            i += 2
        elif args[i] == '-I' and i + 1 < len(args):
            identity = args[i + 1]
            i += 2
        elif args[i].startswith('-Overify-time='):
            verify_time = args[i].split('=', 1)[1]
            i += 1
        else:
            # Remaining argument should be the message file
            if not message_file:
                message_file = args[i]
            i += 1
    
    # Debug logging
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"  namespace: {namespace}, signature_file: {signature_file}, identity: {identity}, message_file: {message_file}\n")
    
    # Verify signature
    if not signature_file:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write("  ERROR: Missing signature file\n")
        return 1
    
    try:
        # Read signature file
        with open(signature_file, 'r', encoding='utf-8') as f:
            sig_content = f.read().strip()
        
        # Extract base64 signature from SSH signature format
        if not (sig_content.startswith('-----BEGIN SSH SIGNATURE-----') and sig_content.endswith('-----END SSH SIGNATURE-----')):
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("  ERROR: Invalid signature format\n")
            return 1
        
        # Extract base64 data
        lines = sig_content.split('\n')
        b64_data = ''.join(line for line in lines if not line.startswith('-----'))
        signature_blob = base64.b64decode(b64_data)
        
        # Parse SSH signature blob
        parsed = parse_ssh_signature_blob(signature_blob)
        if not parsed:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("  ERROR: Failed to parse signature blob\n")
            return 1
        
        pubkey_data, sig_namespace, hash_algorithm, ssh_signature_data = parsed
        
        # Convert public key data to public key line
        pubkey_line = convert_ssh_pubkey_to_line(pubkey_data)
        if not pubkey_line:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("  ERROR: Failed to convert public key data\n")
            return 1
        
        # Check namespace matches
        if namespace and sig_namespace != namespace:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"  ERROR: Namespace mismatch. Expected: {namespace}, Got: {sig_namespace}\n")
            return 1
        
        # Find public key in allowed signers
        if allowed_signers_file:
            found_identity = find_public_key_in_allowed_signers(allowed_signers_file, pubkey_line)
            if not found_identity:
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write("  ERROR: Public key not found in allowed signers\n")
                return 1
            
            # Check identity matches if specified
            if identity and found_identity != identity:
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"  ERROR: Identity mismatch. Expected: {identity}, Found: {found_identity}\n")
                return 1
        
        # Parse SSH signature data
        sig_parsed = parse_ssh_signature_data(ssh_signature_data)
        if not sig_parsed:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("  ERROR: Failed to parse SSH signature data\n")
            return 1
        
        sig_algorithm, signature_bytes = sig_parsed
        
        # Read message data - either from file or stdin
        if message_file and os.path.exists(message_file):
            with open(message_file, 'rb') as f:
                message_data = f.read()
        else:
            # Read from stdin if no message file is provided (Git's typical behavior)
            message_data = sys.stdin.buffer.read()
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"  Message data length: {len(message_data)} bytes\n")
        
        # Recreate the signed data for verification
        if hash_algorithm == "sha512":
            message_hash = hashlib.sha512(message_data).digest()
        elif hash_algorithm == "sha256":
            message_hash = hashlib.sha256(message_data).digest()
        else:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"  ERROR: Unsupported hash algorithm: {hash_algorithm}\n")
            return 1
        
        signed_data = create_signed_data(sig_namespace, hash_algorithm, message_hash)
        
        # Verify the signature cryptographically
        if sig_algorithm == "ssh-ed25519":
            verification_result = verify_real_ed25519_signature(pubkey_line, signature_bytes, signed_data)
            if verification_result:
                with open(log_file, 'a', encoding='utf-8') as debug_f:
                    debug_f.write("  Signature verification SUCCESS (cryptographic verification passed)\n")
                return 0
            else:
                with open(log_file, 'a', encoding='utf-8') as debug_f:
                    debug_f.write("  Signature verification FAILED (cryptographic verification failed)\n")
                return 1
        else:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"  ERROR: Unsupported signature algorithm: {sig_algorithm}\n")
            return 1
        
    except (FileNotFoundError, Exception) as e:
        with open(log_file, 'a', encoding='utf-8') as debug_f:
            debug_f.write(f"  Signature verification FAILED - exception: {e}\n")
        return 1


def main() -> int:
    """Main entry point for ssh-keygen wrapper."""
    
    # Debug: Log all arguments
    log_file = '/workspaces/greenova/ssh-keygen-debug.log'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"ssh-keygen called with: {sys.argv}\n")
    
    # Handle special operations first (find-principals, check-novalidate)
    if len(sys.argv) > 1:
        args_str = ' '.join(sys.argv[1:])
        if 'find-principals' in args_str:
            return handle_find_principals(sys.argv[1:])
        elif 'check-novalidate' in args_str:
            return handle_check_novalidate(sys.argv[1:])
        elif 'verify' in args_str:
            # Handle -Y verify calls with all options
            return handle_verify_operation(sys.argv[1:])
    
    parser = argparse.ArgumentParser(
        description="SSH-keygen wrapper for Dropbear compatibility",
        add_help=False  # We'll handle help ourselves
    )
    
    # Add common ssh-keygen arguments
    parser.add_argument('-t', dest='key_type', help='Key type (rsa, ecdsa, ed25519)')
    parser.add_argument('-f', dest='key_file', help='Key file path')
    parser.add_argument('-b', dest='key_size', help='Key size in bits')
    parser.add_argument('-C', dest='comment', help='Key comment')
    parser.add_argument('-y', action='store_true', dest='output_public', help='Output public key')
    parser.add_argument('-l', action='store_true', dest='fingerprint', help='Show fingerprint')
    parser.add_argument('-p', action='store_true', dest='fingerprint', help='Show fingerprint')
    parser.add_argument('-Y', dest='operation', help='SSH signing operation (sign, verify)')
    parser.add_argument('-n', dest='namespace', help='Signature namespace')
    parser.add_argument('-q', action='store_true', dest='quiet', help='Quiet mode')
    
    # Handle help
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        print("""ssh-keygen wrapper for Dropbear
Usage: ssh-keygen [options]

Key generation:
  -t type     Key type (rsa, ecdsa, ed25519)
  -f filename Key file path
  -b bits     Key size in bits
  -C comment  Key comment

Key operations:
  -y          Output public key from private key
  -l          Show key fingerprint
  -p          Show key fingerprint

SSH signing (Git support):
  -Y sign     Sign data
  -Y verify   Verify signature
  -Y find-principals  Find signing principals
  -Y check-novalidate Check signature without validation
  -n namespace Signature namespace

This wrapper uses Dropbear tools for SSH key operations.
""")
        return 0
    
    # Parse remaining arguments
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit:
        return 1
    
    # Handle signing operations
    if args.operation:
        return handle_signing_operation(args, unknown)
    
    # Handle public key output
    if args.output_public:
        if not args.key_file:
            print("Error: No key file specified (-f)", file=sys.stderr)
            return 1
        
        public_key = dropbear_public_key(args.key_file)
        if public_key:
            print(public_key)
            return 0
        else:
            print("Error: Could not extract public key", file=sys.stderr)
            return 1
    
    # Handle fingerprint
    if args.fingerprint:
        if not args.key_file:
            print("Error: No key file specified (-f)", file=sys.stderr)
            return 1
        
        fingerprint = get_key_fingerprint(args.key_file)
        if fingerprint:
            print(fingerprint)
            return 0
        else:
            print("Error: Could not get key fingerprint", file=sys.stderr)
            return 1
    
    # Handle key generation
    if args.key_type and args.key_file:
        success = dropbear_keygen(args.key_type, args.key_file, args.key_size, args.comment)
        return 0 if success else 1
    
    # Default: show help
    print("Error: Insufficient arguments. Use -h for help.", file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
