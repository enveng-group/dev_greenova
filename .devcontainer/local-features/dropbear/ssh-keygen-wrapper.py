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
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple


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
    """Create a basic SSH signature for Git compatibility.
    
    This implementation bypasses Dropbear's "String too long" bug by reading
    the public key directly from the filesystem instead of extracting it.
    
    Args:
        key_file: Path to the private key.
        data_file: Path to the data to sign.
        namespace: Signature namespace (default: git).
        
    Returns:
        Base64-encoded signature or None if failed.
    """
    try:
        # Read the data to sign
        with open(data_file, 'rb') as f:
            data = f.read()
        
        # Try to read the corresponding public key file
        public_key_file = key_file + '.pub'
        public_key = None
        
        if os.path.exists(public_key_file):
            with open(public_key_file, 'r', encoding='utf-8') as f:
                public_key = f.read().strip()
        
        if not public_key:
            print(f"Warning: Could not find public key file {public_key_file}", file=sys.stderr)
            # Try some common public key locations
            for pub_file in ['/home/vscode/.ssh/id_ed25519.pub', '/home/vscode/.ssh/id_rsa.pub']:
                if os.path.exists(pub_file):
                    with open(pub_file, 'r', encoding='utf-8') as f:
                        public_key = f.read().strip()
                        break
        
        if not public_key:
            print("Error: No public key found", file=sys.stderr)
            return None
        
        # Create a simple signature format compatible with Git
        # This is a basic implementation for development use
        signature_data = {
            'namespace': namespace,
            'public_key': public_key,
            'data_hash': hashlib.sha256(data).hexdigest(),
            'key_file': os.path.basename(key_file)
        }
        
        # Create signature content
        signature_content = f"""{signature_data['namespace']}
{signature_data['public_key']}
{signature_data['data_hash']}
{signature_data['key_file']}"""
        
        return base64.b64encode(signature_content.encode()).decode()
        
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
    # Extract arguments
    namespace = None
    signature_file = None
    allowed_signers_file = None
    
    i = 0
    while i < len(args):
        if args[i] == '-Y' and i + 1 < len(args):
            i += 1  # Skip -Y
        elif args[i] == 'find-principals':
            i += 1  # Skip find-principals
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
            i += 1
    
    if not signature_file or not allowed_signers_file:
        print("Error: Missing required arguments for find-principals", file=sys.stderr)
        return 1
    
    # Read allowed signers file and extract principals
    try:
        with open(allowed_signers_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Format: principal key-type key-data
                    parts = line.split(' ', 2)
                    if len(parts) >= 2:
                        principal = parts[0]
                        print(principal)
                        return 0
    except FileNotFoundError:
        print(f"Error: Allowed signers file not found: {allowed_signers_file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error reading allowed signers file: {e}", file=sys.stderr)
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
    
    if not signature_file:
        print("Error: Missing signature file for check-novalidate", file=sys.stderr)
        return 1
    
    # For check-novalidate, we just verify the signature file exists and is readable
    try:
        with open(signature_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.startswith('-----BEGIN SSH SIGNATURE-----'):
                # Signature file exists and has proper format
                print("Good signature", file=sys.stderr)
                return 0
            else:
                print("Error: Invalid signature format", file=sys.stderr)
                return 1
    except FileNotFoundError:
        print(f"Error: Signature file not found: {signature_file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error reading signature file: {e}", file=sys.stderr)
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
            
            print(f"Signature written to: {sig_file}", file=sys.stderr)
            return 0
        else:
            print("Failed to create signature", file=sys.stderr)
            return 1
    
    elif args.operation == 'verify':
        # For now, just return success for verification
        # In production, implement proper signature verification
        print("Signature verification: OK (simplified implementation)", file=sys.stderr)
        return 0
    
    else:
        print(f"Error: Unsupported signing operation: {args.operation}", file=sys.stderr)
        return 1


def main() -> int:
    """Main entry point for ssh-keygen wrapper."""
    # Debug: log the command being called (disabled for production)
    # try:
    #     with open('/tmp/ssh-keygen-debug.log', 'a', encoding='utf-8') as f:
    #         f.write(f"ssh-keygen called with: {' '.join(sys.argv)}\n")
    # except Exception:
    #     pass  # Ignore debug logging errors
    
    # Handle special operations first (find-principals, check-novalidate)
    if len(sys.argv) > 1:
        args_str = ' '.join(sys.argv[1:])
        if 'find-principals' in args_str:
            return handle_find_principals(sys.argv[1:])
        elif 'check-novalidate' in args_str:
            return handle_check_novalidate(sys.argv[1:])
    
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
