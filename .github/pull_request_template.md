## Description

<!-- Provide a clear and concise description of your changes -->

## Type of Change

<!-- Check all that apply -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Security enhancement
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring
- [ ] Configuration change

## Security Impact

<!-- **REQUIRED**: Describe any security implications of this change -->

- [ ] This change involves handling sensitive data (PII, payment info, credentials)
- [ ] This change modifies authentication or authorization logic
- [ ] This change affects data encryption or cryptography
- [ ] This change adds new dependencies
- [ ] This change modifies API endpoints
- [ ] This change affects rate limiting or DDoS protection
- [ ] No security impact

**Security Details:**
<!-- Explain how this change affects security, or state "No security impact" if applicable -->

## Testing

<!-- Describe the tests you ran to verify your changes -->

### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Security tests added/updated
- [ ] Manual testing completed

### Test Results
```
<!-- Paste relevant test results here -->
```

## Security Checklist

<!-- **REQUIRED**: Complete ALL items before submitting -->

### Code Security
- [ ] No secrets, API keys, or credentials in code or commits
- [ ] All user inputs are validated and sanitized
- [ ] SQL injection prevention measures in place (parameterized queries)
- [ ] XSS prevention measures in place (input escaping, CSP)
- [ ] CSRF protection implemented where needed
- [ ] Authentication/authorization properly implemented
- [ ] Error messages don't leak sensitive information
- [ ] Proper error handling (no exposed stack traces)
- [ ] Secure random number generation used for tokens/keys

### Dependencies & Configuration
- [ ] All dependencies are from trusted sources
- [ ] No known vulnerabilities in dependencies (`npm audit` / `pip check`)
- [ ] Dependencies are pinned to specific versions
- [ ] Default credentials changed
- [ ] Debug mode disabled in production code

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS/SSL used for data in transit
- [ ] No sensitive data logged (passwords, tokens, PII, card data)
- [ ] Data retention policies considered
- [ ] PII handling complies with GDPR/privacy regulations

### Payment Processing (if applicable)
- [ ] PCI DSS requirements followed
- [ ] No storage of CVV/CVC codes
- [ ] No storage of full magnetic stripe data
- [ ] Tokenization implemented for card data
- [ ] Transaction data properly encrypted

### Documentation
- [ ] Security implications documented in code comments
- [ ] README.md updated if needed
- [ ] Security documentation updated if needed
- [ ] API documentation updated if endpoints changed

### Testing & Validation
- [ ] All tests pass locally
- [ ] Security tests included
- [ ] Code linted and formatted
- [ ] No console.log or debug statements in production code

## Compliance

<!-- Check if this change affects compliance requirements -->

- [ ] This change affects PCI DSS compliance
- [ ] This change affects GDPR compliance
- [ ] This change affects SOC 2 compliance
- [ ] This change affects audit logging requirements
- [ ] No compliance impact

## Breaking Changes

<!-- If this is a breaking change, describe the impact and migration path -->

## Additional Context

<!-- Add any other context, screenshots, or information about the changes -->

## Checklist

<!-- Final checks before submitting -->

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published
- [ ] I have reviewed the [Security Best Practices](docs/SECURITY_BEST_PRACTICES.md)
- [ ] I have reviewed the [Security Checklist](.github/SECURITY_CHECKLIST.md)

## Related Issues

<!-- Link related issues using #issue_number -->

Closes #
Related to #

---

**By submitting this pull request, I confirm that:**
- I have read and followed the [Contributing Guidelines](CONTRIBUTING.md)
- I have completed the security checklist above
- I understand that this is a payment gateway security project and security is paramount
- I take responsibility for the security implications of my changes
