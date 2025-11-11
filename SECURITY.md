# Security Considerations

## Overview

Legrand AI is a client-side web application MVP. This document outlines security considerations and known limitations.

## API Key Storage

### Current Implementation
- OpenAI API keys are stored in the browser's `localStorage`
- This is stored as clear text in the browser's local storage
- Keys never leave the user's browser except when making requests to OpenAI's API

### Known Limitations
⚠️ **Alert**: CodeQL flagged clear-text storage of sensitive data (API keys in localStorage)

**Why this is acceptable for this MVP:**
1. This is a client-side only application with no backend
2. Users are explicitly informed that keys are stored locally
3. The key is only used for direct API calls from the user's browser to OpenAI
4. Users have full control and can clear their localStorage at any time
5. This is standard practice for client-side API key management in MVPs

**For Production:**
Consider implementing a backend proxy that:
- Stores API keys server-side
- Authenticates users before proxying API requests
- Implements rate limiting and usage monitoring
- Never exposes API keys to the client

## CDN Security

### Current Implementation
✅ **Fixed**: Three.js is loaded from CDN with Subresource Integrity (SRI) check
- Uses integrity hash to verify the script hasn't been tampered with
- Includes `crossorigin="anonymous"` and `referrerpolicy="no-referrer"`

## Data Privacy

### What We Store Locally
- OpenAI API key (localStorage)
- User preferences (voice enabled, animations enabled)

### What We Don't Store
- Conversation history (cleared on page reload)
- User personal information
- Analytics or tracking data

### External Services
The application makes requests to:
1. **OpenAI API** (api.openai.com)
   - Used for AI conversation responses
   - User's API key is sent with each request
   - See [OpenAI's Privacy Policy](https://openai.com/policies/privacy-policy)

2. **Cloudflare CDN** (cdnjs.cloudflare.com)
   - Used to load Three.js library
   - Protected with SRI integrity checking

## Browser Security Features

### Content Security
- No inline scripts or styles that could be exploited
- External scripts use SRI for integrity verification
- HTML escaping for user input to prevent XSS

### Speech APIs
- Microphone access requires explicit user permission
- Browser handles all voice recognition/synthesis locally

## Recommendations for Users

### Protecting Your API Key
1. ✅ Use a dedicated OpenAI API key with spending limits
2. ✅ Monitor your OpenAI usage dashboard regularly
3. ✅ Clear your browser's localStorage if sharing a device
4. ✅ Use browser incognito/private mode for extra privacy
5. ❌ Never share your API key with others
6. ❌ Don't use API keys with high spending limits

### Safe Usage
1. Use a modern, up-to-date browser
2. Ensure you're accessing the application over HTTPS
3. Be cautious about the information you share in conversations
4. Clear your localStorage when done: Open DevTools → Application → Local Storage → Clear

## Reporting Security Issues

If you discover a security vulnerability, please:
1. Open a GitHub issue with the "security" label
2. Provide detailed information about the vulnerability
3. Suggest a fix if possible

**Do not** publicly disclose security vulnerabilities until they have been addressed.

## Future Security Enhancements

Planned for future versions:
- [ ] Backend API proxy for key management
- [ ] User authentication system
- [ ] Encrypted storage of sensitive data
- [ ] Rate limiting and abuse prevention
- [ ] Content moderation
- [ ] Session management
- [ ] CSRF protection for any future forms
- [ ] Audit logging

## Compliance

### Current Status
- ✅ GDPR: No personal data collected or stored on servers
- ✅ CCPA: No data collection or sharing
- ⚠️ Users must comply with OpenAI's terms of service

### User Responsibility
Users are responsible for:
- Complying with OpenAI's usage policies
- Not using the application for prohibited purposes
- Protecting their own API keys
- Understanding that conversations are processed by OpenAI

---

Last Updated: 2025-11-11
