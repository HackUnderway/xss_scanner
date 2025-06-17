import asyncio
from config.constants import SUCCESS, WARN, ERROR, RESET, Fore, Style

class XSSDetector:
    def __init__(self, page):
        self.page = page
        self.dialog_messages = []
    
    async def setup_detection(self):
        """Setup detection hooks in the browser context."""
        await self.page.expose_function("xssDetected", lambda: True)
        
        # Dialog handler
        def handle_dialog(dialog):
            self.dialog_messages.append(dialog.message)
            asyncio.create_task(dialog.dismiss())
        
        self.page.on("dialog", handle_dialog)
    
    async def detect_xss(self, payload):
        """Perform comprehensive XSS detection checks."""
        detection_results = {
            'dialog': False,
            'dom_injection': False,
            'script_execution': False,
            'context': None,
            'message': None
        }
        
        # Reset detection state
        await self.page.evaluate("() => { window.xssDetectedFlag = false; }")
        self.dialog_messages = []
        
        try:
            # Check for dialog-based XSS
            if self.dialog_messages:
                detection_results['dialog'] = True
                detection_results['message'] = self.dialog_messages[0]
            
            # Check for DOM-based XSS
            dom_injection = await self._check_dom_injection()
            if dom_injection and dom_injection.get('detected'):
                detection_results['dom_injection'] = True
                detection_results['context'] = dom_injection.get('context')
            
            # Check for script execution
            script_executed = await self.page.evaluate("""() => {
                try {
                    return window.xssDetectedFlag === true;
                } catch (e) {
                    return false;
                }
            }""")
            
            if script_executed:
                detection_results['script_execution'] = True
            
            return detection_results
        except Exception as e:
            print(f"{WARN}⚠️ Detection error: {e}{RESET}")
            return detection_results
    
    async def _check_dom_injection(self):
        """Check for various DOM-based XSS patterns."""
        return await self.page.evaluate("""() => {
            const results = {
                suspiciousElements: [],
                contexts: []
            };
            
            // Función para verificar URLs javascript:
            const isJavascriptUrl = (value) => {
                const jsPattern = /javascript:\\s*[^)]*\\s*\\(.*\\)/i;
                return jsPattern.test(value);
            };
            
            Array.from(document.querySelectorAll('*')).forEach(el => {
                const attrs = el.attributes;
                const elementInfo = {
                    tag: el.tagName,
                    attributes: []
                };
                
                for (let i = 0; i < attrs.length; i++) {
                    const attr = attrs[i].name.toLowerCase();
                    const value = attrs[i].value;
                    
                    if (attr.startsWith('on') && attr.length > 2) {
                        try {
                            new Function(value);
                            elementInfo.attributes.push({
                                name: attr,
                                value: value,
                                type: 'event_handler'
                            });
                        } catch (e) {}
                    }
                    
                    if (['src', 'href', 'style', 'background'].includes(attr) && 
                        isJavascriptUrl(value)) {
                        elementInfo.attributes.push({
                            name: attr,
                            value: value,
                            type: 'javascript_url'
                        });
                    }
                    
                    if (attr === 'src' && value.startsWith('data:') && 
                        /<script/i.test(value)) {
                        elementInfo.attributes.push({
                            name: attr,
                            value: value,
                            type: 'data_uri'
                        });
                    }
                }
                
                if (elementInfo.attributes.length > 0) {
                    results.suspiciousElements.push(elementInfo);
                    results.contexts.push(`${el.tagName} element with ${elementInfo.attributes.map(a => a.name).join(', ')}`);
                }
            });
            
            if (results.suspiciousElements.length > 0) {
                return {
                    detected: true,
                    count: results.suspiciousElements.length,
                    context: results.contexts.join('; ')
                };
            }
            return { detected: false };
        }""")
