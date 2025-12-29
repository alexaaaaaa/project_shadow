import base64

def reveal_shadow_map(encoded_pulse):
    """Decodes the Pulse: hash from your GitHub Commits."""
    try:
        # Padding correction for Base64
        missing_padding = len(encoded_pulse) % 4
        if missing_padding:
            encoded_pulse += '=' * (4 - missing_padding)
            
        decoded_bytes = base64.b64decode(encoded_pulse)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return f"Decoding Error: {e}"

# Example: If your commit says "Pulse: NzkuMTc3LjE0"
pulse_from_github = "NzkuMTc3LjE0" 
print(f"Shadow Node IP identified at: {reveal_shadow_map(pulse_from_github)}")